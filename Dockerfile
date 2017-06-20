FROM python:3.6
ARG TRAVIS_JOB_ID
WORKDIR /meetup_loto
COPY test-requirements.txt .
RUN pip install -r test-requirements.txt
COPY ./ ./
RUN nose2 --with-coverage --coverage-report term-missing
RUN test $TRAVIS_JOB_ID && coveralls -i || echo
WORKDIR /meetup_loto/src
ENV PYTHONPATH "/meetup_loto/src:/usr/local/lib/python3.6"
EXPOSE 8080
ENTRYPOINT /meetup_loto/src/entrypoint.sh
