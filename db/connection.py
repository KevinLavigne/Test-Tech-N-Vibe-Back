import psycopg2
import os

conn = psycopg2.connect(
  host = os.getenv('DB_HOST'),
  user = os.getenv('DB_USER'),
  password = os.getenv('DB_PASSWORD'),
  database = os.getenv('DB_NAME'))
  
cur = conn.cursor()