from flask import Flask, jsonify, request
from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func as sqlalchemy_func, select, join
from decimal import Decimal
import datetime

# Inicializar la aplicación Flask
app = Flask(__name__)

# --- Configuración de MongoDB ---
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "proyectoCineMongo"  # Nombre de tu DB MongoDB
client = MongoClient(MONGO_URI)
db_mongo = client[MONGO_DB_NAME]

# --- Configuración de SQL (MySQL) ---
# RECUERDA: Reemplaza 'tu_usuario_sql' y 'tu_contraseña_sql' con tus credenciales.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/proyectoCine' #
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_sql = SQLAlchemy(app)


# --- Helper para serializar Decimal, Date, Time ---
def alchemy_encoder(obj):
    if isinstance(obj, datetime.date) or isinstance(obj, datetime.time):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


# --- Definición de Modelos SQL ---
class PeliculaSQL(db_sql.Model):
    __tablename__ = 'Pelicula'  #
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    titulo = db_sql.Column(db_sql.String(100))  #
    genero = db_sql.Column(db_sql.String(50))  #
    duracion = db_sql.Column(db_sql.Integer)  #
    clasificacion = db_sql.Column(db_sql.String(10))  #
    idioma = db_sql.Column(db_sql.String(50))  #

    funciones = db_sql.relationship('FuncionSQL', backref='pelicula', lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SalaSQL(db_sql.Model):
    __tablename__ = 'Sala'  #
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    nombre = db_sql.Column(db_sql.String(50))  #
    capacidad = db_sql.Column(db_sql.Integer)  #
    tipo = db_sql.Column(db_sql.String(50))  #

    funciones = db_sql.relationship('FuncionSQL', backref='sala', lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClienteSQL(db_sql.Model):
    __tablename__ = 'Cliente'  #
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    nombre = db_sql.Column(db_sql.String(100))  #
    correo = db_sql.Column(db_sql.String(100))  #
    telefono = db_sql.Column(db_sql.String(20))  #

    boletos = db_sql.relationship('BoletoSQL', backref='cliente', lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class FuncionSQL(db_sql.Model):
    __tablename__ = 'Funcion'  #
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    pelicula_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('Pelicula.id'), nullable=False)  #
    sala_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('Sala.id'), nullable=False)  #
    fecha = db_sql.Column(db_sql.Date)  #
    hora = db_sql.Column(db_sql.Time)  #
    precio = db_sql.Column(db_sql.Numeric(6, 2))  #

    boletos = db_sql.relationship('BoletoSQL', backref='funcion', lazy=True)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if data.get('fecha'):
            data['fecha'] = data['fecha'].isoformat()
        if data.get('hora'):
            data['hora'] = data['hora'].isoformat()
        if data.get('precio'):
            data['precio'] = float(data['precio'])
        return data


class BoletoSQL(db_sql.Model):
    __tablename__ = 'Boleto'  #
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    cliente_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('Cliente.id'), nullable=False)  #
    funcion_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('Funcion.id'), nullable=False)  #
    cantidad = db_sql.Column(db_sql.Integer)  #
    fecha_compra = db_sql.Column(db_sql.DateTime, default=datetime.datetime.utcnow)  #

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if data.get('fecha_compra'):
            data['fecha_compra'] = data['fecha_compra'].isoformat()
        return data


# --- Rutas ---
@app.route('/')
def home():
    return jsonify({"mensaje": "API del Proyecto Cine funcionando!"})


# --- CRUD SQL: Pelicula ---
@app.route('/sql/peliculas', methods=['POST'])
def add_sql_pelicula():
    data = request.get_json()
    nueva_pelicula = PeliculaSQL(**data)
    db_sql.session.add(nueva_pelicula)
    db_sql.session.commit()
    return jsonify(nueva_pelicula.to_dict()), 201


@app.route('/sql/peliculas', methods=['GET'])
def get_sql_peliculas():
    peliculas = PeliculaSQL.query.all()
    return jsonify([p.to_dict() for p in peliculas])


@app.route('/sql/peliculas/<int:id>', methods=['GET'])
def get_sql_pelicula(id):
    pelicula = PeliculaSQL.query.get_or_404(id)
    return jsonify(pelicula.to_dict())


