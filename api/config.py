import os

from dotenv import load_dotenv
load_dotenv(".env")

DB_USER=os.environ["DB_USER"]
PASSWORD=os.environ["PASSWORD"]
ENDPOINT=os.environ["ENDPOINT"]
PORT_NUMBER=os.environ["PORT_NUMBER"]
DB_NAME=os.environ["DB_NAME"]

SQLALCHEMY_DATABSE_URI = "postgresql://" +str(DB_USER)+":"+str(PASSWORD)+"@"+str(ENDPOINT)+":"+str(PORT_NUMBER)+"/"+str(DB_NAME)
