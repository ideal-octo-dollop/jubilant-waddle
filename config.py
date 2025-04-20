import os

class Config:
    SECRET_KEY = 'your_top_secret_key'
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    DATABASE = 'users.db'