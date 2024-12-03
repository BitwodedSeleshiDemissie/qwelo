import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use the External Database URL from Render for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgresql://todolist_g9bz_user:AwpfKivOhGL9xc4g2ubqqY0MEpcIU72G@dpg-ct7gimpu0jms73dqrplg-a.oregon-postgres.render.com/todolist_g9bzL')  # Make sure to set this in your environment or use the Render URL directly
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'

# Initialize the database
with app.app_context():
    db.create_all()  # Creates the database tables if they don't exist

@app.route('/')
def index():
    return render_template('index.html')  # This serves your HTML page

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()  # Get all tasks from the database
    return jsonify([task.title for task in tasks])  # Return the task titles in JSON format

@app.route('/api/tasks', methods=['POST'])
def add_task():
    task_data = request.get_json()  # Get the task data from the request body
    new_task = Task(title=task_data['title'])  # Create a new Task object
    db.session.add(new_task)  # Add the task to the session
    db.session.commit()  # Commit the transaction to save it to the database
    return jsonify({"title": new_task.title}), 201  # Return the created task

@app.route('/api/tasks', methods=['DELETE'])
def del_task():
    task_data = request.get_json()  # Get the task data from the request body
    task_title = task_data.get('title')  # Extract the title from the data
    task_to_delete = Task.query.filter_by(title=task_title).first()  # Find the task by title
    if task_to_delete:
        db.session.delete(task_to_delete)  # Delete the task from the session
        db.session.commit()  # Commit the transaction to save the changes
    return jsonify({"message": "Task deleted successfully!"}), 200  # Return a success message

if __name__ == '__main__':
    app.run(debug=True)
