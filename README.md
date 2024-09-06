Installation steps:

git clone social-network
cd social-network

python -m venv env_name
source env_name/bin/activate #for ubuntu

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser (optional)

python manage.py runserver

