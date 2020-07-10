# Google-Magical-Fairy-Castle
This is a design of improving medical resources utilization through building a platform in the form of websites for 2020 Google Girl Hackathon. 

We cater to timely hospital needs by developing a hospital webpage for hospital users and based on transferred hospital data, we visualize the optimized routes on delivery webpage for delivery men.  

Beijing Dongcheng Area practical data, including first-class hospitals in degree three name list, builded delivery center list and the retrieved location data are used for implementation. 

Source Code:

Static : This folder contains several folders needed to beautify webpages, including css and js code, pictures inserted for HTML ui improvements, 

Templates : This folder contains HTML files for visualizing our functions on several web pages.

Application (Python back-end file) : This is the back-end Python code for the optimized routes algorithm implementation, data get and post from front-end submission and retrieve, data storage in csv file.   

Distance (Excel file) : This is an Excel file containing a distance matrix between hospitals. 

Hospital (csv file) : This is a csv file storing all hospital request data, which contains hospital request number, request date and hospital name, and it is constantly updated once new data is submitted. 

Route (csv file) : This is a csv file storing optimized routes calculated by our algorithm. 


To Get started: 

First, install python packages needed:

pip install cplex

pip install docplex

pip install openpyxl

pip install numpy


Mac User:

Once you have installed the packages, go to the terminal and go to the file. Then type in the command “python application.py”. Once it starts running, open the browser and go to http://127.0.0.1:5000/ to view our platform homepage.

Windows User:

After package installation, double click ‘application.py’. Once it starts running, open the browser and go to http://127.0.0.1:5000/ to view our platform homepage. 
