from mongoengine import *


class Highscores(Document):
    username = StringField()
    score = IntField(default=0)

    def __repr__(self):
        return f"<Highscores:{self.username} - {self.score}>"


connect("Highscores")

pass