@app.route('/sql/peliculas/<int:id>', methods=['PUT'])
def update_sql_pelicula(id):
    pelicula = PeliculaSQL.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(pelicula, key, value)
    db_sql.session.commit()
    return jsonify(pelicula.to_dict())


@app.route('/sql/peliculas/<int:id>', methods=['DELETE'])
def delete_sql_pelicula(id):
    pelicula = PeliculaSQL.query.get_or_404(id)
    db_sql.session.delete(pelicula)
    db_sql.session.commit()
    return jsonify({"mensaje": "Pelicula eliminada"}), 200


# --- CRUD SQL: Sala ---
# (Similar a Pelicula: POST, GET all, GET one, PUT, DELETE)
@app.route('/sql/salas', methods=['POST'])
def add_sql_sala():
    data = request.get_json()
    nueva_sala = SalaSQL(**data)
    db_sql.session.add(nueva_sala)
    db_sql.session.commit()
    return jsonify(nueva_sala.to_dict()), 201


@app.route('/sql/salas', methods=['GET'])
def get_sql_salas():
    salas = SalaSQL.query.all()
    return jsonify([s.to_dict() for s in salas])


# ... (GET one, PUT, DELETE para SalaSQL)

# --- CRUD SQL: Cliente ---
# (Similar a Pelicula: POST, GET all, GET one, PUT, DELETE)
@app.route('/sql/clientes', methods=['POST'])
def add_sql_cliente():
    data = request.get_json()
    nuevo_cliente = ClienteSQL(**data)
    db_sql.session.add(nuevo_cliente)
    db_sql.session.commit()
    return jsonify(nuevo_cliente.to_dict()), 201


@app.route('/sql/clientes', methods=['GET'])
def get_sql_clientes():
    clientes = ClienteSQL.query.all()
    return jsonify([c.to_dict() for c in clientes])


# ... (GET one, PUT, DELETE para ClienteSQL)

# --- CRUD SQL: Funcion ---
# (Similar a Pelicula: POST, GET all, GET one, PUT, DELETE, pero con manejo de Decimal, Date, Time)
@app.route('/sql/funciones', methods=['POST'])
def add_sql_funcion():
    data = request.get_json()
    # Convertir precio a Decimal
    if 'precio' in data:
        data['precio'] = Decimal(data['precio'])
    # Convertir fecha y hora
    if 'fecha' in data:
        data['fecha'] = datetime.date.fromisoformat(data['fecha'])
    if 'hora' in data:
        data['hora'] = datetime.time.fromisoformat(data['hora'])

    nueva_funcion = FuncionSQL(**data)
    db_sql.session.add(nueva_funcion)
    db_sql.session.commit()
    return jsonify(nueva_funcion.to_dict()), 201


@app.route('/sql/funciones', methods=['GET'])
def get_sql_funciones():
    funciones = FuncionSQL.query.all()
    return jsonify([f.to_dict() for f in funciones])


# ... (GET one, PUT, DELETE para FuncionSQL)

# --- CRUD SQL: Boleto ---
@app.route('/sql/boletos', methods=['POST'])
def add_sql_boleto():
    data = request.get_json()

    # Lógica de validación de capacidad (equivalente al trigger)
    funcion_id = data.get('funcion_id')
    cantidad_nueva = data.get('cantidad', 0)

    funcion = FuncionSQL.query.get(funcion_id)
    if not funcion:
        return jsonify({"error": "Función no encontrada"}), 404

    sala = SalaSQL.query.get(funcion.sala_id)
    if not sala:
        return jsonify({"error": "Sala no encontrada para la función"}), 404

    capacidad_sala = sala.capacidad

    # Calcular boletos ya vendidos para esa función
    boletos_vendidos_query = db_sql.session.query(sqlalchemy_func.sum(BoletoSQL.cantidad)).filter(
        BoletoSQL.funcion_id == funcion_id)
    boletos_vendidos = boletos_vendidos_query.scalar() or 0

    if boletos_vendidos + cantidad_nueva > capacidad_sala:
        return jsonify({"error": "No hay suficientes asientos disponibles para esta función."}), 400  #

    nuevo_boleto = BoletoSQL(**data)
    db_sql.session.add(nuevo_boleto)
    db_sql.session.commit()
    return jsonify(nuevo_boleto.to_dict()), 201


