import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Compensación de Reactivos",
    page_icon="⚡",
    layout="wide"
)

# Título principal
st.title("⚡ Calculadora de Compensación de Reactivos")
st.markdown("---")

# Sidebar para navegación
st.sidebar.title("Navegación")
seccion = st.sidebar.selectbox(
    "Seleccionar sección:",
    ["Inicio", "Compensación Paralelo", "Compensación Serie", "Resultados"]
)

if seccion == "Inicio":
    st.header("Bienvenido a la Calculadora de Compensación de Reactivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Información del Proyecto")
        st.info("""
        Esta aplicación permite calcular la compensación de reactivos en sistemas eléctricos
        utilizando diferentes métodos:
        - Compensación en paralelo (más común)
        - Compensación en serie
        - Compensación inductiva o capacitiva
        """)
        
        st.subheader("🎯 Objetivos")
        st.success("""
        - Mejorar el factor de potencia
        - Reducir pérdidas en el sistema
        - Optimizar el uso de la energía
        - Cumplir regulaciones eléctricas
        """)
    
    with col2:
        st.subheader("📊 Modos de Compensación")
        
        # Diagrama simple de compensación paralelo
        fig_paralelo = go.Figure()
        fig_paralelo.add_annotation(
            x=0.5, y=0.8,
            text="Fuente",
            showarrow=False,
            font=dict(size=14)
        )
        fig_paralelo.add_shape(
            type="line", x0=0.5, y0=0.7, x1=0.5, y1=0.3,
            line=dict(color="black", width=2)
        )
        fig_paralelo.add_shape(
            type="line", x0=0.5, y0=0.3, x1=0.2, y1=0.1,
            line=dict(color="black", width=2)
        )
        fig_paralelo.add_shape(
            type="line", x0=0.5, y0=0.3, x1=0.8, y1=0.1,
            line=dict(color="black", width=2)
        )
        fig_paralelo.add_annotation(
            x=0.2, y=0.05,
            text="Carga",
            showarrow=False,
            font=dict(size=12)
        )
        fig_paralelo.add_annotation(
            x=0.8, y=0.05,
            text="Compensador",
            showarrow=False,
            font=dict(size=12)
        )
        fig_paralelo.update_layout(
            title="Compensación Paralelo",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=200,
            showlegend=False
        )
        st.plotly_chart(fig_paralelo, use_container_width=True)
        
        # Diagrama simple de compensación serie
        fig_serie = go.Figure()
        fig_serie.add_annotation(
            x=0.2, y=0.5,
            text="Fuente",
            showarrow=False,
            font=dict(size=14)
        )
        fig_serie.add_shape(
            type="line", x0=0.3, y0=0.5, x1=0.5, y1=0.5,
            line=dict(color="black", width=2)
        )
        fig_serie.add_annotation(
            x=0.4, y=0.7,
            text="Compensador",
            showarrow=False,
            font=dict(size=12)
        )
        fig_serie.add_shape(
            type="line", x0=0.5, y0=0.5, x1=0.7, y1=0.5,
            line=dict(color="black", width=2)
        )
        fig_serie.add_annotation(
            x=0.8, y=0.5,
            text="Carga",
            showarrow=False,
            font=dict(size=14)
        )
        fig_serie.update_layout(
            title="Compensación Serie",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=200,
            showlegend=False
        )
        st.plotly_chart(fig_serie, use_container_width=True)

elif seccion == "Compensación Paralelo":
    st.header("Compensación Paralelo")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Parámetros de Entrada")
        
        # Datos de la carga
        st.write("**Datos de la Carga:**")
        potencia_activa = st.number_input(
            "Potencia Activa (P) [kW]:",
            min_value=0.1,
            max_value=10000.0,
            value=100.0,
            step=0.1
        )
        
        fp_actual = st.number_input(
            "Factor de Potencia Actual:",
            min_value=0.1,
            max_value=0.99,
            value=0.75,
            step=0.01
        )
        
        fp_deseado = st.number_input(
            "Factor de Potencia Deseado:",
            min_value=fp_actual + 0.01,
            max_value=0.99,
            value=0.95,
            step=0.01
        )
        
        # Parámetros del sistema
        st.write("**Parámetros del Sistema:**")
        tension = st.number_input(
            "Tensión Nominal [V]:",
            min_value=120,
            max_value=345000,
            value=220,
            step=10
        )
        
        frecuencia = st.selectbox(
            "Frecuencia [Hz]:",
            [50, 60],
            index=1
        )
        
        # Tipo de compensación
        tipo_compensacion = st.radio(
            "Tipo de Compensación:",
            ["Capacitiva", "Inductiva"],
            index=0
        )
    
    with col2:
        st.subheader("📊 Vista Preliminar")
        st.info("Aquí se mostrarán los resultados preliminares y gráficos")
        
        # Espacio placeholder para gráficos
        fig_placeholder = go.Figure()
        fig_placeholder.add_annotation(
            x=0.5, y=0.5,
            text="Gráficos de resultados aparecerán aquí",
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig_placeholder.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=300
        )
        st.plotly_chart(fig_placeholder, use_container_width=True)

