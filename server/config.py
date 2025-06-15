import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pizza.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False 