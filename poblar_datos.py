import random
import datetime
from decimal import Decimal
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from pymongo import MongoClient
from bson import ObjectId

# --- Configuración ---
NUM_PELICULAS = 5000
NUM_SALAS = 50  # Menos salas es más realista
NUM_CLIENTES = 5000
NUM_FUNCIONES = 5000  # Podrían ser más si quieres más variedad
NUM_BOLETOS = 5000

# --- Configuración de Conexión SQL (MySQL) ---
# !!! AJUSTA ESTAS CREDENCIALES !!!
DB_USER_SQL = "root"
DB_PASSWORD_SQL = "1234"  # Tu contraseña de MySQL o la que corresponda
DB_HOST_SQL = "localhost"
DB_NAME_SQL = "proyectoCine"
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER_SQL}:{DB_PASSWORD_SQL}@{DB_HOST_SQL}/{DB_NAME_SQL}'

# --- Configuración de Conexión MongoDB ---
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "proyectoCineMongo"

# --- Inicializar Faker ---
fake = Faker(['es_ES', 'en_US'])  # Para generar datos en español e inglés

# --- Modelos SQLAlchemy (similares a los de tu app.py) ---
Base = declarative_base()


class PeliculaSQL(Base):
    __tablename__ = 'Pelicula'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100))
    genero = Column(String(50))
    duracion = Column(Integer)
    clasificacion = Column(String(10))
    idioma = Column(String(50))
    funciones = relationship('FuncionSQL', backref='pelicula')


class SalaSQL(Base):
    __tablename__ = 'Sala'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    capacidad = Column(Integer)
    tipo = Column(String(50))
    funciones = relationship('FuncionSQL', backref='sala')


class ClienteSQL(Base):
    __tablename__ = 'Cliente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    correo = Column(String(100))
    telefono = Column(String(20))  # Definido como VARCHAR(20) en tu schema
    boletos = relationship('BoletoSQL', backref='cliente')


class FuncionSQL(Base):
    __tablename__ = 'Funcion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pelicula_id = Column(Integer, ForeignKey('Pelicula.id'))
    sala_id = Column(Integer, ForeignKey('Sala.id'))
    fecha = Column(Date)
    hora = Column(Time)
    precio = Column(Numeric(6, 2))
    boletos = relationship('BoletoSQL', backref='funcion')


class BoletoSQL(Base):
    __tablename__ = 'Boleto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('Cliente.id'))
    funcion_id = Column(Integer, ForeignKey('Funcion.id'))
    cantidad = Column(Integer)
    fecha_compra = Column(DateTime, default=datetime.datetime.utcnow)


# --- Conexiones a Bases de Datos ---
# SQL
sql_engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionSQL = sessionmaker(bind=sql_engine)
sql_session = SessionSQL()

# MongoDB
mongo_client = MongoClient(MONGO_URI)
db_mongo = mongo_client[MONGO_DB_NAME]


# --- Funciones de Generación de Datos ---

def generar_peliculas(cantidad):
    peliculas_sql_objs = []
    peliculas_mongo_docs = []
    generos = ["Acción", "Comedia", "Drama", "Ciencia Ficción", "Terror", "Suspenso", "Animación", "Documental",
               "Romance"]
    clasificaciones = ["G", "PG", "PG-13", "R", "NC-17", "ATP", "SAM13", "SAM16", "SAM18"]
    idiomas = ["Español", "Inglés", "Francés", "Japonés", "Coreano"]

    for _ in range(cantidad):
        titulo = fake.catch_phrase() + " " + fake.word().capitalize()
        g = random.choice(generos)
        dur = random.randint(70, 220)
        clas = random.choice(clasificaciones)
        idio = random.choice(idiomas)

        peliculas_sql_objs.append(PeliculaSQL(titulo=titulo, genero=g, duracion=dur, clasificacion=clas, idioma=idio))
        peliculas_mongo_docs.append(
            {"titulo": titulo, "genero": g, "duracion": dur, "clasificacion": clas, "idioma": idio})
    return peliculas_sql_objs, peliculas_mongo_docs


def generar_salas(cantidad):
    salas_sql_objs = []
    salas_mongo_docs = []
    tipos_sala = ["2D", "3D", "IMAX", "4DX", "VIP"]
    for i in range(cantidad):
        nombre = f"Sala {i + 1} {random.choice(tipos_sala)}"
        cap = random.randint(50, 250)
        tipo_s = random.choice(tipos_sala)

        salas_sql_objs.append(SalaSQL(nombre=nombre, capacidad=cap, tipo=tipo_s))
        salas_mongo_docs.append({"nombre": nombre, "capacidad": cap, "tipo": tipo_s})
    return salas_sql_objs, salas_mongo_docs


def generar_clientes(cantidad):
    clientes_sql_objs = []
    clientes_mongo_docs = []
    for _ in range(cantidad):
        nombre = fake.name()
        correo = fake.email()
        telefono_generado = fake.phone_number()
        telefono = telefono_generado[:20]  # <--- MODIFICACIÓN AQUÍ: Acortar a 20 caracteres

        clientes_sql_objs.append(ClienteSQL(nombre=nombre, correo=correo, telefono=telefono))
        clientes_mongo_docs.append(
            {"nombre": nombre, "correo": correo, "telefono": telefono})  # Usamos el teléfono acortado
    return clientes_sql_objs, clientes_mongo_docs


