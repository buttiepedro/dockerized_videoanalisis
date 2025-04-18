from flask import Blueprint, render_template
from bitr.auth import login_required

from bitr.videoanalisis_funciones import get_video_link,extraer_video_id, obtener_segmentos

from bitr import db

bp = Blueprint('cortes', __name__, url_prefix='/cortes')

@bp.route('/<int:id>', methods = ["GET"])
@login_required
def cortes(id):

    video_id = extraer_video_id(get_video_link(id))  # extrae el ID puro del video
    segmentos = obtener_segmentos(id)  # retorna lista: [(inicio1, fin1), (inicio2, fin2), ...]
    
    print(segmentos)

    return render_template('bit_videoanalisis/cortes/cortes.html', video_id=video_id, segmentos=segmentos, id_sesion=id)