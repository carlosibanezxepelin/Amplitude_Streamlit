# Librerías
import streamlit as st
import pandas as pd
from google.cloud import bigquery
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title=f"Amplitude events in Xepelin",
    page_icon=":memo:",
    initial_sidebar_state="expanded",
    layout="wide",
)


########### Config BQ
client = bigquery.Client()
project_id = "xepelin-ds-prod"

query = """
  WITH amplitude as (
SELECT 
  CAST(amplitudeId AS INT64) amplitudeId,
  CAST(sessionId AS INT64) sessionId,
  REPLACE(JSON_EXTRACT(eventProperties, "$.country_id"), '"', "") countryId,
  eventType,
  CAST(eventTime AS TIMESTAMP) eventTime,
  eventProperties,
  groupProperties, 
  userProperties
  FROM xepelin-ds-prod.prod_staging_amplitude.Amplitude
  --ORDER BY amplitudeId, sessionId, eventTime
)
SELECT * 
FROM amplitude
LIMIT 1000000
"""

# df = client.query(query).to_dataframe()
df = pd.read_csv("/Users/carlos.ibanez/Downloads/amplitude_events.csv")
df = df.sort_values(by=["amplitudeId", "sessionId"], ascending=[False, False])

# Data cleaning
df = df.dropna(subset=['eventTime'])


# Convertir la columna 'eventTime' a formato de fecha y hora
df["eventTime"] = pd.to_datetime(df["eventTime"], errors="coerce")

# Verificar si hay algún valor nulo después de la conversión
null_values = df["eventTime"].isnull().sum()
if null_values > 0:
    st.write(
        f"Se encontraron {null_values} valores nulos en la columna 'eventTime' después de la conversión."
    )

# Continuar con los siguientes pasos solo si no hay valores nulos


st.dataframe(df)

############ State of Amplitude
st.title("State of Users")

st.write("Eventos disponibles en producción: ", "117")
st.write("Eventos utilizados: ", df["eventType"].nunique())

st.write("Usuarios: ", df["amplitudeId"].nunique())
st.write("Sesiones: ", df["sessionId"].nunique())

# Agrupar por 'amplitudeId' y contar las sesiones únicas para cada usuario
sessions_per_user = df.groupby("amplitudeId")["sessionId"].nunique()

# Calcular la media y la mediana de sesiones por usuario
average_sessions_per_user = sessions_per_user.mean().round(2)
median_sessions_per_user = sessions_per_user.median()

st.write("Un usuario inicia sesión: ", average_sessions_per_user, "en promedio")
st.write("Un usuario inicia sesión: ", median_sessions_per_user, "en mediana")


# Agrupar por 'amplitudeId' y 'sessionId', y calcular el tiempo de inicio y fin por sesison
session_times = df.groupby(["amplitudeId", "sessionId"])["eventTime"].agg(
    ["min", "max"]
)

# Calcular la duración de cada sesión
session_times["duration"] = session_times["max"] - session_times["min"]

# Ordenar los resultados por usuario y por tiempo de inicio de sesión
session_times = session_times.sort_values(by=["amplitudeId", "min"])

# Filtrar para obtener solo la primera sesión de cada usuario
first_sessions = session_times.groupby("amplitudeId").first()

# Calcular la duración promedio y la mediana de las primeras sesiones
average_duration = first_sessions["duration"].mean()
median_duration = first_sessions["duration"].median()

st.write("Duración promedio de la primera sesión:", average_duration)
st.write("Duración mediana de la primera sesión:", median_duration)

# Agrupar por 'amplitudeId' y 'sessionId', y calcular el tiempo de inicio y fin de cada sesión
session_times_all = df.groupby(["amplitudeId", "sessionId"])["eventTime"].agg(
    ["min", "max"]
)

# Calcular la duración de cada sesión
session_times_all["duration"] = session_times_all["max"] - session_times_all["min"]

# Calcular la duración promedio y la mediana de todas las sesiones
average_duration_all = session_times_all["duration"].mean()
median_duration_all = session_times_all["duration"].median()

# Mostrar los resultados en Streamlit
st.write("Duración promedio de la sesión:", average_duration_all)
st.write("Duración mediana de la sesión:", median_duration_all)


# Contar las ocurrencias de cada tipo de evento
event_type_counts = df["eventType"].value_counts()

# Seleccionar los 20 eventos con más interacciones y ordenarlos de mayor a menor
top_events = event_type_counts.head(20).sort_values(ascending=False)

# Seleccionar los 20 eventos con menos interacciones y ordenarlos de menor a mayor
lowest_events = event_type_counts.tail(20).sort_values(ascending=True)

# Mostrar el gráfico de barras para los eventos con más interacciones
st.write("Eventos con más interacciones: ")
st.bar_chart(top_events)

# Mostrar el gráfico de barras para los eventos con menos interacciones
st.write("Eventos con menos interacciones: ")
st.bar_chart(lowest_events)


############# Filtro de mes

import calendar
df = df.dropna(subset=['eventTime'])
df['month'] = df['eventTime'].dt.month.astype(int)

# Añadir una columna con los nombres de los meses
df['month_name'] = df['month'].apply(lambda x: calendar.month_name[x])

# Obtener los meses únicos y luego ordenarlos según el orden natural de los meses
unique_months = df['month_name'].unique()
unique_months = sorted(unique_months, key=lambda x: list(calendar.month_name).index(x))

# Agregar la opción de 'Todos los meses' al principio de la lista de meses
month_options = ['Todos los meses'] + list(calendar.month_name)[1:]
selected_month_name = st.selectbox('Selecciona un mes', month_options)


################### Gráfico horas pico
if selected_month_name != 'Todos los meses':
    filtered_df = df[df['month_name'] == selected_month_name]
else:
    filtered_df = df.copy()  # Usar .copy() para evitar SettingWithCopyWarning

# Extraer la hora de cada evento en el DataFrame filtrado
filtered_df["hour"] = filtered_df["eventTime"].dt.hour
peak_hours = filtered_df["hour"].value_counts().sort_index()

# Mostrar las Horas Pico en Streamlit
st.write(f"Horas Pico para {selected_month_name}")
st.bar_chart(peak_hours)


################# Gráfico días pico (1 a 31)
# Extraer el día de cada evento
df["day"] = df["eventTime"].dt.day

# Días pico
peak_days = df["day"].value_counts().sort_index()

# Mostrar los días pico en Streamlit
st.write("Días Pico")
st.bar_chart(peak_days)

################# Gráfico días de la semana pico (Lunes a domingo)
# Extraer el día de la semana (0 = lunes, 6 = domingo)
df["day_of_week"] = df["eventTime"].dt.dayofweek

days = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}
df["day_name"] = df["day_of_week"].apply(lambda x: days.get(x, "Desconocido"))

# Calcular los días pico
peak_days = df["day_name"].value_counts().sort_index()

# Mostrar los Días Pico en Streamlit
st.write("Días Pico de la semana")
st.bar_chart(peak_days)
