import logging
from time import sleep

import requests

from libsaas import http
from . import base

try:
    import queue as Queue
except:
    import Queue

__all__ = ['requests_executor']

logger = logging.getLogger('libsaas.executor.requests_executor')

URLENCODE_METHODS = ('GET', 'HEAD', 'OPTIONS')

RETRIES_NUMBER = 3


def requests_executor(request, parser):
    """
    An executor using the requests module.
    """
    logger.info('requesting %r', request)

    # assert We working with the right object
    assert isinstance(request, http.Request)

    kwargs = {
        'method': request.method,
        'url': request.uri,
        'headers': request.headers,
        'files': request.files
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
        return requests_executor(request, parser)

    if not 200 <= resp.status_code < 300 and request.retries == RETRIES_NUMBER:
        resp.raise_for_status()

    if resp.status_code >= 500 and request.retries < RETRIES_NUMBER:
        request.retries += 1
        return requests_executor(request, parser)

    logger.debug('response code: %r, body: %r, headers: %r', resp.status_code, resp.content, resp.headers)

    return parser(resp.content, resp.status_code, resp.headers)


extra_params = {'extra': {}}


def use(**extra):
    base.use_executor(requests_executor)
    extra_params['extra'] = extra
