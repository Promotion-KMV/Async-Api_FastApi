import os
from datetime import timedelta

DB_PORT = os.getenv('DB_PORT', 4321)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
ENV_JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-super-secret-key')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG', False) == 'True'
    SQLALCHEMY_DATABASE_URI = f'postgresql://auth_app:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/auth_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = ENV_JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
