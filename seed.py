from app import app, db, Pet

def seed_data():
    with app.app_context():
        # Clear existing data
        Pet.query.delete()

        # Add sample pets with valid image URLs
        pets = [
            Pet(name="Buddy", species="Dog", photo_url="https://upload.wikimedia.org/wikipedia/commons/6/6e/Golde33443.jpg", age=3, notes="Friendly dog", available=True),
            Pet(name="Mittens", species="Cat", photo_url="https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg", age=5, notes="Calm and loving", available=False),
            Pet(name="Charlie", species="Dog", photo_url="https://cdn.mos.cms.futurecdn.net/ASHH5bDmsp6wnK6mEfZdcU-1200-80.jpg", age=2, notes="Playful pup", available=True)
        ]

        db.session.bulk_save_objects(pets)
        db.session.commit()

if __name__ == "__main__":
    seed_data()

