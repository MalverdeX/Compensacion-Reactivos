"""
Módulo de cálculos matemáticos para compensación de reactivos
"""
import math
import numpy as np
from typing import Dict, Tuple, Optional

class PowerCalculator:
    """Clase principal para cálculos de potencia y compensación"""
    
    @staticmethod
    def calculate_parallel_compensation(
        potencia_activa: float,
        fp_actual: float,
        fp_deseado: float,
        tension: float,
        frecuencia: float,
        tipo_comp: str
    ) -> Dict:
        """
        Calcula la compensación paralelo
        
        Args:
            potencia_activa: Potencia activa en kW
            fp_actual: Factor de potencia actual (0.1-0.99)
            fp_deseado: Factor de potencia deseado (0.1-0.99)
            tension: Tensión nominal en V
            frecuencia: Frecuencia en Hz
            tipo_comp: "Capacitiva" o "Inductiva"
            
        Returns:
            Diccionario con todos los resultados del cálculo
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
            'phi2': math.degrees(phi2),
            'potencia_activa': potencia_activa,
            'tension': tension,
            'frecuencia': frecuencia,
            'tipo_comp': tipo_comp
        }
    
    @staticmethod
    def calculate_series_compensation(
        corriente: float,
        reactancia_carga: float,
        tension: float,
        frecuencia: float,
        tipo_comp: str,
        porcentaje_reduccion: float
    ) -> Optional[Dict]:
        """
        Calcula la compensación serie
        
        Args:
            corriente: Corriente de carga en A
            reactancia_carga: Reactancia de carga en Ω
            tension: Tensión nominal en V
            frecuencia: Frecuencia en Hz
            tipo_comp: "Capacitiva" o "Inductiva"
            porcentaje_reduccion: Porcentaje de reducción deseado
            
        Returns:
            Diccionario con resultados o None si hay error
        """
        # Validar reactancia
        if abs(reactancia_carga) < 0.001:
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
            'potencia_aparente': potencia_aparente_actual / 1000,  # kVA
            'corriente': corriente,
            'reactancia_carga': reactancia_carga,
            'tension': tension,
            'frecuencia': frecuencia,
            'tipo_comp': tipo_comp
        }
    
    @staticmethod
    def calculate_economic_analysis(
        perdidas_actuales: float,
        perdidas_compensadas: float,
        costo_componente: float,
        horas_operacion_anual: float = 8760,
        costo_kwh: float = 0.15
    ) -> Dict:
        """
        Calcula análisis económico de la compensación
        
        Args:
            perdidas_actuales: Pérdidas actuales en kW
            perdidas_compensadas: Pérdidas compensadas en kW
            costo_componente: Costo del componente en $
            horas_operacion_anual: Horas de operación anual
            costo_kwh: Costo por kWh en $
            
        Returns:
            Diccionario con análisis económico
        """
        ahorro_anual_kwh = (perdidas_actuales - perdidas_compensadas) * horas_operacion_anual
        ahorro_anual_usd = ahorro_anual_kwh * costo_kwh
        periodo_recuperacion = costo_componente / ahorro_anual_usd if ahorro_anual_usd > 0 else float('inf')
        roi_anual = (ahorro_anual_usd / costo_componente) * 100 if costo_componente > 0 else 0
        
        return {
            'ahorro_anual_kwh': ahorro_anual_kwh,
            'ahorro_anual_usd': ahorro_anual_usd,
            'periodo_recuperacion': periodo_recuperacion,
            'roi_anual': roi_anual,
            'costo_componente': costo_componente,
            'horas_operacion_anual': horas_operacion_anual,
            'costo_kwh': costo_kwh
        }

class SolutionComparator:
    """Clase para comparar múltiples soluciones de compensación"""
    
    @staticmethod
    def compare_solutions(solutions: list) -> Dict:
        """
        Compara múltiples soluciones de compensación
        
        Args:
            solutions: Lista de diccionarios con resultados de cálculos
            
        Returns:
            Diccionario con análisis comparativo
        """
        if not solutions:
            return {}
        
        comparison = {
            'num_solutions': len(solutions),
            'best_economic': None,
            'best_technical': None,
            'detailed_comparison': []
        }
        
        best_economic_score = float('inf')
        best_technical_score = float('-inf')
        
        for i, solution in enumerate(solutions):
            # Calcular scores
            economic_score = SolutionComparator._calculate_economic_score(solution)
            technical_score = SolutionComparator._calculate_technical_score(solution)
            
            solution_data = {
                'index': i,
                'name': solution.get('name', f'Solución {i+1}'),
                'type': solution.get('tipo_comp', 'Desconocido'),
                'method': solution.get('method', 'Desconocido'),
                'economic_score': economic_score,
                'technical_score': technical_score,
                'q_compensacion': solution.get('q_compensacion', 0),
                'reduccion_perdidas': solution.get('reduccion_perdidas', 0),
                'costo_estimado': solution.get('costo_estimado', 0),
                'periodo_recuperacion': solution.get('periodo_recuperacion', float('inf'))
            }
            
            comparison['detailed_comparison'].append(solution_data)
            
            # Mejor solución económica
            if economic_score < best_economic_score:
                best_economic_score = economic_score
                comparison['best_economic'] = solution_data
            
            # Mejor solución técnica
            if technical_score > best_technical_score:
                best_technical_score = technical_score
                comparison['best_technical'] = solution_data
        
        return comparison
    
    @staticmethod
    def _calculate_economic_score(solution: Dict) -> float:
        """Calcula score económico (menor es mejor)"""
        costo = solution.get('costo_estimado', 0)
        recuperacion = solution.get('periodo_recuperacion', float('inf'))
        ahorro_anual = solution.get('ahorro_anual_usd', 0)
        
        if ahorro_anual <= 0:
            return float('inf')
        
        # Score combinado de costo y período de recuperación
        return costo * 0.6 + recuperacion * 1000 * 0.4
    
    @staticmethod
    def _calculate_technical_score(solution: Dict) -> float:
        """Calcula score técnico (mayor es mejor)"""
        reduccion_perdidas = solution.get('reduccion_perdidas', 0)
        mejora_fp = solution.get('mejora_fp', 0)
        q_compensacion = solution.get('q_compensacion', 0)
        
        # Penalizar compensaciones muy grandes
        penalty = max(0, q_compensacion - 100) * 0.1
        
        return reduccion_perdidas * 0.5 + mejora_fp * 30 - penalty
