# day40_100
I am currently engaged in a 100-day Python Bootcamp, which I am documenting and sharing my progress on GitHub. The boot camp is designed to progressively intensify, allowing me to deepen my understanding and proficiency in Python programming.

Additionally, I have chosen to include the beginner, intermediate and advanced in my documentation to provide a valuable reference for my future growth and development.

----------------
# Flight Deals Notification System

## Overview
This project is designed to help users receive notifications about cheap flight deals. Users can fill out a Google Form to provide their credentials and opt-in to receive notifications. The system uses the SHEETY API to extract user emails from the Google Form responses and automatically sends notifications if any flight price drops below the listed price on the Google Sheet.

## Features
- __Google Form Integration:__ Collects user credentials and email addresses from a Google Form and linked it to a Google Sheet.
- __SHEETY API Integration:__ Extracts user emails from the Google sheet.
- __Automatic Notifications:__ Sends emails to users when flight prices drop below the listed price.
- __Support for Indirect Flights:__ Now includes support for notifying users about cheaper indirect flight options.

## How It Works

1. __User Sign-Up:__ Users fill out a Google Form to sign up for notifications.
   
![](https://github.com/AlvinChin1608/day40_100/blob/main/Google_Form_Screenshot.png)

2. __Data Extraction:__ The SHEETY API extracts user emails from the Google Form responses.
   
![](https://github.com/AlvinChin1608/day40_100/blob/main/Google_Sheet_Screenshot.png)

3. __Flight Price Monitoring:__ The system monitors flight prices including in-direct flights and then compares them with the listed prices on the Google Sheet.
   
![](https://github.com/AlvinChin1608/day40_100/blob/main/Pycharm_console_Screenshot.png)
   
4. __Notification:__ If a flight price drops below the listed price, users receive an email notification. The system now also checks for cheaper indirect flights and notifies users accordingly.
   
![](https://github.com/AlvinChin1608/day40_100/blob/main/Notification_Email_Screenshot.PNG
)

Google Form: https://forms.gle/mJHtbRXsgXLJUz4v5

Google Sheet: https://docs.google.com/spreadsheets/d/1nPTyNo2Nb9c9J-BQWFlBvtxhH-N2-r_51QJbuvpxCcQ/edit?usp=sharing
