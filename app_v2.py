"""
Versión 2.0 - Calculadora de Compensación de Reactivos con arquitectura modular
"""
import streamlit as st
import math
from components import PowerCalculator, SolutionComparator, TemplateManager, ComponentDatabase, ChartGenerator, PDFExporter

# Configuración de página
st.set_page_config(
    page_title="Calculadora de Compensación de Reactivos v2.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("⚡ Calculadora de Compensación de Reactivos v2.0")
st.markdown("---")

# Inicializar session state
if 'current_calculation' not in st.session_state:
    st.session_state.current_calculation = None
if 'comparison_results' not in st.session_state:
    st.session_state.comparison_results = None
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None

# Sidebar mejorado
st.sidebar.title("🚀 Panel de Control")

# Sección de navegación
seccion = st.sidebar.selectbox(
    "📍 Navegación:",
    ["🏠 Dashboard", "📋 Plantillas", "⚡ Compensación Paralelo", "🔗 Compensación Serie", "📊 Comparador", "📄 Reportes"],
    index=0,
    help="Selecciona la sección que deseas visitar"
)

# Navegación automática si hay página seleccionada
if hasattr(st.session_state, 'page') and st.session_state.page != seccion:
    # Mapeo de páginas a índices
    page_mapping = {
        "🏠 Dashboard": 0,
        "📋 Plantillas": 1,
        "⚡ Compensación Paralelo": 2,
        "🔗 Compensación Serie": 3,
        "📊 Comparador": 4,
        "📄 Reportes": 5
    }
    
    if st.session_state.page in page_mapping:
        # Actualizar el selectbox al índice correcto
        current_index = page_mapping[seccion]
        target_index = page_mapping[st.session_state.page]
        
        # Solo cambiar si es diferente
        if current_index != target_index:
            st.session_state.page = seccion  # Evitar bucle infinito

# Información del sistema
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Estado del Sistema")
if st.session_state.current_calculation:
    st.sidebar.success("✅ Cálculo realizado")
    st.sidebar.info(f"Tipo: {st.session_state.current_calculation.get('method', 'Desconocido')}")
else:
    st.sidebar.warning("⚠️ Sin cálculos realizados")

# Indicador de plantilla activa
if st.session_state.selected_template:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Plantilla Activa")
    template = st.session_state.selected_template
    st.sidebar.success(f"{template['icon']} {template['name']}")
    st.sidebar.info(f"Categoría: {template['category_name']}")
    
    if st.sidebar.button("🗑️ Limpiar", key="sidebar_clear_template", use_container_width=True):
        st.session_state.selected_template = None
        st.rerun()

if seccion == "🏠 Dashboard":
    st.header("🏠 Dashboard Principal")
    
    # Métricas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Plantillas Disponibles",
            len(TemplateManager.get_all_templates_flat()),
            "Configuraciones predefinidas"
        )
    
    with col2:
        st.metric(
            "Cálculos Realizados",
            "1" if st.session_state.current_calculation else "0",
            "Sesión actual"
        )
    
    with col3:
        st.metric(
            "Comparaciones",
            "1" if st.session_state.comparison_results else "0",
            "Análisis realizados"
        )
    
    with col4:
        st.metric(
            "Reportes Generados",
            "0",
            "PDF profesionales"
        )
    
    # Acciones rápidas
    st.markdown("### 🎯 Acciones Rápidas")
    
    col_quick1, col_quick2, col_quick3 = st.columns(3)
    
    with col_quick1:
        if st.button("📋 Usar Plantilla", type="primary", use_container_width=True):
            st.session_state.page = "📋 Plantillas"
            st.rerun()
    
    with col_quick2:
        if st.button("⚡ Nuevo Cálculo", use_container_width=True):
            st.session_state.page = "⚡ Compensación Paralelo"
            st.rerun()
    
    with col_quick3:
        if st.button("📊 Comparar", use_container_width=True):
            st.session_state.page = "📊 Comparador"
            st.rerun()
    
    # Actualizar métricas del dashboard para mostrar cálculos serie
    if st.session_state.current_calculation:
        calc = st.session_state.current_calculation
        method = calc.get('method', 'paralelo')
        
        if method == 'serie':
            col_last1, col_last2, col_last3 = st.columns(3)
            
            with col_last1:
                st.metric(
                    "Reactancia de Compensación",
                    f"{calc.get('x_compensacion', 0):.3f} Ω",
                    "Valor requerido"
                )
            
            with col_last2:
                st.metric(
                    "Componente",
                    f"{calc.get('valor_componente', 0):.2f} {calc.get('unidad', '')}",
                    "Tipo de componente"
                )
            
            with col_last3:
                cambio_corriente = ((calc.get('i_compensada', 0) - calc.get('i_actual', 0)) / calc.get('i_actual', 1)) * 100
                st.metric(
                    "Cambio Corriente",
                    f"{cambio_corriente:+.1f}%",
                    "Variación obtenida"
                )
        else:
            # Mantener lógica existente para paralelo
            col_last1, col_last2, col_last3 = st.columns(3)
            
            with col_last1:
                st.metric(
                    "Potencia Reactiva",
                    f"{calc.get('q_compensacion', 0):.2f} kVAR",
                    "Compensación necesaria"
                )
            
            with col_last2:
                st.metric(
                    "Componente",
                    f"{calc.get('valor_componente', 0):.2f} {calc.get('unidad', '')}",
                    "Valor requerido"
                )
            
            with col_last3:
                if calc.get('method') == 'paralelo':
                    reduccion = ((calc.get('i_actual', 0) - calc.get('i_compensada', 0)) / calc.get('i_actual', 1)) * 100
                    st.metric(
                        "Reducción Corriente",
                        f"{reduccion:.1f}%",
                        "Mejora obtenida"
                    )
                else:
                    st.metric(
                        "Reducción Reactancia",
                        f"{calc.get('reduccion_porcentaje', 0):.0f}%",
                        "Objetivo alcanzado"
                    )
    
    # Dashboard actualizado para mostrar cálculos serie
    if st.session_state.current_calculation:
        st.markdown("### 📈 Visualización Rápida")
        
        calc = st.session_state.current_calculation
        method = calc.get('method', 'paralelo')
        
        if method == 'serie':
            # Gráfico específico para compensación serie
            fig_series = ChartGenerator.create_series_impedance_chart(calc)
            st.plotly_chart(fig_series, use_container_width=True)
        else:
            # Gráfico para compensación paralelo
            fig = ChartGenerator.create_comparison_chart(calc, method)
            st.plotly_chart(fig, use_container_width=True)

