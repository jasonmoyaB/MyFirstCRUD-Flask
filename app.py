from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,render_template,request, redirect, url_for,abort

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# ================ Conexión a la BD ============================
USER_DB = "postgres"
USER_PASSWORD = "mbrenes12"
SERVER_DB = "localhost"
NAME_DB = "demo"

FULL_URL_DB = f"postgresql://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}"

app.config["SQLALCHEMY_DATABASE_URI"] = FULL_URL_DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    instructor = db.Column(db.String(100), unique=True, nullable=False)
    topico = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Curso {self.nombre}>"
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html",error = error),404

@app.route("/")
def inicio():
    # select a toda la tabla
    cursos = Curso.query.all()
    total_cursos = Curso.query.count()
    return render_template("index.html",total = total_cursos, datos = cursos)

@app.route("/curso/<int:id>", methods = ["GET", "POST"])
def curso(id):
    curso = Curso.query.get(id)
    return render_template("curso.html", dato = curso)

@app.route("/insertarDatos", methods = ["GET","POST"])
def insertarDatos():
    if request.method == "POST":
        nuevo = Curso(
            nombre = request.form["nombre"],
            instructor = request.form["instructor"],
            topico = request.form["topico"],
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("insertar.html")