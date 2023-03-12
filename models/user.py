#!/usr/bin/python3
"""Class User that inherits from BaseModel"""
from models.base_model import BaseModel


class User(BaseModel):
    """Our beautiful class User"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
