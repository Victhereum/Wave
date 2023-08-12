# Wave

Caption and Translation API

### Build and Run the Docker Image Locally:

```$ docker compose -f local.yml build```

```$ docker compose -f local.yml up```

### Make local migrations:

```$ docker compose -f local.yml run --rm django python manage.py makemigrations```

```$ docker compose -f local.yml run --rm django python manage.py migrate```

### Docs:

```localhost:8000/api/v1/docs```
