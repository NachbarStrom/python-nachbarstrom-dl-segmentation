# tms-nachbarstrom-python
Repo for the Python functions of Nachbarschaftstrom.
# Setup server
The application runs on Python 3 and needs the packages specified 
in the file 'requirements.txt'. If you worki on Google 
Cloud with an 'Ubuntu 16.04 LTS' os, you can setup the server by doing the 
following steps:
* Update Ubuntu, to get Python 3
* Clone the repository. Give your credentials, since the repo is private.

````commandline
$ sudo apt-get update -y
$ git clone https://github.com/tomasruizt/tms-nachbarstrom-python
$ cd tms-nachbarstrom-python/
````

* Then setup and activate your Python environment:
```commandline
$ sudo apt-get install python3-dev python3-venv python3-pip -y
$ python3 -m venv env
$ source env/bin/activate
$ sudo python3 -m pip install -r requirements.txt
```

* Finally, start running the server:
```commandline
$ nohup sudo python3 app.py >>/dev/null 2>>/dev/null &
```

# Send a request
You can send requests to the server with JSON payloads. You have to 
replace 'SERVER_ADDRESS' with the actual http address, which you can
find on Google Cloud.
```commandline
$ curl -H "Content-Type: application/json" -X POST -d '{"data":[{"lat":"1",
"lng":"2"}]}' http://SERVER_ADDRESS
```
