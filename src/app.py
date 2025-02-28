from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mysql = MySQL(app)
mongo = PyMongo(app)

@app.route('/add_mongo',methods=["POST"])
def add_mongo():
    
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    ciudad = request.json["ciudad"]
    genero = request.json["genero"]

    if nombre and edad and ciudad  and  genero:
        id = mongo.db.personas.insert_one({
            "nombre" : nombre,
            "edad" : edad,
            "ciudad" : ciudad,
            "genero" : genero
        })

        response = {
            "id": str(id.inserted_id),
            "nombre" : nombre,
            "edad" : edad,
            "ciudad" : ciudad,
            "genero" : genero
        }

        return jsonify(response)
        
    return jsonify({"error":"faltan datos"})

@app.route('/get_mongo',methods=["GET"])
def get_mongo():
    personas = mongo.db.personas.find()
    return jsonify(personas)

@app.route('/get_mongo/<id>',methods=["GET"])
def get_mongoid(id):
    personas = mongo.db.personas.find({"_id": ObjectId(id)})

    if personas:
        return jsonify({personas})


@app.route('/delete_mongo/<id>',methods=["DELETE"])
def delete_mongo(id):
    mongo.db.personas.delete_one({"_id": ObjectId(id)})
    
    return jsonify({"message":"Eliminado con exito"})

@app.route('/update_mongo/<id>', methods=["PUT"])
def update_mongo(id):
    
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    ciudad = request.json["ciudad"]
    genero = request.json["genero"]

    personas = mongo.db.personas.update_one({"_id":ObjectId(id)},{"$set":{

            "nombre" : nombre,
            "edad" : edad,
            "ciudad" : ciudad,
            "genero" : genero

    }})

    return jsonify({"message":"ACTUALIZADO"})


@app.route('/add_sql', methods=["POST"])
def add_sql():
    
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    ciudad = request.json["ciudad"]
    genero = request.json["genero"]

    if nombre and edad and ciudad and genero:

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO personas VALUES(NULL,%s,%s,%s,%s)",(nombre,edad,ciudad,genero))
        mysql.connection.commit()

        return jsonify({"usuario":{"nombre":nombre,"edad":edad,"ciudad":ciudad,"genero":genero}})
    return jsonify({"message":"error"})


@app.route('/get_sql', methods=["GET"])
def get_sql():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM personas ")
    sql = cursor.fetchall()
    return jsonify(sql)


@app.route('/get_sql/<id>', methods=["GET"])
def get_sqlid(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM personas where id = %s ",(id,))
    sql = cursor.fetchall()
    return jsonify(sql)

@app.route('/delete_sql/<id>', methods=["DELETE"])
def delete_sql(id):
    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM personas where id=%s",(id,))
    mysql.connection.commit()
    return jsonify({"message":"ELIMINADO CON EXITO" + id})

@app.route('/update_sql/<id>', methods=["PUT"])
def update_sql(id):
    
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    ciudad = request.json["ciudad"]
    genero = request.json["genero"]

    if nombre and edad and ciudad and genero:

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE personas SET nombre=%s,edad=%s,ciudad=%s,genero=%s where id=%s",(nombre,edad,ciudad,genero,id))
        mysql.connection.commit()

        return jsonify({"usuario":{"nombre":nombre,"edad":edad,"ciudad":ciudad,"genero":genero}})
    return jsonify({"message":"error"})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")