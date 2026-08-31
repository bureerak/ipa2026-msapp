FROM python

WORKDIR /app

COPY req.txt .

RUN pip install -r req.txt

COPY database.py .
COPY worker.py .

CMD ["python", "worker.py"]