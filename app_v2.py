"""
Versión 2.0 - Calculadora de Compensación de Reactivos con arquitectura modular
"""
import streamlit as st
import math
import pandas as pd
import base64
from datetime import datetime
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

# Inicializar session state al inicio de la app
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []
if 'current_calculation' not in st.session_state:
    st.session_state.current_calculation = None
if 'comparison_results' not in st.session_state:
    st.session_state.comparison_results = None
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'comparison_list' not in st.session_state:
    st.session_state.comparison_list = []

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
    calc = st.session_state.current_calculation
    st.sidebar.success("✅ Cálculo realizado")
    st.sidebar.info(f"Tipo: {calc.get('method', 'Desconocido')}")
    st.sidebar.info(f"Nombre: {calc.get('name', 'Sin nombre')}")
    st.sidebar.info(f"Componente: {calc.get('valor_componente', 0):.2f} {calc.get('unidad', '')}")
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
            st.plotly_chart(fig_series, use_container_width=True, key="dashboard_series_chart")
        else:
            # Gráfico para compensación paralelo
            fig = ChartGenerator.create_comparison_chart(calc, method)
            st.plotly_chart(fig, use_container_width=True, key="dashboard_parallel_chart")

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
        
        # Grid de plantillas con mejor contraste y animación
        cols = st.columns(3)
        for i, template in enumerate(filtered_templates):
            with cols[i % 3]:
                # ID único para cada tarjeta
                template_id = f"template_{template['template_id']}"
                
                # Contenedor principal con mejor contraste - usando componentes nativos de Streamlit
                with st.container():
                    st.markdown(f"""
                    <div style="border: 3px solid #2c3e50; border-radius: 15px; padding: 25px; margin: 15px 0; background: linear-gradient(145deg, #ffffff, #f8f9fa); box-shadow: 0 8px 16px rgba(0,0,0,0.15);">
                        <h3 style="color: #1a1a1a; margin-bottom: 15px; font-size: 1.3em; font-weight: bold;">
                            {template['icon']} {template['name']}
                        </h3>
                        <p style="color: #2c3e50; margin: 15px 0; line-height: 1.5; font-size: 0.95em;">
                            {template['description']}
                        </p>
                        <p style="font-size: 0.85em; color: #34495e; margin: 0;">
                            <strong style="color: #2c3e50;">Categoría:</strong> {template['category_name']}<br>
                            <strong style="color: #2c3e50;">Tipo:</strong> {template['params'].get('tipo_comp', 'N/A')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Detalles técnicos en expander
                    with st.expander(f"📋 Detalles Técnicos - {template['name']}"):
                        # Título más pequeño y subtítulo informativo
                        st.markdown(f"<h4 style='font-size: 0.85em; color: #666; margin-bottom: 10px;'>Parámetros Técnicos de {template['name']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"<p style='font-size: 0.75em; color: #888; margin-bottom: 15px;'>Configuración recomendada para este escenario</p>", unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Potencia", f"{template['params'].get('potencia_activa', 'N/A')} kW")
                            st.metric("FP Actual", f"{template['params'].get('fp_actual', 'N/A')}")
                            st.metric("Tensión", f"{template['params'].get('tension', 'N/A')} V")
                        with col2:
                            st.metric("FP Deseado", f"{template['params'].get('fp_deseado', 'N/A')}")
                            st.metric("Frecuencia", f"{template['params'].get('frecuencia', 'N/A')} Hz")
                            st.metric("Tipo", f"{template['params'].get('tipo_comp', 'N/A')}")
                
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
        <div style="background: #d4edda; border-left: 5px solid #155724; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #155724; margin-bottom: 15px; font-size: 1.2em;">📋 Plantilla Seleccionada Activa</h3>
            <p style="color: #155724; font-weight: bold; margin: 8px 0; font-size: 1.1em;">{template['icon']} {template['name']}</p>
            <p style="color: #155724; margin: 8px 0; line-height: 1.4;">{template['description']}</p>
            <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #c3e6cb;">
                <small style="color: #155724;">
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
                potencia_activa, fp_actual, fp_deseado, tension, frecuencia, tipo_compensacion,
                resistencia_conductor=0.1,  # Ω/km valor estándar
                longitud_conductor=1.0  # km valor estándar
            )
            
            if resultados:
                # Agregar método para identificación
                resultados['method'] = 'paralelo'
                
                # Mostrar alerta de éxito
                st.success("✅ ¡Cálculo realizado con éxito!")
                st.balloons()
                
                # Pedir nombre para guardar el cálculo
                st.markdown("---")
                st.markdown("### 💾 Guardar Cálculo")
                st.info("📝 Asigna un nombre descriptivo para identificar este cálculo:")
                
                solution_name = st.text_input(
                    "Nombre del cálculo:",
                    value=f"Paralelo {tipo_compensacion} {potencia_activa:.0f}kW {fp_actual:.2f}→{fp_deseado:.2f}FP {tension}V {frecuencia}Hz",
                    help="Este nombre se usará para identificar el cálculo en el comparador",
                    key="parallel_solution_name"
                )
                
                # Guardado automático al cambiar el nombre
                if solution_name.strip():
                    # Calcular costo estimado
                    costo_estimado = ComponentDatabase.estimate_component_cost(resultados['q_compensacion'], tension)
                    resultados['costo_estimado'] = costo_estimado
                    
                    # Análisis económico mejorado
                    analisis_economico = PowerCalculator.calculate_economic_analysis(
                        resultados['perdidas_actuales'],
                        resultados['perdidas_compensadas'],
                        costo_estimado,
                        horas_operacion_anual=8760,
                        costo_kwh=None,  # Usará valor por defecto industrial
                        corriente_actual=resultados['i_actual'],
                        corriente_compensada=resultados['i_compensada'],
                        resistencia_conductor=0.1,  # Ω/km valor estándar
                        longitud_conductor=1.0  # km valor estándar
                    )
                    resultados.update(analisis_economico)
                    
                    # Guardar con nombre personalizado
                    resultados['name'] = solution_name.strip()
                    resultados['added_time'] = datetime.now().strftime("%H:%M:%S")
                    
                    # Guardar en session state como cálculo actual y en historial
                    st.session_state.current_calculation = resultados.copy()
                    st.session_state.calculation_history.append(resultados.copy())
                    
                    st.success(f"🎉 Cálculo '{solution_name}' guardado automáticamente!")
                    st.info("📊 Ya disponible en el comparador y reportes")
                    st.rerun()
                
                # Mostrar vista previa de resultados
                st.markdown("---")
                st.markdown("### 📊 Vista Previa de Resultados")
                
                # Métricas principales con mejor espaciado
                col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
                
                with col_metrics1:
                    st.metric(
                        "Potencia Reactiva",
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
                st.markdown("#### 📈 Gráfico Comparativo")
                fig = ChartGenerator.create_comparison_chart(resultados, "paralelo")
                st.plotly_chart(fig, use_container_width=True, key="parallel_preview_chart")
                
                # Información adicional
                with st.expander("📋 Ver más detalles"):
                    col_detail1, col_detail2 = st.columns(2)
                    
                    with col_detail1:
                        st.write("**Datos Actuales:**")
                        st.write(f"• Potencia Activa: {potencia_activa:.2f} kW")
                        st.write(f"• Factor de Potencia: {fp_actual:.3f}")
                        st.write(f"• Corriente: {resultados['i_actual']:.2f} A")
                    
                    with col_detail2:
                        st.write("**Datos Compensados:**")
                        st.write(f"• Factor de Potencia: {fp_deseado:.3f}")
                        st.write(f"• Corriente: {resultados['i_compensada']:.2f} A")
                        st.write(f"• Reducción: {reduccion_corriente:.1f}%")
        else:
            st.info("Ingrese los parámetros y presione 'Calcular Compensación' para ver los resultados")
    
    # Mostrar resultados si hay cálculo guardado
    if st.session_state.current_calculation:
        calc = st.session_state.current_calculation
        method = calc.get('method', 'paralelo')
        
        st.markdown("### 📊 Resultados Guardados")
        st.info(f"📋 Cálculo actual: **{calc.get('name', 'Sin nombre')}**")
        
        # Mostrar resultados completos según el método
        if method == 'serie':
            col_results1, col_results2, col_results3 = st.columns(3)
            
            with col_results1:
                st.metric(
                    "Reactancia de Compensación",
                    f"{calc.get('x_compensacion', 0):.3f} Ω",
                    "Valor requerido"
                )
            
            with col_results2:
                st.metric(
                    "Componente",
                    f"{calc.get('valor_componente', 0):.2f} {calc.get('unidad', '')}",
                    "Tipo de componente"
                )
            
            with col_results3:
                cambio_corriente = ((calc.get('i_compensada', 0) - calc.get('i_actual', 0)) / calc.get('i_actual', 1)) * 100
                st.metric(
                    "Cambio de Corriente",
                    f"{cambio_corriente:+.1f}%",
                    "Variación obtenida"
                )
            
            # Información técnica detallada
            st.markdown("#### ⚡ Análisis Técnico")
            col_tech1, col_tech2 = st.columns(2)
            
            with col_tech1:
                st.metric(
                    "Reactancia Original",
                    f"{abs(calc.get('reactancia_carga', 0)):.3f} Ω",
                    "Valor inicial"
                )
            
            with col_tech2:
                st.metric(
                    "Reactancia Final",
                    f"{abs(calc.get('x_total', 0)):.3f} Ω",
                    "Después de compensación"
                )
            
            # Información económica
            st.markdown("#### 💰 Información Económica")
            col_econ1, col_econ2 = st.columns(2)
            
            with col_econ1:
                st.metric(
                    "Costo Estimado",
                    f"${calc.get('costo_estimado', 0):,.2f}",
                    "Componente + instalación"
                )
            
            with col_econ2:
                st.metric(
                    "Potencia Aparente",
                    f"{calc.get('potencia_aparente', 0):.2f} kVA",
                    "Sistema trifásico"
                )
        else:
            # Resultados para compensación paralelo
            col_results1, col_results2, col_results3 = st.columns(3)
            
            with col_results1:
                st.metric(
                    "Potencia Reactiva",
                    f"{calc.get('q_compensacion', 0):.2f} kVAR",
                    "Compensación necesaria"
                )
            
            with col_results2:
                st.metric(
                    "Componente",
                    f"{calc.get('valor_componente', 0):.2f} {calc.get('unidad', '')}",
                    "Valor requerido"
                )
            
            with col_results3:
                if calc.get('method') == 'paralelo':
                    reduccion = ((calc.get('i_actual', 0) - calc.get('i_compensada', 0)) / calc.get('i_actual', 1)) * 100
                    st.metric(
                        "Reducción de Corriente",
                        f"{reduccion:.1f}%",
                        "Mejora obtenida"
                    )
                else:
                    st.metric(
                        "Reducción Reactancia",
                        f"{calc.get('reduccion_porcentaje', 0):.0f}%",
                        "Objetivo alcanzado"
                    )
            
            # Información económica
            st.markdown("#### 💰 Análisis Económico")
            col_econ1, col_econ2 = st.columns(2)
            
            with col_econ1:
                st.metric(
                    "Costo Estimado",
                    f"${calc.get('costo_estimado', 0):,.2f}",
                    "Componente + instalación"
                )
            
            with col_econ2:
                st.metric(
                    "Período de Recuperación",
                    f"{calc.get('periodo_recuperacion', 0):.1f} años",
                    "ROI"
                )
        
        # Gráfico de resultados
        st.markdown("#### 📈 Visualización")
        if method == 'serie':
            fig_series = ChartGenerator.create_series_impedance_chart(calc)
            st.plotly_chart(fig_series, use_container_width=True, key="parallel_results_series_chart")
        else:
            fig = ChartGenerator.create_comparison_chart(calc, method)
            st.plotly_chart(fig, use_container_width=True, key="parallel_results_parallel_chart")
    else:
        st.info("Ingrese los parámetros y presione 'Calcular Compensación' para ver los resultados")

elif seccion == "🔗 Compensación Serie":
    st.header("🔗 Compensación Serie")
    
    # Mostrar plantilla seleccionada si existe (para compensación serie)
    if st.session_state.selected_template and 'reactancia_carga' in st.session_state.selected_template['params']:
        template = st.session_state.selected_template
        st.markdown("---")
        st.markdown(f"""
        <div style="background: #d4edda; border-left: 5px solid #155724; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #155724; margin-bottom: 15px; font-size: 1.2em;">📋 Plantilla Seleccionada Activa</h3>
            <p style="color: #155724; font-weight: bold; margin: 8px 0; font-size: 1.1em;">{template['icon']} {template['name']}</p>
            <p style="color: #155724; margin: 8px 0; line-height: 1.4;">{template['description']}</p>
            <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #c3e6cb;">
                <small style="color: #155724;">
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
    
    # Parámetros de entrada
    col_params1, col_params2 = st.columns(2)
    
    with col_params1:
        corriente = st.number_input(
            "📊 Corriente (A):",
            min_value=1.0,
            max_value=1000.0,
            value=50.0,
            step=1.0,
            help="Corriente de línea del sistema"
        )
        
        reactancia_carga = st.number_input(
            "⚡ Reactancia de Carga (Ω):",
            min_value=0.001,
            max_value=100.0,
            value=10.0,
            step=0.1,
            help="Reactancia de la carga a compensar"
        )
        
        tension = st.number_input(
            "🔌 Tensión (V):",
            min_value=100.0,
            max_value=50000.0,
            value=220.0,
            step=100.0,
            help="Tensión del sistema (valor de línea)"
        )
    
    with col_params2:
        frecuencia = st.number_input(
            "🔄 Frecuencia (Hz):",
            min_value=50.0,
            max_value=400.0,
            value=60.0,
            step=1.0,
            help="Frecuencia del sistema"
        )
        
        tipo_compensacion = st.selectbox(
            "🔧 Tipo de Compensación:",
            ["Capacitiva", "Inductiva"],
            index=0,
            help="Tipo de componente a utilizar"
        )
        
        objetivo_serie = st.number_input(
            "🎯 Objetivo de Reducción (%):",
            min_value=5.0,
            max_value=50.0,
            value=20.0,
            step=5.0,
            help="Porcentaje de reducción de reactancia deseado"
        )
    
    # Realizar cálculos
    if st.button("🔢 Calcular Compensación Serie", type="primary"):
        resultados = PowerCalculator.calculate_series_compensation(
            corriente, reactancia_carga, tension, frecuencia, tipo_compensacion, objetivo_serie
        )
        
        if resultados:
            # Agregar método para identificación
            resultados['method'] = 'serie'
            
            # Mostrar alerta de éxito
            st.success("✅ ¡Cálculo realizado con éxito!")
            st.balloons()
            
            # Pedir nombre para guardar el cálculo
            st.markdown("---")
            st.markdown("### 💾 Guardar Cálculo")
            st.info("📝 Asigna un nombre descriptivo para identificar este cálculo:")
            
            solution_name = st.text_input(
                "Nombre del cálculo:",
                value=f"Serie {tipo_compensacion} {corriente:.0f}A {reactancia_carga:.2f}Ω {objetivo_serie}% {tension}V {frecuencia}Hz",
                help="Este nombre se usará para identificar el cálculo en el comparador",
                key="series_solution_name"
            )
            
            # Guardado automático al cambiar el nombre
            if solution_name.strip():
                # Calcular costo estimado
                costo_estimado = ComponentDatabase.estimate_component_cost(resultados["q_compensacion"], tension)
                resultados["costo_estimado"] = costo_estimado
                
                # Análisis económico mejorado
                analisis_economico = PowerCalculator.calculate_economic_analysis(
                    0, 0,  # Sin pérdidas directas en compensación serie
                    costo_estimado,
                    horas_operacion_anual=8760,
                    costo_kwh=None,  # Usará valor por defecto industrial
                    multa_fp_bajo=None,  # Usará valor por defecto industrial
                    corriente_actual=resultados['i_actual'],
                    corriente_compensada=resultados['i_compensada'],
                    resistencia_conductor=0.1,  # Ω/km valor estándar
                    longitud_conductor=1.0  # km valor estándar
                )
                resultados.update(analisis_economico)
                
                # Guardar con nombre personalizado
                resultados["name"] = solution_name.strip()
                resultados["added_time"] = datetime.now().strftime("%H:%M:%S")
                
                # Guardar en session state como cálculo actual y en historial
                st.session_state.current_calculation = resultados.copy()
                st.session_state.calculation_history.append(resultados.copy())
                
                st.success(f"🎉 Cálculo '{solution_name}' guardado automáticamente!")
                st.info("📊 Ya disponible en el comparador y reportes")
                st.rerun()
            
            # Mostrar vista previa de resultados
            st.markdown("---")
            st.markdown("### 📊 Vista Previa de Resultados")
            
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
            st.markdown("#### 📈 Gráfico Comparativo")
            fig = ChartGenerator.create_comparison_chart(resultados, "serie")
            st.plotly_chart(fig, use_container_width=True, key="series_preview_chart")
            
            # Información adicional
            with st.expander("📋 Ver más detalles"):
                col_detail1, col_detail2 = st.columns(2)
                
                with col_detail1:
                    st.write("**Datos Actuales:**")
                    st.write(f"• Corriente: {corriente:.2f} A")
                    st.write(f"• Reactancia: {reactancia_carga:.3f} Ω")
                    st.write(f"• Tensión: {tension:.0f} V")
                
                with col_detail2:
                    st.write("**Datos Compensados:**")
                    st.write(f"• Reactancia Final: {resultados['x_total']:.3f} Ω")
                    st.write(f"• Corriente Final: {resultados['i_compensada']:.2f} A")
                    st.write(f"• Cambio: {cambio_corriente:+.1f}%")
        else:
            st.info("Ingrese los parámetros y presione 'Calcular Compensación Serie' para ver los resultados")
    
    # Mostrar resultados si hay cálculo guardado
    if st.session_state.current_calculation:
        calc = st.session_state.current_calculation
        method = calc.get('method', 'paralelo')
        
        st.markdown("### 📊 Resultados Guardados")
        st.info(f"📋 Cálculo actual: **{calc.get('name', 'Sin nombre')}**")
        
        # Mostrar resultados completos según el método
        if method == 'serie':
            col_results1, col_results2, col_results3 = st.columns(3)
            
            with col_results1:
                st.metric(
                    "Reactancia de Compensación",
                    f"{calc.get('x_compensacion', 0):.3f} Ω",
                    "Valor requerido"
                )
            
            with col_results2:
                st.metric(
                    "Componente",
                    f"{calc.get('valor_componente', 0):.2f} {calc.get('unidad', '')}",
                    "Tipo de componente"
                )
            
            with col_results3:
                cambio_corriente = ((calc.get('i_compensada', 0) - calc.get('i_actual', 0)) / calc.get('i_actual', 1)) * 100
                st.metric(
                    "Cambio de Corriente",
                    f"{cambio_corriente:+.1f}%",
                    "Variación obtenida"
                )
            
            # Información técnica detallada
            st.markdown("#### ⚡ Análisis Técnico")
            col_tech1, col_tech2 = st.columns(2)
            
            with col_tech1:
                st.metric(
                    "Reactancia Original",
                    f"{abs(calc.get('reactancia_carga', 0)):.3f} Ω",
                    "Valor inicial"
                )
            
            with col_tech2:
                st.metric(
                    "Reactancia Final",
                    f"{abs(calc.get('x_total', 0)):.3f} Ω",
                    "Después de compensación"
                )
            
            # Información económica
            st.markdown("#### 💰 Información Económica")
            col_econ1, col_econ2 = st.columns(2)
            
            with col_econ1:
                st.metric(
                    "Costo Estimado",
                    f"${calc.get('costo_estimado', 0):,.2f}",
                    "Componente + instalación"
                )
            
            with col_econ2:
                st.metric(
                    "Potencia Aparente",
                    f"{calc.get('potencia_aparente', 0):.2f} kVA",
                    "Sistema trifásico"
                )
        else:
            # Resultados para compensación paralelo
            col_results1, col_results2, col_results3 = st.columns(3)
            
            with col_results1:
                st.metric(
                    "Potencia Reactiva",
                    f"{calc.get('q_compensacion', 0):.2f} kVAR",
                    "Compensación necesaria"
                )
            
            with col_results2:
                st.metric(
                    "Componente",
                    f"{calc.get('valor_componente', 0):.2f} {calc.get('unidad', '')}",
                    "Valor requerido"
                )
            
            with col_results3:
                if calc.get('method') == 'paralelo':
                    reduccion = ((calc.get('i_actual', 0) - calc.get('i_compensada', 0)) / calc.get('i_actual', 1)) * 100
                    st.metric(
                        "Reducción de Corriente",
                        f"{reduccion:.1f}%",
                        "Mejora obtenida"
                    )
                else:
                    st.metric(
                        "Reducción Reactancia",
                        f"{calc.get('reduccion_porcentaje', 0):.0f}%",
                        "Objetivo alcanzado"
                    )
            
            # Información económica
            st.markdown("#### 💰 Análisis Económico")
            col_econ1, col_econ2 = st.columns(2)
            
            with col_econ1:
                st.metric(
                    "Costo Estimado",
                    f"${calc.get('costo_estimado', 0):,.2f}",
                    "Componente + instalación"
                )
            
            with col_econ2:
                st.metric(
                    "Período de Recuperación",
                    f"{calc.get('periodo_recuperacion', 0):.1f} años",
                    "ROI"
                )
        
        # Gráfico de resultados
        st.markdown("#### 📈 Visualización")
        if method == 'serie':
            fig_series = ChartGenerator.create_series_impedance_chart(calc)
            st.plotly_chart(fig_series, use_container_width=True, key="parallel_results_series_chart")
        else:
            fig = ChartGenerator.create_comparison_chart(calc, method)
            st.plotly_chart(fig, use_container_width=True, key="parallel_results_parallel_chart")
    else:
        st.info("Ingrese los parámetros y presione 'Calcular Compensación' para ver los resultados")

elif seccion == "📊 Comparador":
    st.header("📊 Comparador de Soluciones")
    
    # Mostrar historial de cálculos disponibles
    st.markdown("### 📋 Historial de Cálculos Disponibles")
    
    if st.session_state.calculation_history:
        st.info(f"📊 Tienes {len(st.session_state.calculation_history)} cálculos guardados")
        
        # Mostrar todos los cálculos del historial
        for i, calc in enumerate(st.session_state.calculation_history):
            with st.container():
                col_info, col_actions = st.columns([3, 1])
                
                with col_info:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; margin: 5px 0; border-radius: 5px; background: {'#e8f5e8' if i == len(st.session_state.calculation_history)-1 else 'white'};">
                        <h4 style="color: #333; margin-bottom: 10px;">📊 {calc['name']}</h4>
                        <p style="color: #555; margin: 5px 0;"><strong>Tipo:</strong> {calc.get('method', 'paralelo').capitalize()}</p>
                        <p style="color: #555; margin: 5px 0;"><strong>Componente:</strong> {calc.get('valor_componente', 0):.2f} {calc.get('unidad', '')}</p>
                        <p style="color: #555; margin: 5px 0;"><strong>Costo:</strong> ${calc.get('costo_estimado', 0):,.2f}</p>
                        <p style="color: #555; margin: 5px 0;"><strong>Fecha:</strong> {calc.get('added_time', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_actions:
                    st.markdown("<br>", unsafe_allow_html=True)  # Espaciado
                    col_add, col_del = st.columns(2)
                    
                    with col_add:
                        if st.button("➕ Agregar", key=f"add_{i}", help="Agregar a comparación"):
                            # Verificar si ya está en comparación
                            existing_names = [s['name'] for s in st.session_state.comparison_list]
                            if calc['name'] in existing_names:
                                st.warning(f"⚠️ '{calc['name']}' ya está en la comparación")
                            else:
                                st.session_state.comparison_list.append(calc.copy())
                                st.success(f"✅ '{calc['name']}' agregada a la comparación")
                                st.rerun()
                    
                    with col_del:
                        if st.button("🗑️", key=f"del_hist_{i}", help="Eliminar del historial"):
                            # Eliminar del historial
                            removed_name = st.session_state.calculation_history[i]['name']
                            st.session_state.calculation_history.pop(i)
                            st.success(f"✅ '{removed_name}' eliminada del historial")
                            st.rerun()
    else:
        st.warning("⚠️ No hay cálculos en el historial. Realiza cálculos primero.")
        st.info("💡 Ve a 'Compensación Paralelo' para realizar y guardar cálculos.")
    
    # Sección de comparación
    if st.session_state.comparison_list:
        st.markdown("---")
        st.markdown("### 📈 Soluciones en Comparación")
        
        # Mostrar soluciones actuales
        for i, solution in enumerate(st.session_state.comparison_list):
            with st.container():
                col_comp_info, col_comp_actions = st.columns([3, 1])
                
                with col_comp_info:
                    st.markdown(f"""
                    <div style="border: 2px solid #667eea; padding: 15px; margin: 5px 0; border-radius: 5px; background: #f8f9ff;">
                        <h4 style="color: #333; margin-bottom: 10px;">🔹 {solution['name']}</h4>
                        <p style="color: #555; margin: 5px 0;"><strong>Tipo:</strong> {solution.get('method', 'paralelo').capitalize()}</p>
                        <p style="color: #555; margin: 5px 0;"><strong>Componente:</strong> {solution.get('valor_componente', 0):.2f} {solution.get('unidad', '')}</p>
                        <p style="color: #555; margin: 5px 0;"><strong>Costo:</strong> ${solution.get('costo_estimado', 0):,.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_comp_actions:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"🗑️", key=f"del_{i}", help="Eliminar de comparación"):
                        removed_name = st.session_state.comparison_list[i]['name']
                        st.session_state.comparison_list.pop(i)
                        st.success(f"✅ '{removed_name}' eliminada de la comparación")
                        st.rerun()
        
        # Botones de acción
        st.markdown("---")
        col_action1, col_action2, col_action3 = st.columns(3)
        
        with col_action1:
            if st.button("🔄 Realizar Comparación", type="primary"):
                if len(st.session_state.comparison_list) >= 2:
                    comparison = SolutionComparator.compare_solutions(st.session_state.comparison_list)
                    st.session_state.comparison_results = comparison
                    st.success("✅ Comparación realizada exitosamente")
                    st.rerun()
                else:
                    st.warning("⚠️ Necesitas al menos 2 soluciones para comparar")
        
        with col_action2:
            if st.button("🗑️ Limpiar Comparación", help="Eliminar todas las soluciones de la comparación"):
                st.session_state.comparison_list = []
                st.session_state.comparison_results = None
                st.warning("🗑️ Comparación limpiada")
                st.rerun()
        
        with col_action3:
            if st.button("📊 Exportar Comparación", help="Exportar a Excel"):
                if st.session_state.comparison_results:
                    # Crear DataFrame con resultados de comparación
                    comparison_data = st.session_state.comparison_results['detailed_comparison']
                    df_export = pd.DataFrame(comparison_data)
                    
                    # Exportar a Excel
                    from io import BytesIO
                    import xlsxwriter
                    
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df_export.to_excel(writer, index=False, sheet_name='Comparación')
                    writer.close()
                    
                    excel_data = output.getvalue()
                    output.close()
                    
                    # Crear enlace de descarga
                    b64 = base64.b64encode(excel_data).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="comparacion_soluciones.xlsx" style="display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">📊 Descargar Comparación Excel</a>'
                    st.markdown(href, unsafe_allow_html=True)
        
        # Mostrar resultados de comparación
        if st.session_state.comparison_results:
            comparison = st.session_state.comparison_results
            
            st.markdown("#### 📊 Resultados de la Comparación")
            
            # Tabla comparativa
            df_data = []
            for sol in comparison['detailed_comparison']:
                df_data.append({
                    'Solución': sol['name'],
                    'Tipo': sol['type'],
                    'Método': sol['method'],
                    'Q Compensación (kVAR)': f"{sol['q_compensacion']:.2f}",
                    'Componente': f"{sol['valor_componente']:.2f} {sol['unidad']}",
                    'Costo Estimado ($)': f"${sol['costo_estimado']:,.0f}",
                    'ROI Anual (%)': f"{sol.get('roi_anual', 0):.1f}",
                    'Score Económico': f"{sol['economic_score']:.0f}",
                    'Score Técnico': f"{sol['technical_score']:.1f}",
                    'Score Total': f"{sol.get('total_score', 0):.1f}"
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Mejores soluciones
            col_best1, col_best2, col_best3 = st.columns(3)
            
            with col_best1:
                if comparison.get('best_economic'):
                    best = comparison['best_economic']
                    st.markdown(f"""
                    <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; border: 2px solid #28a745; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h3 style="color: #155724; margin-bottom: 15px;">🏆 Mejor Solución Económica</h3>
                        <h4 style="color: #155724; margin-bottom: 10px;">{best['name']}</h4>
                        <p style="color: #333; margin: 5px 0;"><strong>Tipo:</strong> {best['type']}</p>
                        <p style="color: #333; margin: 5px 0;"><strong>Costo:</strong> ${best['costo_estimado']:,.0f}</p>
                        <p style="color: #333; margin: 5px 0;"><strong>ROI:</strong> {best.get('roi_anual', 0):.1f}% anual</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_best2:
                if comparison.get('best_technical'):
                    best = comparison['best_technical']
                    st.markdown(f"""
                    <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; border: 2px solid #2196f3; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h3 style="color: #0d47a1; margin-bottom: 15px;">⚡ Mejor Solución Técnica</h3>
                        <h4 style="color: #0d47a1; margin-bottom: 10px;">{best['name']}</h4>
                        <p style="color: #333; margin: 5px 0;"><strong>Tipo:</strong> {best['type']}</p>
                        <p style="color: #333; margin: 5px 0;"><strong>Score Técnico:</strong> {best['technical_score']:.1f}</p>
                        <p style="color: #333; margin: 5px 0;"><strong>Q Compensación:</strong> {best['q_compensacion']:.2f} kVAR</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_best3:
                if comparison.get('best_overall'):
                    best = comparison['best_overall']
                    st.markdown(f"""
                    <div style="background: #fff3e0; padding: 20px; border-radius: 10px; border: 2px solid #ff9800; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <h3 style="color: #e65100; margin-bottom: 15px;">🌟 Mejor Solución Global</h3>
                        <h4 style="color: #e65100; margin-bottom: 10px;">{best['name']}</h4>
                        <p style="color: #333; margin: 5px 0;"><strong>Tipo:</strong> {best['type']}</p>
                        <p style="color: #333; margin: 5px 0;"><strong>Score Total:</strong> {best.get('total_score', 0):.1f}</p>
                        <p style="color: #333; margin: 5px 0;"><strong>Balance:</strong> Económico + Técnico</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Gráfico comparativo
            st.markdown("#### 📈 Visualización Comparativa")
            fig = ChartGenerator.create_solution_comparison_chart(comparison)
            st.plotly_chart(fig, use_container_width=True, key="comparator_chart")
    else:
        st.info("ℹ️ No hay soluciones en comparación. Agrega cálculos desde el historial arriba.")

elif seccion == "📄 Reportes":
    st.header("📄 Generación de Reportes")
    
    if st.session_state.current_calculation:
        st.success("✅ Tienes datos para generar reporte")
        
        calc = st.session_state.current_calculation
        st.info(f"📋 Cálculo disponible: **{calc.get('name', 'Sin nombre')}** ({calc.get('method', 'paralelo')})")
        
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
        st.info("💡 Ve a 'Compensación Paralelo' para realizar un cálculo.")

# Footer
st.markdown("---")
st.markdown("""
**⚡ Calculadora de Compensación de Reactivos v2.0**  
*Arquitectura modular con plantillas, comparador de soluciones y reportes profesionales*
""")
