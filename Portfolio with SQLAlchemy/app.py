from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projects.db"
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    github_link = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Project {self.title}>"


@app.route("/")
def homepage():
    projects = Project.query.all()
    return render_template("index.html", projects=projects)


@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/project/<int:id>")
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template("detail.html", project=project)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/skills")
def skills():
    return render_template("skills.html")


@app.route("/projects")
def project_list():
    projects = Project.query.all()
    return render_template("project_list.html", projects=projects)


@app.route("/project/new", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        title = request.form["title"]
        date_str = request.form["date"]
        date = datetime.strptime(date_str, "%Y-%m").date()
        description = request.form["description"]
        skills = request.form["skills"]
        github_link = request.form["github_link"]

        new_project = Project(
            title=title,
            date=date,
            description=description,
            skills=skills,
            github_link=github_link,
        )

        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("homepage"))

    return render_template("projectform.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_project(id):
    project = Project.query.get(id)

    if request.method == "POST":
        project.title = request.form["title"]
        project.date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        project.description = request.form["description"]
        project.skills = request.form["skills"]
        project.github_link = request.form["github_link"]

        db.session.commit()

        return redirect(url_for("homepage"))

    return render_template("edit.html", project=project)


@app.route("/project/<int:id>/delete")
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
