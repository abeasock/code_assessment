# Coding Assessment

Please save ALL of your code, as you’ll need to submit this to GitHub upon completion for review.
All the data needed for the exercises can be downloaded from:
https://github.com/abeasock/coding_assessment

### Part I
Datasets needed for exercise: 
- patients.csv 
-	appointments.csv

Please write code to accomplish the following steps and save all the code for Part I in a Python script named *part_1.py*.
  1. Join the two datasets and keep only matching records.
  2a. Derive a new variable day_of_week to provide the day of the week the appointment was scheduled for.
  2b. Take a frequency count of day_of_week to examine what day of the week patients are most likely to not show up for an appointment.
  3. Bin the ages into 10 groups and plot status by age. 
  4. Build a basic model to predict whether a patient shows up for their appointment. The intent of this is to show you understand the basic steps to building a model…the model may not be strongly predictive and this is ok. 

### Part II
Dataset needed for exercise: 
- locations.csv

Save all the code for Part II in a new Python script named *part_2.py*.

For this exercise, register for an API key on World Weather Online. You can sign up for their Premium Weather API for a free 60 day trial (no credit card needed to sign up) and this will give you access to historical weather data. https://developer.worldweatheronline.com/signup.aspx

For each observation in locations.csv, make a call to the API for that time and location and retrieve the data as JSON format. The following weather features from the API should be collected:
	areaName, population, tempF, weatherDesc, precipMM, cloudcover
Return a Pandas DataFrame that contains the original variables from locations.csv plus the ones listed above to be collected from the API. Save the new DataFrame as a csv files named locations_weather.csv
Submitting

When you finish the coding assessment:
-	Create a repository on GitHub
-	Upload your scripts for Part I and II, and the csv from Part II to your repository
-	Create a simple ReadMe file to explain your work
-	Send the link for your GitHub repository to the recruiter 
