FROM python:3.9-slim AS python-deps

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=true pipenv install --deploy

FROM python:3.9-alpine AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY /src .
VOLUME /config
VOLUME /data

ENTRYPOINT ["python", "main.py", "config/config.json"]