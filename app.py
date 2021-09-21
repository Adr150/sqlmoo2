# Ejemplo de consultas SQL
# Elaborado por Adriel Ortiz

from flask import Flask, render_template, redirect, request, jsonify
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.elements import literal_column

# Set up database
engine = create_engine("postgres://moujwumorxinad:e33450750c03940b0a975117ef00e99fde8904e5c7ad9a22c02af11a8b019127@ec2-44-193-150-214.compute-1.amazonaws.com:5432/d4206p5ccjqhor")
db = scoped_session(sessionmaker(bind=engine))


# Archivos que no me interesa ver en el menu
nomostrar = [ "index.html","layout.html","resultados.html","actualizador.html", "error.html"]

app = Flask(__name__)

@app.route("/")
def index():
    x = os.listdir('templates')
    print(x)

    #elimina las view que no quiero mostrar
    for i in nomostrar:
        x.remove(i)

    #define las rutas (solo elimina el ".html" )
    functions = []
    
    for i in x:
        functions.append(i.split('.')[0])

    return render_template("index.html",funciones = functions)


@app.route("/agregar",methods=["GET","POST"])
def insert():
    if request.method == "POST":
        name = request.form.get("name")
        year = int(request.form.get("year"))
        desc = request.form.get("description")
        image = request.form.get("imagelink")

        if not name or not year or not desc:
            return render_template('error.html',error = 400, message = "Informacion insuficiente")

        # Consulta SQL
        consulta = "INSERT INTO movies(name,year,description,image) VALUES(:name,:year,:description,:image);"

        # Datos
        datos = {
            "name":name,
            "year":year,
            "description":desc,
            "image":image
            }

        response = db.execute(consulta,datos)
        db.commit()

        # Hacemos cambios en el retorno
        return render_template("agregar.html")
        
    else:
        return render_template("agregar.html")


@app.route("/buscar",methods=["GET","POST"])
def select():
    if request.method == "POST":
        
        # Obtenido del formulario html
        q = request.form.get("q")

        if not q:
            return render_template("error.html", error=400,message="Sin datos para buscar")

        q = "%"+q+"%"

        # Consulta SQL
        consulta = "SELECT * FROM movies WHERE name LIKE :q OR description LIKE :q"

        # Datos 
        datos = {"q":q}

        # -----------------------    
        # Vamos a generar el json
        # -----------------------


        # Enviar consulta a la db
        rows = db.execute(consulta,datos).fetchall()

        if not len(rows):
            respuesta = {
                "items_counter":0,
                "items":[]
            }
            return jsonify(respuesta)
        # Creamos la lista para las respuestas
        elementos = []
        for element in rows:
            # Creamos el diccionario temporal para la informacion
            temp = {
                "id":element["id"],
                "name":element["name"],
                "year":element["year"],
                "description":element["description"],
                "image":element["image"]
            }

            # agregamos el elemento a la lista
            elementos.append(temp)

        respuesta = {
            "items_counter":len(elementos),
            "items":elementos
        }
        return jsonify(respuesta)
            
     

    else:
        return render_template("buscar.html")
    
@app.route("/mostrar")
def selectall():
    # Consulta SQL
    consulta = "SELECT * FROM movies"
    response = db.execute(consulta).fetchall()

    if not len(response):
            return render_template('error.html', error=404, message="No hay registros")

    return render_template("mostrar.html",response = response)
    

@app.route("/actualizar",methods=["GET","POST"])
def update():
    if request.method == "POST":

        id = request.form.get("select")

        if not id:
            return render_template('error.html', error=400, message="No valido")

        # Consulta SQL
        consulta = "SELECT * FROM movies WHERE id = :id "

        # Datos
        datos = {
            "id": id
        }

        response = db.execute(consulta,datos).fetchone()

        return render_template("actualizador.html", info = response)

    else:
        # Consulta
        consulta = "SELECT * FROM movies"

        response = db.execute(consulta).fetchall()

        if not len(response):
            return render_template('error.html', error=404, message="No hay registros")

        return render_template("actualizar.html",items = response)

@app.route("/actualizador",methods=["GET","POST"])
def actualizador():
    if request.method == "POST":

        id_item = request.form.get("id")
        name = request.form.get("name")
        year = int(request.form.get("year"))
        desc = request.form.get("description")
        image = request.form.get("imagelink")

        if not name or not year or not desc:
            return render_template('error.html', error=400, message="Datos incompletos")

        # Consulta 
        consulta = "UPDATE movies SET name = :name,year = :year,description = :description,image = :image WHERE id = :id"

        # Datos 
        datos = {
            "name": name,
            "year":year,
            "description":desc,
            "image":image,
            "id":id_item
        }
        response = db.execute(consulta, datos)
        db.commit()

        # Consulta
        consulta = "SELECT * FROM movies"

        response = db.execute(consulta).fetchall()

        if not len(response):
            return render_template('error.html', error=404, message="No hay registros")

        return render_template("actualizar.html",items = response)

      
        
    else:
        return render_template("agregar.html")


@app.route("/eliminar",methods=["GET","POST"])
def delete():
    if request.method == "POST":

        id = request.form.get("select")

        if not id:
            return render_template('error.html', error=400, message="No valido")

        # Consulta 
        consulta = "DELETE FROM movies WHERE id = :id"

        # Datos
        datos = {
            "id":id
        }

        response = db.execute(consulta, datos)
        db.commit()


        
    # Consulta
    consulta = "SELECT * FROM movies"

    response = db.execute(consulta).fetchall()

    return render_template("eliminar.html",items = response)