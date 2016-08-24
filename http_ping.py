from locust import HttpLocust, TaskSet, task

class HttpPingTasks(TaskSet):
    @task
    def ping(self):
        self.client.get("/")

class SayHelloLocust(HttpLocust):
    task_set = HttpPingTasks
    min_wait = 100
    max_wait = 500
