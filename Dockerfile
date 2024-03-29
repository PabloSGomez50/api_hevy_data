FROM python:3.9.18-alpine

WORKDIR /fran_app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

# CMD uvicorn main:app --host 0.0.0.0 --port 8080