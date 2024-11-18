# Image qui build l'app/ le code source

ARG dependencies
FROM python:3.12-slim-bullseye

WORKDIR /app

ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=dependencies $VIRTUAL_ENV $VIRTUAL_ENV

COPY . /app

# Ajout d'un utilisateur non root
RUN useradd -m myuser
USER myuser

# Démarre l'application
# CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]