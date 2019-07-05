# Webtentacle
Webtentacle is project for active/passive scanning a web application, by default only web headers configuration fingerprinting is set up.
The scanning is running in cron regularly and the results gathered to SIEM (Splunk) where are further analyzed.
### Prerequisites
you need to install Docker to be able to run the application
- MAC: [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
- NIX: 
    - CentOS 
        ```console
        sudo yum install -y yum-utils device-mapper-persistent-data lvm2
        sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        sudo yum install docker-ce docker-ce-cli containerd.io
        sudo systemctl start docker
        ```
    - Debian
        ```console
        sudo apt-get update
        sudo apt-get install apt-transport-https ca-certificates curl gnupg2 \
        software-properties-common
        curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
        sudo add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable"
        sudo apt-get update
        sudo apt-get install docker-ce docker-ce-cli containerd.io
        ```
- Windows: [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-windows)

## Define your websites to be scanned
Open the file _config.yml_ and in section
```yml
webapps:
  - 10.0.2.5
  ```
  you can add here FQDNs hosting a web application. 
## Running the application
Within the directory webtentacle start:
```console
./docker-build-run.sh
```
or
```console
docker-compose up
```
Currently the cron is set for running every 5 minutes up, you can change this in a file _entry.sh_
## Changing the default passwords
Open **.env** file and change the passwords
## Reading the results
On your local machine will be running an Enterprise instance of Splunk reachable at:
http://localhost:8000
Credentials for admin and webtentacle user is stored in _.env_ file
## Versioning
:wrench:
## Authors
* **Monika vos Mueller**
## License
This project is licensed under the 2-Clause BSD License - see the [LICENSE](LICENSE) file for details
## Acknowledgements
* :alien:
