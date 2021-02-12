import argparse
import sys

import pymongo

from app.core.auth import get_password_hash
from app.core.config import db_config

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", required=True)
parser.add_argument("-p", "--password", required=True)
parser.add_argument("-P", "--phone", required=True)


def get_db():
    return pymongo.MongoClient(db_config.URI, serverSelectionTimeoutMS=1000)[
        db_config.DATABASE_NAME
    ]


def create_new_user(user: dict):
    db = get_db()
    result = db[db_config.USERS_COLLECTION_NAME].insert_one(user)
    print(f"Insertion result: {result}")


if __name__ == "__main__":
    parsed = parser.parse_args(sys.argv[1:])
    user = {
        "username": parsed.username,
        "hashed_password": get_password_hash(parsed.password),
        "phone_number": parsed.phone,
    }
    create_new_user(user)
