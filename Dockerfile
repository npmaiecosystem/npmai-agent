FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md requirements.txt ./
COPY npmai_agents ./npmai_agents

RUN pip install --no-cache-dir ".[full]"

RUN npmai --help

ENTRYPOINT ["npmai"]
CMD ["--help"]
