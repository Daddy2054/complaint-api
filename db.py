import dotenv
import os
import sqlalchemy
import databases

dotenv.load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
