import os
from dotenv import load_dotenv
load_dotenv('./.env')

DB_USER=os.getenv("DB_USER")
PASSWORD=os.getenv("PASSWORD")
ENDPOINT=os.getenv("ENDPOINT")
PORT_NUMBER=os.getenv("PORT_NUMBER")
DB_NAME=os.getenv("DB_NAME")

SQLALCHEMY_DATABSE_URI = "postgresql://" +str(DB_USER)+":"+str(PASSWORD)+"@"+str(ENDPOINT)+":"+str(PORT_NUMBER)+"/"+str(DB_NAME)
