FROM python:3.11
EXPOSE 5000
WORKDIR /app
RUN pip install flask
CMD ["pip", "install", "-r", "./requirements.txt"]
RUN pip install Flask-SQLAlchemy
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]