elif seccion == "📋 Plantillas":
    st.header("📋 Plantillas Preconfiguradas")
    
    # Búsqueda de plantillas
    col_search, col_filter = st.columns([2, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Buscar plantillas:", placeholder="Ej: motor, edificio, industrial...")
    
    with col_filter:
        category_filter = st.selectbox("📂 Categoría:", ["Todas"] + list(TemplateManager.get_templates().keys()))
    
    # Obtener plantillas
    all_templates = TemplateManager.get_all_templates_flat()
    
    # Filtrar plantillas
    if search_query:
        filtered_templates = TemplateManager.search_templates(search_query)
    elif category_filter != "Todas":
        filtered_templates = [t for t in all_templates if t['category'] == category_filter]
    else:
        filtered_templates = all_templates
    
    # Mostrar plantillas
    if filtered_templates:
        st.info(f"📋 Se encontraron {len(filtered_templates)} plantillas")
        
        # Grid de plantillas
        cols = st.columns(3)
        for i, template in enumerate(filtered_templates):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="border: 2px solid #667eea; border-radius: 10px; padding: 20px; margin: 10px 0; background: white;">
                    <h3>{template['icon']} {template['name']}</h3>
                    <p style="color: #666; margin: 10px 0;">{template['description']}</p>
                    <p style="font-size: 0.9em; color: #888;">
                        <strong>Categoría:</strong> {template['category_name']}<br>
                        <strong>Tipo:</strong> {template['params'].get('tipo_comp', 'N/A')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📋 Usar Plantilla", key=f"template_{template['template_id']}", use_container_width=True):
                    st.session_state.selected_template = template
                    st.session_state.page = "⚡ Compensación Paralelo" if 'potencia_activa' in template['params'] else "🔗 Compensación Serie"
                    
                    # Mostrar feedback inmediato
                    st.success(f"✅ Plantilla '{template['name']}' seleccionada exitosamente")
                    st.info("🔄 Redirigiendo a la sección de cálculos...")
                    st.balloons()
                    
                    # Forzar rerun para mostrar feedback y cambiar de página
                    st.rerun()
    else:
        st.warning("⚠️ No se encontraron plantillas con los criterios especificados")
    
    # Recomendaciones inteligentes
    st.markdown("### 🤖 Recomendaciones Inteligentes")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        potencia_input = st.number_input("💪 Potencia (kW):", min_value=0.1, value=100.0, step=10.0)
    
    with col_rec2:
        tension_input = st.number_input("⚡ Tensión (V):", min_value=120, value=220, step=10)
    
    if st.button("🎯 Obtener Recomendaciones"):
        recommendations = TemplateManager.get_recommended_templates(potencia_input, tension_input)
        
        if recommendations:
            st.success(f"🎯 Se encontraron {len(recommendaciones)} recomendaciones")
            
            for rec in recommendations:
                st.markdown(f"""
                <div style="background: #f0f8ff; border-left: 4px solid #667eea; padding: 15px; margin: 10px 0;">
                    <h4>{rec['icon']} {rec['name']}</h4>
                    <p>{rec['description']}</p>
                    <small>Score de relevancia: ⭐⭐⭐⭐⭐</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No se encontraron recomendaciones para los valores ingresados")

elif seccion == "⚡ Compensación Paralelo":
    st.header("⚡ Compensación Paralelo")
    
    # Mostrar plantilla seleccionada si existe
    if st.session_state.selected_template and 'potencia_activa' in st.session_state.selected_template['params']:
        template = st.session_state.selected_template
        st.markdown("---")
        st.markdown(f"""
        <div style="background: #e8f5e8; border-left: 5px solid #28a745; padding: 20px; margin: 20px 0; border-radius: 5px;">
            <h3>📋 Plantilla Seleccionada Activa</h3>
            <p><strong>{template['icon']} {template['name']}</strong></p>
            <p>{template['description']}</p>
            <div style="margin-top: 15px;">
                <small>
                    <strong>Categoría:</strong> {template['category_name']} | 
                    <strong>Tipo:</strong> {template['params'].get('tipo_comp', 'N/A')}
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón para limpiar plantilla
        if st.button("🗑️ Limpiar Plantilla Seleccionada", key="clear_template"):
            st.session_state.selected_template = None
            st.warning("📋 Plantilla eliminada. Usando valores por defecto.")
            st.rerun()
        
        st.markdown("---")
        
        # Cargar valores de la plantilla
        default_values = template['params']
    else:
        default_values = {
            "potencia_activa": 100.0,
            "fp_actual": 0.75,
            "fp_deseado": 0.95,
            "tension": 220,
            "frecuencia": 60,
            "tipo_comp": "Capacitiva"
        }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Parámetros de Entrada")
        
        # Datos de la carga
        st.write("**Datos de la Carga:**")
        potencia_activa = st.number_input(
            "Potencia Activa (P) [kW]:",
            min_value=0.1,
            max_value=10000.0,
            value=default_values["potencia_activa"],
            step=0.1,
            help="Potencia activa consumida por la carga en kilovatios"
        )
        
        fp_actual = st.number_input(
            "Factor de Potencia Actual:",
            min_value=0.1,
            max_value=0.99,
            value=default_values["fp_actual"],
            step=0.01,
            help="Factor de potencia actual de la instalación (0.1 a 0.99)"
        )
        
        fp_deseado = st.number_input(
            "Factor de Potencia Deseado:",
            min_value=fp_actual + 0.01,
            max_value=0.99,
            value=default_values["fp_deseado"],
            step=0.01,
            help="Factor de potencia objetivo después de la compensación"
        )
        
        # Parámetros del sistema
        st.write("**Parámetros del Sistema:**")
        tension = st.number_input(
            "Tensión Nominal [V]:",
            min_value=120,
            max_value=345000,
            value=default_values["tension"],
            step=10,
            help="Tensión de operación del sistema en voltios"
        )
        
        frecuencia = st.selectbox(
            "Frecuencia [Hz]:",
            [50, 60],
            index=1 if default_values["frecuencia"] == 60 else 0
        )
        
        # Tipo de compensación
        st.write("**Tipo de Compensación:**")
        tipo_compensacion = st.radio(
            "Seleccione el tipo:",
            ["Capacitiva", "Inductiva"],
            index=0 if default_values["tipo_comp"] == "Capacitiva" else 1
        )
        
        # Explicación del tipo de compensación
        if tipo_compensacion == "Capacitiva":
            st.success("""📋 **Compensación Capacitiva Paralelo**
            
            **Uso recomendado para:**
            - Cargas inductivas (motores, transformadores)
            - Sistemas con factor de potencia bajo (< 0.9)
            - Reducción de corriente en conductores
            """)
        else:
            st.warning("""📋 **Compensación Inductiva Paralelo**
            
            **Uso recomendado para:**
            - Cargas capacitivas (cables largos, bancos de capacitores)
            - Sistemas con factor de potencia capacitivo (adelantado)
            - Corrección de sobrecompensación
            """)
    
    with col2:
        st.subheader("📊 Resultados del Cálculo")
        
        # Realizar cálculos
        if st.button("🔢 Calcular Compensación", type="primary"):
            resultados = PowerCalculator.calculate_parallel_compensation(
                potencia_activa, fp_actual, fp_deseado, tension, frecuencia, tipo_compensacion
            )
            
            if resultados:
                # Agregar método para identificación
                resultados['method'] = 'paralelo'
                
                # Guardar en session state
                st.session_state.current_calculation = resultados
                
                # Calcular costo estimado
                costo_estimado = ComponentDatabase.estimate_component_cost(resultados['q_compensacion'], tension)
                resultados['costo_estimado'] = costo_estimado
                
                # Análisis económico
                analisis_economico = PowerCalculator.calculate_economic_analysis(
                    resultados['perdidas_actuales'],
                    resultados['perdidas_compensadas'],
                    costo_estimado
                )
                resultados.update(analisis_economico)
                
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
                fig = ChartGenerator.create_comparison_chart(resultados, "paralelo")
                st.plotly_chart(fig, use_container_width=True)
                
                # Información económica
                st.markdown("### 💰 Análisis Económico")
                
                col_econ1, col_econ2 = st.columns(2)
                
                with col_econ1:
                    st.metric(
                        "Costo Estimado",
                        f"${costo_estimado:,.2f}",
                        "Componente + instalación"
                    )
                
                with col_econ2:
                    st.metric(
                        "Período de Recuperación",
                        f"{resultados['periodo_recuperacion']:.1f} años",
                        "ROI"
                    )
        else:
            st.info("Ingrese los parámetros y presione 'Calcular Compensación' para ver los resultados")

elif seccion == "🔗 Compensación Serie":
    st.header("🔗 Compensación Serie")
    
    # Cargar plantilla si está seleccionada
    if st.session_state.selected_template and 'corriente' in st.session_state.selected_template['params']:
        template = st.session_state.selected_template
        st.markdown("---")
        st.markdown(f"""
        <div style="background: #e8f5e8; border-left: 5px solid #28a745; padding: 20px; margin: 20px 0; border-radius: 5px;">
            <h3>📋 Plantilla Seleccionada Activa</h3>
            <p><strong>{template['icon']} {template['name']}</strong></p>
            <p>{template['description']}</p>
            <div style="margin-top: 15px;">
                <small>
                    <strong>Categoría:</strong> {template['category_name']} | 
                    <strong>Tipo:</strong> {template['params'].get('tipo_comp', 'N/A')}
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón para limpiar plantilla
        if st.button("🗑️ Limpiar Plantilla Seleccionada", key="clear_template_serie"):
            st.session_state.selected_template = None
            st.warning("📋 Plantilla eliminada. Usando valores por defecto.")
            st.rerun()
        
        st.markdown("---")
        
        # Cargar valores de la plantilla
        default_values = template['params']
    else:
        default_values = {
            "corriente": 50.0,
            "reactancia_carga": 10.0,
            "tension": 220,
            "frecuencia": 60,
            "tipo_comp": "Capacitiva",
            "reduccion_porcentaje": 50
        }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Parámetros de Entrada")
        
        # Datos del circuito
        st.write("**Datos del Circuito:**")
        corriente = st.number_input(
            "Corriente de Carga [A]:",
            min_value=0.1,
            max_value=1000.0,
            value=default_values.get("corriente", 50.0),
            step=0.1,
            help="Corriente que circula por la carga en amperios"
        )
        
        reactancia_carga = st.number_input(
            "Reactancia de Carga [Ω]:",
            min_value=-1000.0,
            max_value=1000.0,
            value=default_values.get("reactancia_carga", 10.0),
            step=0.1,
            help="Reactancia de la carga. Positivo para inductiva, negativo para capacitiva"
        )
        
        # Parámetros del sistema
        st.write("**Parámetros del Sistema:**")
        tension = st.number_input(
            "Tensión Nominal [V]:",
            min_value=120,
            max_value=345000,
            value=default_values.get("tension", 220),
            step=10,
            help="Tensión de operación del sistema en voltios"
        )
        
        frecuencia = st.selectbox(
            "Frecuencia [Hz]:",
            [50, 60],
            index=1 if default_values.get("frecuencia", 60) == 60 else 0
        )
        
        # Tipo de compensación
        st.write("**Tipo de Compensación Serie:**")
        tipo_compensacion = st.radio(
            "Seleccione el tipo:",
            ["Capacitiva", "Inductiva"],
            index=0 if default_values.get("tipo_comp", "Capacitiva") == "Capacitiva" else 1
        )
        
        # Explicación del tipo de compensación
        if tipo_compensacion == "Capacitiva":
            st.success("""📋 **Compensación Capacitiva Serie**
            
            **Uso recomendado para:**
            - Circuitos inductivos con reactancia alta
            - Mejora de regulación de tensión
            - Reducción de caídas de tensión en líneas
            
            **Cómo funciona:**
            El capacitor en serie reduce la reactancia total del circuito (X_total = X_carga - X_c),
            permitiendo mayor flujo de corriente para la misma tensión.
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
            """)
        
        # Objetivo de compensación
        st.write("**Objetivo de Compensación:**")
        objetivo_serie = st.slider(
            "Reducción de Reactancia [%]:",
            min_value=10,
            max_value=90,
            value=default_values.get("reduccion_porcentaje", 50),
            step=5,
            help="Porcentaje de reducción deseado de la reactancia total"
        )
    
    with col2:
        st.subheader("📊 Resultados del Cálculo")
        
        # Realizar cálculos
        if st.button("🔢 Calcular Compensación Serie", type="primary"):
            resultados = PowerCalculator.calculate_series_compensation(
                corriente, reactancia_carga, tension, frecuencia, tipo_compensacion, objetivo_serie
            )
            
            if resultados:
                # Agregar método para identificación
                resultados['method'] = 'serie'
                
                # Guardar en session state
                st.session_state.current_calculation = resultados
                
                # Calcular costo estimado
                costo_estimado = ComponentDatabase.estimate_component_cost(resultados['q_compensacion'], tension)
                resultados['costo_estimado'] = costo_estimado
                
                # Análisis económico
                analisis_economico = PowerCalculator.calculate_economic_analysis(
                    0, 0,  # Sin pérdidas directas en compensación serie
                    costo_estimado,
                    horas_operacion_anual=8760,
                    costo_kwh=0.15
                )
                resultados.update(analisis_economico)
                
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
                        f"Valor del {tipo_compensacion.lower()}",
                        f"{resultados['valor_componente']:.2f} {resultados['unidad']}"
                    )
                
                with col_metrics3:
                    cambio_corriente = ((resultados['i_compensada'] - resultados['i_actual']) / resultados['i_actual']) * 100
                    st.metric(
                        "Cambio de Corriente",
                        f"{cambio_corriente:+.1f}%",
                        delta=f"{resultados['i_compensada'] - resultados['i_actual']:.2f} A"
                    )
                
                # Gráfico de comparación
                fig = ChartGenerator.create_comparison_chart(resultados, "serie")
                st.plotly_chart(fig, use_container_width=True)
                
                # Información técnica detallada
                st.markdown("### ⚡ Análisis Técnico")
                
                col_tech1, col_tech2 = st.columns(2)
                
                with col_tech1:
                    st.metric(
                        "Reactancia Original",
                        f"{abs(reactancia_carga):.3f} Ω",
                        "Valor inicial"
                    )
                
                with col_tech2:
                    st.metric(
                        "Reactancia Final",
                        f"{abs(resultados['x_total']):.3f} Ω",
                        "Después de compensación"
                    )
                
                # Información económica
                st.markdown("### 💰 Información Económica")
                
                col_econ1, col_econ2 = st.columns(2)
                
                with col_econ1:
                    st.metric(
                        "Costo Estimado",
                        f"${costo_estimado:,.2f}",
                        "Componente + instalación"
                    )
                
                with col_econ2:
                    st.metric(
                        "Potencia Aparente",
                        f"{resultados['potencia_aparente']:.2f} kVA",
                        "Sistema trifásico"
                    )
        else:
            st.info("Ingrese los parámetros y presione 'Calcular Compensación Serie' para ver los resultados")

elif seccion == "📊 Comparador":
    st.header("📊 Comparador de Soluciones")
    
    st.info("Para usar el comparador, realice primero varios cálculos y luego compárelos aquí")
    
    if st.session_state.current_calculation:
        st.success("✅ Tienes un cálculo listo para comparar")
        
        # Botón para agregar a comparación
        if st.button("➕ Agregar a Comparación"):
            if 'comparison_list' not in st.session_state:
                st.session_state.comparison_list = []
            
            # Agregar nombre si no existe
            if 'name' not in st.session_state.current_calculation:
                st.session_state.current_calculation['name'] = f"Solución {len(st.session_state.comparison_list) + 1}"
            
            st.session_state.comparison_list.append(st.session_state.current_calculation.copy())
            st.success(f"✅ Agregado a comparación. Total: {len(st.session_state.comparison_list)} soluciones")
    
    # Mostrar comparación si hay soluciones
    if 'comparison_list' in st.session_state and st.session_state.comparison_list:
        st.markdown("### 📈 Análisis Comparativo")
        
        comparison = SolutionComparator.compare_solutions(st.session_state.comparison_list)
        st.session_state.comparison_results = comparison
        
        # Mostrar tabla comparativa
        import pandas as pd
        
        df_data = []
        for sol in comparison['detailed_comparison']:
            df_data.append({
                'Solución': sol['name'],
                'Tipo': sol['type'],
                'Método': sol['method'],
                'Q Compensación (kVAR)': f"{sol['q_compensacion']:.2f}",
                'Costo Estimado ($)': f"${sol['costo_estimado']:,.2f}",
                'ROI Anual (%)': f"{sol.get('roi_anual', 0):.1f}",
                'Score Económico': f"{sol['economic_score']:.0f}",
                'Score Técnico': f"{sol['technical_score']:.1f}"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Mejores soluciones
        col_best1, col_best2 = st.columns(2)
        
        with col_best1:
            if comparison['best_economic']:
                best = comparison['best_economic']
                st.markdown(f"""
                <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; border: 2px solid #28a745;">
                    <h3>🏆 Mejor Solución Económica</h3>
                    <h4>{best['name']}</h4>
                    <p><strong>Tipo:</strong> {best['type']}</p>
                    <p><strong>Costo:</strong> ${best['costo_estimado']:,.2f}</p>
                    <p><strong>ROI:</strong> {best.get('roi_anual', 0):.1f}% anual</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_best2:
            if comparison['best_technical']:
                best = comparison['best_technical']
                st.markdown(f"""
                <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; border: 2px solid #2196f3;">
                    <h3>⚡ Mejor Solución Técnica</h3>
                    <h4>{best['name']}</h4>
                    <p><strong>Tipo:</strong> {best['type']}</p>
                    <p><strong>Score Técnico:</strong> {best['technical_score']:.1f}</p>
                    <p><strong>Q Compensación:</strong> {best['q_compensacion']:.2f} kVAR</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Gráfico comparativo
        fig = ChartGenerator.create_solution_comparison_chart(comparison)
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ No hay soluciones para comparar. Realiza cálculos primero.")

elif seccion == "📄 Reportes":
    st.header("📄 Generación de Reportes")
    
    if st.session_state.current_calculation:
        st.success("✅ Tienes datos para generar reporte")
        
        # Información de la empresa
        st.markdown("### 🏢 Información de la Empresa")
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            company_name = st.text_input("Nombre de la Empresa:", value="Consultoría Eléctrica Profesional")
            company_address = st.text_input("Dirección:", value="Dirección de la Empresa")
        
        with col_info2:
            company_phone = st.text_input("Teléfono:", value="+1 234 567 890")
            company_email = st.text_input("Email:", value="info@empresa.com")
        
        company_info = {
            "name": company_name,
            "address": company_address,
            "phone": company_phone,
            "email": company_email,
            "website": "www.empresa.com"
        }
        
        # Generar reporte
        if st.button("📄 Generar Reporte PDF", type="primary"):
            # Generar HTML del reporte
            html_report = PDFExporter.generate_html_report(
                st.session_state.current_calculation,
                st.session_state.current_calculation.get('method', 'paralelo'),
                company_info
            )
            
            # Crear enlace de descarga
            download_link = PDFExporter.create_download_link(html_report, "reporte_compensacion_reactivos.html")
            st.markdown(download_link, unsafe_allow_html=True)
            
            # Vista previa
            st.markdown("### 📋 Vista Previa del Reporte")
            st.components.v1.html(html_report, height=600, scrolling=True)
        
        # Exportación a Excel
        st.markdown("### 📊 Exportación de Datos")
        
        excel_link = PDFExporter.export_to_excel(st.session_state.current_calculation)
        st.markdown(excel_link, unsafe_allow_html=True)
    
    else:
        st.warning("⚠️ No hay cálculos realizados. Realiza un cálculo primero para generar reportes.")

# Footer
st.markdown("---")
st.markdown("""
**⚡ Calculadora de Compensación de Reactivos v2.0**  
*Arquitectura modular con plantillas, comparador de soluciones y reportes profesionales*
""")

# Sidebar con referencias rápidas (mejorado)
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Referencias Rápidas")

if seccion == "⚡ Compensación Paralelo":
    st.sidebar.markdown("""
    **Fórmulas - Compensación Paralelo:**
    
    **Potencia Reactiva:**
    • Q = P × tan(φ)
    
    **Factor de Potencia:**
    • FP = cos(φ)
    
    **Reactivos de Compensación:**
    • Q_c = P × (tan(φ₁) - tan(φ₂))
    
    **Capacitancia:**
    • C = Q_c / (2π × f × V²)
    
    **Inductancia:**
    • L = V² / (2π × f × Q_c)
    """)
elif seccion == "🔗 Compensación Serie":
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
    """)
