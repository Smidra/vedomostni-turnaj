FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python-dev build-essential pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
ENV FLASK_APP=flask_app.py
CMD ["flask_app.py"]
