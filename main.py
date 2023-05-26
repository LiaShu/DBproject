from flask import Flask, jsonify
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from flask import request
from flask import abort
from app_tasks import app_tasks
from EmailNotificationService import EmailService
app = Flask(__name__)
auth = HTTPBasicAuth()


#c = app_tasks("postgres", "postgres", "Skyline20205", "localhost", "5432")
c = app_tasks("postgres", "postgres", "postgres", "localhost", "5432")
e = EmailService(c)

'''Возможно использование хэшированного пароля. Использовать для этого hash_password.
https://flask-httpauth.readthedocs.io/en/latest/'''
@auth.get_password
def get_pw(username):
    users = c.get_usr_dict()
    if username in users:
        return users.get(username)
    return None

@app.route('/todo/api/v1.0/users', methods=['GET'])
def get_all_users():
    users = c.get_table(['*'], 'users')
    return jsonify({'users': users})

'''@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_all_tasks():
    tasks = c.get_tasks()
    return jsonify({'tasks': tasks})'''

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_one_task(task_id):
    '''first param: table fields
       second param: table name
       third param: condition for WHERE
       fourth param: value for condition'''
    task = c.get_rec_param(['title', 'description'],'task', 'id_task', task_id)
    return jsonify({'tasks': task})

@app.route('/todo/api/v1.0/status', methods=['GET'])
def get_all_statuses():
    status = c.get_table(['*'],'status')
    return jsonify({'statuses': status})

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/todo/api/v1.0/your_tasks', methods=['GET'])
@auth.login_required
def get_tasks_usr():
    cur_user = str(auth.current_user())
    tasks = c.get_tasks_user(cur_user)
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/create_tasks', methods=['POST'])
@auth.login_required
def create_task():
    cur_user = str(auth.current_user())
    data = {
        "title": request.json['title'],
        "description": request.json['description']
    }
    if not request.json or not 'title' in request.json or not data.get('title'):
        abort(400)
    if c.create_task(data, cur_user):
        return 'Record inserted successfully into table'
    else:
        return 'Such an entry already exists. Please change the title or description.'

@app.route('/todo/api/v1.0/upd_task/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    cur_user = str(auth.current_user())
    data = {
        "status": request.json['status']
    }
    new_tasks = c.upd_task(cur_user, task_id, data)
    return jsonify({'task': new_tasks})

'''# @app.route('/todo/api/v1.0/user_task', methods=['GET'])
# @auth.login_required
# def get_user_task():
#     user_task = c.get_table(['*'], 'user_task')
#     return jsonify({'user_task': user_task})'''
@app.route('/todo/api/v1.0/mail', methods=['POST'])
def get_contact():
    e.email_notif(c.get_tasks_usr())
    return 'the letter was sent'


if __name__ == '__main__':
    app.run(debug=True)


'''http://localhost:5000/todo/api/v1.0/your_tasks'''
# select_users = "SELECT * FROM task"
# print(c.execute_read_query(select_users))
# test_insert = "INSERT INTO task (title, description) VALUES ('test', 'test')"
# c.execute_write_query(test_insert)
# c.close_connection()
# c.check_connect()
