# app.py
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_migrate import Migrate
from models import db, Curso  # <-- importamos db y el modelo desde models

# $env:FLASK_DEBUG = "1"
# flask run

app = Flask(__name__)

# ================ Conexión a la BD ============================
USER_DB = "postgres"
USER_PASSWORD = "mbrenes12"
SERVER_DB = "localhost"
NAME_DB = "demo"
FULL_URL_DB = f"postgresql://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}"

app.config["SQLALCHEMY_DATABASE_URI"] = FULL_URL_DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar extensiones con la app
db.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404

@app.route("/")
def inicio():
    cursos = Curso.query.all()
    total_cursos = Curso.query.count()
    return render_template("index.html", total=total_cursos, datos=cursos)

@app.route("/curso/<int:id>", methods=["GET", "POST"])
def curso(id):
    curso = Curso.query.get_or_404(id)
    return render_template("curso.html", dato=curso)

@app.route("/insertarDatos", methods=["GET","POST"])
def insertarDatos():
    if request.method == "POST":
        nuevo = Curso(
            nombre=request.form["nombre"],
            instructor=request.form["instructor"],
            topico=request.form["topico"],
        )
        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("inicio"))
    return render_template("insertar.html")


@app.route("/editar/<int:id>", methods= ["GET", "POST"])
def editar(id):
    curso = Curso.query.get_or_404(id)
    if request.method == "POST":
        curso.nombre = request.form["nombre"]
        curso.instructor = request.form["instructor"]
        curso.topico= request.form["topico"]
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("editar.html", curso = curso)


@app.route("/eliminar/<int:id>", methods = ["GET", "POST"], endpoint = "eliminar")
def elimar(id):
    curso = Curso.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("eliminar.html",curso= curso)


if __name__ == "__main__":
    app.run(debug=True)
