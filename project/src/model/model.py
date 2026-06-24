#!/usr/bin/python3
import os

from database import database
from dotenv import load_dotenv

load_dotenv()
DRIVER_NAME = os.getenv("DRIVER_NAME")
USERNAME = os.getenv("USERNAME")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

model = database.Database(
    drivername=DRIVER_NAME,
    username=USERNAME,
    host=HOST,
    database_name=DATABASE,
    password=PASSWORD,
    port=PORT,
)
