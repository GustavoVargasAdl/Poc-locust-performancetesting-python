from locust import HttpUser, task, between, tag, TaskSet, events

class UserBehavior(TaskSet):

    @task
    def getListUsers(self):
        self.client.get('/api/users?page=2')

    def on_start(self):
        print("--|--|--|--|--|--|--|--|--|-->  hello from taskset on_start")
     
    def on_stop(self):
        print("--.--.--.--.--.--.--.--.--.-->  hello from taskset on_stop")
        
        
class WorkUser(HttpUser):
    host = 'http://localhost:5000'
    wait_time = between(1,2)
    tasks = [UserBehavior]
    
    @events.test_start.add_listener
    def on_test_start(**kwargs):
        print(":::::::::::::::::::::::::::::::> Un nuevo test a comenzado...")
        
    @events.test_stop.add_listener
    def on_test_stop(**kwargs):
        print("=================================> Finalizó la prueba")