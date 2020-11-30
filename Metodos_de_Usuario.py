from locust import HttpUser, task, between, tag

class QuickStarUser(HttpUser):
    wait_time = between(1,2)
    
    @task
    def getListUsers(self):
        self.client.get('/api/users?page=2')
        
    def on_start(self):
        print("=========================>  hello from taskset on_start")
     
    def on_stop(self):
        print("::::::::::::::::::::::::::::>  hello from taskset on_stop")
        