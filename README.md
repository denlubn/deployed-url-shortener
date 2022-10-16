# Deployed URL Shortener

Link shortening service written on DRF

## Check it out!

[Link shortening service deployed to Heroku](https://)

```shell
login: 
password: 
```

## Installing using Github

Python3 must be already installed

```shell
git clone 
cd 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Getting access
-
- create user via /user/register/
- get access token via /user/token/


Features
-
- JWT authenticated
- Admin panel /admin/
- Documentation is located at /doc/swagger/
- Managing urls
- Creating and customize short url
- Every url has counter
- Registration by mail instead of username