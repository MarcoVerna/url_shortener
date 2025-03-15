FROM python:3.13.2-slim

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src url_shortener/src

# CMD ["python", "url_shortener/url_shortener.py"]
ENTRYPOINT ["python","url_shortener/src/url_shortener.py","--minify", "https://www.example.com/path?q=search"]

