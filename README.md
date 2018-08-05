# tms-nachbarstrom-python
Repo for the Python functions of Nachbarschaftstrom.
# Get the files
* Get the source code:
````commandline
sudo apt-get update -y
git clone https://github.com/tomasruizt/tms-nachbarstrom-python
cd tms-nachbarstrom-python/
````

# If not running on Google Cloud
* Prepare a folder for the credentials:
````commandline
mkdir cred
````
* If running on Azure, you can find a machine address e.g. 
'the-machine-address' to connect to. 
* Put the Google service credentials on the server. For example, by copying 
them from your machine to the server:
````commandline
scp -i private_key google_service_credentials.json 
the-machine-address:~/tms-nachbarstrom-python/cred
````
# Setup the environment
* Run the setup script for 'Ubuntu 16.04 LTS', or follow its steps, if you are
 on another platform.
````commandline
bash ./setup_ubuntu16.sh
````
* Your new Python environment is located in the 'env-prod/' folder.
* Activate your Python environment. If you are on Windows,
replace the command with 'env-prod/Scripts/activate'.
```commandline 
source env-prod/bin/activate
```
* Set your environment variables, for example API keys.
* Finally, you can start the server either in 'production' mode or in 
'develop' mode.

For production:
```commandline
nohup sudo --preserve-env python3 -m nachbarstrom.inference.web_server.app >>logs 2>>logs &
```
* Here ``preserve-env`` is used to keep the environment variables when using ``sudo``.
* We use ``-m`` to call the ``app.py `` as a module.
* ``>>logs 2>>logs`` redirects all output to the ``logs`` file.
* The ``&`` command detaches the process from the command line.

For development:
````commandline
sudo --preserve-env python3 -m nachbarstrom.inference.web_server.app --development
````


# Testing
Make sure your Python environment is active.
* Run unit tests. The option 'rs' stands for report skipped.
````commandline
pytest -rs
````
* Integration tests: Usually launched on the 'develop', but not necessarily.
```commandline
pytest -rs --integration
```

# Stopping the server
```commandline
sudo killall python3
```

# Development tips
Lint the code:
````bash
pylint app.py
````
Use static type checker:
````bash
mypy --ignore-missing-imports app.py
````