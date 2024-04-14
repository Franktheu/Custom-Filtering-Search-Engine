                                           Project Overview
In this project, we'll build a custom-filtering search engine that uses filtering to reorder results. The engine will get results from the Google API, store them, then rank them based on filters we define. We'll end up with a basic search page and results list.

We'll use visual studio code to write our code and run it.

Project Steps

Setup a programmable search engine Custom Search API, 
Create an API key for the engine, 
Create a module to search using the API, 
Create a Flask application to search and render results, 
and create filters to re-rank results before displaying them.

FILE OVERVIEW:

1. app.py - the web interface
2. filter.py - the code to filter results
3. search.py - code to get the search results
4. settings.py - settings needed by the other files
5. storage.py - code to save the results to a database

LOCAL SETUP
Installation
To follow this project, please install the following locally:

Python 3.9+
Required Python packages (pip install -r requirements.txt)

OTHER SETUP
You will need to create a programmable search engine and get an API key by following these directions. You will need a Google account, and as part of this you may also need to sign up for Google Cloud.

Other files
You'll need to download a list of ad and tracker urls from https://github.com/Franktheu/Custom-Filtering-Search-Engine. We'll use this to filter out bad domains. Please save it as blacklist.txt.

RUN
Run the project with:

'pip install -r requirements.txt'  
 then 'flask --debug run'
