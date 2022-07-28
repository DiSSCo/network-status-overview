# network-status-overview  
  
An application that identifies the progress of
the DiSSCo project in terms of digitisation. It uses
GBIF and GeoCASe as the primary data sources.  
  
The application is build to do the following:  
- Extract data from GBIF and GeoCASe
- Reformat the data to usable dictionaries
- Save the data inside the DiSSCo database
- Provide an graphical endpoint
- Render graphs in a HTML document

The application makes use of the following libraries:  
- CSV (reading and writing csv files, Python)
- Requests (questioning DiSSCo API, Python)
- Flask (api endpoint, Python)
- Plotly (graphs, Python as well as Javascript)
- Jquery and AJAX (HTML rendering and fetching API, Javascript)
- Bootstrap (grid system, CSS)

### Using the application(s)
The repository consists not out of one, but multiple applications that each
represent a part of the overall concept of the Network Status Overview.
Applications are divided in the folder structure and each contain their
'own' sub repository. Resources however, like the database model and 
information, are stored at the top level. This way every application can 
make use of these without the need to change each individual folder 
on updating the information.

#### The Processing Service 
The Processing Service exists to collect and format the data from GBIF and GeoCASe
and save these in the DiSSCo Postgres database. Different properties are 
collected and used to measure the amount of digitsation between the infrastructures.
Notable are: the amount of datasets, specimens per specimen type, issues and flags.
The Processing Service is a fully automated application that needs to be run 
every month. The Dashboard uses the months (of years) to visualize the data.
A Kubernetes cronjob has been installed to let the service run at every second 
day of a new month (at 00:00). A logger will display the process of the application
and eventually display errors. Running the Processing Service schould take around 
3-5 minutes.
