import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# Funciones de cálculo
def calcular_compensacion_paralelo(potencia_activa, fp_actual, fp_deseado, tension, frecuencia, tipo_comp):
    """
    Calcula la compensación paralelo
    """
    # Convertir potencia a W
    P_w = potencia_activa * 1000
    
    # Calcular ángulos
    phi1 = math.acos(fp_actual)
    phi2 = math.acos(fp_deseado)
    
    # Calcular potencias reactivas
    q1 = P_w * math.tan(phi1)  # Reactivos actuales
    q2 = P_w * math.tan(phi2)  # Reactivos deseados
    q_compensacion = abs(q1 - q2)  # Reactivos de compensación
    
    # Corrientes
    i_actual = P_w / (tension * fp_actual)
    i_compensada = P_w / (tension * fp_deseado)
    
    # Valores del compensador
    if tipo_comp == "Capacitiva":
        capacitancia = q_compensacion / (2 * math.pi * frecuencia * tension**2)
        valor_componente = capacitancia * 1e6  # Convertir a μF
        unidad = "μF"
        reactancia = -1 / (2 * math.pi * frecuencia * capacitancia)
    else:  # Inductiva
        inductancia = tension**2 / (2 * math.pi * frecuencia * q_compensacion)
        valor_componente = inductancia * 1000  # Convertir a mH
        unidad = "mH"
        reactancia = 2 * math.pi * frecuencia * inductancia
    
    # Pérdidas (asumiendo resistencia constante)
    r_conductor = 0.1  # Resistencia estimada en ohmios
    perdidas_actuales = 3 * i_actual**2 * r_conductor / 1000  # kW
    perdidas_compensadas = 3 * i_compensada**2 * r_conductor / 1000  # kW
    
    return {
        'q_actual': q1 / 1000,  # kVAR
        'q_deseado': q2 / 1000,  # kVAR
        'q_compensacion': q_compensacion / 1000,  # kVAR
        'i_actual': i_actual,
        'i_compensada': i_compensada,
        'valor_componente': valor_componente,
        'unidad': unidad,
        'reactancia': reactancia,
        'perdidas_actuales': perdidas_actuales,
        'perdidas_compensadas': perdidas_compensadas,
        'phi1': math.degrees(phi1),
        'phi2': math.degrees(phi2)
    }

