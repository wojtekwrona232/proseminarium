FROM amd64/python:3.6.8 as builder
WORKDIR /app
COPY ./ .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python app.py
