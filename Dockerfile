# start with a common python & poetry base img
FROM python:3.12-slim as poetryimg
ENV APP_DIR=/app \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PATH="${PATH}:/root/.local/bin" \
    POETRY_VERSION=1.8.3
WORKDIR "${APP_DIR}"
RUN pip install "poetry==${POETRY_VERSION}"

# build poetry dependencies with custom gcc libraries
# poetry will natively create a dedicated venv in ${pwd}/.venv
FROM poetryimg as poetry-builder
RUN apt-get update -qq \
    && apt-get install -qq git gcc build-essential \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    CFLAGS="-fcommon" \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

# build a full tooled dev image as a derivate of builder image
FROM poetry-builder as devimg
RUN poetry install
COPY . .

# let's get rid of gcc & build dependencies by copying venv
# install is required again because we asked "no-root" the 1st time
FROM poetryimg as prodimg
COPY --from=poetry-builder "${APP_DIR}" "${APP_DIR}"
COPY . .
RUN poetry install --no-dev
CMD ["poetry", "run", "python", "-m", "app"]

