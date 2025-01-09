from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify, send_file

from bitr.auth import login_required

from .models import User, Eventos, Clubes, Torneos, Sesiones, Jugadores, Jugadores_sesion, Puestos, Divisiones
from bitr import db

from bitr.videoanalisis_funciones import get_nombre_equipo,get_nombre_jugador,get_sesiones_activas,get_video_link,get_nombre_division
import bitr.data_analisis

import pandas as pd

bp = Blueprint('dashboards', __name__, url_prefix='/dashboards')

#VISTAS

@bp.route('/tackles/<int:id>', methods=['GET'])
@login_required
def tackles(id):

    return render_template('bit_videoanalisis/datos/tackles.html', sesion = id)

#GRAFICOS

@bp.route('/tackles_pie/<int:id>', methods=['GET'])
@login_required
def tackles_pie(id):

    plot = bitr.data_analisis.tackle_efectividad(id)

    return send_file(plot, mimetype='image/png', as_attachment=False)

@bp.route('/tackles_distr/<int:id>', methods=['GET'])
@login_required
def tackles_distr(id):

    plot = bitr.data_analisis.tackle_distribucion(id)

    return send_file(plot, mimetype='image/png', as_attachment=False)

@bp.route('/tackles_jugador/<int:id>', methods=['GET'])
@login_required
def tackles_jugador(id):

    plot = bitr.data_analisis.tackle_jugadores(id)

    return send_file(plot, mimetype='image/png', as_attachment=False)