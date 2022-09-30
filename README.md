# HVA Big data project: Football 2.

This was a five man project made by three BIM, one SE and one CS student. This project was Issued by the KNVB through Sport Data Valley. It is a website which lets professional football organizations see the insightful statistics about their players regarding anthropometric and physical results in the form of a dashboard. KNVB currently only issues out paper reports to their organizations. This dashboard helps bring the data to an online enviroment.

## Project Architecture
This project was made with Python through the FLASK framework. To learn more about FLASK, please visit: https://flask.palletsprojects.com
<br>The data is hosted in a relational database using mySQL.

## Prerequisites
- Python (tested with 3.8.x or higher).
- A host with mySQL- and WSGI-support where you can store the data.

## Installing

1. Clone the project to your personal repository and write out commands from the root of the project.
2. Ensure you have pip installed with this command: _<code>pip3 install pip --upgrade --user</code>_
3. Install the necessary packages with this command: _<code>pip3 install -r requirements.txt</code>_
4. app.py requires config changes. Change the credentials to your own host.
5. dev_bdproject.sql is an export of our database through phpmyadmin. Import the sql file in your own database interface.
6. Run app.py and check the terminal on which adress the the program is running on.
7. Test accounts have been made named sdz/sdz and tos/tos to gain access to the dashboard and show that different data is used for different organizations.

## Docker

A docker file has already been made to streamline the process when running the application. Visit https://docs.docker.com/get-started/ to learn more on how to implement the application with docker.

## Usage

Disclaimer: Peter Odenhoven has stated that the project will continue with another group made up of new big data students.
