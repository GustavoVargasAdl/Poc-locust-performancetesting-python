from locust import HttpUser, task, between, tag

class QuickStarUser(HttpUser):
    wait_time = between(1, 2)

    @tag('tag1')
    @task
    def getListUsers(self):
        self.client.get('/api/users?page=2')

    @tag('tag2')
    @task
    def createUser(self):
        body={"name": "morpheus", "job": "leader"}
        self.client.post('/api/users', data = body)

    @tag('tag3')
    @task
    def updateUser(self):
        body = {"name": "Rocio", "job": "Presidente"}
        self.ednPointUser(body)

    def ednPointUser(self, body):
        self.client.put('/api/users/2', data=body)

