from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from modelos import * 
import psycopg2

connection = connection = psycopg2.connect(
	database = "todosdb", 
	user = "adminTodo", 
	password = "to-do123",
	port="5432",
	host="database-3.ciwvjt7kpguc.us-east-1.rds.amazonaws.com")
# connection = connection = psycopg2.connect(database = "todosdb", user = "rrodriguez", password = "1234")
cursor = connection.cursor()

# Register
@app.route('/auth/signup', methods=['POST'])
def signup():
	try:
		username = request.get_json()['username']
		email = request.get_json()['email']
		password = request.get_json()['password']

		cursor.execute("select count(username) from usr where username='%s';" % (username))
		usxr_count = cursor.fetchone()[0]

		cursor.execute("select count(email) from usr where email='%s';" % (email))
		eml_count = cursor.fetchone()[0]
	
		if usxr_count > 0:
			return render_template('login.html')
		elif eml_count > 0:
			return render_template('login.html')
		else:
			encrypt_pass = generate_password_hash(password, "sha256")

			cursor.execute("select max(id) from usr;")
			id_max = cursor.fetchone()[0]
			id_max = id_max if (id_max != None) else 0

			user = User(id=id_max+1, username=username, email=email, password=encrypt_pass)
			db.session.add(user)
			db.session.commit()

			cursor.execute("select id from usr where username='%s'" %user.username)
			user_id = cursor.fetchone()[0]

			cursor.execute("select max(id) from tablero;")
			id_tab_max = cursor.fetchone()[0]
			id_tab_max = id_tab_max if (id_tab_max != None) else 0
			table = Tablero(id=id_tab_max+1,name="default", user_id=user_id, is_admin=True)

			db.session.add(table)
			db.session.commit()

			return jsonify({
				'username': user.username,
				'email': user.email,
				'status': 'true',
				'table': table.name
			})
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()

# Login
@app.route('/auth/login', methods=['POST'])
def login():
	if request.method == 'POST':
		username = request.get_json()['username']
		password = request.get_json()['password']
		print(password)
		usxr = User.query.filter_by(username=username).first()
		print(usxr)
		passwd_validate = check_password_hash(usxr.password, password)
		
		if usxr.username == username and passwd_validate:
			cursor.execute("select id from usr where username='%s'" %usxr.username)
			user_id = cursor.fetchone()[0]

			cursor.execute("select id from tablero where user_id='%s' and name='default'" %user_id)
			tablero_id = cursor.fetchone()[0]
			
			return jsonify({
				'response': 'true',
				'user': usxr.username,
				'tablero_name': 'default',
				'table_id': tablero_id
			})
		else:
			return jsonify({
				'response': 'false'
			})

# Display all
@app.route('/<user_name>/<table_name>/todos/displayall/', methods=['POST'])
def display_all(user_name, table_name):
	table_id = request.get_json()['table_id']
	user = User.query.filter_by(username=user_name).first()
	# Se filtra por id porque lo unico que importa es mostrar la informacion de la tabla
	table = Tablero.query.filter(Tablero.id == table_id).first()
	todo = Todo.query.filter(Todo.tablero_id==table_id).all()
	return(jsonify(todo))

# Display completed
@app.route('/<user_name>/<table_name>/todos/displaycompleted/')
def display_completed(user_name):
    user = User.query.filter_by(username=user_name).first()
    status = True
    todo = Todo.query.filter((Todo.user_id == user.id) & (Todo.is_done == status)).all()
    return(jsonify(todo))

# Display incompleted
@app.route('/<user_name>/<table_name>/todos/displayincompleted/')
def display_imcompleted(user_name):
    user = User.query.filter_by(username=user_name).first()
    status = False
    todo = Todo.query.filter((Todo.user_id == user.id) & (Todo.is_done == status)).all()
    return(jsonify(todo))

# Todos Route
@app.route('/<user_name>/<table_name>/<table_id>/todos/')
def todos(user_name, table_id,table_name):
	user = User.query.filter_by(username=user_name).first()
	tables = Tablero.query.filter(Tablero.user_id == user.id)
	return render_template('todos.html', data=user_name, tables=tables, tableid=table_id)

# Add Todo - C
@app.route('/<user_name>/<table_name>/todos/add/', methods=['POST'])
def add_todo(user_name, table_name):
	try:
		cursor.execute("select count(name) from category where name ='general'")
		contGenCat = cursor.fetchone()[0]

		if(contGenCat == 0):
			cat = Category(name="general")
			db.session.add(cat)
			db.session.commit()

		desc = request.get_json()['description']
		dead = request.get_json()['deadline']
		tablero_id = request.get_json()['table_id']
		cat_id = Category.query.filter_by(name="general").first().id
		user_id = User.query.filter_by(username=user_name).first().id

		cursor.execute("select max(id) from todo;")	
		id_max = cursor.fetchone()[0]
		id_max = id_max if (id_max != None) else 0

		todo = Todo(id=id_max+1, user_id=user_id, tablero_id=tablero_id, description=desc, category_id=cat_id, deadline=dead)

		db.session.add(todo)
		db.session.commit()
		return jsonify({
			'status': 'true'
		})
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()

