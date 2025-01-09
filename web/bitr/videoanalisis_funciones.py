from .models import Clubes, Sesiones, Jugadores, Divisiones

def get_nombre_equipo(id):

    equipo =  Clubes.query.get(id)

    if equipo:
        return equipo.nombre
    else:
        return 'Desconocido'
    
def get_nombre_jugador(id):

    jugador =  Jugadores.query.get(id)

    if jugador:
        return f"{jugador.nombre} {jugador.apellido}"
    else:
        return 'Desconocido'
    
def get_nombre_division(id):

    division =  Divisiones.query.get(id)

    if division:
        return f"{division.division}"
    else:
        return 'Desconocido'

def get_video_link(id):

    sesion =  Sesiones.query.get(id)

    link = sesion.video

    if link:
        return link
    else:
        return 'Desconocido'
    
def get_sesiones_activas(heartbeats):

    return list(heartbeats.keys())