def calcular_compensacion_serie(corriente, reactancia_carga, tension, frecuencia, tipo_comp, porcentaje_reduccion):
    """
    Calcula la compensación serie
    """
    # Calcular reactancia de compensación necesaria
    if abs(reactancia_carga) < 0.001:
        st.error("La reactancia de carga no puede ser cero")
        return None
    
    x_compensacion = abs(reactancia_carga) * (porcentaje_reduccion / 100)
    
    # Reactancia total
    if tipo_comp == "Capacitiva":
        x_total = reactancia_carga - x_compensacion
        if reactancia_carga > 0:  # Carga inductiva
            q_c = corriente**2 * x_compensacion
        else:  # Carga capacitiva
            q_c = -corriente**2 * x_compensacion
    else:  # Inductiva
        x_total = reactancia_carga + x_compensacion
        if reactancia_carga > 0:  # Carga inductiva
            q_c = -corriente**2 * x_compensacion
        else:  # Carga capacitiva
            q_c = corriente**2 * x_compensacion
    
    # Valores del compensador
    if tipo_comp == "Capacitiva":
        capacitancia = 1 / (2 * math.pi * frecuencia * x_compensacion)
        valor_componente = capacitancia * 1e6  # Convertir a μF
        unidad = "μF"
    else:  # Inductiva
        inductancia = x_compensacion / (2 * math.pi * frecuencia)
        valor_componente = inductancia * 1000  # Convertir a mH
        unidad = "mH"
    
    # Potencias
    potencia_aparente_actual = math.sqrt(3) * tension * corriente
    impedancia_actual = abs(reactancia_carga)
    impedancia_compensada = abs(x_total)
    
    # Corriente compensada (aproximada)
    i_compensada = corriente * (impedancia_actual / impedancia_compensada) if impedancia_compensada > 0 else corriente
    
    return {
        'x_compensacion': x_compensacion,
        'x_total': x_total,
        'q_compensacion': abs(q_c) / 1000,  # kVAR
        'valor_componente': valor_componente,
        'unidad': unidad,
        'i_actual': corriente,
        'i_compensada': i_compensada,
        'reduccion_porcentaje': porcentaje_reduccion,
        'potencia_aparente': potencia_aparente_actual / 1000  # kVA
    }
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
            step=0.1,
            help="Potencia activa consumida por la carga en kilovatios"
        )
        
        fp_actual = st.number_input(
            "Factor de Potencia Actual:",
            min_value=0.1,
            max_value=0.99,
            value=0.75,
            step=0.01,
            help="Factor de potencia actual de la instalación (0.1 a 0.99)"
        )
        
        fp_deseado = st.number_input(
            "Factor de Potencia Deseado:",
            min_value=fp_actual + 0.01,
            max_value=0.99,
            value=0.95,
            step=0.01,
            help="Factor de potencia objetivo después de la compensación"
        )
        
        # Parámetros del sistema
        st.write("**Parámetros del Sistema:**")
        tension = st.number_input(
            "Tensión Nominal [V]:",
            min_value=120,
            max_value=345000,
            value=220,
            step=10,
            help="Tensión de operación del sistema en voltios"
        )
        
        frecuencia = st.selectbox(
            "Frecuencia [Hz]:",
            [50, 60],
            index=1
        )
        
        # Tipo de compensación
        st.write("**Tipo de Compensación:**")
        tipo_compensacion = st.radio(
            "Seleccione el tipo:",
            ["Capacitiva", "Inductiva"],
            index=0
        )
        
        # Explicación del tipo de compensación seleccionado
        if tipo_compensacion == "Capacitiva":
            st.success("""📋 **Compensación Capacitiva Paralelo**
            
            **Uso recomendado para:**
            - Cargas inductivas (motores, transformadores)
            - Sistemas con factor de potencia bajo (< 0.9)
            - Reducción de corriente en conductores
            
            **Cómo funciona:**
            Los capacitores suministran potencia reactiva (Qc) a la carga,
            reduciendo la demanda de reactivos de la fuente.
            
            **Efecto principal:** Mejora el factor de potencia hacia valores más altos.
            """)
        else:
            st.warning("""📋 **Compensación Inductiva Paralelo**
            
            **Uso recomendado para:**
            - Cargas capacitivas (cables largos, bancos de capacitores)
            - Sistemas con factor de potencia capacitivo (adelantado)
            - Corrección de sobrecompensación
            
            **Cómo funciona:**
            Los inductores absorben potencia reactiva (Qc) del sistema,
            reduciendo el exceso de reactivos capacitivos.
            
            **Efecto principal:** Corrige factores de potencia excesivamente altos o adelantados.
            """)
    
    with col2:
        st.subheader("📊 Resultados del Cálculo")
        
        # Realizar cálculos
        if st.button("🔢 Calcular Compensación", type="primary"):
            resultados = calcular_compensacion_paralelo(
                potencia_activa, fp_actual, fp_deseado, tension, frecuencia, tipo_compensacion
            )
            
            if resultados:
                # Mostrar resultados principales
                st.success("✅ Cálculo realizado con éxito")
                
                # Métricas principales
                col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
                
                with col_metrics1:
                    st.metric(
                        "Potencia Reactiva de Compensación",
                        f"{resultados['q_compensacion']:.2f} kVAR",
                        delta=f"{resultados['q_actual'] - resultados['q_deseado']:.2f} kVAR"
                    )
                
                with col_metrics2:
                    st.metric(
                        f"Valor del {tipo_compensacion.lower()}",
                        f"{resultados['valor_componente']:.2f} {resultados['unidad']}"
                    )
                
                with col_metrics3:
                    reduccion_corriente = ((resultados['i_actual'] - resultados['i_compensada']) / resultados['i_actual']) * 100
                    st.metric(
                        "Reducción de Corriente",
                        f"{reduccion_corriente:.1f}%",
                        delta=f"{resultados['i_actual'] - resultados['i_compensada']:.2f} A"
                    )
                
                # Gráfico de comparación
                fig_comparacion = go.Figure()
                
                # Datos para el gráfico
                categorias = ['Corriente [A]', 'Pérdidas [kW]', 'Ángulo φ [°]']
                valores_actuales = [resultados['i_actual'], resultados['perdidas_actuales'], resultados['phi1']]
                valores_compensados = [resultados['i_compensada'], resultados['perdidas_compensadas'], resultados['phi2']]
                
                fig_comparacion.add_trace(go.Bar(
                    name='Actual',
                    x=categorias,
                    y=valores_actuales,
                    marker_color='lightcoral'
                ))
                
                fig_comparacion.add_trace(go.Bar(
                    name='Compensado',
                    x=categorias,
                    y=valores_compensados,
                    marker_color='lightgreen'
                ))
                
                fig_comparacion.update_layout(
                    title='Comparación: Antes vs Después de Compensación',
                    xaxis_title='Parámetros',
                    yaxis_title='Valor',
                    barmode='group',
                    height=400
                )
                
                st.plotly_chart(fig_comparacion, use_container_width=True)
                
                # Triángulo de potencias
                fig_triangulo = make_subplots(
                    rows=1, cols=2,
                    specs=[[{"type": "polar"}, {"type": "polar"}]],
                    subplot_titles=['Antes de Compensación', 'Después de Compensación']
                )
                
                # Antes
                fig_triangulo.add_trace(
                    go.Scatterpolar(
                        r=[0, resultados['q_actual'], potencia_activa],
                        theta=[0, resultados['phi1'], 90],
                        mode='lines+markers',
                        name='Actual',
                        line_color='red'
                    ),
                    row=1, col=1
                )
                
                # Después
                fig_triangulo.add_trace(
                    go.Scatterpolar(
                        r=[0, resultados['q_deseado'], potencia_activa],
                        theta=[0, resultados['phi2'], 90],
                        mode='lines+markers',
                        name='Compensado',
                        line_color='green'
                    ),
                    row=1, col=2
                )
                
                fig_triangulo.update_layout(
                    title='Triángulo de Potencias',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_triangulo, use_container_width=True)
                
                # Guardar resultados en session state para la sección de resultados
                st.session_state.resultados_paralelo = resultados
                st.session_state.tipo_calculo = "paralelo"
        else:
            st.info("Ingrese los parámetros y presione 'Calcular Compensación' para ver los resultados")

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
            step=0.1,
            help="Corriente que circula por la carga en amperios"
        )
        
        reactancia_carga = st.number_input(
            "Reactancia de Carga [Ω]:",
            min_value=-1000.0,
            max_value=1000.0,
            value=10.0,
            step=0.1,
            help="Reactancia de la carga. Positivo para inductiva, negativo para capacitiva"
        )
        
        tension_serie = st.number_input(
            "Tensión Nominal [V]:",
            min_value=120,
            max_value=345000,
            value=220,
            step=10,
            help="Tensión de operación del sistema en voltios"
        )
        
        frecuencia_serie = st.selectbox(
            "Frecuencia [Hz]:",
            [50, 60],
            index=1
        )
        
        # Tipo de compensación serie
        st.write("**Tipo de Compensación Serie:**")
        tipo_comp_serie = st.radio(
            "Seleccione el tipo:",
            ["Capacitiva", "Inductiva"],
            index=0
        )
        
        # Explicación del tipo de compensación serie seleccionado
        if tipo_comp_serie == "Capacitiva":
            st.success("""📋 **Compensación Capacitiva Serie**
            
            **Uso recomendado para:**
            - Circuitos inductivos con reactancia alta
            - Mejora de regulación de tensión
            - Reducción de caídas de tensión en líneas
            
            **Cómo funciona:**
            El capacitor en serie reduce la reactancia total del circuito (X_total = X_carga - X_c),
            permitiendo mayor flujo de corriente para la misma tensión.
            
            **Efecto principal:** Reduce la impedancia total y mejora la transferencia de potencia.
            """)
        else:
            st.warning("""📋 **Compensación Inductiva Serie**
            
            **Uso recomendado para:**
            - Circuitos capacitivos (cables largos)
            - Limitación de corriente de cortocircuito
            - Control de flujo de potencia
            
            **Cómo funciona:**
            El inductor en serie aumenta la reactancia total del circuito (X_total = X_carga + X_c),
            limitando la corriente y controlando la transferencia de potencia.
            
            **Efecto principal:** Aumenta la impedancia para controlar corrientes excesivas.
            """)
        
        # Objetivo de compensación
        objetivo_serie = st.slider(
            "Reducción de Reactancia [%]:",
            min_value=10,
            max_value=90,
            value=50,
            step=5,
            help="Porcentaje de reducción deseado de la reactancia total"
        )
    
    with col2:
        st.subheader("📊 Resultados del Cálculo")
        
        # Realizar cálculos
        if st.button("🔢 Calcular Compensación Serie", type="primary"):
            resultados = calcular_compensacion_serie(
                corriente, reactancia_carga, tension_serie, frecuencia_serie, tipo_comp_serie, objetivo_serie
            )
            
            if resultados:
                st.success("✅ Cálculo realizado con éxito")
                
                # Métricas principales
                col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
                
                with col_metrics1:
                    st.metric(
                        "Reactancia de Compensación",
                        f"{resultados['x_compensacion']:.3f} Ω",
                        delta=f"{objetivo_serie}% reducción"
                    )
                
                with col_metrics2:
                    st.metric(
                        f"Valor del {tipo_comp_serie.lower()}",
                        f"{resultados['valor_componente']:.2f} {resultados['unidad']}"
                    )
                
                with col_metrics3:
                    cambio_corriente = ((resultados['i_compensada'] - resultados['i_actual']) / resultados['i_actual']) * 100
                    st.metric(
                        "Cambio de Corriente",
                        f"{cambio_corriente:+.1f}%",
                        delta=f"{resultados['i_compensada'] - resultados['i_actual']:.2f} A"
                    )
                
                # Gráfico de reactancias
                fig_reactancias = go.Figure()
                
                fig_reactancias.add_trace(go.Bar(
                    name='Reactancia Carga',
                    x=['Original'],
                    y=[abs(reactancia_carga)],
                    marker_color='lightblue'
                ))
                
                fig_reactancias.add_trace(go.Bar(
                    name='Compensación',
                    x=['Compensación'],
                    y=[resultados['x_compensacion']],
                    marker_color='orange'
                ))
                
                fig_reactancias.add_trace(go.Bar(
                    name='Total',
                    x=['Final'],
                    y=[abs(resultados['x_total'])],
                    marker_color='lightgreen'
                ))
                
                fig_reactancias.update_layout(
                    title='Evolución de Reactancias',
                    xaxis_title='Etapa',
                    yaxis_title='Reactancia [Ω]',
                    height=400
                )
                
                st.plotly_chart(fig_reactancias, use_container_width=True)
                
                # Gráfico de comparación de corrientes
                fig_corrientes = go.Figure()
                
                fig_corrientes.add_trace(go.Scatter(
                    x=['Antes', 'Después'],
                    y=[resultados['i_actual'], resultados['i_compensada']],
                    mode='lines+markers',
                    line=dict(color='blue', width=3),
                    marker=dict(size=10),
                    name='Corriente'
                ))
                
                fig_corrientes.update_layout(
                    title='Variación de Corriente',
                    xaxis_title='Estado',
                    yaxis_title='Corriente [A]',
                    height=300
                )
                
                st.plotly_chart(fig_corrientes, use_container_width=True)
                
                # Guardar resultados en session state
                st.session_state.resultados_serie = resultados
                st.session_state.tipo_calculo = "serie"
        else:
            st.info("Ingrese los parámetros y presione 'Calcular Compensación Serie' para ver los resultados")

