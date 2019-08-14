from app import db


class ExcellentList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    votes = db.Column(db.Integer, nullable=False)


    def upvote(self):
        self.votes += 1
        db.session.commit()


    def __repr__(self):
        return '<Title {}>'.format(self.title)


class WeirdList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    votes = db.Column(db.Integer, nullable=False)


    def upvote(self):
        self.votes += 1
        db.session.commit()


    def __repr__(self):
        return '<Title {}>'.format(self.title)


