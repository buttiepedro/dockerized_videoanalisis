from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify, send_file

from bitr.auth import login_required

from .models import User, Eventos, Clubes, Torneos, Sesiones, Jugadores, Jugadores_sesion, Puestos, Divisiones
from bitr import db

from bitr.videoanalisis_funciones import get_nombre_equipo,get_nombre_jugador,get_sesiones_activas,get_video_link,get_nombre_division

bp = Blueprint('eventos', __name__, url_prefix='/eventos')

heartbeats = dict()

@bp.route('/register_heartbeat', methods=['POST'])
@login_required
def register_heartbeat():

    if request.method == "POST":

        data = request.json
        timestamp = data.get('timestamp', 0)
        sesion = data.get('sesion')

        heartbeats.update({sesion:timestamp})
        
        print(heartbeats)
    
    return jsonify({"status": "success", "message": "Event registered!"}), 201

@bp.route('/remove_sesion/<int:id>', methods=['POST'])
@login_required
def remove_sesion(id):

    if id in heartbeats:

        del heartbeats[id]
        print(f"Session {id} removed.")
        print(heartbeats)
        return jsonify({"status": "success"}), 200
    
    else:

        return jsonify({"status": "session not found"}), 404

@bp.route('/register_event', methods = ['POST'])
@login_required
def register_event():


    if request.method == 'POST':
        id_sesion = request.form['sesion']
        event = request.form['event']
        id_jugador = request.form['jugador']

        url = request.form['url']

        evento = Eventos(event = event, id_sesion = id_sesion, id_jugador = id_jugador, momento = heartbeats.get(int(id_sesion),"error"))

        #print(evento)

        db.session.add(evento)
        db.session.commit()

        return redirect(url)
    
    return(redirect(url_for('videoanalisis.sesiones_creadas')))

@bp.route('/register_event_noplayer', methods = ['POST'])
@login_required
def register_event_noplayer():

    if request.method == 'POST':

        data = request.get_json()

        event = data.get('event')
        sesion = data.get('sesion')

        registro = Eventos(id_sesion=sesion, event=event, momento = heartbeats.get(int(sesion),"error"))

        #print(registro)

        db.session.add(registro)
        db.session.commit()        

        return jsonify({"success": True, "state": event, "sesion": sesion})

    return jsonify({"succes": False})