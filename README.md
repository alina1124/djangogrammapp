# Djangogramm
Djangogramm is a social network platform for sharing photos with your followers

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

Update the System
```
sudo apt-get update
```

Clone this repository
```
git clone https://github.com/alina1124/djangogrammapp.git
```

Go into the repository
```
cd djangogrammapp
```

Download django usig pip
```
sudo apt install python3-pip -y
```
```
sudo apt-get install libpq-dev
```
Install packages from requirements.txt
```
pip install -r requirements.txt
```  
Create Amazon S3 bucket to store images and add default image for the avatar with the ```default_avatar.jpg``` name.
Add bucket polisy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucket_name/*"
        }
    ]
}
```

Create Environment Variables:
```export VARIABLE="value"```
  ```
  SECRET_KEY
  DEBUG_VALUE
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  EMAIL_USER
  EMAIL_PASS  
  AWS_STORAGE_BUCKET_NAME
```
```
python3 manage.py makemigrations
```
This will create all the migrations file (database migrations) required to run this App.
Now, to apply this migrations run the following command
```
python3 manage.py migrate
```
One last step and then our App will be live. We need to create an admin user to run this App. On the terminal, type the following command and provide username, password and email for the admin user

```
python3 manage.py createsuperuser
```
 We just need to start the server now and then we can start using Djangogrammapp. Start the server by following command

```
python3 manage.py runserver
```



