FROM python:3.9.10

WORKDIR /app.py
COPY . /app.py

RUN pip3 install -U pip
COPY requirments.txt .
RUN pip3 install -r requirments.txt

CMD ["python3", "-m", "app"]
