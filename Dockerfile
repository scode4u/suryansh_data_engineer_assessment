FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install MySQL client + netcat for waiting script
RUN apt-get update && apt-get install -y default-mysql-client netcat-openbsd && apt-get clean


# Copy required files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

# Run ETL script on container start
# CMD ["python", "src/etl.py"]

COPY src/wait_for_mysql.sh /app/src/wait_for_mysql.sh
RUN chmod +x /app/src/wait_for_mysql.sh

CMD ["sh", "/app/src/wait_for_mysql.sh"]

