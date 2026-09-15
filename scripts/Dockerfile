FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml requirements.txt README.md ./
COPY wtinydb/ ./wtinydb/
COPY tests/ ./tests/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

CMD ["pytest", "--cov=wtinydb", "--cov-report=term-missing", "tests/"]
