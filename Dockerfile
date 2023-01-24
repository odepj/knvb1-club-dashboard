FROM python:3.10

RUN pip install --upgrade pip

# Include the ODBC Driver 17 for SQL Server in the container (required for Azure DB)
RUN apt-get update
RUN apt-get update && apt-get install -y gnupg2
RUN apt-get install -y curl apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

ENV SRC_DIR /app

WORKDIR ${SRC_DIR}

COPY .  ${SRC_DIR}

RUN pip install flask

RUN pip install -r requirements.txt

RUN export FLASK_APP=wsgi.py

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]