elif seccion == "Resultados":
    st.header("Resultados y Análisis")
    
    # Verificar si hay resultados guardados
    if hasattr(st.session_state, 'tipo_calculo'):
        if st.session_state.tipo_calculo == "paralelo" and hasattr(st.session_state, 'resultados_paralelo'):
            resultados = st.session_state.resultados_paralelo
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Resumen de Cálculos - Compensación Paralelo")
                
                # Tabla de resultados detallados
                datos_resultados = {
                    "Parámetro": ["Factor de Potencia Actual", "Factor de Potencia Final", "Potencia Reactiva Actual", "Potencia Reactiva Final", "Corriente Actual", "Corriente Final", "Pérdidas Actuales", "Pérdidas Finales"],
                    "Valor": [f"{math.cos(math.radians(resultados['phi1'])):.3f}", f"{math.cos(math.radians(resultados['phi2'])):.3f}", f"{resultados['q_actual']:.2f} kVAR", f"{resultados['q_deseado']:.2f} kVAR", f"{resultados['i_actual']:.2f} A", f"{resultados['i_compensada']:.2f} A", f"{resultados['perdidas_actuales']:.3f} kW", f"{resultados['perdidas_compensadas']:.3f} kW"],
                    "Mejora": ["-", f"+{((math.cos(math.radians(resultados['phi2']))/math.cos(math.radians(resultados['phi1'])))-1)*100:.1f}%", "-", f"{resultados['q_actual'] - resultados['q_deseado']:.2f} kVAR", "-", f"{((resultados['i_actual'] - resultados['i_compensada'])/resultados['i_actual'])*100:.1f}%", "-", f"{((resultados['perdidas_actuales'] - resultados['perdidas_compensadas'])/resultados['perdidas_actuales'])*100:.1f}%"]
                }
                
                st.dataframe(datos_resultados, use_container_width=True)
                
                # Información del compensador
                st.subheader("🔧 Especificaciones del Compensador")
                st.info(f"""
                **Tipo:** Capacitivo
                **Valor requerido:** {resultados['valor_componente']:.2f} {resultados['unidad']}
                **Reactancia:** {resultados['reactancia']:.3f} Ω
                **Potencia reactiva:** {resultados['q_compensacion']:.2f} kVAR
                """)
            
            with col2:
                st.subheader("📊 Análisis de Beneficios")
                
                # Métricas de beneficio
                ahorro_anual = ((resultados['perdidas_actuales'] - resultados['perdidas_compensadas']) * 8760 * 0.15)  # Asumiendo 24/7 y $0.15/kWh
                
                col_beneficio1, col_beneficio2 = st.columns(2)
                
                with col_beneficio1:
                    st.metric(
                        "Ahorro de Energía Anual",
                        f"{resultados['perdidas_actuales'] - resultados['perdidas_compensadas']:.3f} kW",
                        delta=f"{((resultados['perdidas_actuales'] - resultados['perdidas_compensadas'])/resultados['perdidas_actuales'])*100:.1f}%"
                    )
                
                with col_beneficio2:
                    st.metric(
                        "Ahorro Económico Anual",
                        f"${ahorro_anual:.2f}",
                        delta="Estimado"
                    )
                
                # Gráfico circular de composición de potencia
                fig_composicion = go.Figure(data=[
                    go.Pie(
                        labels=['Potencia Activa', 'Reactivos Compensación', 'Reactivos Restantes'],
                        values=[100, resultados['q_compensacion'], abs(resultados['q_deseado'])],
                        hole=0.3
                    )
                ])
                
                fig_composicion.update_layout(
                    title='Composición de Potencia Final',
                    height=400
                )
                
                st.plotly_chart(fig_composicion, use_container_width=True)
        
        elif st.session_state.tipo_calculo == "serie" and hasattr(st.session_state, 'resultados_serie'):
            resultados = st.session_state.resultados_serie
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Resumen de Cálculos - Compensación Serie")
                
                # Tabla de resultados detallados
                datos_resultados = {
                    "Parámetro": ["Reactancia Original", "Reactancia Compensación", "Reactancia Total", "Corriente Original", "Corriente Final", "Potencia Aparente"],
                    "Valor": [f"{abs(resultados['x_compensacion'] * 100/resultados['reduccion_porcentaje']):.3f} Ω", f"{resultados['x_compensacion']:.3f} Ω", f"{resultados['x_total']:.3f} Ω", f"{resultados['i_actual']:.2f} A", f"{resultados['i_compensada']:.2f} A", f"{resultados['potencia_aparente']:.2f} kVA"],
                    "Cambio": ["-", f"{resultados['reduccion_porcentaje']}%", f"{((abs(resultados['x_total']) - abs(resultados['x_compensacion'] * 100/resultados['reduccion_porcentaje']))/abs(resultados['x_compensacion'] * 100/resultados['reduccion_porcentaje']))*100:.1f}%", "-", f"{((resultados['i_compensada'] - resultados['i_actual'])/resultados['i_actual'])*100:+.1f}%", "-"]
                }
                
                st.dataframe(datos_resultados, use_container_width=True)
                
                # Información del compensador
                st.subheader("� Especificaciones del Compensador")
                st.info(f"""
                **Tipo:** Capacitivo Serie
                **Valor requerido:** {resultados['valor_componente']:.2f} {resultados['unidad']}
                **Reactancia:** {resultados['x_compensacion']:.3f} Ω
                **Potencia reactiva:** {resultados['q_compensacion']:.2f} kVAR
                """)
            
            with col2:
                st.subheader("📊 Análisis de Impacto")
                
                # Métricas de impacto
                col_impacto1, col_impacto2 = st.columns(2)
                
                with col_impacto1:
                    st.metric(
                        "Reducción de Reactancia",
                        f"{resultados['reduccion_porcentaje']:.0f}%",
                        delta="Objetivo alcanzado"
                    )
                
                with col_impacto2:
                    cambio_corriente = ((resultados['i_compensada'] - resultados['i_actual']) / resultados['i_actual']) * 100
                    st.metric(
                        "Modificación de Corriente",
                        f"{cambio_corriente:+.1f}%",
                        delta=f"{resultados['i_compensada'] - resultados['i_actual']:.2f} A"
                    )
                
                # Gráfico de barras apiladas
                fig_impacto = go.Figure()
                
                fig_impacto.add_trace(go.Bar(
                    name='Reactancia Original',
                    x=['Sistema'],
                    y=[abs(resultados['x_compensacion'] * 100/resultados['reduccion_porcentaje'])],
                    marker_color='lightblue'
                ))
                
                fig_impacto.add_trace(go.Bar(
                    name='Compensación',
                    x=['Sistema'],
                    y=[resultados['x_compensacion']],
                    marker_color='orange'
                ))
                
                fig_impacto.update_layout(
                    title='Descomposición de Reactancias',
                    xaxis_title='Componente',
                    yaxis_title='Reactancia [Ω]',
                    barmode='stack',
                    height=400
                )
                
                st.plotly_chart(fig_impacto, use_container_width=True)
    
    else:
        st.warning("⚠️ No hay cálculos realizados. Por favor, realice un cálculo en las secciones de Compensación Paralelo o Serie.")
        
        # Botones para navegar a las secciones de cálculo
        col_nav1, col_nav2 = st.columns(2)
        
        with col_nav1:
            if st.button("🔄 Ir a Compensación Paralelo", type="secondary"):
                st.session_state.pagina_actual = "Compensación Paralelo"
                st.rerun()
        
        with col_nav2:
            if st.button("🔄 Ir a Compensación Serie", type="secondary"):
                st.session_state.pagina_actual = "Compensación Serie"
                st.rerun()

