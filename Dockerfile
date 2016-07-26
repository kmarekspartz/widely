FROM python:2.7
ADD requirements.txt /widely/requirements.txt
RUN cd /widely && pip install -r requirements.txt
RUN cd /widely && pip install flake8
ADD . /widely
RUN cd /widely && flake8 .
RUN cd /widely && python -m unittest -f tests
