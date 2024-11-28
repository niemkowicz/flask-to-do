from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    content = request.form.get('content')
    if content:
        task = Task(content=content)
        db.session.add(task)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = request.form['status']
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.content = request.form['content']
    db.session.commit()
    return redirect('/')

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
