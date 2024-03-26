FROM python:3.12.2-slim

ENV APP_HOME /app
ENV PYTHONPATH /app

WORKDIR ${APP_HOME}

COPY ./requirements.txt ${APP_HOME}

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR $APP_HOME

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
