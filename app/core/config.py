import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'store_project')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
