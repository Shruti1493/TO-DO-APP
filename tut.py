from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(2000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Todo:{self.sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        Title = request.form["title"]
        Desc = request.form["desc"]

        todo = Todo(title=Title, desc=Desc)
        db.session.add(todo)
        db.session.commit()
        data = todo.query.all()
        # print(data)

    else:
        data = Todo.query.all()
    return render_template('index.html', todo=data)


@app.route("/delete/<int:sno>", methods=['GET', 'POST'])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect("/")


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        Title = request.form["title"]
        Desc = request.form["desc"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = Title
        todo.desc = Desc
        db.session.add(todo)
        db.session.commit()
      
        return redirect('/')

    data = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
