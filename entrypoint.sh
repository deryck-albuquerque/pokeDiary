#!/bin/sh

if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Waiting for database..."
  sleep 5

  echo "Generating Prisma client..."
  prisma generate --schema=app/prisma/schema.prisma

  echo "Applying database migrations..."
  prisma migrate deploy --schema=app/prisma/schema.prisma
fi

echo "Starting application..."
exec "$@"