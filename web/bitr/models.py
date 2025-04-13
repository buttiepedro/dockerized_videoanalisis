from bitr import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = True)
    photo = db.Column(db.String(200))
    id_club = db.Column(db.Integer, db.ForeignKey('clubes.id'), nullable = True)

    def __init__(self, username, password, email = None, photo = None, id_club = None):
        self.username = username
        self.password = password
        self.email = email
        self.photo = photo
        self.id_club = id_club

    def __repr__(self):       
        return (f'<User: {self.username}>')
    

class Clubes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), unique = True, nullable = False)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return (f'<Club: {self.nombre}>')
    
class Puestos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    puesto = db.Column(db.String(50), unique = True, nullable = False)

    def __init__(self, puesto):
        self.puesto = puesto

    def __repr__(self):
        return (f'<Puesto: {self.puesto}>')

class Divisiones(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    division = db.Column(db.String(50), unique = True, nullable = False)

    def __init__(self, division):
        self.division = division

    def __repr__(self):
        return (f'<Division: {self.division}>')

class Jugadores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), unique = True, nullable = False)
    apellido = db.Column(db.String(50), unique = True, nullable = False)
    ano_nacimiento = db.Column(db.Integer, unique = False, nullable = False)
    id_club = db.Column(db.Integer, db.ForeignKey('clubes.id'), nullable = True)
    id_puesto = db.Column(db.Integer, db.ForeignKey('puestos.id'), nullable = True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)

    def __init__(self, nombre, apellido, id_club, id_puesto, id_user = None, ano_nacimiento = None):
        self.nombre = nombre
        self.apellido = apellido
        self.id_club = id_club
        self.ano_nacimiento = ano_nacimiento
        self.id_puesto = id_puesto
        self.id_user = id_user

    def __repr__(self):
        return (f'<Jugador: {self.nombre} {self.apellido}>')

class Torneos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_division = db.Column(db.Integer, db.ForeignKey('divisiones.id'), nullable = True)
    nombre = db.Column(db.String(100), nullable = False)

    def __init__(self, nombre, id_division):
        self.nombre = nombre
        self.id_division = id_division

    def __repr__(self):
        return (f"<Torneo: {self.nombre}>")

class Sesiones(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_club_local = db.Column(db.Integer, db.ForeignKey('clubes.id'), nullable = True)
    id_club_visitante = db.Column(db.Integer, db.ForeignKey('clubes.id'), nullable = True)
    fecha = db.Column(db.Date, unique = False, nullable = False)
    id_torneo = db.Column(db.Integer, db.ForeignKey('torneos.id'), nullable = True)
    video = db.Column(db.String(250), unique = True)

    def __init__(self, id_club_local, id_club_visitante, fecha, id_torneo ,video):
        self.id_club_local = id_club_local
        self.id_club_visitante = id_club_visitante
        self.fecha = fecha
        self.id_torneo = id_torneo
        self.video = video

    def __repr__(self):
        return (f'<Partido: {self.fecha}, {self.id_club_local} vs {self.id_club_visitante}>')

class Jugadores_sesion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    camiseta = db.Column(db.Integer, nullable = True)
    id_jugador = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable = True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesiones.id'), nullable = True)

    def __init__(self, id_jugador, id_sesion, camiseta):
        self.camiseta = camiseta
        self.id_jugador = id_jugador
        self.id_sesion = id_sesion

    def __repr__(self):
        return (f'<Sesion: {self.id_sesion}, Jugador {self.id_jugador}>')

class Eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(50), nullable = False)
    id_jugador = db.Column(db.Integer, db.ForeignKey('jugadores.id'), nullable = True)
    id_sesion = db.Column(db.Integer, db.ForeignKey('sesiones.id'), nullable = False)
    momento = db.Column(db.Float, nullable = False)

    def __init__(self, event = "Unknown", id_sesion = None, momento = None, id_jugador=None):
        self.event = event
        self.id_sesion = id_sesion
        self.id_jugador = id_jugador
        self.momento = momento

    def __repr__(self):       
        return (f'<Evento: {self.event}, Momento: {self.momento}>')