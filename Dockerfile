FROM python:3.10

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

#ENTRYPOINT [ "python" ]

#CMD [ "app.py" ]

#CMD [ "gunicorn", "app:app", "--host", "0.0.0.0", "--post", "8080"]
CMD ["gunicorn", "app:app", "-w", "2", "-b", "0.0.0.0:8080"]
