from app import app, db, Pet

with app.app_context():
    pets = Pet.query.all()
    for pet in pets:
        print(pet.name, pet.available)