@app.route('/sql/boletos', methods=['GET'])
def get_sql_boletos():
    boletos = BoletoSQL.query.all()
    return jsonify([b.to_dict() for b in boletos])


# ... (GET one, PUT, DELETE para BoletoSQL - Cuidado con PUT, validar capacidad también si cambia cantidad o funcion_id)


# --- SQL Vistas Equivalentes ---
@app.route('/sql/vista/funciones', methods=['GET'])  # Equivalente a VistaFunciones
def get_sql_vista_funciones():
    resultados = db_sql.session.query(
        FuncionSQL.id,
        PeliculaSQL.titulo,
        SalaSQL.nombre.label('sala'),
        FuncionSQL.fecha,
        FuncionSQL.hora,
        FuncionSQL.precio
    ).join(PeliculaSQL, FuncionSQL.pelicula_id == PeliculaSQL.id) \
        .join(SalaSQL, FuncionSQL.sala_id == SalaSQL.id) \
        .all()

    lista_funciones = []
    for row in resultados:
        lista_funciones.append({
            "id": row.id,
            "titulo": row.titulo,
            "sala": row.sala,
            "fecha": row.fecha.isoformat() if row.fecha else None,
            "hora": row.hora.isoformat() if row.hora else None,
            "precio": float(row.precio) if row.precio else None
        })
    return jsonify(lista_funciones)


@app.route('/sql/vista/ingresos-por-pelicula', methods=['GET'])  # Equivalente a IngresosPorPelicula
def get_sql_vista_ingresos_pelicula():
    resultados = db_sql.session.query(
        PeliculaSQL.titulo,
        sqlalchemy_func.sum(BoletoSQL.cantidad * FuncionSQL.precio).label('ingresos')
    ).select_from(BoletoSQL) \
        .join(FuncionSQL, BoletoSQL.funcion_id == FuncionSQL.id) \
        .join(PeliculaSQL, FuncionSQL.pelicula_id == PeliculaSQL.id) \
        .group_by(PeliculaSQL.titulo) \
        .all()

    lista_ingresos = [{"titulo": row.titulo, "ingresos": float(row.ingresos) if row.ingresos else 0.0} for row in
                      resultados]
    return jsonify(lista_ingresos)


# --- MongoDB Funciones Auxiliares ---
def serialize_mongo_doc(doc):
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    if doc and 'pelicula_id' in doc and isinstance(doc.get('pelicula_id'), ObjectId):  #
        doc['pelicula_id'] = str(doc['pelicula_id'])
    if doc and 'sala_id' in doc and isinstance(doc.get('sala_id'), ObjectId):  #
        doc['sala_id'] = str(doc['sala_id'])
    if doc and 'cliente_id' in doc and isinstance(doc.get('cliente_id'), ObjectId):  #
        doc['cliente_id'] = str(doc['cliente_id'])
    if doc and 'funcion_id' in doc and isinstance(doc.get('funcion_id'), ObjectId):  #
        doc['funcion_id'] = str(doc['funcion_id'])
    if doc and 'fecha' in doc and isinstance(doc.get('fecha'), datetime.datetime):  #
        doc['fecha'] = doc['fecha'].strftime('%Y-%m-%d')
    if doc and 'fecha_compra' in doc and isinstance(doc.get('fecha_compra'), datetime.datetime):  #
        doc['fecha_compra'] = doc['fecha_compra'].isoformat()
    return doc


# --- CRUD MongoDB: peliculas ---
@app.route('/mongo/peliculas', methods=['POST'])
def add_mongo_pelicula():
    data = request.get_json()
    result = db_mongo.peliculas.insert_one(data)  #
    return jsonify(serialize_mongo_doc(db_mongo.peliculas.find_one({"_id": result.inserted_id}))), 201


@app.route('/mongo/peliculas', methods=['GET'])
def get_mongo_peliculas_all():
    peliculas = list(db_mongo.peliculas.find())  #
    return jsonify([serialize_mongo_doc(p) for p in peliculas])


