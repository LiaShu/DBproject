import cursor as cursor
import psycopg2
import requests as requests
from psycopg2 import OperationalError
from psycopg2 import Error
# from flask import Flask, jsonify
# from flask import abort
# from flask import make_response
# from flask import request
import requests
# from flask import url_for
# from flask_httpauth import HTTPBasicAuth

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class app_tasks(metaclass=Singleton):
    '''Соединение с базой из экземпляра класса'''
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

        '''if __name__ == '__main__':
            app.run(debug=True)'''

    '''Чтение запроса из базы'''
    def execute_read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    '''Запись данных в базу'''
    def execute_write_query(self, query, vars = None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, vars)
            self.connection.commit()
            cursor.close()
            return 'Record inserted successfully into table'
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection is closed")

    def check_connect(self):
        if self.connection.closed == 1:
            self.__init__(self.db_name, self.db_user, self.db_password, self.db_host, self.db_port)
            print('Connection re-established')
        else:
            print('Connection is stable')

    '''Get a specific task by ID. КАК ОБРАЗЕЦ РАБОТЫ С ПАРАМЕТРАМИ'''
    # def get_task(self, task_id):
    #     select_task = f"SELECT title, description FROM task where id_task = {task_id}"
    #     task = self.execute_read_query(select_task)
    #     return task

    '''Get all records in a table'''
    def get_table(self, fields: list, table):
        fields_list = ", ".join(fields)
        select = f"SELECT {fields_list} from {table}"
        data = self.execute_read_query(select)
        return data

    '''Get records with parameters'''
    def get_rec_param(self, fields: list, table, option, value):
        fields_list = ", ".join(fields)
        select = f"SELECT {fields_list} from {table} WHERE {option} = {value}"
        data = self.execute_read_query(select)
        return data

    '''Сhecking if the user exists in the database.
    логин и пароль'''
    def get_usr_dict(self):
        usr = self.get_table(['*'],'users')
        auth_dict = {}
        for i in usr:
            login = list(i)[1::2]
            passwd = list(i)[-1]
            auth_dict[login[0]] = passwd
        return auth_dict

    '''dict {'login': 'id'}'''
    def get_id_login(self):
        usr = self.get_table(['*'], 'users')
        dict_usr = {}
        for i in usr:
            login = list(i)[1::2]
            id = list(i)[0]
            dict_usr[login[0]] = id
        return dict_usr

    '''Get a list of tasks for a specific user'''
    def get_tasks_user(self, cur_user):
        if cur_user in self.get_id_login():
            id = int(self.get_id_login().get(cur_user))
        new_list =[]
        tasks = self.get_rec_param(['user_id', 'task_id', 'status_id'], 'user_task', 'user_id',id)
        for i in tasks:
            new_dict = {}
            task = list(i)[1::2]
            status = list(i)[-1]
            task_int = int(task[0])
            new_dict['title'] = str(self.get_rec_param(['title'], 'task', 'id_task', task_int)[0][0])
            new_dict['description'] = str(self.get_rec_param(['description'], 'task', 'id_task', task_int)[0][0])
            new_dict['status'] = str(self.get_rec_param(['condition'], 'status', 'id_status', status)[0][0])
            new_list.append(new_dict)
        return new_list

    '''Create task'''
    '''ДОПИСАТЬ. Id новой задачки добавляется в таблицу user_task с id соответствующего
    пользователя и со статусом id = 5 (in progres) '''
    def create_task(self, data, cur_user):
        if cur_user in self.get_id_login():
            id_user = int(self.get_id_login().get(cur_user))
        tasks = self.get_table(['title', 'description'], 'task')
        tasks_dict = {}
        for i in tasks:
            i = list(i)
            title = i[0].lower()
            val = i[1].lower()
            tasks_dict[title] = val
        if data.get('title').lower() in tasks_dict and data.get('description').lower() in tasks_dict.values():
            return False
        else:
            cursor = self.connection.cursor()
            insert = ("""INSERT INTO task (title, description) VALUES (%s, %s) RETURNING id_task""")
            cursor.execute(insert, (data['title'], data['description']))
            new_id = cursor.fetchone()[0]
            insert_task = ("""INSERT INTO user_task (user_id, task_id, status_id) VALUES (%s, %s, %s)""")
            cursor.execute(insert_task, (id_user, new_id, 5))
            self.connection.commit()
            cursor.close()
            return True

    '''Update task'''
    '''Передаем id  задачи.
       Можно изменять title, description и status
       По id_user и id_task определяем поля и меняем их.
       Если все поля изменили на те же значения, то выдавать "Запись не изменена"
       Если изменили, то выдавать текст задачи с новыми значениями'''
    def upd_task(self, cur_user, task_id, data):
        if cur_user in self.get_id_login():
            id_user = int(self.get_id_login().get(cur_user))
        cursor = self.connection.cursor()
        upd_task =  f"""UPDATE user_task set status_id = %s WHERE user_id = {id_user} and task_id = {task_id}"""
        new_task = cursor.execute(upd_task, (data['status']))
        select_usr_task = self.get_rec_param(['*'], 'user_task', 'task_id', task_id)
        self.connection.commit()
        cursor.close()
        return select_usr_task
    '''ДОПИСАТЬ. Если пользователь ставит статус Cenceled, то удалять ее из таблицы user_task.'''
