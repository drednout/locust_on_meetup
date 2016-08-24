import random
import gevent

from locust import HttpLocust, TaskSet, task


HTTP_USER = "test"
HTTP_PASSWORD = "1"

class NewsAppApi(TaskSet):
    def get_news(self):
        self.client.get("/news", auth=(HTTP_USER, HTTP_PASSWORD) )

    def get_single_news(self, news_id):
        self.client.get("/news/{}".format(news_id), auth=(HTTP_USER, HTTP_PASSWORD), 
                        name="/news/{id}")

    def _make_comment_request(self, method, news_id):
        self.client.request(method, "/news/{}/comments".format(news_id), auth=(HTTP_USER, HTTP_PASSWORD),
                        name="/news/{id}/comments")

    def get_single_news_comments(self, news_id):
        self._make_comment_request('GET', news_id)

    def add_news_comment(self, news_id):
        self._make_comment_request('POST', news_id)

    def edit_news_comment(self, news_id):
        self._make_comment_request('PUT', news_id)

    def delete_news_comment(self, news_id):
        self._make_comment_request('DELETE', news_id)


class NormalUserBehavior(NewsAppApi):
    @task(10)
    def read_news(self):
        news_id = random.randint(1, 1000)
        self.get_single_news(news_id)
        gevent.sleep(3)
        self.get_single_news_comments(news_id)

    @task(3)
    def do_comment_news(self):
        news_id = random.randint(1, 1000)
        self.add_news_comment(news_id)

    @task(1)
    def do_edit_news_comments(self):
        news_id = random.randint(1, 1000)
        self.edit_news_comment(news_id)

    @task(1)
    def do_delete_news_comments(self):
        news_id = random.randint(1, 1000)
        self.delete_news_comment(news_id)

    def on_start(self):
        self.get_news()

class SpamUserBehavior(NewsAppApi):
    @task(1)
    def do_comment_news(self):
        for i in range(1, 10):
            news_id = random.randint(1, 1000)
            self.add_news_comment(news_id)
            self.edit_news_comment(news_id)

    def on_start(self):
        self.get_news()


class NormalUserLocust(HttpLocust):
    task_set = NormalUserBehavior
    weight = 10
    min_wait = 100
    max_wait = 500

class SpamUserLocust(HttpLocust):
    task_set = SpamUserBehavior
    weight = 1
    min_wait = 1
    max_wait = 1
