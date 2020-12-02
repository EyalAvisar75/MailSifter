import pprint
from pymongo import MongoClient


def get_emails_db_table():
    client = MongoClient()
    emails_db = client.weather_database
    emails_table = emails_db['mails_table']
    return emails_table


def push_entry(entry):
    table = get_emails_db_table()
    table.insert_one(entry).inserted_id


def get_entry(mail_address):
    table = get_emails_db_table()
    pprint.pprint(table.find_one({'email_address': mail_address}))
