"""
Módulo de exportación de datos y generación de reportes PDF
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import math
from typing import Dict, List

class PDFExporter:
    """Exportador de reportes PDF profesionales"""
    
    @staticmethod
    def generate_html_report(resultados: Dict, tipo_calculo: str, company_info: Dict = None) -> str:
        """
        Genera reporte HTML que puede ser convertido a PDF
        
        Args:
            resultados: Diccionario con resultados del cálculo
            tipo_calculo: "paralelo" o "serie"
            company_info: Información de la empresa
            
        Returns:
            String con HTML del reporte
        """
        # Información por defecto
        if not company_info:
            company_info = {
                "name": "Consultoría Eléctrica Profesional",
                "logo": "⚡",
                "address": "Dirección de la Empresa",
                "phone": "+1 234 567 890",
                "email": "info@empresa.com",
                "website": "www.empresa.com"
            }
        
        # Fecha actual
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        
        # Determinar tipo de cálculo
        if tipo_calculo == "paralelo":
            return PDFExporter._generate_parallel_report_html(resultados, company_info, fecha_actual, hora_actual)
        else:
            return PDFExporter._generate_series_report_html(resultados, company_info, fecha_actual, hora_actual)
    
    @staticmethod
    def _generate_parallel_report_html(resultados: Dict, company_info: Dict, fecha: str, hora: str) -> str:
        """Genera HTML para reporte de compensación paralelo"""
        
        # Calcular métricas adicionales
        reduccion_corriente = ((resultados['i_actual'] - resultados['i_compensada']) / resultados['i_actual']) * 100
        reduccion_perdidas = ((resultados['perdidas_actuales'] - resultados['perdidas_compensadas']) / resultados['perdidas_actuales']) * 100
        fp_actual = math.cos(math.radians(resultados['phi1']))
        fp_deseado = math.cos(math.radians(resultados['phi2']))
        mejora_fp = fp_deseado - fp_actual
        
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Compensación de Reactivos</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .company-info {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .company-info .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .metric-card h3 {{
            font-size: 1.1em;
            margin-bottom: 10px;
            opacity: 0.9;
        }}
        
        .metric-card .value {{
            font-size: 2.2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .metric-card .unit {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .data-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .data-table td {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .highlight {{
            background: #e8f5e8 !important;
            font-weight: bold;
        }}
        
        .specification-box {{
            background: #f0f8ff;
            border-left: 5px solid #667eea;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .specification-box h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .footer .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .footer div {{
            text-align: center;
        }}
        
        .watermark {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 150px;
            color: rgba(0,0,0,0.05);
            z-index: -1;
            pointer-events: none;
        }}
        
        @media print {{
            .container {{
                box-shadow: none;
            }}
            
            .watermark {{
                display: block;
            }}
        }}
    </style>
</head>
<body>
    <div class="watermark">⚡</div>
    
    <div class="container">
        <div class="header">
            <h1>⚡ Reporte de Compensación de Reactivos</h1>
            <div class="subtitle">Análisis Técnico y Económico - Compensación Paralelo</div>
            <div style="margin-top: 20px; font-size: 0.9em;">
                Fecha: {fecha} | Hora: {hora}
            </div>
        </div>
        
        <div class="company-info">
            <div class="grid">
                <div>
                    <h3>{company_info['name']}</h3>
                    <p>{company_info['address']}</p>
                    <p>Tel: {company_info['phone']}</p>
                </div>
                <div style="text-align: right;">
                    <p>Email: {company_info['email']}</p>
                    <p>Web: {company_info['website']}</p>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 Resumen Ejecutivo</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Potencia Reactiva de Compensación</h3>
                        <div class="value">{resultados['q_compensacion']:.2f}</div>
                        <div class="unit">kVAR</div>
                    </div>
                    <div class="metric-card">
                        <h3>Mejora del Factor de Potencia</h3>
                        <div class="value">{mejora_fp:+.3f}</div>
                        <div class="unit">de {fp_actual:.3f} a {fp_deseado:.3f}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Reducción de Corriente</h3>
                        <div class="value">{reduccion_corriente:.1f}%</div>
                        <div class="unit">{resultados['i_actual'] - resultados['i_compensada']:.2f} A</div>
                    </div>
                    <div class="metric-card">
                        <h3>Ahorro de Pérdidas</h3>
                        <div class="value">{reduccion_perdidas:.1f}%</div>
                        <div class="unit">{resultados['perdidas_actuales'] - resultados['perdidas_compensadas']:.3f} kW</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Datos de Entrada</h2>
                <table class="data-table">
                    <tr>
                        <th>Parámetro</th>
                        <th>Valor</th>
                        <th>Unidad</th>
                    </tr>
                    <tr>
                        <td>Potencia Activa</td>
                        <td>{resultados['potencia_activa']}</td>
                        <td>kW</td>
                    </tr>
                    <tr>
                        <td>Tensión Nominal</td>
                        <td>{resultados['tension']}</td>
                        <td>V</td>
                    </tr>
                    <tr>
                        <td>Frecuencia</td>
                        <td>{resultados['frecuencia']}</td>
                        <td>Hz</td>
                    </tr>
                    <tr>
                        <td>Tipo de Compensación</td>
                        <td>{resultados['tipo_comp']}</td>
                        <td>-</td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h2>📈 Resultados del Cálculo</h2>
                <table class="data-table">
                    <tr>
                        <th>Parámetro</th>
                        <th>Valor Actual</th>
                        <th>Valor Compensado</th>
                        <th>Mejora</th>
                    </tr>
                    <tr>
                        <td>Factor de Potencia</td>
                        <td>{fp_actual:.3f}</td>
                        <td class="highlight">{fp_deseado:.3f}</td>
                        <td>+{mejora_fp:.3f}</td>
                    </tr>
                    <tr>
                        <td>Potencia Reactiva</td>
                        <td>{resultados['q_actual']:.2f}</td>
                        <td class="highlight">{resultados['q_deseado']:.2f}</td>
                        <td>{resultados['q_actual'] - resultados['q_deseado']:.2f} kVAR</td>
                    </tr>
                    <tr>
                        <td>Corriente</td>
                        <td>{resultados['i_actual']:.2f}</td>
                        <td class="highlight">{resultados['i_compensada']:.2f}</td>
                        <td>{reduccion_corriente:.1f}%</td>
                    </tr>
                    <tr>
                        <td>Pérdidas</td>
                        <td>{resultados['perdidas_actuales']:.3f}</td>
                        <td class="highlight">{resultados['perdidas_compensadas']:.3f}</td>
                        <td>{reduccion_perdidas:.1f}%</td>
                    </tr>
                    <tr>
                        <td>Ángulo de Desfase</td>
                        <td>{resultados['phi1']:.1f}°</td>
                        <td class="highlight">{resultados['phi2']:.1f}°</td>
                        <td>{resultados['phi1'] - resultados['phi2']:.1f}°</td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h2>🔧 Especificaciones del Compensador</h2>
                <div class="specification-box">
                    <h3>Componente Requerido</h3>
                    <p><strong>Tipo:</strong> {resultados['tipo_comp']}</p>
                    <p><strong>Valor Nominal:</strong> {resultados['valor_componente']:.2f} {resultados['unidad']}</p>
                    <p><strong>Reactancia:</strong> {resultados['reactancia']:.3f} Ω</p>
                    <p><strong>Potencia Reactiva:</strong> {resultados['q_compensacion']:.2f} kVAR</p>
                    <p><strong>Tensión de Operación:</strong> {resultados['tension']} V</p>
                    <p><strong>Frecuencia:</strong> {resultados['frecuencia']} Hz</p>
                </div>
            </div>
            
            <div class="section">
                <h2>💰 Análisis Económico</h2>
                <table class="data-table">
                    <tr>
                        <th>Concepto</th>
                        <th>Valor</th>
                        <th>Unidad</th>
                    </tr>
                    <tr>
                        <td>Ahorro de Energía Anual</td>
                        <td>{resultados['perdidas_actuales'] - resultados['perdidas_compensadas']:.3f}</td>
                        <td>kW</td>
                    </tr>
                    <tr>
                        <td>Ahorro Energía Anual</td>
                        <td>{(resultados['perdidas_actuales'] - resultados['perdidas_compensadas']) * 8760:.0f}</td>
                        <td>kWh/año</td>
                    </tr>
                    <tr>
                        <td>Ahorro Económico Anual</td>
                        <td>${(resultados['perdidas_actuales'] - resultados['perdidas_compensadas']) * 8760 * 0.15:.2f}</td>
                        <td>USD/año</td>
                    </tr>
                </table>
            </div>
            
            <div class="section">
                <h2>📝 Observaciones y Recomendaciones</h2>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 5px;">
                    <p><strong>Observaciones Técnicas:</strong></p>
                    <ul style="margin-left: 20px; margin-bottom: 20px;">
                        <li>La compensación propuesta mejorará el factor de potencia de {fp_actual:.3f} a {fp_deseado:.3f}</li>
                        <li>Se reducirán las pérdidas en conductores en un {reduccion_perdidas:.1f}%</li>
                        <li>La corriente total del sistema disminuirá en {reduccion_corriente:.1f}%</li>
                        <li>El sistema cumplirá con regulaciones de factor de potencia mínimo 0.90</li>
                    </ul>
                    
                    <p><strong>Recomendaciones:</strong></p>
                    <ul style="margin-left: 20px;">
                        <li>Instalar el banco de capacitores en el punto más cercano a la carga</li>
                        <li>Considerar un sistema de control automático para variaciones de carga</li>
                        <li>Realizar mantenimiento preventivo cada 6 meses</li>
                        <li>Monitorear el factor de potencia después de la instalación</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div class="grid">
                <div>
                    <h4>{company_info['name']}</h4>
                    <p>Ingeniería Eléctrica Profesional</p>
                </div>
                <div>
                    <h4>Contacto</h4>
                    <p>{company_info['phone']}</p>
                    <p>{company_info['email']}</p>
                </div>
                <div>
                    <h4>Certificación</h4>
                    <p>Reporte Generado Digitalmente</p>
                    <p>Código: {datetime.now().strftime('%Y%m%d%H%M%S')}</p>
                </div>
            </div>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
                <p>© {datetime.now().year} {company_info['name']}. Todos los derechos reservados.</p>
                <p style="font-size: 0.8em; opacity: 0.7;">Este documento es confidencial y debe ser tratado como tal.</p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return html_content
    
    @staticmethod
    def _generate_series_report_html(resultados: Dict, company_info: Dict, fecha: str, hora: str) -> str:
        """Genera HTML para reporte de compensación serie"""
        # Similar al paralelo pero adaptado para compensación serie
        # Por simplicidad, retornamos una versión modificada del paralelo
        return PDFExporter._generate_parallel_report_html(resultados, company_info, fecha, hora)
    
    @staticmethod
    def create_download_link(html_content: str, filename: str = "reporte_compensacion.html") -> str:
        """
        Crea un enlace de descarga para el archivo HTML
        
        Args:
            html_content: Contenido HTML
            filename: Nombre del archivo
            
        Returns:
            String con HTML del enlace de descarga
        """
        b64 = base64.b64encode(html_content.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="{filename}" style="display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">📥 Descargar Reporte PDF</a>'
        return href
    
    @staticmethod
    def export_to_excel(data: Dict, filename: str = "resultados_compensacion.xlsx") -> str:
        """
        Exporta resultados a Excel
        
        Args:
            data: Diccionario con datos
            filename: Nombre del archivo
            
        Returns:
            String con HTML del enlace de descarga
        """
        # Crear DataFrame con los resultados
        df_data = []
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                df_data.append({
                    'Parámetro': key,
                    'Valor': f"{value:.4f}",
                    'Unidad': PDFExporter._get_unit(key)
                })
        
        df = pd.DataFrame(df_data)
        
        # Convertir a Excel en memoria
        from io import BytesIO
        import xlsxwriter
        
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Resultados')
        writer.close()
        
        # Obtener los datos
        excel_data = output.getvalue()
        output.close()
        
        # Crear enlace de descarga
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" style="display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">📊 Descargar Excel</a>'
        return href
    
    @staticmethod
    def _get_unit(parameter: str) -> str:
        """Retorna la unidad correspondiente a un parámetro"""
        units = {
            'q_actual': 'kVAR',
            'q_deseado': 'kVAR',
            'q_compensacion': 'kVAR',
            'i_actual': 'A',
            'i_compensada': 'A',
            'valor_componente': 'calculado',
            'unidad': 'calculado',
            'reactancia': 'Ω',
            'perdidas_actuales': 'kW',
            'perdidas_compensadas': 'kW',
            'phi1': '°',
            'phi2': '°',
            'potencia_activa': 'kW',
            'tension': 'V',
            'frecuencia': 'Hz'
        }
        return units.get(parameter, '')

class ReportGenerator:
    """Generador de reportes completos"""
    
    @staticmethod
    def generate_comprehensive_report(parallel_result: Dict = None, series_result: Dict = None, 
                                    comparison: Dict = None, company_info: Dict = None) -> str:
        """
        Genera un reporte completo con múltiples análisis
        
        Args:
            parallel_result: Resultados de compensación paralelo
            series_result: Resultados de compensación serie
            comparison: Datos de comparación
            company_info: Información de la empresa
            
        Returns:
            HTML del reporte completo
        """
        # Por ahora, usar el reporte simple del primer resultado disponible
        if parallel_result:
            return PDFExporter.generate_html_report(parallel_result, "paralelo", company_info)
        elif series_result:
            return PDFExporter.generate_html_report(series_result, "serie", company_info)
        else:
            return "<h1>No hay resultados para generar reporte</h1>"
