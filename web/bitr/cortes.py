from flask import Blueprint, render_template
from bitr.auth import login_required

from bitr.videoanalisis_funciones import get_video_link,extraer_video_id, obtener_segmentos

from bitr import db

bp = Blueprint('cortes', __name__, url_prefix='/cortes')

@bp.route('/<int:id>', methods = ["GET"])
@login_required
def cortes(id):

    return render_template('bit_videoanalisis/cortes/elegir_cortes.html', id=id)

@bp.route('/lines/<int:id>', methods = ["GET"])
@login_required
def lines(id):

    return render_template('bit_videoanalisis/cortes/lines.html', id=id)

@bp.route('/scrums/<int:id>', methods = ["GET"])
@login_required
def scrums(id):

    return render_template('bit_videoanalisis/cortes/scrums.html', id=id)