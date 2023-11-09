from random import sample, randint, choice
from faker import Faker
from datetime import datetime, timedelta
from setup import db, app

from models import User, Admin


fake=Faker()

with app.app_context():


    db.session.query(User).delete()
    db.session.commit()

    
    for i in range(10):
        admin = Admin(
            name=fake.name(),
            email=fake.email(),
            contact=fake.phone_number(),
            address=fake.address(),
            _password_hash=fake.password(length=10)
        )
        db.session.add(admin)

    db.session.commit()


    for i in range(10):
        user = User(
            name=fake.name(),
            email=fake.email(),
            contact=fake.phone_number(),
            address=fake.address(),
            _password_hash=fake.password(length=10)
        )
        db.session.add(user)

    db.session.commit()

        