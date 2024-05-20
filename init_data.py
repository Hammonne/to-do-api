import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

connection = psycopg2.connect(
    database = "todosdb",
    user = "adminTodo",
    password = "to-do123",
)

cursor = connection.cursor()

insert_category = 'insert into category(id, name) values(%s, %s);'
c1 = (1, 'general')
cursor.execute(insert_category, c1)

insert_usuario = 'insert into usr(id ,username, email, password) values(%s, %s, %s, %s);'

password = 'lolxd'
encrypt_pass = generate_password_hash(password, "sha256")
u1 = (1, 'marvin', 'prueba@gmail.com', encrypt_pass)
cursor.execute(insert_usuario, u1)

insert_todos = 'insert into todo(user_id, category_id, description, is_done) values(%s, %s, %s, %s);'

t1 = (1, 1, "todo1", False)
t2 = (1, 1, "todo2", False)
t3 = (1, 1, "todo3", False)
t4 = (1, 1, "todo4", False)
t5 = (1, 1, "todo5", False)
t6 = (1, 1, "todo6", False)
t7 = (1, 1, "todo7", False)
t8 = (1, 1, "todo8", False)
t9 = (1, 1, "todo9", False)
t10 = (1, 1, "todo10", True)

li2 = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10]

for i in range(10):
    cursor.execute(insert_todos, li2[i])

connection.commit()
connection.close()
cursor.close()