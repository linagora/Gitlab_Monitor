# Image docker contenant les sources du projet python utilisé afin d'optimiser la 
# vitesse d'éxécution d'une pipeline.

# Stage 1: Builder
FROM python:3.11.4-slim-bullseye AS builder
WORKDIR /app
ENV POETRY_HOME="/opt/poetry"
ENV VIRTUAL_ENV="/opt/project"
ENV PATH="$VIRTUAL_ENV/bin:$POETRY_HOME/bin:$PATH"
ENV NEXUS_PYPI_URL="https://gso-nexus.linagora.com/repository/pypi-private/simple"
ARG NEXUS_PASSWORD
ARG NEXUS_USER

LABEL licence="EUPL"
LABEL description=""
LABEL equipe="Flavien Perez"
LABEL version="0.0.0"

COPY ./pyproject.toml .

RUN apt update &&\
    apt install --no-install-recommends -y build-essential libffi-dev libssh-dev python3-dev &&\
    pip install --no-cache-dir poetry==1.6.1 setuptools==65.3.0 pip==22.2.2 --upgrade &&\
    python3 -m venv $POETRY_HOME &&\
    python3 -m venv $VIRTUAL_ENV &&\ 
    poetry source add --priority=supplemental nexus $NEXUS_PYPI_URL &&\
    poetry poetry config certificates.nexus.cert false &&\
    poetry config http-basic.nexus $NEXUS_USER $NEXUS_PASSWORD &&\
    poetry lock &&\
    poetry install --no-root

# Stage 2: Final image
FROM python:3.12-slim-bullseye

ENV POETRY_HOME="/opt/poetry"
ENV VIRTUAL_ENV="/opt/project"
ENV PATH="$VIRTUAL_ENV/bin:$POETRY_HOME/bin:$PATH"

# Ajout d'un utilisateur non root
RUN useradd -m myuser
USER myuser

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=builder /app /app

WORKDIR /app

# Instruction HEALTHCHECK
# Ajouter ici une instruction qui vérifie que le conteneur docker est fonctionnel

CMD ["poetry", "run", "your_command_here"]
