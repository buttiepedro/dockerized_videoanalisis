from .models import Clubes, Sesiones, Jugadores, Divisiones, Eventos
from urllib.parse import urlparse, parse_qs
from sqlalchemy import or_
from bitr import db

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


def extraer_video_id(url):
    
    parsed_url = urlparse(url)

    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path.startswith('/watch'):
            # https://www.youtube.com/watch?v=VIDEO_ID
            query = parse_qs(parsed_url.query)
            return query.get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            # https://www.youtube.com/embed/VIDEO_ID
            return parsed_url.path.split('/embed/')[1].split('?')[0]
        
    elif parsed_url.hostname == 'youtu.be':
        # https://youtu.be/VIDEO_ID
        return parsed_url.path.strip('/')
    
    return None


def obtener_segmentos(id_sesion):
    # Filtramos eventos de una sesión y solo los relevantes
    eventos = (
        db.session.query(Eventos)
        .filter(
            Eventos.id_sesion == id_sesion,
            or_(
                Eventos.event.like("inicio_%"),
                Eventos.event.like("finalizacion_%")
            )
        )
        .order_by(Eventos.momento)
        .all()
    )

    # Creamos los segmentos
    segmentos = []
    inicio = None

    print(eventos)
    
    for evento in eventos:
        if evento.event.startswith("inicio_"):
            inicio = evento.momento
            
        elif evento.event.startswith("finalizacion_") and inicio is not None:
            segmentos.append((inicio, evento.momento))
            inicio = None  # reiniciar para el próximo segmento
            
            print(segmentos)

    return segmentos
    