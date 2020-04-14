from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://xldgewakwrsnui:340c954698e497f612a85be9a7fd0c5e14f485c8a60debc3b" \
                                        "9fb542a9f6ab24c@ec2-50-17-21-170.compute-1.amazonaws.com:5432/dap46s0s0pgc91"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Task {}>".format(self.student_id)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route("/", methods=["POST", "GET"])
def index():
    global student_id
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        new_student = Student(first_name=first_name, last_name=last_name)
        print(new_student)
        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect("/")
        except:
            return "FML DB FAILED"

    else:
        students = Student.query.order_by(Student.last_name).all()
        return render_template("index.html", students=students)


@app.route("/delete/<int:id>")
def delete(id):
    student_to_delete = Student.query.get_or_404(id)

    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "An exception occurred during deletion."


if __name__ == "__main__":
    app.run(debug=True)
