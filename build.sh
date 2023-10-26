set -o errexit  # exit on error

# apt-get update && \
#     apt-get install -y ffmpeg

pip install -r requirements/production.txt

python manage.py collectstatic --noinput
python manage.py compress

python manage.py spectacular --color --file schema.yml
python manage.py migrate
