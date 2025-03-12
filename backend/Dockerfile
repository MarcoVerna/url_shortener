FROM python:3.13.2-slim AS base

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

COPY src src
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

FROM python:3.13.2-slim AS final

COPY --from=base /app/wheels /wheels

RUN pip install --no-cache /wheels/* fastapi uvicorn && rm -rf /wheels

EXPOSE 8000

CMD ["uvicorn", "url_shortener.main:app", "--host", "0.0.0.0", "--port", "8000"]