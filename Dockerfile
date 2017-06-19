FROM python:3.6 as tester
ARG TRAVIS_JOB_ID
WORKDIR /meetup_loto
COPY test-requirements.txt .
RUN pip install -r test-requirements.txt
COPY ./ ./
ENV REQUESTS_CA_BUNDLE ""
ENV CURL_CA_BUNDLE ""
RUN nose2 --with-coverage --coverage-report term-missing
RUN test $TRAVIS_JOB_ID && coveralls -i

FROM python:3.6-alpine
COPY requirements.txt .
COPY --from=tester /root/.cache/ /root/.cache/
RUN pip install -r requirements.txt && rm -Rf /root/.cache
COPY --from=tester /meetup_loto/src /src
COPY --from=tester /meetup_loto/entrypoint.sh /src
WORKDIR /src
ENV PYTHONPATH "/src:/usr/local/lib/python3.6"
EXPOSE 8080
ENTRYPOINT /src/entrypoint.sh
