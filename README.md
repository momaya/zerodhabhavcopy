# Zerodha Equity BhavCopy 
(Mandatory Django + Vue + CSV export on UI)

## Requirements:
Write a standalone Python Django web app/server that:

- Downloads the equity bhavcopy zip from the above page every day at 18:00 IST for the current date.
- Extracts and parses the CSV file in it.
- Writes the records into Redis with appropriate data structures (Fields: code, name, open, high, low, close).
- Renders a simple VueJS frontend with a search box that allows the stored entries to be searched by name and renders a table of results and optionally downloads the results as CSV. Make this page look nice!
- The search needs to be performed on the backend using Redis.

## Technology Stack:

- Python3 based Django Framework
- Vue.js
- Redis Database

## Application Features:

- Search equity stock by name.
- Export search response table to csv.
- Scheduled update of Redis database at 18:00 IST every weekday(i.e, stock market is closed on weekends). 

## Setup Instructions:

- Application is a standalone Python Django web app,to run locally use below commands in python(.venv).
 1.  pip install -r requirements.txt
 2.  python manage.py runserver
- Redis instance created on https://app.redislabs.com/.

## Deployment

- Python Django web app is deployed on Heroku with two dynos:
1. Web - for web application.
2. Clock - for job scheduling.

## Demo 

Heroku App Link - https://zerodhabhavcopy.herokuapp.com/

![image](https://user-images.githubusercontent.com/31745382/117525222-d8cf5900-afde-11eb-8c02-197baeafb31d.png)



