import streamlit as st
import pandas as pd

st.set_page_config(
    page_title=f"Amplitude events in Xepelin",
    page_icon="☞",
)

st.title("Amplitude Monitoring")

st.sidebar.success("Selecciona una página de arriba")

st.markdown(
    """
    Amplitude Monitoring es una App en donde puedes monitorear y obtener insights a través del comportamiento del usuario.
    **👈 Selecciona una de las siguientes secciones en el sidebar para comenzar el análisis**
    ### Secciones:
    - Amplitude 
      - Eventos más utilizados por el usuario, retención y horas pico.
    - Payments **AP**
      - Cantidad de facturas promedio un usuario envía antes de revisión en Payments, Carrito vacío.
    - PF & PP **AR**
      - Cantidad de facturas promedio un usuario envía antes de revisión en Financiamiento Directo y Pronto Pago, Carrito vacío.
    - Onboarding **PG**
      - Onboarding del usuario, registro y login.
    - Revisa nuestra documentación en Notion
        - [Amplitude](https://www.notion.so/xepelin/Amplitude-f6877dd93e17443f8bf1ea8baaf69b72) **Author: BI & Analytics**
        - [EDA](https://www.notion.so/xepelin/Amplitude-7439b912b5114de2a9b2e6c8781d5a5e) **Author: BI & Analytics**
    ### Vistas Adicionales
    - Nodos [streamlit.io](https://google.com)
      - ¿Cómo se relacionan los eventos de nuestros usuarios?
    - Asociación [streamlit.io](https://google.com)
      - ¿Cuál es el Customer Journey de nuestros usuarios? ¿Cuál es su Canasta?
    ### Más info
    - Consultar en nuestro canal de BI & Analytics en Slack
"""
)

st.markdown(
    """
    # Documentación
    
"""
)
