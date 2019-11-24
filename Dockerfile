FROM registry.ng.bluemix.net/piplsearch/django:python3.6

RUN mkdir /libsaas
WORKDIR /libsaas
COPY . /libsaas
VOLUME /libsaas

RUN pip install -r requirements.txt
RUN pip install .

CMD python test.py

