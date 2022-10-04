FROM python:3.10

RUN pip install --upgrade pip

ENV SRC_DIR /app

WORKDIR ${SRC_DIR}

COPY .  ${SRC_DIR}

RUN pip install flask

RUN pip install -r requirements.txt

RUN export FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]