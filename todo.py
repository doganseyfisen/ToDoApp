from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/dogan/Desktop/ToDoApp/todo.db"
db.init_app(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    completed = db.Column(db.Boolean)

@app.route("/")
def index():
    todos = ToDo.query.all()
    
    return render_template("index.html", todos = todos)


@app.route("/completed/<string:id>")
def complete_todo(id):
    todo = ToDo.query.filter_by(id = id).first()
    todo.completed = not todo.completed
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def delete_todo(id):
    todo = ToDo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/add", methods = ["POST"])
def add_todo():
    title = request.form.get("title")
    new_todo = ToDo(title = title, completed = False)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
