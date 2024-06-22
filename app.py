from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

class Pet(db.Model):
    """Model for the pets table."""
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(30), nullable=False)
    photo_url = db.Column(db.String(200), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)

@app.route('/')
def show_homepage():
    """Show the homepage with lists of available and not-available pets."""
    available_pets = Pet.query.filter_by(available=True).all()
    not_available_pets = Pet.query.filter_by(available=False).all()
    return render_template('home.html', available_pets=available_pets, not_available_pets=not_available_pets)

@app.route('/add', methods=['GET', 'POST'])
def show_add_form():
    """Show the form to add a new pet and handle the form submission."""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"Added {name} the {species}!", "success")
        return redirect(url_for('show_homepage'))
    
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_edit_pet(pet_id):
    """Show the pet detail and edit form, handle form submission."""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash(f"Updated {pet.name}!", "success")
        return redirect(url_for('show_edit_pet', pet_id=pet.id))
    
    return render_template('pet_detail.html', pet=pet, form=form)

if __name__ == '__main__':
    app.run(debug=True)
