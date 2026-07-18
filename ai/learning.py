# ai/learning.py

from collections import defaultdict


class LearningEngine:

    def __init__(self):

        self.preferences = defaultdict(dict)

        self.counter = defaultdict(int)


    def learn(self, app, query=""):

        if not app:
            return

        self.counter[app] += 1

        if query:

            self.preferences[app][query] = (

                self.preferences[app].get(query, 0) + 1

            )


    def get_usage(self, app):

        return self.counter.get(app, 0)


    def favorite_app(self):

        if not self.counter:

            return None

        return max(

            self.counter,

            key=self.counter.get

        )


    def favorite_query(self, app):

        if app not in self.preferences:

            return None

        queries = self.preferences[app]

        if not queries:

            return None

        return max(

            queries,

            key=queries.get

        )


    def statistics(self):

        return {

            "apps": dict(self.counter),

            "preferences": {

                k: dict(v)

                for k, v in self.preferences.items()

            }

        }


    def clear(self):

        self.counter.clear()

        self.preferences.clear()