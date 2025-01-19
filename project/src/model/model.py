#!/usr/bin/python3
from database import database
from dotenv import load_dotenv
import os

load_dotenv()
DRIVER_NAME = os.getenv('DRIVER_NAME')
USERNAME = os.getenv('USERNAME')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')

model = database.database(
    drivername=DRIVER_NAME,
    username=USERNAME,
    host=HOST,
    database=DATABASE,
    password=PASSWORD,
    port = PORT
)
