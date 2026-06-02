#!/bin/sh

set -e

if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Waiting for database..."

  until nc -z postgres 5432; do
    echo "Postgres not ready..."
    sleep 2
  done

  echo "Generating Prisma client..."
  prisma generate --schema=app/prisma/schema.prisma

  echo "Applying database migrations..."
  prisma migrate deploy --schema=app/prisma/schema.prisma
fi

if [ -n "$RABBITMQ_HOST" ]; then
  echo "Waiting for RabbitMQ..."

  until nc -z "$RABBITMQ_HOST" 5672; do
    echo "RabbitMQ not ready..."
    sleep 2
  done

  echo "RabbitMQ is ready!"
fi

echo "Starting application..."
exec "$@"