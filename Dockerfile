FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
COPY npmai_agents ./npmai_agents

RUN pip install --no-cache-dir -e .

RUN python -c "
import sys
print(sys.path)
import npmai_agents
print('OK: npmai_agents found')
print('Version:', getattr(npmai_agents, '__version__', 'No version'))
"

ENTRYPOINT ["npmai"]
CMD ["--help"]
