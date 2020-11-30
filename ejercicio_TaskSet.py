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
    host = 'http://localhost:5000'
    wait_time = between(1,2)
    tasks = [UserBehavior]