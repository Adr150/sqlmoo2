from flask import Flask, render_template, redirect, request
import json
import os
from cs50 import SQL

db = SQL("sqlite:///moovie.db")

#Archivos que no me interesa ver en el menu
nomostrar = [ "index.html","layout.html","resultados.html","actualizador.html"]

app = Flask(__name__)

@app.route("/")
def index():
    x = os.listdir('templates')
    
    #elimina las view que no quiero mostrar
    for i in nomostrar:
        x.remove(i)

    #define las rutas (solo elimina el ".html" )
    functions = []
    
    for i in x:
        functions.append(i.split('.')[0])

    return render_template("index.html",funciones = functions)

#esto funciona como menu de las view similar al switch de C
@app.route("/views/<string:option>")
def hacer(option):
    return redirect('/'+option)

@app.route("/agregar",methods=["GET","POST"])
def insert():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            year = int(request.form.get("year"))
            desc = request.form.get("description")
            image = request.form.get("imagelink")

            response = db.execute("INSERT INTO movies(name,year,description,image) VALUES(:name,:year,:description,:image)" ,name=name,year=year,description=desc,image=image)

            if response:
                return redirect('/')

        except:
            return "<h1>Informacion insuficiente :C </h1>"
        
    else:
        return render_template("agregar.html")


@app.route("/buscar",methods=["GET","POST"])
def select():
    if request.method == "POST":
      
        q = "%"+request.form.get("q")+"%"

        response = db.execute("SELECT * FROM movies WHERE name LIKE :q OR year LIKE :q OR description LIKE :q", q =q)
        print(response)

        return render_template("resultados.html",response = response)
            
     

    else:
        return render_template("buscar.html")
    
@app.route("/mostrar")
def selectall():
    response = db.execute("SELECT * FROM movies")

    return render_template("mostrar.html",response = response)
    

@app.route("/actualizar",methods=["GET","POST"])
def update():
    if request.method == "POST":
        response = db.execute("SELECT * FROM movies WHERE id = :id ",id = request.form.get("select"))

        return render_template("actualizador.html", info = response[0])

    else:
        response = db.execute("SELECT * FROM movies")

        return render_template("actualizar.html",items = response)

@app.route("/actualizador",methods=["GET","POST"])
def actualizador():
    if request.method == "POST":
        try:
            id = request.form.get("id")
            name = request.form.get("name")
            year = int(request.form.get("year"))
            desc = request.form.get("description")
            image = request.form.get("imagelink")

            response = db.execute("UPDATE movies SET name = :name,year = :year,description = :description,image = :image WHERE id = :id" ,name=name,year=year,description=desc,image=image, id = id)

            if response:
                return redirect('/')

        except:
            return "<h1>Que paso master? </h1>"
        
    else:
        return render_template("agregar.html")


@app.route("/eliminar",methods=["GET","POST"])
def delete():
    if request.method == "POST":
        response = db.execute("DELETE FROM movies WHERE id = :id ",id = request.form.get("select"))

        return redirect('/')


    else:
        response = db.execute("SELECT * FROM movies")

        return render_template("eliminar.html",items = response)