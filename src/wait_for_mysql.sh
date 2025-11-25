#!/bin/sh

echo "Waiting for MySQL to be ready..."

until nc -z mysql_db 3306; do
  echo "MySQL not ready yet..."
  sleep 2
done

echo "MySQL is up! Starting ETL..."
python src/etl.py
