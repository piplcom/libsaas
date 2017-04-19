import logging
import threading

import atexit
import requests

from threading import Thread
from time import sleep
from libsaas import http
from . import base

try:
    import queue as Queue
except:
    import Queue

__all__ = ['requests_executor']

logger = logging.getLogger('libsaas.executor.requests_executor')

URLENCODE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class Consumer(Thread):
    RETRIES_NUMBER = 3

    def __init__(self, queue, on_error=None):
        """Create a consumer thread."""
        Thread.__init__(self)

        self.daemon = True

        self.on_error = on_error
        self.queue = queue

        self.tick_event = threading.Event()
        self.threads_lock = threading.Lock()
        self._threads = set()

        # Rate limit per second. will be updated after each call.
        self.rate_limit = 100 / 10
        # Last time request been sent
        self.last_request_time = None

        # It's important to set running in the constructor: if we are asked to
        # pause immediately after construction, we might set running to True in
        # run() *after* we set it to False in pause... and keep running forever.
        self.running = True

    def run(self):
        """Runs the consumer."""
        logger.debug('consumer is running...')
        while self.running:
            self.consume()

            # Polling of 1 sec
            sleep(1)

            # self.tick_event.wait(1)
            # self.tick_event.clear()

        logger.info(u'Joining searching threads')
        for t in list(self._threads):
            t.join()

        logger.info(u'Exit %s', self.__class__.__name__)
        logger.debug('consumer exited.')

    def pause(self):
        """Pause the consumer."""
        self.running = False

    def consume(self):
        """Return the next batch of items to upload."""
        queue = self.queue
        batch = []
        with self.threads_lock:
            while len(batch) + len(self._threads) < self.rate_limit or self.queue.empty():
                try:
                    batch.append(queue.get(block=True, timeout=0.5))
                except Queue.Empty:
                    break

            if len(batch) == 0:
                return False

            for request in batch:
                t = threading.Thread(target=self.do_request, args=(request,))
                self._threads.add(t)
                t.start()

    def do_request(self, request):
        try:
            response = self.request(request)

            if request.callback:
                request.callback(response, request.parser)

        except Exception as e:
            logger.exception(u"Error Processing request to %s", request.uri)
            raise e
        finally:
            self.queue.task_done()
            self._threads.discard(threading.current_thread())

        return response

    @staticmethod
    def request(request):

        # assert We working with the right object
        assert isinstance(request, http.Request)

        kwargs = {
            'method': request.method,
            'url': request.uri,
            'headers': request.headers,
            'extra': {},
        }

        if request.params:
            if request.method.upper() in URLENCODE_METHODS:
                kwargs['params'] = request.params
            else:
                kwargs['data'] = request.params

        resp = requests.request(**kwargs)

        # Throttle Limit Reached.
        if resp.status_code == 429:
            sec_to_wait = int(resp.headers.get('Retry-After', 0))
            logger.debug(u'Throttle Reached, sleeping for %d', sec_to_wait)

            sleep(sec_to_wait)

            # Retrying the same request again.
            return Consumer.request(request)

        if not 200 <= resp.status_code < 300 and request.retries == Consumer.RETRIES_NUMBER:
            resp.raise_for_status()

        if not 200 <= resp.status_code < 300 and request.retries < Consumer.RETRIES_NUMBER:
            request.retries += 1
            return Consumer.request(request)

        logger.debug('response code: %r, body: %r, headers: %r', resp.status_code, resp.content, resp.headers)
        return resp


class ConsumerRunner(object):
    MAX_QUEUE_SIZE = 10000

    def __init__(self):
        self.queue = Queue.Queue(self.MAX_QUEUE_SIZE)
        self.consumer = Consumer(self.queue)

        atexit.register(self.join)
        self.consumer.start()

    def join(self):
        """Ends the consumer thread once the queue is empty. Blocks execution until finished"""
        self.consumer.pause()
        try:
            self.consumer.join()
        except RuntimeError:
            # consumer thread has not started
            pass

    def enqueue(self, request, parser, callback):
        logger.debug('queueing: %s', request)

        try:
            request.parser = parser
            request.callback = cb
            self.queue.put(request, block=False)
            logger.debug('enqueued %s.', request.uri)
            return True, request
        except Queue.Full:
            logger.warn('analytics-python queue is full')
            return False, request


consumer_runner = ConsumerRunner()


def requests_executor(request, parser, cb=None):
    """
    An executor using the requests module.
    """
    logger.info('requesting %r', request)

    if request.async:
        consumer_runner.enqueue(request, parser, cb)
    else:
        resp = Consumer.request(request)
        return parser(resp.content, resp.status_code, resp.headers)


extra_params = {'extra': {}}


def use(**extra):
    base.use_executor(requests_executor)
    extra_params['extra'] = extra
