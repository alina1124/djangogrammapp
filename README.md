# Djangogramm
Djangogramm is a social media platform for sharing photos with your followers

# Go to the site
[Djangogramm](https://web-production-0387.up.railway.app/)

# Technology Stack
This project was built using Django and uses Amazon S3 to store images.

# Key Features
* Create, delete, like, comment photos
* Follow other users
* Add tags for photos
* Searching for specific users and tags
* Edit profile

# Preview
![djangogramm](https://user-images.githubusercontent.com/99839351/207478168-55305ea8-70d1-4fd0-a8bf-03c93b094eb0.gif)

# How To Use
If you have an Djangogramm account, you need to enter your username and password on the login page. Otherwise, you need to click `register here`. Next, you enter your personal information and receive a confirmation message to your e-mail. Click on the link in the email and you will be redirected to your profile page on Djangogramm.

![register_hint](https://user-images.githubusercontent.com/99839351/207478208-4352575d-b2d7-4575-92b9-037caa0c87eb.jpg)

# How to Install the Project
To clone and run this application, you'll need [Git](https://git-scm.com) .From your command line:
```
# Clone this repository
  git clone https://github.com/alina1124/djangogrammapp.git

# Create and activate venv
  python -m venv venv
  venv\Scripts\activate

# Go into the repository
  cd djangogrammapp
  
# Install packages from requirements.txt
  pip install -r requirements.txt
  
# Apply migrations to the database
  python manage.py migrate
  
# Create Amazon S3 bucket to store images

# Create Environment Variables:
  SECRET_KEY
  DEBUG_VALUE
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  EMAIL_USER
  EMAIL_PASS  
```



