FROM python:3.13.2-slim

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src url_shortener

CMD ["python", "url_shortener/url_shortener.py"]

