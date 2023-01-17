FROM tadeorubio/pyodbc-msodbcsql17

RUN pip install --upgrade pip

ENV SRC_DIR /app

WORKDIR ${SRC_DIR}

COPY .  ${SRC_DIR}

RUN pip install flask

RUN pip install -r requirements.txt

RUN export FLASK_APP=wsgi.py

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]