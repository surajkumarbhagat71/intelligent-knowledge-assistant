# Docker setup

Run these commands from the folder containing docker-compose.yml.

## First setup / after changing Dockerfile or requirements.txt

docker compose down
docker compose build
docker compose up -d
docker compose ps
docker compose logs --tail=100 django

Open: http://localhost:8000

## Normal start next day

docker compose up -d
docker compose ps

## Stop

docker compose down

## Logs

docker compose logs -f django
docker compose logs -f db

## Do NOT run every time

docker compose build --no-cache
docker system prune -f

These are not normal start commands.

## PostgreSQL from Windows

localhost:5433

Inside Django container:

DB_HOST=db
DB_PORT=5432

## Required Django static setting

STATIC_ROOT = BASE_DIR / "staticfiles"

Recommended media setting:

MEDIA_ROOT = BASE_DIR / "media"

## If localhost:8000 gives ERR_EMPTY_RESPONSE

docker compose ps
docker compose logs --tail=150 django


docker compose exec django python manage.py createsuperuser
docker compose exec django python manage.py makemigrations
docker compose exec django python manage.py migrate
