import cursor as cursor
import psycopg2
import requests as requests
from psycopg2 import OperationalError
from psycopg2 import Error
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import requests
from flask import url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

'''DONE!'''
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection("postgres", "postgres", "postgres", "localhost", "5432")

'''DONE!'''
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


select_users = "SELECT * FROM users"
select_tasks = "SELECT * FROM task"
users = execute_read_query(connection, select_users)
tasks = execute_read_query(connection, select_tasks)

'''DONE!'''
@app.route('/todo/api/v1.0/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

'''DONE!'''
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

'''DONE!'''
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # task = list(filter(lambda t: t[0][0] == task_id, tasks))
    select_task = f"SELECT title, description FROM task where id_task = {task_id}"
    task = execute_read_query(connection, select_task)
    if len(task) == 0:
        abort(404)
    return task
    # return jsonify({'task':task})

'''DONE!'''
@app.route('/todo/api/v1.0/status/<int:status_id>', methods=['GET'])
def get_status(status_id):
    # task = list(filter(lambda t: t[0][0] == task_id, tasks))
    select_status = f"SELECT status.Condition FROM status where id_status = {status_id}"
    status = execute_read_query(connection, select_status)
    if len(status) == 0:
        abort(404)
    return status
    # return jsonify({'task':task})

'''DONE!'''
@auth.get_password
def get_auth(username):
    user_pswd = "SELECT * from users"
    users_pswd = execute_read_query(connection, user_pswd)
    auth_dict = {}
    for i in users_pswd:
        login = list(i)[1::2]
        passwd = list(i)[-1]
        auth_dict[login[0]] = passwd
    if username in auth_dict:
        global pswd
        pswd = auth_dict.get(username)
        return pswd
    return None

'''DONE!'''
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

'''DONE!'''
@app.route('/todo/api/v1.0/your_tasks', methods=['GET'])
@auth.login_required
def get_tasks_user():
    cur_user = str(auth.current_user())
    users = f"SELECT id_user, login FROM users"
    users_id = execute_read_query(connection, users)
    user_dict = {}
    for i in users_id:
        id_u = list(i)[::2]
        login = list(i)[-1]
        user_dict[login] = id_u
    if cur_user in user_dict.keys():
        id_n = user_dict.get(cur_user)
    id_n = int(id_n[0])
    new_list = []
    select_user_task = f"SELECT user_id, task_id, status_id FROM user_task where user_id = {id_n}"
    user_task = execute_read_query(connection, select_user_task)
    for i in user_task:
        new_dict = {}
        status = list(i)[-1]
        task = list(i)[1::2]
        task_int = int(task[0])
        new_dict['title'] = str(get_task(task_int)[0][0])
        new_dict['discription'] = str(get_task(task_int)[0][1])
        new_dict['status'] = str(get_status(status)[0][0])
        new_list.append(new_dict)
    return jsonify({'task': new_list})

'''DONE!'''
@app.route('/todo/api/v1.0/create_tasks', methods=['POST'])
def create_task():
    '''Создание новой задачи'''
    if not request.json or not 'title' in request.json:
        abort(400)
    data = {
        "title": request.json['title'],
        "description": request.json['description']
    }
    select_task = """SELECT title, description FROM task"""
    DB_tasks = execute_read_query(connection, select_task)
    tasks_dict = {}
    for i in DB_tasks:
        i = list(i)
        title = i[0].lower()
        val = i[1].lower()
        tasks_dict[title] = val
    if data.get('title').lower() in tasks_dict and data.get('description').lower() in tasks_dict.values():
        return 'Such an entry already exists. Please change the title or description.'
    else:
        try:
            cursor = connection.cursor()
            test_insert = ("""INSERT INTO task (title, description) VALUES (%s, %s)""")
            cursor.execute(test_insert, (data['title'], data['description']))
            connection.commit()
            cursor.close()
            return 'Record inserted successfully into table'
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into table", error)
        finally:
            # closing database connection.
            if connection:
                # cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


if __name__ == '__main__':
    app.run(debug=True)
