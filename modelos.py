from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
import datetime
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jamona@localhost:5432/todosdb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rrodriguez:1234@localhost:5432/todosdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  
# c9e891672c09
# User
@dataclass
class User(db.Model):
    __tablename__ = 'usr'
    id: int
    username: str
    email: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    # todos = db.relationship('Todo', backref='usr', lazy=True)
    tableros = db.relationship('Tablero', backref='usr', lazy=True, cascade='delete')

# Tablero
@dataclass
class Tablero(db.Model):
    __tablename__ = 'tablero'
    id: int
    user_id: User
    name: str
    is_admin: bool

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('usr.id'),primary_key=True)
    name = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    todos = db.relationship('Todo', backref='tablero', lazy=True, cascade='delete')
    # tableroid = db.relationship('Todo', backref='userid', lazy=True, cascade='delete', foreign_keys=["user_id"])
    
# Category
@dataclass
class Category(db.Model):
    __tablename__ = 'category'
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    todos = db.relationship('Todo', backref='category', lazy=True, cascade='delete')

# Todo
@dataclass
class Todo(db.Model):
    __tablename__ = 'todo'
    __table_args__ = (
        db.ForeignKeyConstraint(['tablero_id','user_id'],['tablero.id','tablero.user_id'], name='uniquetodo'),
    )
    id: int
    user_id: User
    tablero_id: Tablero
    category_id: Category
    description: str
    is_done: bool
    created_date: datetime
    deadline: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tablero_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.String(), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    deadline = db.Column(db.DateTime)
    

