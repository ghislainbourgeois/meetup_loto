FROM python:3.6 as tester
WORKDIR /meetup_loto
COPY test-requirements.txt .
RUN pip install -r test-requirements.txt
COPY src/ ./src
COPY tests ./tests
RUN nose2 --with-coverage --coverage-report term-missing
RUN coveralls -i

FROM python:3.6-alpine
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY --from=tester /meetup_loto/src /src
CMD "export FLASK_APP=/src/server.py; flask run"
