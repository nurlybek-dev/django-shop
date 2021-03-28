# django-shop
Implementation simple shop on django.

Features:
- Standat django user system
- Cart with add/delete items
- Products
- Product Rating system (1-5 star)
- Create\Cancel Orders
- Standart django admin panel


# Install
    git clone https://github.com/nurlybek-dev/django-shop.git
    pipenv install
    or
    pip install -r requirements.txt

    rename .env-copy > .env
    and update it

    python manage.py migrate
    python manage.py runserver

In Production, media files are stored in the AWS S3 Storage. If you need that export AWS enviroment variables or change `config/settings.py` before deploy it.