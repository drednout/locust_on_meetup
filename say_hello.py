from locust import HttpLocust, TaskSet, task

class SayHelloTasks(TaskSet):
    @task
    def say_hello(self):
        self.client.get("/say_hello")

class SayHelloLocust(HttpLocust):
    task_set = SayHelloTasks
    min_wait = 0
    max_wait = 0
