from flask import Blueprint, render_template, request, jsonify
from bitr.auth import login_required

from bitr.videoanalisis_funciones import get_video_link,extraer_video_id, obtener_segmentos

from bitr import db

bp = Blueprint('cortes', __name__, url_prefix='/cortes')

@bp.route('/<int:id>', methods = ["GET"])
@login_required
def cortes(id):

    return render_template('bit_videoanalisis/cortes/elegir_cortes.html', id=id)

@bp.route('lines/<int:id>', methods = ["GET"])
@login_required
def lines(id):

    return render_template('bit_videoanalisis/cortes/lines.html', id=id)

@bp.route('scrums/<int:id>', methods = ["GET"])
@login_required
def scrums(id):

    return render_template('bit_videoanalisis/cortes/scrums.html', id=id)

@bp.route('/line_cortes/<int:id>', methods = ["GET","POST"])
@login_required
def line_cortes(id):

    tipo = request.form.get("tipo")

    tipo = "line_"+tipo

    segmentos = obtener_segmentos(id,tipo)
    video_id = extraer_video_id(get_video_link(id))

    return render_template('bit_videoanalisis/cortes/cortes.html', id=id, tipo=tipo, segmentos=segmentos, video_id=video_id)

@bp.route('/scrum_cortes/<int:id>', methods = ["GET","POST"])
@login_required
def scrum_cortes(id):

    tipo = request.form.get("tipo")
    
    tipo = "scrum_"+tipo

    segmentos = obtener_segmentos(id,tipo)
    video_id = extraer_video_id(get_video_link(id))

    return render_template('bit_videoanalisis/cortes/cortes.html', id=id, tipo=tipo, segmentos=segmentos, video_id=video_id)