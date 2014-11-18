The purpose of this project is for presenting how a a linear test automation framework(record&playback) based on a 
Selenium IDE script exported to python webdriver can evolve to a modular,data driven,keyword driven and a hybrid test automation framework.
  
- deploy the autframeworks site - note that the selenium tests will point by default to the following url:http://localhost:81/autframeworks/
- run the python project file ftests.py to run all the tests
- all the unit tests for all frameworks are found in utests.py
- scripts are split in dedicated packages corresponding to the type of automation framework
- in config package you can find utilities and constants
- in data folder is present an xls that contain sheets for different scenarios desired per type of automation framework
- look at the /data/project_architecture.png for the architecture of the project and flow details
- the drivers for IE and Chrome change at certain intervals for different browser versions support( download and replace in workspace the drivers for newer versions)