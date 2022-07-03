# django-online-shop

This project is a store website.
In Backend, the Django framework, celery , celery beat and gunicorn are used, and the template is made with Bootstrap, JavaScript, and so on. The project uses Docker (Nginx and RabbitMQ broker and celery and postgres database)
It is possible to register (by sending an activation SMS) and login user.
It is possible to buy, like and save products, comment and rate and search products, and ...
Products are categorized. Product images are stored in AWS. Celery is used to access the AWS bucket.
Sessions have been used to implement the shopping cart.
AbstractBaseUser is used to implement the user model.

===========================================================
# Installation guide:

create virtualenv and activate

pip install -r requirements.txt

cp .env-sample .env

python manage.py runserver
