FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md requirements.txt ./
COPY npmai_agents ./npmai_agents

RUN pip install --no-cache-dir -e ".[full]"

RUN python -c "
import sys
print('Python path:', sys.path)
import npmai_agents
print('npmai_agents version:', npmai_agents.__version__)
from npmai_agents.cli import app
print('CLI Dne')
"

RUN npmai --help

ENTRYPOINT ["npmai"]
CMD ["--help"]
