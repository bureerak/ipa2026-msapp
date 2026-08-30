FROM python

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY . /app

CMD ["python3", "-u", "scheduler.py"]
