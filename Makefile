backup_path = "core/fixtures/backup.json"
branch_name = $$(git branch --show-current)
changed_files = $$(git ls-files '*.py')
os_type = $$(uname -sr)
upload_path = "core/uploads/"

all: help
checks: lint test
install: update

# activate:
# 	case $(os_type) in "Darwin*"
# 		@echo 'Mac OS X';;
# 	esac

backup:
	mkdir -p core/.fixtures
	python -Xutf8 manage.py dumpdata \
		--natural-primary \
		--exclude=contenttypes \
		--exclude=auth.permission \
		--exclude=admin.logentry \
		--exclude=sessions.session > $(backup_path)
	echo $(backup_path)

env:
	python -m venv env

fixdb:
	make backup
	rm core.db
	make migrate
	make restore

help:
	@echo
	@echo "Usage: make [commands] e.g. make backup"
	@echo "* backup  | Export database content as json for backup purposes"
	@echo "* env     | Creates a virtual environment in current working directory"
	@echo "* fixdb   | Fixes your database if it gets corrupted. Creates a backup and also restore current data"
	@echo "* help    | Displays this help text"
	@echo "* install | Syncs the project dependencies"
	@echo "* lint    | Checks if code is conforming to best practices like PEP8"
	@echo "* migrate | Runs makemigrations and migrate commands"
	@echo "* push    | Pushes committed changes to the Gitlab remote repository"
	@echo "* restore | Loads previously backed up data into the database"
	@echo "* server  | Spawns the Django server"
	@echo "* test    | Runs unit test"
	@echo "* update  | Syncs the project dependencies"
	@echo


lint:
	pylint $(changed_files)
	flake8 .

migrate-venv:
	python manage.py makemigrations --dry-run -v 2
	python manage.py makemigrations
	python manage.py migrate

push:
	git pull
	git push -u origin $(branch_name)

restore:
	python manage.py loaddata $(backup_path)

server:
	python manage.py runserver 0.0.0.0:8000

venvs:
	cd venv/bin/activate

test:
	python manage.py test -v 2 --keepdb

shell:
	python manage.py shell

shell_plus:
	python manage.py shell_plus

update:
	pip install -r requirements/local.txt

admin:
	python manage.py createsuperuser

redis:
	redis-server --port 6379

celery:
	python -m celery -A config worker -l info

minio:
	minio server $(upload_path)

docker-buildup:
	docker compose -f local.yml up --build

docker-up:
	docker compose -f local.yml up

docker-down:
	docker compose -f local.yml down

# GitHub
pr_create:
	gh pr create --base staging --head dev --fill

pr_merge:
	gh pr merge $(pr)

# DOCKER
# ---------------------------------------------------------------------------------------------------------------------
# Local development commands
# ---------------------------------------------------------------------------------------------------------------------

# Run the local development server
run-local:
	docker-compose -f local.yml up --no-build --remove-orphans

run-production:
	docker-compose -f production.yml up --no-build --remove-orphans

run-local-build:
	make local-down && docker-compose -f local.yml up --build

run-production-build:
	make production-down && docker-compose -f production.yml up --build --remove-orphans


local-down:
	docker-compose -f local.yml down --remove-orphans

production-down:
	docker-compose -f production.yml down --remove-orphans

build-local:
	docker-compose -f local.yml build

build-production:
	docker-compose -f production.yml build

pre-commit:
	pre-commit run --all-files

# Run tests locally
test-local:
	docker-compose -f local.yml run --rm --remove-orphans django coverage run -m pytest && docker-compose -f local.yml run --rm django coverage report

# Coverage Report
coverage-report:
	docker-compose -f local.yml run --rm django coverage report

# Execute the makemigrations command
makemigrations:
	docker compose -f local.yml run --rm django python manage.py makemigrations

makemigrations-production:
	docker compose -f production.yml run --rm django python manage.py makemigrations

collectstatic:
	docker compose -f local.yml run --rm django python manage.py $@ --no-input

# Execute the custom manage.py run_test command
run_test:
	docker-compose -f local.yml run --rm django python manage.py $@

activate_account:
	docker-compose -f local.yml run --rm django python manage.py $@

# Execute the makemigrations command
merge:
	docker-compose -f local.yml run --rm django python manage.py makemigrations --merge

swagger:
	docker-compose -f local.yml run --rm django python manage.py generate_swagger swagger.json -o -m -u http://localhost:8000

# Execute the migrate command
migrate:
	docker-compose -f local.yml run --rm django python manage.py $@

migrate-production:
	docker compose -f production.yml run --rm django python manage.py migrate

generatesuperuser:
	docker-compose -f local.yml run --rm django python manage.py $@

migrate-fake:
	docker-compose -f local.yml run --rm django python manage.py migrate --fake

create-superuser:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser

# Run the django shell
shell:
	docker-compose -f local.yml run --rm django python manage.py $@ -i python

shell-production:
	docker-compose -f production.yml run --rm django python manage.py shell -i python


createsuperuser:
	docker-compose -f local.yml run --rm django python manage.py $@

# Run the django shell
bash:
	docker-compose -f local.yml run --rm django $@

migrate-all:
	make makemigrations && make migrate


# Open a shell in the container
bash-local:
	docker-compose -f local.yml run --rm django /bin/bash

# ---------------------------------------------------------------------------------------------------------------------
# Services Commands
# ---------------------------------------------------------------------------------------------------------------------

start-web:
	/start

start-beat:
	/start-celerybeat

start-worker:
	/start-celeryworker

start-flower:
	/start-flower
