# syntax=docker/dockerfile:1
FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

WORKDIR /app

ADD https://astral.sh/uv/0.7.16/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock* README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=secret,id=socket_auth_token \
    if [ -s /run/secrets/socket_auth_token ]; then \
      export UV_DEFAULT_INDEX="https://socket:$(cat /run/secrets/socket_auth_token)@pkgfw.standardmetrics.dev/pypi/simple"; \
    fi && \
    uv sync --locked

COPY src/ ./src/

EXPOSE 8000

ENTRYPOINT ["uv", "run", "python", "src/server.py"]
