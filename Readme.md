# Weather API

This API allows you to access weather data for various locations and years. The data can be filtered by date and location. The API also provides statistical information on the weather data.

## Features
- Retrieve weather data for a specific date and location
- Retrieve statistical information on the weather data, including the maximum, minimum, and total precipitation for a specific date and location

## These are the respective API endpoints :

    /api/weather - retrieves weather data
    /api/weather/stats - provides statistics about the data
    /swagger - provides documentation using openapi

## Prerequisites

The following prerequisites are required to use this API:

- Python (3.7 or higher)
- Virtualenv
- SQLite
- AWS account (if deploying to AWS)


# Environment_setup
```base
- python3 -m venv env
- source env/bin/activate
```
# Installation

>Install the required packages:
```base
pip3 install -r requirements.txt
```
# Change directory

>Install the required packages:
```base
cd src
```
## Usage

- Run the following command to create the database and populate it with data:

```bash
python3 -m flask create
```

- Start the API server
```bash
 python3 -m flask run
```
- The API can now be accessed at http://127.0.0.1:5000.

# Endpoints

## **Swagger**
[http://127.0.0.1:5000/swagger/](http://127.0.0.1:5000/swagger/)

##### Weather data
```
GET /api/weather/
```
This endpoint returns a paginated list of weather records. You can filter the results by date and station using query parameters:
```
GET /api/weather/?date=19850103&station=USC00257715
```
##### Statistics
```
GET /api/weather/stats/

```
This endpoint returns statistical information about the weather data. You can filter the results by date and station using query parameters, in the same way as the /api/weather/ endpoint.

### Example Request

``` bash
 curl -X GET "http://127.0.0.1:5000/api/weather?date=19850103&station=USC00257715"
```
### Example Response
```json
[{"date":"19850103","maximum_temperature":22,"minimum_temperature":-111,"precipitation":0,"station":"USC00257715"}]
```


# Testing

## Run the tests

```bash
pytest -v
```


# Deployment
To deploy the Flask application to AWS, you can follow these steps: First, create a Python project with the Flask code in the app.py file. Then, create a new AWS Lambda function with Python 3.8 or a later version runtime. Afterward, package your Python code and its dependencies into a ZIP file and upload it to AWS Lambda. Next, set the handler function of your Lambda function to the name of your Flask application function. Once done, create an API Gateway, REST API, or HTTP API and integrate it with your Lambda function. Finally, deploy the respective APIs to a publicly accessible endpoint and use Amazon RDS to store the ingested data.

By deploying on AWS, developers can leverage scalability and security features such as autoscaling and load balancing, ensuring that their API is always available to handle increasing traffic. Moreover, AWS provides robust security features to protect the API against potential security threats, giving developers peace of mind.

# Screen Shots

![Alt text](/ss1.png?raw=true "Swagger")
![Alt text](/ss2.png?raw=true "Response")





