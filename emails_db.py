import pprint
from pymongo import MongoClient


def get_emails_db_table():
    client = MongoClient()
    emails_db = client.weather_database
    emails_table = emails_db['emails_table']
    return emails_table
