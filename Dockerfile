FROM python:2.7
ADD requirements.txt /widely/requirements.txt
RUN cd /widely && pip install -r requirements.txt
ADD . /widely
RUN cd /widely && python -m unittest -f tests
