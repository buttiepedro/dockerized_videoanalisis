import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

from .models import User, Eventos, Clubes, Torneos, Sesiones, Jugadores, Jugadores_sesion, Puestos, Divisiones

def tackle_efectividad(id_sesion):

    eventos = Eventos.query.filter_by(id_sesion=id_sesion).all()

    df = pd.DataFrame([{
        'id': evento.id,
        'event': evento.event,
        'id_jugador': evento.id_jugador,
        'id_sesion': evento.id_sesion,
        'momento': evento.momento
    } for evento in eventos])

    plot = tackle_efectividad_plot(df)

    return plot

def tackle_efectividad_plot(df):

    # Contar tackles positivos y errados
    tackle_counts = df["event"].value_counts()
    tackle_data = {
        "Tackles errados": tackle_counts.get("tackle_errado", 0),
        "Tackles concretados": tackle_counts.get("tackle_positivo", 0)
    }

    fig, ax = plt.subplots(figsize=(6, 6))

    # Añadir porcentaje y cantidad en el gráfico
    total_tackles = sum(tackle_data.values())
    wedges, texts, autotexts = ax.pie(
        tackle_data.values(),
        labels=tackle_data.keys(),
        autopct=lambda p: f"{int(round(p * total_tackles / 100))} ({p:.1f}%)",
        colors=["red", "green"],
        startangle=90,
        textprops={"fontsize": 10}
    )

    # Mejorar la visibilidad del texto dentro del gráfico
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_weight("bold")

    # Guardar la imagen en un objeto BytesIO
    image = BytesIO()
    fig.savefig(image, format='png', bbox_inches='tight')
    image.seek(0)

    return image


def tackle_distribucion(id_sesion):

    eventos = Eventos.query.filter_by(id_sesion=id_sesion).all()

    df = pd.DataFrame([{
        'id': evento.id,
        'event': evento.event,
        'id_jugador': evento.id_jugador,
        'id_sesion': evento.id_sesion,
        'momento': evento.momento
    } for evento in eventos])

    plot = tackle_distribucion_plot(df)

    return plot


def tackle_distribucion_plot(df):

    # Filtrar eventos específicos
    df_filtered = df[df["event"].isin(["tackle_positivo", "tackle_errado"])]
    df_filtered["momento"] = (df_filtered["momento"] // 60).astype(int)
    df_filtered["event"] = df_filtered["event"].replace({"tackle_positivo": "Tackle concretado", "tackle_errado" : "Tackle errado"})

    # Crear una tabla pivot para contar eventos por momento
    pivot_table = df_filtered.pivot_table(
        index="momento",
        columns="event",
        aggfunc="size",
        fill_value=0
    )

    # Graficar eventos por momento
    fig, ax = plt.subplots(figsize=(10, 6))

    pivot_table.plot(kind="bar", stacked=True, ax=ax, color={"Tackle concretado": "green", "Tackle errado": "red"})

    ax.set_xlabel("Momento", fontsize=12)
    ax.set_ylabel("Tackles", fontsize=12)
    ax.legend(title="Tipo de Evento")

    # Guardar la imagen en un objeto BytesIO
    image = BytesIO()
    fig.savefig(image, format='png', bbox_inches='tight')
    image.seek(0)

    return image

def tackle_jugadores(id_sesion):

    eventos = Eventos.query.filter_by(id_sesion=id_sesion).all()

    df = pd.DataFrame([{
        'id': evento.id,
        'event': evento.event,
        'id_jugador': evento.id_jugador,
        'id_sesion': evento.id_sesion,
        'momento': evento.momento
    } for evento in eventos])

    jugadores_ids = df['id_jugador'].dropna().tolist()
    jugadores = Jugadores.query.filter(Jugadores.id.in_(jugadores_ids)).all()

    df_jugadores= pd.DataFrame([{
        'id': jugador.id,
        'nombre': jugador.nombre + " " + jugador.apellido,
    } for jugador in jugadores])

    plot = tackle_jugadores_plot(df, df_jugadores)

    return plot

def tackle_jugadores_plot(df, df_jugadores):
    # Filtrar eventos específicos
    df_filtered = df[df["event"].isin(["tackle_positivo", "tackle_errado"])]  # Cambio aquí
    df_filtered["event"] = df_filtered["event"].replace({"tackle_positivo": "Tackle concretado", "tackle_errado" : "Tackle errado"})

    # Crear una tabla pivot para contar eventos por jugador
    pivot_table = df_filtered.pivot_table(
        index="id_jugador",
        columns="event",
        aggfunc="size",
        fill_value=0
    )

    jugadores_dict = df_jugadores.set_index('id')['nombre'].to_dict()  # Asumiendo que la columna con el nombre del jugador se llama 'nombre'
    pivot_table.index = pivot_table.index.map(jugadores_dict)

    # Graficar eventos por jugador
    fig, ax = plt.subplots(figsize=(10, 6))

    pivot_table.plot(kind="bar", ax=ax, color={"Tackle concretado": "green", "Tackle errado": "red"})  # Cambio aquí

    ax.set_xlabel("Jugador", fontsize=12)
    ax.set_ylabel("Cantidad de Tackles", fontsize=12)
    ax.legend(title="Tipo de Evento")

    # Mejorar la visibilidad de los nombres de los jugadores en el eje X
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    for container in ax.containers:
        ax.bar_label(container, label_type="edge", fontsize=10, color="black", padding=3)

    # Guardar la imagen en un objeto BytesIO
    image = BytesIO()
    fig.savefig(image, format='png', bbox_inches='tight')
    image.seek(0)

    return image