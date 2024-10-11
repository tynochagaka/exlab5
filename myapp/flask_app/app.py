# myapp/flask_app/app.py
from flask import Flask
import redis
import psycopg2
import os

app = Flask(__name__)

# Connect to Redis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

# Connect to PostgreSQL
db_conn = psycopg2.connect(
    host='db',
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
)

@app.route('/')
def index():
    count = redis_client.incr('counter')
    return f'This page has been visited {count} times.'

@app.route('/data')
def data():
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM my_table;")
        results = cursor.fetchall()
        return str(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
