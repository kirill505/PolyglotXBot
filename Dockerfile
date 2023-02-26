FROM python:3.9.12

WORKDIR .

COPY . .

RUN pip install -r requirements.txt

ENV PORT 8080
EXPOSE 8080

CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]