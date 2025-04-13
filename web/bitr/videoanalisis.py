from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify

from bitr.auth import login_required

from .models import User, Eventos, Clubes, Torneos, Sesiones, Jugadores, Jugadores_sesion, Puestos, Divisiones
from bitr import db

from bitr.videoanalisis_funciones import get_nombre_equipo,get_nombre_jugador,get_sesiones_activas,get_video_link,get_nombre_division
import bitr.data_analisis

import pandas as pd

bp = Blueprint('videoanalisis', __name__, url_prefix='/videoanalisis')

#SESIONES (PARTIDOS)

@bp.route('/sesion')
@login_required
def sesion():

    return render_template('bit_videoanalisis/sesiones/sesion.html')

@bp.route('/crear_sesion',  methods=['GET', 'POST'])
@login_required
def crear_sesion():

    clubes = Clubes.query.all()
    torneos = Torneos.query.all()

    if request.method == "POST":
        id_club_local = request.form['dropdown_local']
        id_club_visitante = request.form['dropdown_visitante']
        id_torneo = request.form['dropdown_torneo']
        fecha = request.form['fecha']
        video = request.form['video']

        sesion = Sesiones(id_club_local, id_club_visitante, fecha, id_torneo, video)

        db.session.add(sesion)
        db.session.commit()

        return redirect(url_for('videoanalisis.plantilla', id = sesion.id))

    return render_template('bit_videoanalisis/sesiones/nueva_sesion.html', clubes = clubes, torneos = torneos, get_nombre_division = get_nombre_division)


@bp.route('/sesiones_creadas')
@login_required
def sesiones_creadas():

    sesiones = Sesiones.query.all()

    return render_template('bit_videoanalisis/sesiones/sesiones_creadas.html', sesiones = sesiones, get_nombre_equipo = get_nombre_equipo)


@bp.route('/eliminar_sesion/<int:id>', methods=['GET'])
@login_required
def eliminar_sesion(id):

    sesion = Sesiones.query.get_or_404(id)

    db.session.delete(sesion)
    db.session.commit()

    return redirect(url_for('videoanalisis.sesiones_creadas'))

#PLANTILLA (JUGADORES) DEL PARTIDO

@bp.route('/plantilla/<int:id>', methods = ['GET'])
@login_required
def plantilla(id):

    jugadores = Jugadores.query.all() 

    jugadores_plantilla = Jugadores_sesion.query.filter(Jugadores_sesion.id_sesion == id)     

    return render_template('bit_videoanalisis/plantilla.html', id_sesion = id, opciones = jugadores, jugadores_plantilla = jugadores_plantilla, get_nombre_jugador = get_nombre_jugador)

@bp.route('/actualizar_plantilla', methods = ['POST'])
@login_required
def actualizar_plantilla():

    if request.method == "POST":
        id_jugador = request.form.get('id_jugador')
        id_sesion = request.form.get('id_sesion')
        camiseta = request.form.get('numero_camiseta')

        sesion_jugador = Jugadores_sesion(id_jugador=id_jugador,id_sesion=id_sesion, camiseta=camiseta)

        db.session.add(sesion_jugador)
        db.session.commit()

    return redirect(url_for('videoanalisis.plantilla', id=id_sesion))

@bp.route('/eliminar_jugador_plantilla', methods = ['POST'])
@login_required
def eliminar_jugador_plantilla():

    if request.method == "POST":

        id = request.form.get('id')
        id_plantilla = request.form.get('id_plantilla')

        jugador_plantilla = Jugadores_sesion.query.get_or_404(id_plantilla)

        db.session.delete(jugador_plantilla)
        db.session.commit()

    return redirect(url_for('videoanalisis.plantilla', id=id))

#CREAR Y MODIFICAR JUGADORES

@bp.route('/jugadores', methods=['GET', 'POST'])
@login_required
def jugadores():

    jugadores = Jugadores.query.filter_by(id_club=g.user.id_club)
    puestos = Puestos.query.all()
    divisiones = Divisiones.query.all()

    club = Clubes.query.get(g.user.id_club)

    if request.method == "POST":

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        ano_nacimiento = request.form['ano_nacimiento']
        id_club = club.id
        id_puesto = request.form['id_puesto']

        jugador = Jugadores(nombre=nombre, apellido=apellido, ano_nacimiento=ano_nacimiento, id_club=id_club, id_puesto=id_puesto)

        db.session.add(jugador)
        db.session.commit()

        return redirect(url_for('videoanalisis.jugadores'))

    return render_template('bit_videoanalisis/jugadores.html', club = club, puestos=puestos, jugadores=jugadores, divisiones=divisiones)


@bp.route('/eliminar_jugador/<int:id>', methods=['GET'])
@login_required
def eliminar_jugador(id):

    jugador = Jugadores.query.get_or_404(id)

    db.session.delete(jugador)
    db.session.commit()

    return redirect(url_for('videoanalisis.jugadores'))

