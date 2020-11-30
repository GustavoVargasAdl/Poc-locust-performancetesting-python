from locust import HttpUser, task, between, TaskSet, events
import csv

token = ''
USER_CREDENTIALS = None

class RequestAllUsers(TaskSet):
    @task
    def getListUsers(self):
        global token

        header = {
            'Content-Type': 'application/json',
            'X-ID_user': 'AB005LT98',
            'X-Channel': 'OK',
            'X-CompanyId': '3333',
            'X-LegalName': 'nameLegalName',
            'X-IdentSerialNum': '792531',
            'X-GovIssueIdentType': 'CC',
            'Authorization': token
        }

        self.client.get('/api/users?page=2')
        #self.client.get('/api/users?page=2', headers = header)

class CreateUser(TaskSet):
    @task
    def createUser(self):
        body = {"name": "Anita", "job": "QAE"}
        self.client.post('/api/users', data=body)

class UpdateUser(TaskSet):
    @task(3)
    def updateUser(self):
        body = {"name": "morpheus", "job": "zion resident"}
        self.endpointUpdateUser(body)

    def endpointUpdateUser(self, body):
        self.client.put('/api/users/2', data=body)


class UserBehavior(TaskSet):
    tasks = {RequestAllUsers: 3, CreateUser: 2}

    email = 'NOT_FOUND'
    password = 'NOT_FOUND'

    def on_start(self):
        global token

        if len(USER_CREDENTIALS) > 0:
            self.email, self.password = USER_CREDENTIALS.pop()
        token = self.login()
        print("Iniciando usuario =======>======----------------- token obtenido: " + token)

    def login(self):
        #headers =  {'Content-Type': 'application/x-www-form-urlencoded',
        #       'Authorization': 'Basic Aba789QA-TEST-55'
        #       }
        body = {
            "email": self.email,
            "password": self.password
        }

        url = '/api/login'

        with self.client.post(url,
            #headers = headers,
            data = body) as response:
            key = response.json().get('token')

        return key

    def on_stop(self):
        print("->->->->->->->->->->->->->->->->->-> Realizando accion despues de que cada usuario raliza las tareas")


class User(HttpUser):
    host = 'http://localhost:5000'
    tasks = [UserBehavior]
    wait_time = between(1, 2)

    @events.test_start.add_listener
    def on_test_start(**kw):
        global USER_CREDENTIALS
        print('================================================================> Starting actions before test')
        with open('credentials.csv', mode='r') as file:
            reader = csv.reader(file)
            USER_CREDENTIALS = [tuple(r) for r in reader]

    @events.test_stop.add_listener
    def on_test_start(**kw):
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::>>>>>>>>performing actions after testing")