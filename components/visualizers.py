"""
Módulo de visualización de datos y gráficos
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math

class ChartGenerator:
    """Generador de gráficos para visualización de resultados"""
    
    @staticmethod
    def create_comparison_chart(resultados: dict, tipo: str = "paralelo") -> go.Figure:
        """Crea gráfico comparativo antes/después"""
        if tipo == "paralelo":
            categorias = ['Corriente [A]', 'Pérdidas [kW]', 'Ángulo φ [°]']
            valores_actuales = [resultados['i_actual'], resultados['perdidas_actuales'], resultados['phi1']]
            valores_compensados = [resultados['i_compensada'], resultados['perdidas_compensadas'], resultados['phi2']]
        else:  # serie
            categorias = ['Reactancia [Ω]', 'Corriente [A]', 'Potencia [kVA]']
            valores_actuales = [abs(resultados.get('x_compensacion') * 100/resultados.get('reduccion_porcentaje', 50)), 
                              resultados['i_actual'], resultados['potencia_aparente']]
            valores_compensados = [abs(resultados['x_total']), resultados['i_compensada'], resultados['potencia_aparente']]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Actual', x=categorias, y=valores_actuales, marker_color='lightcoral'))
        fig.add_trace(go.Bar(name='Compensado', x=categorias, y=valores_compensados, marker_color='lightgreen'))
        fig.update_layout(title='Comparación: Antes vs Después', barmode='group', height=400)
        return fig
    
    @staticmethod
    def create_power_triangle(resultados: dict) -> go.Figure:
        """Crea triángulo de potencias"""
        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "polar"}, {"type": "polar"}]], 
                          subplot_titles=['Antes', 'Después'])
        
        # Antes
        fig.add_trace(go.Scatterpolar(r=[0, resultados['q_actual'], resultados['potencia_activa']], 
                                     theta=[0, resultados['phi1'], 90], mode='lines+markers', 
                                     name='Actual', line_color='red'), row=1, col=1)
        
        # Después
        fig.add_trace(go.Scatterpolar(r=[0, resultados['q_deseado'], resultados['potencia_activa']], 
                                     theta=[0, resultados['phi2'], 90], mode='lines+markers', 
                                     name='Compensado', line_color='green'), row=1, col=2)
        
        fig.update_layout(title='Triángulo de Potencias', height=400, showlegend=False)
        return fig
    
    @staticmethod
    def create_series_impedance_chart(resultados: dict) -> go.Figure:
        """Crea gráfico de evolución de impedancias para compensación serie"""
        fig = go.Figure()
        
        # Datos para el gráfico
        etapas = ['Original', 'Compensación', 'Final']
        valores = [
            abs(resultados.get('x_compensacion') * 100/resultados.get('reduccion_porcentaje', 50)),
            resultados.get('x_compensacion', 0),
            abs(resultados.get('x_total', 0))
        ]
        
        fig.add_trace(go.Bar(
            name='Reactancia',
            x=etapas,
            y=valores,
            marker_color=['lightblue', 'orange', 'lightgreen']
        ))
        
        fig.update_layout(
            title='Evolución de Reactancia Serie',
            xaxis_title='Etapa del Proceso',
            yaxis_title='Reactancia [Ω]',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_solution_comparison_chart(comparison_data: dict) -> go.Figure:
        """Crea gráfico comparativo de múltiples soluciones"""
        solutions = comparison_data.get('detailed_comparison', [])
        
        fig = go.Figure()
        
        names = [s['name'] for s in solutions]
        economic_scores = [s['economic_score'] for s in solutions]
        technical_scores = [s['technical_score'] for s in solutions]
        
        fig.add_trace(go.Bar(name='Score Económico', x=names, y=economic_scores, marker_color='blue'))
        fig.add_trace(go.Bar(name='Score Técnico', x=names, y=technical_scores, marker_color='orange'))
        
        fig.update_layout(title='Comparación de Soluciones', barmode='group', height=400)
        return fig