def generar_funciones(cantidad, peliculas_sql_ids, salas_sql_ids, peliculas_mongo_ids, salas_mongo_ids):
    funciones_sql_objs = []
    funciones_mongo_docs = []
    for _ in range(cantidad):
        if not peliculas_sql_ids or not salas_sql_ids or not peliculas_mongo_ids or not salas_mongo_ids: continue

        pelicula_id_sql = random.choice(peliculas_sql_ids)
        sala_id_sql = random.choice(salas_sql_ids)
        pelicula_id_mongo = random.choice(peliculas_mongo_ids)
        sala_id_mongo = random.choice(salas_mongo_ids)

        fecha = fake.date_between(start_date="-30d", end_date="+90d")
        hora_obj = fake.time_object()
        precio = Decimal(random.uniform(5.0, 25.0)).quantize(Decimal("0.01"))

        funciones_sql_objs.append(
            FuncionSQL(pelicula_id=pelicula_id_sql, sala_id=sala_id_sql, fecha=fecha, hora=hora_obj, precio=precio))
        funciones_mongo_docs.append({
            "pelicula_id": pelicula_id_mongo,
            "sala_id": sala_id_mongo,
            "fecha": datetime.datetime(fecha.year, fecha.month, fecha.day),
            "hora": hora_obj.strftime("%H:%M"),
            "precio": float(precio)
        })
    return funciones_sql_objs, funciones_mongo_docs


def generar_boletos(cantidad, clientes_sql_ids, funciones_sql_ids, clientes_mongo_ids, funciones_mongo_ids):
    boletos_sql_objs = []
    boletos_mongo_docs = []
    for _ in range(cantidad):
        if not clientes_sql_ids or not funciones_sql_ids or not clientes_mongo_ids or not funciones_mongo_ids: continue

        cliente_id_sql = random.choice(clientes_sql_ids)
        funcion_id_sql = random.choice(funciones_sql_ids)
        cliente_id_mongo = random.choice(clientes_mongo_ids)
        funcion_id_mongo = random.choice(funciones_mongo_ids)

        cant = random.randint(1, 6)
        fecha_compra_dt = fake.date_time_between(start_date="-60d", end_date="now")

        boletos_sql_objs.append(BoletoSQL(cliente_id=cliente_id_sql, funcion_id=funcion_id_sql, cantidad=cant,
                                          fecha_compra=fecha_compra_dt))
        boletos_mongo_docs.append({
            "cliente_id": cliente_id_mongo,
            "funcion_id": funcion_id_mongo,
            "cantidad": cant,
            "fecha_compra": fecha_compra_dt
        })
    return boletos_sql_objs, boletos_mongo_docs


# --- Lógica Principal de Inserción ---
try:
    Base.metadata.create_all(sql_engine)

    print(f"Generando {NUM_PELICULAS} películas...")
    peliculas_s, peliculas_m = generar_peliculas(NUM_PELICULAS)
    sql_session.add_all(peliculas_s)
    sql_session.commit()
    print("Películas SQL insertadas.")
    peliculas_sql_ids = [p.id for p in sql_session.query(PeliculaSQL.id).all()]
    if peliculas_m:
        result_m_pel = db_mongo.peliculas.insert_many(peliculas_m)
        peliculas_mongo_ids = result_m_pel.inserted_ids
        print("Películas MongoDB insertadas.")
    else:
        peliculas_mongo_ids = []

    print(f"Generando {NUM_SALAS} salas...")
    salas_s, salas_m = generar_salas(NUM_SALAS)
    sql_session.add_all(salas_s)
    sql_session.commit()
    print("Salas SQL insertadas.")
    salas_sql_ids = [s.id for s in sql_session.query(SalaSQL.id).all()]
    if salas_m:
        result_m_sal = db_mongo.salas.insert_many(salas_m)
        salas_mongo_ids = result_m_sal.inserted_ids
        print("Salas MongoDB insertadas.")
    else:
        salas_mongo_ids = []

    print(f"Generando {NUM_CLIENTES} clientes...")
    clientes_s, clientes_m = generar_clientes(NUM_CLIENTES)
    sql_session.add_all(clientes_s)
    sql_session.commit()
    print("Clientes SQL insertados.")
    clientes_sql_ids = [c.id for c in sql_session.query(ClienteSQL.id).all()]
    if clientes_m:
        result_m_cli = db_mongo.clientes.insert_many(clientes_m)
        clientes_mongo_ids = result_m_cli.inserted_ids
        print("Clientes MongoDB insertados.")
    else:
        clientes_mongo_ids = []

    print(f"Generando {NUM_FUNCIONES} funciones...")
    funciones_s, funciones_m = generar_funciones(NUM_FUNCIONES, peliculas_sql_ids, salas_sql_ids, peliculas_mongo_ids,
                                                 salas_mongo_ids)
    if funciones_s:
        sql_session.add_all(funciones_s)
        sql_session.commit()
        print("Funciones SQL insertadas.")
    funciones_sql_ids = [f.id for f in sql_session.query(FuncionSQL.id).all()]
    if funciones_m:
        result_m_fun = db_mongo.funciones.insert_many(funciones_m)
        funciones_mongo_ids = result_m_fun.inserted_ids
        print("Funciones MongoDB insertadas.")
    else:
        funciones_mongo_ids = []

    print(f"Generando {NUM_BOLETOS} boletos...")
    boletos_s, boletos_m = generar_boletos(NUM_BOLETOS, clientes_sql_ids, funciones_sql_ids, clientes_mongo_ids,
                                           funciones_mongo_ids)
    if boletos_s:
        batch_size = 500
        for i in range(0, len(boletos_s), batch_size):
            sql_session.add_all(boletos_s[i:i + batch_size])
            sql_session.commit()
        print("Boletos SQL insertados.")
    if boletos_m:
        db_mongo.boletos.insert_many(boletos_m)
        print("Boletos MongoDB insertados.")

    print("\n¡Bases de datos pobladas exitosamente!")

except Exception as e:
    sql_session.rollback()
    print(f"Ocurrió un error: {e}")
    import traceback

    traceback.print_exc()
finally:
    sql_session.close()
    mongo_client.close()