elif seccion == "Compensación Serie":
    st.header("Compensación Serie")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Parámetros de Entrada")
        
        # Datos para compensación serie
        st.write("**Datos del Circuito:**")
        corriente = st.number_input(
            "Corriente de Carga [A]:",
            min_value=0.1,
            max_value=1000.0,
            value=50.0,
            step=0.1
        )
        
        reactancia_carga = st.number_input(
            "Reactancia de Carga [Ω]:",
            min_value=-1000.0,
            max_value=1000.0,
            value=10.0,
            step=0.1
        )
        
        tension_serie = st.number_input(
            "Tensión Nominal [V]:",
            min_value=120,
            max_value=345000,
            value=220,
            step=10
        )
        
        frecuencia_serie = st.selectbox(
            "Frecuencia [Hz]:",
            [50, 60],
            index=1
        )
        
        # Tipo de compensación serie
        tipo_comp_serie = st.radio(
            "Tipo de Compensación Serie:",
            ["Capacitiva", "Inductiva"],
            index=0
        )
        
        # Objetivo de compensación
        objetivo_serie = st.slider(
            "Reducción de Reactancia [%]:",
            min_value=10,
            max_value=90,
            value=50,
            step=5
        )
    
    with col2:
        st.subheader("📊 Vista Preliminar")
        st.info("Aquí se mostrarán los resultados preliminares y gráficos")
        
        # Espacio placeholder para gráficos
        fig_placeholder_serie = go.Figure()
        fig_placeholder_serie.add_annotation(
            x=0.5, y=0.5,
            text="Gráficos de resultados aparecerán aquí",
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig_placeholder_serie.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=300
        )
        st.plotly_chart(fig_placeholder_serie, use_container_width=True)

elif seccion == "Resultados":
    st.header("Resultados y Análisis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Resumen de Cálculos")
        st.success("Los resultados detallados aparecerán aquí")
        
        # Tabla placeholder para resultados
        datos_resultados = {
            "Parámetro": ["Valor Actual", "Valor Compensado", "Mejora"],
            "Factor de Potencia": ["0.75", "0.95", "+26.7%"],
            "Corriente [A]": ["150.2", "118.6", "-21.0%"],
            "Pérdidas [kW]": ["2.8", "1.8", "-35.7%"]
        }
        
        st.dataframe(datos_resultados, use_container_width=True)
    
    with col2:
        st.subheader("📊 Gráficos Comparativos")
        st.info("Gráficos comparativos aparecerán aquí")
        
        # Gráfico placeholder
        fig_comparativo = go.Figure()
        fig_comparativo.add_annotation(
            x=0.5, y=0.5,
            text="Gráficos comparativos aparecerán aquí",
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig_comparativo.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=300
        )
        st.plotly_chart(fig_comparativo, use_container_width=True)

# Barra inferior con información
st.markdown("---")
st.markdown("**Nota:** Esta es una versión preliminar para visualizar la distribución de la interfaz. Los cálculos serán implementados en la siguiente fase.")

# Sidebar adicional con información teórica
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Referencias Rápidas")
st.sidebar.markdown("""
**Fórmulas Principales:**

- Q = P × tan(φ)
- FP = cos(φ)
- Q_c = P × (tan(φ₁) - tan(φ₂))

**Factores de Potencia Típicos:**
- Motores: 0.7-0.9
- Transformadores: 0.8-0.95
- Iluminación: 0.5-0.9
""")
