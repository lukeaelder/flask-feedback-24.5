"""Seed file to create table."""

from models import User, db
from app import app

db.drop_all()
db.create_all()