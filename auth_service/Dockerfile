# Stage 1: Build dependencies
FROM python:3.11.9 AS build

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# Stage 2: Run application
FROM python:3.11.9-slim AS runtime

WORKDIR /app

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY templates /app/templates
COPY static /app/static
COPY app.py /app/app.py

EXPOSE 5001

RUN useradd appuser
USER appuser

CMD ["python", "app.py"]