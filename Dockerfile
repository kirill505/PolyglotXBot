FROM python:3.9.12

WORKDIR .

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD exec uvicorn --port $PORT --host 0.0.0.0 main:app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]