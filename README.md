1.  PREPARACIÓN DE HERRAMIENTAS Y AMBIENTES

        UPDATE Python
        	- Descargar e instalar (https://www.python.org/downloads/)
        	- brew update && brew upgrade python
        	- brew install python3 && cp /usr/local/bin/python3 /usr/local/bin/python
        	- Reiniciar cosola
        	- Verificar

        LOCUST: Es un paquete de python
        	Install = pip3 install locust
        	Version = locust --v

        NODE.JS
        	- Descargar e instalar (https://nodejs.org/en/download/)
        	- Verificar: node --v


        SERVIDOR
        	1. Clonar:
        		https://github.com/jdmesalosada/reqres.git
        		
        	2. Modificar archivo \reqres\public\js\app.js
        		- Agregar: en (login-successful / data) linea 86
        				,
        				"email": "george.bluth@reqres.in",
        				"password": "cityslick1",
        				"email": "janet.weaver@reqres.in",
        				"password": "cityslick2",
        				"email": "emma.wong@reqres.in",
        				"password": "cityslick3",
        				"email": "charles.morris@reqres.in",
        				"password": "cityslick4",
        				"email": "tracey.ramos@reqres.in",
        				"password": "cityslick5",
        				"email": "michael.lawson@reqres.in",
        				"password": "cityslick6",
        				"email": "lindsay.ferguson@reqres.in",
        				"password": "cityslick7",
        				"email": "tobias.funke@reqres.in",
        				"password": "cityslick8",
        				"email": "byron.fields@reqres.in",
        				"password": "cityslick9"

        		- Arrancar = Desde el directorio reqres lanzar node app.js
        		- Verificar: En el navegador entrar http://localhost:5000


        	3. Instalar Extenciones VS Code
        		Prettier-Code formater
        		MagicPython

2.  EJERCICIOS: Tener en cuenta la identación

    2.1 Primer archivo Locust: Crear un locustfile: EjercicioDummy.py

        	from locust import HttpUser, task, between

        	class QuickStarUser(HttpUser):
        	    wait_time = between(1,2)
        	    @task
        	    def getListUsers(self):
        	        self.client.get('/api/users?page=2')
        	    @task
        	    def createUser(self):
        	        body = {"name": "morpheus", "job": "leader"}
        	        self.client.post('/api/users', data = body)

    2.1.1 Comandos de ejecución:

        	Lanzar locust
        		Interfaz grafica
        		- locust -f EjercicioDummy.py

        		Consola
        		- locust -f EjercicioDummy.py --headless -u 10 -r 2 --run-time 10s

    2.1.2 Abrir navegador con http://127.0.0.1:8089 o http://localhost:8089

        	- Ingresar la cantidad de usuarios a ejecutar
        	- Ingresar el numero de usuarios por segundo
        	- Ingresar la URL Base

    2.2 Decoradores: Task's y Tag's

        	- Decorador @task: tareas que realizara el usuario
        	- @task(3) peso de cada tarea respecto a las demas
        	-Deorador @tag('tag1', 'tag2') para indicar las tareas que realizará el usuario en la ejecución (por línea de comandos)

        	- Ejercicio

        		Crear un locustfile: Decoradores_Task_Tag.py

        			from locust import HttpUser, task, between, tag

        			class QuickStarUser(HttpUser):
        			    wait_time = between(1,2)

        			    @tag('tag1')
        			    @task
        			    def getListUsers(self):
        			        self.client.get('/api/users?page=2')

        			    @tag('tag2')
        			    @task(3)
        			    def createUser(self):
        			        body = {"name": "morpheus", "job": "leader"}
        			        self.client.post('/api/users', data = body)

        			    @tag('tag3')
        			    @task(6)
        			    def updateUser(self):
        			        body = {"name": "morpheus", "job": "zion resident"}
        			        self.endpointUpdateUser(body)

        			    def endpointUpdateUser(self, body):
        			        self.client.put('/api/users/2', data = body


        	- Ejecutar: locust -f Decoradores_Task_Tag.py--host=http://localhost:5000 --tags tag1 tag3 --headless -u 10 -r 2 --run-time 10s

    2.3 Métodos de Usuario (on_start and on_stop)
    Sirven para que los usuarios puedan ejecutar scripts antes o despues de que realice o termine una tarea (@task)

        	- Crear un locustfile: Metodos_de_Usuario.py

        		from locust import HttpUser, task, between, TaskSet

        		class UserBehavior(TaskSet):

        		    def on_start(self):
        		        print("=========================>  hello from taskset on_start")

        		    def on_stop(self):
        		        print("::::::::::::::::::::::::::::>  hello from taskset on_stop")

        		    @task
        		    def reserve_task(self):
        		        self.client.get('/api/users?page=2')

        		class WorkUser(HttpUser):
        		    tasks = [UserBehavior]
        		    wait_time = between(1, 2)
        		    host = 'http://localhost:5000'

        	- Ejecutar: locust -f  Metodos_de_Usuario.py --headless -u 10 -r 2 --run-time 10s

    2.4 TaskSet
    Colección de tareas que se ejecutarán según el peso indicado

        	- Crear un locustfile: ejercicio_TaskSet.py

        			from locust import HttpUser, task, between, tag, TaskSet

        			class UserBehavior(TaskSet):

        			    @task
        			    def getListUsers(self):
        			        self.client.get('/api/users?page=2')

        			    @task(3)
        			    def createUser(self):
        			        body = {"name": "morpheus", "job": "leader"}
        			        self.client.post('/api/users', data = body)

        			    @task(6)
        			    def updateUser(self):
        			        body = {"name": "morpheus", "job": "zion resident"}
        			        self.endpointUpdateUser(body)

        			    def endpointUpdateUser(self, body):
        			        self.client.put('/api/users/2', data = body)

        			class WorkUser(HttpUser):
        			    host = 'http//localhost:5000'
        			    tasks  = [UserBehavior]
        			    wait_time = between(1,2)

        	- Ejecutar: locust -f ejercicio_TaskSet.py --headless -u 10 -r 2 --run-time 10s

    2.5 Events (HOOKS)
    Para ejecutar scripts de configuración antes de ejecutar las pruebas o al terminar

        	- Crear un locustfile: eventos_Hooks.py


        			from locust import HttpUser, task, between, TaskSet, events

        			class UserBehavior(TaskSet):

        			    def on_start(self):
        			        print("--|--|--|--|--|--|--|--|--|-->  hello from taskset on_start")

        			    def on_stop(self):
        			        print("--.--.--.--.--.--.--.--.--.-->  hello from taskset on_stop")

        			    @task
        			    def reserve_task(self):
        			        self.client.get('/api/users?page=2')

        			class WorkUser(HttpUser):
        			    tasks = [UserBehavior]
        			    wait_time = between(1, 2)
        			    host = 'http://localhost:5000'

        			    @events.test_start.add_listener

        			    def on_test_start(**kwargs):
        			        print(":::::::::::::::::::::::::::::::::::::::::::> A new test is starting")

        			    @events.test_stop.add_listener
        			    def on_test_stop(**kwargs):
        			        print("==========================================> A new test is ending")

        - Ejecutar: locust -f eventos_Hooks.py --headless -u 10 -r 2 --run-time 10s

    10. PROYECTO

        - Crear archivo CSV: credentials.csv
        - Agregar:
          eve.holt@reqres.in,cityslicka
          george.bluth@reqres.in,cityslick1
          janet.weaver@reqres.in,cityslick2
          emma.wong@reqres.in,cityslick3
          charles.morris@reqres.in,cityslick4
          tracey.ramos@reqres.in,cityslick5
          michael.lawson@reqres.in,cityslick6
          lindsay.ferguson@reqres.in,cityslick7
          tobias.funke@reqres.in,cityslick8
          byron.fields@reqres.in,cityslick9

        - Crear un locustfile: pocLocust.py

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
                      body = {"name": "morpheus", "job": "leader"}
                      self.client.post('/api/users', data = body)


              class UpdateUser(TaskSet):
                  @task(3)
                  def updateUser(self):
                      body = {"name": "morpheus", "job": "zion resident"}
                      self.endpointUpdateUser(body)

                  def endpointUpdateUser(self, body):
                      self.client.put('/api/users/2', data = body)


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
                      print("->->->->->->->->->->->->->->->->->-> Realizando accion despues de cada usuario raliza las tareas")

              class User(HttpUser):
                  host = 'http://localhost:5000'
                  tasks = [UserBehavior]
                  wait_time = between(1, 2)
                  sock = None

                  @events.test_start.add_listener
                  def on_test_start(**kw):
                      global USER_CREDENTIALS
                      print('================================================================> Starting actions before test')
                      #if (USER_CREDENTIALS == None):
                      with open('credentials.csv', mode='r') as file:
                          reader = csv.reader(file)
                          USER_CREDENTIALS = [tuple(r) for r in reader]

                  @events.test_stop.add_listener
                  def on_test_start(**kw):
                      print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::>>>>>>>>performing actions after testing")

        - Ejecutar: locust -f pocLocust.py --headless -u 10 -r 2 --run-time 10s
