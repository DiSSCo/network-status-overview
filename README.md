# network-status-overview  
  
An application that identifies the progress of
the DiSSCo project in terms of digitisation. It uses
GBIF and GeoCASe as the primary data sources.  
  
The application is build to do the following:  
- Extract data from GBIF and GeoCASe
- Reformat the data to usable dictionaries
- Save the data inside multiple csv files
- Draw the data as graphs

The application makes use of the following libraries:  
- CSV (reading and writing csv files)
- Plotly (graphs)
- Requests (questioning APIs)

### Using the application
The application consists of separate functions that 
fill in each other. Functions are divided per API,
but all are called on from the main.py file by calling on
main. This will list all individual methods that 
can be called on. Insert a method's name to call it on.
It is also possible to call on all methods in order
by typing 'all'.  
  
A method will first request data from GBIF and/or GeoCASe,
after it will be prepared and stored in a dictionary.
The dictionary will then be used for writing the 
CSV files and creating the graphs.  
  
CSV files are stored in: /csv_files
