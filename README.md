# **HVA Big data project: KNVB 2**

This project was Issued by the KNVB through Sport Data Valley. It is a website which lets professional football organizations see the insightful statistics about their players regarding anthropometric and physical results in the form of a dashboard. KNVB currently only issues out paper reports to their organizations. This dashboard helps bring the data to an online enviroment.

## **Project Architecture**
This project was made with Python through the FLASK framework. To learn more about FLASK, please visit: https://flask.palletsprojects.com
<br>The data is hosted in a relational database using mySQL.

## **Prerequisites**
- Python (tested with 3.8.x or higher).
- A host with mySQL- and WSGI-support where you can store the data.

## **Installing**

1. Clone the project to your personal repository and write out commands from the root of the project.
2. Ensure you have pip installed with this command: _<code>pip3 install pip --upgrade --user</code>_
3. Install the necessary packages with this command: _<code>pip3 install -r requirements.txt</code>_
4. app.py requires config changes. Change the credentials to your own host.
5. dev_bdproject.sql is an export of our database through phpmyadmin. Import the sql file in your own database interface.
6. Run app.py and check the terminal on which adress the the program is running on.
7. Test accounts have been made named sdz/sdz and tos/tos to gain access to the dashboard and show that different data is used for different organizations.

## **Docker**
This application's process is being streamlined with the help of Docker. You can visit https://docs.docker.com/get-started/ to learn more about Docker and it's implications.
- You can use Docker in this project to run the application locally on you own environment.
- Docker is also used in a DevOps CI/CD pipeline to automatically build and deploy new images to GitLab when pushing changes to the staging or main branch.

### **Use Docker locally**
When using Docker, there are multiple ways to run the application locally. Below are the three most common ways to do it.

#### **1. Using Docker Compose**
Docker Compose has been added to this project for ease of use. 
1. You can build and run this application locally by entering: <code>*docker-compose up*</code> into the terminal. 
2. Docker Compose will handle the whole process and all there's left to do is to visit: http://localhost:5000/

#### **2. Using the VS Code Docker extension**
VS Code has a great Docker extension that you can use to run this application locally.
1. First download the Docker extension in VS Code by searching for the extension: ms-azuretools.vscode-docker
2. Right click on the Dockerfile in this project and click on the option: *Build Image*
3. After the image has been built, go the Docker extension in the left taskbar and run the preferred image by right clicking the option: *run*
4. The only step left now is to visit: http://localhost:5000/

#### **3. Using the terminal**
If the first two options are not applicable to you, then we can always use the terminal.
1. First build and tag the image by entering: <code>*docker build -t knvb-team-2 .*</code> into the terminal.
2. Run the built image on port 5000 by entering: <code>*docker run -p 5000:5000 knvb-team-2*</code> into the terminal.
3. The only step left now is to visit: http://localhost:5000/

### **Docker with CI/CD pipeline**
This project contains a CI/CD pipeline that automatically builds Docker images and adds them to the Docker Container Registry when pushing changes to the staging or main branch.
With the Docker Container Registry integrated into GitLab, every GitLab project can have its own space to store its Docker images. You can visit this URL to learn more about the Container Registry: https://docs.gitlab.com/ee/user/packages/container_registry/  
The project's images can be viewed at the following URL: https://gitlab.fdmci.hva.nl/knvb-2/knvb-team-2/container_registry/

#### **Run a Docker image from the Container Registry**
1. We first need to get a Deploy Token with at least *read_registry* access from GitLab. That token will be used to login to the Container Registry. Follow the steps in this URL to obtain such a token: https://docs.gitlab.com/ee/user/project/deploy_tokens/index.html
2. The second step is to authenticate with the Container Registry. You can do that by entering: <code>*docker login gitlab.fdmci.hva.nl:5050 -u (token username) -p (token)*</code> into the terminal.
3. After logging in, we now need to choose which image we want to run from the Container Registry. Use this URL: https://gitlab.fdmci.hva.nl/knvb-2/knvb-team-2/container_registry/, then choose an image and copy the image path like this: *gitlab.fdmci.hva.nl:5050/knvb-2/knvb-team-2/knvb-images:latest*.
4. With this image path we can now enter: <code>*docker run gitlab.fdmci.hva.nl:5050/knvb-2/knvb-team-2/knvb-images:latest -p 5000:5000*</code> into the terminal. This will run the image on port 5000.
5. The only step left now is to visit: http://localhost:5000/