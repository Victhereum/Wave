set -o errexit  # exit on error

pip install -r requirements/production.txt

python manage.py collectstatic --noinput
python manage.py spectacular --color --file schema.yml
python manage.py migrate
