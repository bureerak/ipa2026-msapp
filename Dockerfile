FROM python

RUN pip install flask

RUN pip install pymongo

COPY ./static /home/myapp/static/

COPY ./templates /home/myapp/templates/

COPY ./app.py /home/myapp/

CMD ["python3", "/home/myapp/app.py"]

EXPOSE 8080
