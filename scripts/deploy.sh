#!/usr/bin/env bash
set -euo pipefail

# GitHub Actions passes the commit ID
SHA="${1:?Missing Git commit SHA}"

if [[ ! "$SHA" =~ ^[0-9a-f]{40}$ ]]; then
    echo "Invalid Git commit SHA"
    exit 1
fi

cd /home/ec2-user/django_web

echo "Deploying commit: $SHA"

# Verify production configuration and data volume
test -f .env
docker volume inspect military_buff_pgdata >/dev/null

# Download new code from GitHub
export GIT_TERMINAL_PROMPT=0
git fetch origin main

# Only deploy commits that belong to main
git merge-base --is-ancestor "$SHA" origin/main

# Avoid overwriting local modifications
test -z "$(git status --porcelain --untracked-files=no)"

# Select the precise commit tested by CI
git checkout --detach "$SHA"

# Validate Docker configuration
docker compose config --quiet

# Start or keep the database healthy
docker compose up -d --no-recreate --wait db

# Back up production PostgreSQL before migrations
mkdir -p /home/ec2-user/backups
chmod 700 /home/ec2-user/backups
umask 077

BACKUP="/home/ec2-user/backups/db_$(date -u +%Y%m%d_%H%M%S).dump"

docker compose exec -T db sh -c \
  'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' \
  > "$BACKUP"

test -s "$BACKUP"
docker compose exec -T db pg_restore -l \
  < "$BACKUP" > /dev/null

echo "Database backup: $BACKUP"

# Build the new Django Docker image
docker compose build web

# Apply pending migrations
docker compose run --rm --no-deps -T web \
    python manage.py migrate --noinput

# Start the updated Django container
docker compose up -d --no-deps web

# Check Django
docker compose exec -T web python manage.py check

# Verify HTTP response

# Wait for Django/Gunicorn to become ready
echo "Waiting for Django to respond..."

READY=false

for attempt in $(seq 1 20); do

    if curl -fsS \
        --max-time 5 \
        -o /dev/null \
        http://127.0.0.1:8000/; then

        echo "Django is ready!"
        READY=true
        break
    fi

    echo "Attempt $attempt: Django not ready yet"
    sleep 2
done

if [ "$READY" != "true" ]; then
    echo "Deployment failed: Django did not become ready"
    docker compose ps
    docker compose logs --tail=100 web
    exit 1
fi

echo "Deployment successful!"


echo "Deployment successful: $SHA"
docker compose ps