@app.route('/mongo/peliculas/<string:id>', methods=['GET'])
def get_mongo_pelicula_one(id):
    pelicula = db_mongo.peliculas.find_one({"_id": ObjectId(id)})  #
    if pelicula:
        return jsonify(serialize_mongo_doc(pelicula))
    return jsonify({"error": "Pelicula no encontrada"}), 404


@app.route('/mongo/peliculas/<string:id>', methods=['PUT'])
def update_mongo_pelicula(id):
    data = request.get_json()
    result = db_mongo.peliculas.find_one_and_update(  #
        {"_id": ObjectId(id)},
        {"$set": data},
        return_document=ReturnDocument.AFTER
    )
    if result:
        return jsonify(serialize_mongo_doc(result))
    return jsonify({"error": "Pelicula no encontrada"}), 404


@app.route('/mongo/peliculas/<string:id>', methods=['DELETE'])
def delete_mongo_pelicula(id):
    result = db_mongo.peliculas.delete_one({"_id": ObjectId(id)})  #
    if result.deleted_count > 0:
        return jsonify({"mensaje": "Pelicula eliminada"}), 200
    return jsonify({"error": "Pelicula no encontrada"}), 404


# --- CRUD MongoDB: salas ---
# (Similar a peliculas: POST, GET all, GET one, PUT, DELETE)
@app.route('/mongo/salas', methods=['POST'])
def add_mongo_sala():
    data = request.get_json()
    result = db_mongo.salas.insert_one(data)  #
    return jsonify(serialize_mongo_doc(db_mongo.salas.find_one({"_id": result.inserted_id}))), 201


@app.route('/mongo/salas', methods=['GET'])
def get_mongo_salas_all():
    salas = list(db_mongo.salas.find())  #
    return jsonify([serialize_mongo_doc(s) for s in salas])


# ... (GET one, PUT, DELETE para salas en MongoDB)

# --- CRUD MongoDB: clientes ---
# (Similar a peliculas: POST, GET all, GET one, PUT, DELETE)
@app.route('/mongo/clientes', methods=['POST'])
def add_mongo_cliente():
    data = request.get_json()
    result = db_mongo.clientes.insert_one(data)  #
    return jsonify(serialize_mongo_doc(db_mongo.clientes.find_one({"_id": result.inserted_id}))), 201


@app.route('/mongo/clientes', methods=['GET'])
def get_mongo_clientes_all():
    clientes = list(db_mongo.clientes.find())  #
    return jsonify([serialize_mongo_doc(c) for c in clientes])


# ... (GET one, PUT, DELETE para clientes en MongoDB)

# --- CRUD MongoDB: funciones ---
# (Similar a peliculas: POST, GET all, GET one, PUT, DELETE)
@app.route('/mongo/funciones', methods=['POST'])
def add_mongo_funcion():
    data = request.get_json()
    # Convertir IDs de referencia a ObjectId si vienen como string
    if 'pelicula_id' in data:  #
        data['pelicula_id'] = ObjectId(data['pelicula_id'])
    if 'sala_id' in data:  #
        data['sala_id'] = ObjectId(data['sala_id'])
    if 'fecha' in data:  #
        data['fecha'] = datetime.datetime.strptime(data['fecha'], '%Y-%m-%d')

    result = db_mongo.funciones.insert_one(data)  #
    return jsonify(serialize_mongo_doc(db_mongo.funciones.find_one({"_id": result.inserted_id}))), 201


@app.route('/mongo/funciones', methods=['GET'])
def get_mongo_funciones_all():
    funciones = list(db_mongo.funciones.find())  #
    return jsonify([serialize_mongo_doc(f) for f in funciones])


# ... (GET one, PUT, DELETE para funciones en MongoDB)

