FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY main.py wsgi.py ./
COPY providers/ ./providers/

USER nobody

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "wsgi:app", "--capture-output", "--log-level=debug"]
