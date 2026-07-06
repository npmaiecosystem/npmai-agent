FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
COPY npmai_agents ./npmai_agents

RUN pip install --no-cache-dir -e .

RUN python -c "import sys; print('Path:', sys.path); import npmai_agents; print('Imported npmai_agents successfully'); print('Version:', getattr(npmai_agents, '__version__', 'unknown'))"

ENTRYPOINT ["npmai"]
CMD ["--help"]
