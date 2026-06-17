FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin aegisfleet

COPY api/requirements.txt ./api/requirements.txt

RUN pip install --no-cache-dir -r ./api/requirements.txt

COPY api ./api

USER aegisfleet

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
