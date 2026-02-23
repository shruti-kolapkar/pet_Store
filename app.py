from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'change-this-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'petstore.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.makedirs(app.instance_path, exist_ok=True)

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(120), nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    latest = Pet.query.order_by(Pet.created_at.desc()).limit(6).all()
    total = Pet.query.count()
    return render_template('index.html', latest=latest, total=total)

@app.route('/pets')
def pets():
    q = request.args.get('q', '').strip()
    species = request.args.get('species', '').strip()
    query = Pet.query
    if q:
        query = query.filter(Pet.name.ilike(f'%{q}%'))
    if species:
        query = query.filter(Pet.species.ilike(f'%{species}%'))
    all_pets = query.order_by(Pet.name).all()
    return render_template('pets.html', pets=all_pets, q=q, species=species)

@app.route('/pet/<int:pet_id>')
def product(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('product.html', pet=pet)

@app.route('/add', methods=['GET','POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form.get('name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        price = float(request.form.get('price') or 0)
        stock = int(request.form.get('stock') or 0)
        description = request.form.get('description')

        p = Pet(name=name, species=species, breed=breed, price=price, stock=stock, description=description)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('pets'))
    return render_template('add_pet.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
