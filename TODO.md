# Testing
* AsyncModelUpdater and GoogleFileUpdater arent really working
* TensorFlowRoofProvider, isolate TF from the rest of the logic.
* pv_solar_benefits
* test web_server by refactoring the parser into a function: 
https://stackoverflow.com/questions/18160078/how-do-you-write-tests-for-the-argparse-portion-of-a-python-module

# Design
* Put secrets into environment variables
* Dockerize
* Cleanly initialize the components of the --develop server. Encapsulate that
 from the app.py