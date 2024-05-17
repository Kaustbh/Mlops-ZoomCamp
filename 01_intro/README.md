# Introduction

Machine Learning engineering extends beyond merely running experiments; it aims to leverage machine learning capabilities in real-world applications. **MLOps** is a framework comprising principles and practices designed to efficiently manage the entire Machine Learning lifecycle—from experimentation to deployment.

**MLOps** encompasses:

- Version control for both data and model artifacts.
- Integration of the ML development and release process within a Continuous Integration/Continuous Deployment (CI/CD) ecosystem.
- Monitoring of model performance in production to ensure ongoing effectiveness.


# Environment Setup

This guide outlines the steps for configuring a development environment, specifically tailored for Linux OS. We'll be utilizing an Ubuntu server rented on AWS, focusing on configurations suitable for our needs.

**Note:** All configurations performed locally are intended for Windows OS due to my current setup on a Windows laptop.

## Step 1: Launching an EC2 Instance

- Navigate to the AWS Console and launch an EC2 instance using the Ubuntu flavor, selecting a `t2.xlarge` size.
- Download the secret access keys (`.pem` file).
- Note down the public IP address assigned to the instance.


## Step 2: Connect to Ubuntu EC2 server ##

* [Optional] Move .pem secret access keys file to .ssh folder in home directory
* Execute the following command from .ssh directory to change the permission of .pem file to protect it

  ``` sh
  chmod 400 downloaded_pem_file
  ```

* Execute the following command to connect to the server

  ``` sh
  ssh -i pem_file ubuntu@public_ip
  ```

* For ease of connecting the server add the connection details in config file in .ssh directory.

  ``` sh
  nano ~/.ssh/config
  ```

* If config file is missing you can create a new one

  ``` sh
  touch config
  ```

  Add the following and save it.

  ```
  Host short-name-of-your-choice
       Hostname public-ip-of-ec2
       User ubuntu
       IdentityFile path-to-.pem-file
       StrictHostKeyChecking no
  ```

  Now run ```ssh short-name-of-your-choice``` to quickly connect to the ubuntu server. 


## Step 3: Configuring the Ubuntu Server ##

### Install Anaconda ###

* Obtain the Linux (x86) version download link from the Anaconda website and execute the following to download the file on the server:

  ``` sh
  wget link_copied_from_anaconda_website
  ```

* Install the downloaded file:

  ``` sh
  bash downloaded_installation_file
  ```

  If required, logout and re-login to the server.

### Installing Docker ###

* Next we install Docker. However if you run into "Package ‘docker.io’ has no installation candidates" error just update the system first and then try installing again.

  ``` sh
  sudo apt update
  sudo apt install docker.io
  ```

* Add your user to the Docker group to run commands without sudo:

  ``` sh
  sudo groupadd docker
  sudo usermod -aG docker $USER
  ```

### Installing Docker Compose ###

* Create a separate directory to install docker compose.

  ``` sh
  mkdir soft
  cd soft
  ```

* To install Docker Compose get the latest release version for your OS (https://github.com/docker/compose -> Releases -> Assets) and make it executable.

  ``` sh
  wget link-from-docker-compose-github -o docker-compose
  chmod -x docker-compose
  ```

* Ensure Docker Compose is accessible globally by editing .bashrc:

  ``` sh
  nano ~/.bashrc
  export PATH="${HOME}/soft:${PATH}"
  source .bashrc
  ```

  If required, logout and re-login to the server.

### Running Docker ###

* To verify that docker setup the following should run successfully.

``` sh
  docker run hello-world
```

### VS Code Setup ###

* Install "Remote - SSH" extension in VS Code
* Click on "Open a Remote Window" icon on bottom-left corner
* From dropdown select "Connect to Host" and then select Linux. That opens a new VSCode window.
* In terminal clone MLOps-Zoomcamp project

  ``` sh
  git clone https://github.com/DataTalksClub/mlops-zoomcamp.git
  ```

* Create a notebooks folder:

  ``` sh
  mkdir notebooks
  cd notebooks
  ```

* The notebooks are hosted on the server. However to access them locally we need to do the port forwarding that can be easily done in VSCode. Open Ports section next to terminal in VSCode and enter 8888 as port for source and enter. This will add the port to allow traffic.
* Next open jupyter notebook

  ``` sh
  jupyter notebook
  ```

**Congratulations Your environment is now configured.**


# Important #
Remember to stop the EC2 instance when it's not in use to avoid unnecessary charges.