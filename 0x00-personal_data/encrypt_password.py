#!/usr/bin/env python3
"""
User passwords should NEVER be stored in plain text
in a database.

Implement a hash_password function that expects one
string argument name password and returns a salted,
hashed password, which is a byte string.

Use the bcrypt package to perform the hashing (with hashpw).
"""

import bcrypt


def hash_password(password):
    """
    User passwords should NEVER be stored in plain text
    in a database.

    Implement a hash_password function that expects one string
    argument name password and returns a salted,
    hashed password, which is a byte string.

    Use the bcrypt package to perform the hashing (with hashpw).
    """

    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(password, salt)

    return hash_pass
