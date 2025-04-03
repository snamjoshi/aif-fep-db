from src.db import Database


def load_database():
    database = Database()
    database.load("data/database__2025-03-21__17:12:35.196730.pkl")
    return database.db