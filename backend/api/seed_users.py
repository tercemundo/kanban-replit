import hashlib
import binascii
import os
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def seed():
    db = SessionLocal()
    try:
        users_to_seed = [
            {"username": "user", "password": "pass", "firstName": "Marcelo", "lastName": "Guazzardo", "sub": "mock-user-123"},
            {"username": "user1", "password": "pass1", "firstName": "User", "lastName": "One", "sub": "mock-user-456"},
        ]

        for u_data in users_to_seed:
            user = db.query(User).filter(
                (User.username == u_data["username"]) | 
                (User.externalId == u_data["sub"])
            ).first()
            if not user:
                user = User(
                    username=u_data["username"],
                    externalId=u_data["sub"],
                    firstName=u_data["firstName"],
                    lastName=u_data["lastName"],
                    hashedPassword=hash_password(u_data["password"])
                )
                db.add(user)
            else:
                user.username = u_data["username"]
                user.hashedPassword = hash_password(u_data["password"])
            
        db.commit()
        print("Seeding completed successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
