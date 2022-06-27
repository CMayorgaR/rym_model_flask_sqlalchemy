import os #Objeto de Python que nos da acceso a nuestro sistema de archivos.
from flask import Flask, jsonify, request
from models import db, User, Favorites, Character, Location, Episode
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

BASEDIR = os.path.abspath(os.path.dirname(__file__)) #Nos permite decirle la carpeta raíz donde se va a crear nuestra base de datos
app = Flask(__name__)

#Configs
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+ os.path.join(BASEDIR, 'test.db') #Dónde voy a crear mi base de datos
app.config['DEBUG']= True #nos permite que en la terminal se impriman los errores que puedan aparecer.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Evitamos que sqlalchemy nos entregue un reporte de cada cambio que se haga en la base de datos

db.init_app(app) #Esta línea se encarga de cargar la base de datos al momento de levantar el server. Creamos una conexión con nuestra base de datos
CORS(app) #Cors es una depencia que nos permite evitar errores de permisos en nuestro servidor (es lo que está declarado en app.run)
Migrate(app, db) #al ejecutar los comandos va a comenzar a migrar y a crear la base de datos

@app.route('/user', methods=['POST'])
def user():
    user = User()
    user.user_email = request.json.get("user_email")
    user.user_password = request.json.get("user_password")
    db.session.add(user) #guarda la instancia de la clase como una nueva inserción en la tabla
    db.session.commit() #guarda los cambios durante la sesión
    return jsonify(user.serialize()), 200 #esto retorna el usuario creado con la función serialize (id y email) que es un diccionario python en un elemento JSON

@app.route('/users', methods=['GET'])
def all_users():    
    users = User.query.all() #query = consulta. 
    users = list(map(lambda x: x.serialize(), users)) #x = user. cada elemento de la lista debe serializarse individualmente. Para eso usamos list y map.
    return jsonify(users), 200

@app.route('/user/<int:id>', methods=['GET'])
def one_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize()), 200 #aquí se puede serializar directamente porque es un solo elemento el que se selecciona.
    
@app.route('/user/<int:id>', methods=['DELETE'])
def erase_user(id):
    user = User.query.get(id)
    db.session.delete(user) #delete se usa para eliminar en sql-alchemy
    db.session.commit()
    return jsonify('Usuario eliminado exitosamente')




if __name__==  "__main__":
    app.run(host="localhost", port="5000")