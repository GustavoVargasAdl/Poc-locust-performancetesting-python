from locust import HttpUser, task, between

class QuickStarUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def getListUsers(self):
        self.client.get('/api/users?page=2')

    @task
    def createUser(self):
        body={"name": "morpheus", "job": "leader"}
        self.client.post('/api/users', data = body)
