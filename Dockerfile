FROM python:3.9.12

WORKDIR .

# ENV PORT 8080

COPY . .

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]