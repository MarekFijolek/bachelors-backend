FROM python:3.8.2
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn",  "main:app", "-b", "0.0.0.0:8000"]