# --- CRUD MongoDB: boletos ---
@app.route('/mongo/boletos', methods=['POST'])
def add_mongo_boleto():
    data = request.get_json()

    # Convertir IDs a ObjectId
    if 'cliente_id' in data:  #
        data['cliente_id'] = ObjectId(data['cliente_id'])
    funcion_id_str = data.get('funcion_id')  #
    if funcion_id_str:
        data['funcion_id'] = ObjectId(funcion_id_str)

    # Lógica de validación de capacidad
    funcion_obj_id = data.get('funcion_id')
    cantidad_nueva = data.get('cantidad', 0)

    funcion_doc = db_mongo.funciones.find_one({"_id": funcion_obj_id})  #
    if not funcion_doc:
        return jsonify({"error": "Función no encontrada en MongoDB"}), 404

    sala_obj_id = funcion_doc.get('sala_id')  #
    sala_doc = db_mongo.salas.find_one({"_id": sala_obj_id})  #
    if not sala_doc:
        return jsonify({"error": "Sala no encontrada para la función en MongoDB"}), 404

    capacidad_sala = sala_doc.get('capacidad', 0)  #

    boletos_vendidos_agg = list(db_mongo.boletos.aggregate([  #
        {"$match": {"funcion_id": funcion_obj_id}},
        {"$group": {"_id": "$funcion_id", "total_cantidad": {"$sum": "$cantidad"}}}
    ]))
    boletos_vendidos = boletos_vendidos_agg[0]['total_cantidad'] if boletos_vendidos_agg else 0

    if boletos_vendidos + cantidad_nueva > capacidad_sala:
        return jsonify({"error": "No hay suficientes asientos disponibles para esta función (MongoDB)."}), 400

    data['fecha_compra'] = datetime.datetime.utcnow()  #
    result = db_mongo.boletos.insert_one(data)  #
    return jsonify(serialize_mongo_doc(db_mongo.boletos.find_one({"_id": result.inserted_id}))), 201


@app.route('/mongo/boletos', methods=['GET'])
def get_mongo_boletos_all():
    boletos = list(db_mongo.boletos.find())  #
    return jsonify([serialize_mongo_doc(b) for b in boletos])


# ... (GET one, PUT, DELETE para boletos en MongoDB)


# --- MongoDB Vistas Equivalentes ---
@app.route('/mongo/vista/funciones', methods=['GET'])
def get_mongo_vista_funciones():
    pipeline = [
        {
            "$lookup": {  #
                "from": "peliculas",  #
                "localField": "pelicula_id",  #
                "foreignField": "_id",
                "as": "pelicula_info"
            }
        },
        {"$unwind": "$pelicula_info"},
        {
            "$lookup": {  #
                "from": "salas",  #
                "localField": "sala_id",  #
                "foreignField": "_id",
                "as": "sala_info"
            }
        },
        {"$unwind": "$sala_info"},
        {
            "$project": {
                "_id": 1,
                "titulo": "$pelicula_info.titulo",  #
                "sala": "$sala_info.nombre",  #
                "fecha": 1,  #
                "hora": 1,  #
                "precio": 1  #
            }
        }
    ]
    resultados = list(db_mongo.funciones.aggregate(pipeline))  #
    return jsonify([serialize_mongo_doc(r) for r in resultados])


@app.route('/mongo/vista/ingresos-por-pelicula', methods=['GET'])
def get_mongo_vista_ingresos_pelicula():
    pipeline = [
        {  # Join Boletos con Funciones
            "$lookup": {  #
                "from": "funciones",  #
                "localField": "funcion_id",  #
                "foreignField": "_id",
                "as": "funcion_info"
            }
        },
        {"$unwind": "$funcion_info"},
        {  # Join con Peliculas
            "$lookup": {  #
                "from": "peliculas",  #
                "localField": "funcion_info.pelicula_id",  #
                "foreignField": "_id",
                "as": "pelicula_info"
            }
        },
        {"$unwind": "$pelicula_info"},
        {  # Calcular ingresos por boleto y agrupar por película
            "$group": {
                "_id": "$pelicula_info.titulo",  #
                "ingresos": {"$sum": {"$multiply": ["$cantidad", "$funcion_info.precio"]}}  #
            }
        },
        {  # Formatear salida
            "$project": {
                "_id": 0,
                "titulo": "$_id",
                "ingresos": 1
            }
        }
    ]
    resultados = list(db_mongo.boletos.aggregate(pipeline))  #
    return jsonify([serialize_mongo_doc(r) for r in resultados])


if __name__ == '__main__':
    # Para crear las tablas SQL la primera vez si no existen (basado en modelos)
    # with app.app_context():
    #     db_sql.create_all()
    app.run(debug=True)