# Barra inferior con información
st.markdown("---")
st.markdown("**✅ Versión funcional con cálculos matemáticos completos implementados.**")

# Sidebar adicional con información teórica
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Referencias Rápidas")

# Mostrar fórmulas según la sección actual
if seccion == "Compensación Paralelo":
    st.sidebar.markdown("""
    **Fórmulas - Compensación Paralelo:**
    
    **Potencia Reactiva:**
    • Q = P × tan(φ)
    
    **Factor de Potencia:**
    • FP = cos(φ)
    
    **Reactivos de Compensación:**
    • Q_c = P × (tan(φ₁) - tan(φ₂))
    
    **Capacitancia (si es capacitiva):**
    • C = Q_c / (2π × f × V²)
    
    **Inductancia (si es inductiva):**
    • L = V² / (2π × f × Q_c)
    
    **Ángulos:**
    • φ₁ = arccos(FP_actual)
    • φ₂ = arccos(FP_deseado)
    """)
    
elif seccion == "Compensación Serie":
    st.sidebar.markdown("""
    **Fórmulas - Compensación Serie:**
    
    **Reactancia de Compensación:**
    • X_c = Q_c / I²
    
    **Capacitancia Serie:**
    • C = 1 / (2π × f × X_c)
    
    **Inductancia Serie:**
    • L = X_c / (2π × f)
    
    **Reactancia Total:**
    • X_total = X_carga ± X_c
    
    **Potencia Reactiva:**
    • Q_c = I² × X_c
    
    **Reducción de Reactancia:**
    • % = (X_c / |X_carga|) × 100
    """)
    
else:
    st.sidebar.markdown("""
    **Fórmulas Generales:**
    
    **Triángulo de Potencias:**
    • S² = P² + Q²
    • S = P/cos(φ)
    • Q = P × tan(φ)
    
    **Factor de Potencia:**
    • FP = P/S = cos(φ)
    
    **Compensación Paralelo:**
    • Q_c = P × (tan(φ₁) - tan(φ₂))
    
    **Compensación Serie:**
    • X_c = Q_c / I²
    
    **Factores de Potencia Típicos:**
    • Motores: 0.7‑0.9
    • Transformadores: 0.8‑0.95
    • Iluminación: 0.5‑0.9
    """)
