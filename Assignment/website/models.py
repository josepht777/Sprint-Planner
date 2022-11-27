from . import db

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(150))
    storyPoint = db.Column(db.Integer)
    tag = db.Column(db.String(150))
    priority = db.Column(db.String(150))
    status = db.Column(db.String(150), default = 'Not Started')
    total_time = db.Column(db.Integer, default = 0)
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    description = db.Column(db.String(10000))
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprint.id'), nullable=True)
    time_taken = db.Column(db.Float,  default = 0)
    is_added = db.Column(db.Boolean, default = False)

class Sprint(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    status = db.Column(db.String(150), default = 'created')
    tasks = db.relationship('Task')

#fix one to many relationship between user and task
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    email = db.Column(db.String(150))
    tasks = db.relationship('Task')
    stamps = db.relationship('Workstamp')

class Workstamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    hours = db.Column(db.Integer)
    date = db.Column(db.Date())
    task_id = db.Column(db.Integer)