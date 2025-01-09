from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import functools

from .models import User
from bitr import db 

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/inicio', methods = ('GET', 'POST'))
def login():

    if request.method ==  'POST':

        username = request.form['username']
        password = request.form['password']

        error = None

        #Validar los datos del usuario ingresado
        user = User.query.filter_by(username=username).first()

        if (user == None):
            error = 'El nombre de usuario es incorrecto'

        elif not check_password_hash(user.password, password):
            error = 'La contraseña es incorrecta'

        #Iniciar sesion
        if (error == None):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/inicio_sesion.html')

#Funcion que se ejecuta en cada peticion, verifica si hay una sesion iniciada
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

@bp.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('index'))

#Funcion que chequea si esta iniciada la sesion y devuelve la vista solicitada si esta iniciada y la vista de login si no lo esta
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return(view(**kwargs))
    return wrapped_view


@bp.route('/perfil/<int:id>', methods = ('GET', 'POST'))
@login_required
def perfil(id):

    user = User.query.get_or_404(id)

    if request.method == 'POST':

        user.email = request.form.get('email')

        password = request.form.get('password')

        error = None
        if (len(password) > 0 and len(password) < 6) or len(password) > 25:
            error = 'La contraseña debe contener entre 6 y 25 caracteres'
        elif len(password) == 0:
            user.password = user.password
        else:
            user.password = generate_password_hash(password)
        
        if request.files['photo']:

            photo = request.files['photo']
            photo.save(f'bitr/static/media/{secure_filename(photo.filename)}')
            user.photo = (f'media/{secure_filename(photo.filename)}')

        if error is not None:
            flash(error)
        else:
            db.session.commit()
            return(redirect(url_for('auth.perfil', id = user.id)))

        flash(error)

    return render_template('auth/perfil.html', user = user)