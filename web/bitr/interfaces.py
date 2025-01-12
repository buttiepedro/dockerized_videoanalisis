from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify, send_file

from bitr.auth import login_required

from .models import User, Eventos, Clubes, Torneos, Sesiones, Jugadores, Jugadores_sesion, Puestos, Divisiones
from bitr import db

from bitr.videoanalisis_funciones import get_nombre_equipo,get_nombre_jugador,get_sesiones_activas,get_video_link,get_nombre_division

import bitr.eventos

bp = Blueprint('interfaces', __name__, url_prefix='/interfaces')

@bp.route('/interfaces/<int:id>', methods = ['GET'])
@login_required
def interfaces(id):

    id_utilizado = str(id) in get_sesiones_activas(bitr.eventos.heartbeats)

    #print(f"ID: {id}, ID_UTILIZADOS: {get_sesiones_activas(bitr.eventos.heartbeats)}")

    return render_template('bit_videoanalisis/interfaces/interfaces.html', id = id, id_utilizado = id_utilizado)

@bp.route('/pases/<int:id>', methods = ['GET'])
@login_required
def pases(id):

    jugadores_sesion = Jugadores_sesion.query.filter_by(id_sesion=id).all()

    return(render_template('bit_videoanalisis/interfaces/pases.html', id = id, jugadores_sesion = jugadores_sesion, get_nombre_jugador=get_nombre_jugador))

@bp.route('/video/<int:id>', methods = ['GET'])
@login_required
def video(id):

    return render_template('bit_videoanalisis/interfaces/video.html', id_sesion = id, get_video_link = get_video_link)


@bp.route('/tackle/<int:id>', methods = ["GET"])
@login_required
def tackle(id):

    jugadores_sesion = Jugadores_sesion.query.filter_by(id_sesion=id).all()

    return render_template('bit_videoanalisis/interfaces/tackle.html', id=id, jugadores_sesion = jugadores_sesion, get_nombre_jugador=get_nombre_jugador)

@bp.route('/cortes/<int:id>', methods = ["GET"])
@login_required
def cortes(id):

    return render_template('bit_videoanalisis/interfaces/cortes.html', sesion=id)

@bp.route('/zonas/<int:id>', methods = ["GET"])
@login_required
def zonas(id):

    return render_template('bit_videoanalisis/interfaces/zonas.html', sesion=id)