# Update Todo -	U
@app.route('/<user_name>/<table_name>/todos/update/', methods=['POST'])
def update_todo(user_name,table_name):
	try: 
		todo_id = request.get_json()['todo_id']
		desc = request.get_json()['description']
		todo = Todo.query.filter(Todo.id == todo_id).first()
		todo.description = desc
		db.session.commit()
		return jsonify({
			'status': 'true'
		})
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()

# Update Deadline -	U
@app.route('/<user_name>/<table_name>/todos/editdeadline/', methods=['POST'])
def editdeadline_todo(user_name,table_name):
	try: 
		todo_id = request.get_json()['todo_id']
		dead_line = request.get_json()['deadline']
		todo = Todo.query.filter(Todo.id == todo_id).first()
		todo.deadline = dead_line
		
		db.session.commit()
		return jsonify({
			'status': 'true'
		})
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()

# Update Todo is_done -	U
@app.route('/<user_name>/<table_name>/todos/update_is_done/', methods=['POST'])
def update_todo_is_done(user_name,table_name):
	try: 
		todo_id = request.get_json()['todo_id']
		todo = Todo.query.filter(Todo.id == todo_id).first()
		if(todo.is_done):
			todo.is_done = False
		else:
			todo.is_done = True
		db.session.commit()
		return jsonify({
			'status': 'true'
		})
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()


# Delete Todo -	D
@app.route('/<user_name>/<table_name>/todos/delete/', methods=['POST'])
def delete_todo(user_name,table_name):
	try: 
		todo_id = request.get_json()['todo_id']
		todo = Todo.query.filter(Todo.id == todo_id).first()
		
		db.session.delete(todo)
		db.session.commit()
		
		return jsonify({
			'status': 'true'
		})
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()

# Create Table -	D
@app.route('/table/create', methods=['POST'])
def create_table2():
	print("post")
	try:
		table_name = request.get_json()['name']
		owner_name = request.get_json()['owner']
		is_admin = request.get_json()['admin']

		owner_id = User.query.filter_by(username=owner_name).first().id
		
		if(table_name != 'default'):
			cursor.execute("select max(id) from tablero;")
			id_tab_max = cursor.fetchone()[0]
			id_tab_max = id_tab_max if (id_tab_max != None) else 0
			table = Tablero(id=id_tab_max+1,name=table_name, user_id=owner_id, is_admin=is_admin)
			db.session.add(table)
			db.session.commit()
			return jsonify({
				'name': table.name,
				'status': 'true'
			})
		else:
			return jsonify({
				'status': 'false'
			})
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()

# Delete Table - D
@app.route('/<user_name>/<table_name>/tablero/delete/', methods=['POST'])
def delete_tablero(user_name,table_name):
	try: 
		tablero_id = request.get_json()['table_id']
		user_name_ = request.get_json()['owner_name']
		

		user = User.query.filter_by(username=user_name).first()
		user_id = user.id
		
		# id_default = Tablero.query.filter((Tablero.name == 'default') & (Tablero.user_id == user_id))
		# print(id_default)
		cursor.execute("select id from tablero where user_id=%s and name='default';" %user_id)
		id_default = cursor.fetchone()[0]
		
		tablero = Tablero.query.filter((Tablero.user_id == user_id) & (Tablero.name == table_name)).first()
		cursor.execute("select * from tablero where id=%s;" %tablero_id)
		tableros = cursor.fetchall()
		print(tableros)
		if(tablero.is_admin == True):
			# # delete_q = Tablero.__table__.delete().where(Tablero.id == tablero_id)
			# # delete_q = db.session.query(Tablero).filter(Tablero.id == tablero_id)
			# # db.session.delete(delete_q)
			# cursor.execute("DELETE FROM tablero WHERE id=%s;" %tablero_id)
			db.session.commit()
			return jsonify({
			'status': 'true',
			'table_id': id_default
			})
		else:
			db.session.rollback()
			return jsonify({
				'status': 'false',
				'table_id': id_default 
			})
		
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()

# Share Table
@app.route('/<user_name>/<table_name>/tablero/share/', methods=['POST'])
def share_tablero(user_name,table_name):
	try: 
		
		shared_user = request.get_json()['shared_user']
		owner_name = request.get_json()['owner_user']
		
		sh_user = User.query.filter_by(username=shared_user).first()
		sh_user_id = sh_user.id
		
		user = User.query.filter_by(username=user_name).first()

		user_id = user.id
		tablero = Tablero.query.filter((Tablero.user_id == user_id) & (Tablero.name == table_name)).first()
		
		if(tablero.name != "default" and owner_name == user.username):
			share_tablero = Tablero(id=tablero.id, user_id=sh_user_id,name=tablero.name, is_admin=False)

			db.session.add(share_tablero)
			db.session.commit()
		
			return jsonify({
				'status': 'true'
			})
		else:
			return jsonify({
				'status': 'false'
			})
	except Exception as e:
		db.session.rollback()
		return jsonify({
			'status': 'false'
		})
	finally:
		db.session.close()
		
@app.route('/')
def index():
	return render_template('login.html')

#Error page
@app.errorhandler(404)
def page_not_found(error):
  return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def error_ocurred(error):
  return render_template('page_not_found.html'), 500

if __name__ == '__main__':
	app.run(debug=True, port=5001)
