"""
Módulo de cálculos matemáticos para compensación de reactivos
"""
import math
from typing import Dict, List, Tuple, Optional

class PowerCalculator:
    """Clase principal para cálculos de potencia y compensación"""
    
    @staticmethod
    def calculate_parallel_compensation(
        potencia_activa: float,
        fp_actual: float,
        fp_deseado: float,
        tension: float,
        frecuencia: float,
        tipo_comp: str,
        resistencia_conductor: float = 0.1,
        longitud_conductor: float = 1.0
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
            resistencia_conductor: Resistencia del conductor en Ω/km (default: 0.1)
            longitud_conductor: Longitud del conductor en km (default: 1.0)
            
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
        
        # Corrientes (sistema trifásico)
        i_actual = P_w / (math.sqrt(3) * tension * fp_actual)
        i_compensada = P_w / (math.sqrt(3) * tension * fp_deseado)
        
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
        
        # Pérdidas (cálculo realista basado en porcentaje de la carga)
        # Las pérdidas en conductores suelen ser 1-5% de la potencia activa
        porcentaje_perdidas = 0.03  # 3% de pérdidas (típico industrial)
        perdidas_actuales = potencia_activa * porcentaje_perdidas  # kW
        
        # Para compensación paralelo, las pérdidas se reducen proporcionalmente
        if i_compensada > 0 and i_actual > 0:
            factor_reduccion = i_compensada / i_actual
            perdidas_compensadas = perdidas_actuales * factor_reduccion
        else:
            perdidas_compensadas = perdidas_actuales  # Sin compensación
        
        # Pérdidas por efecto Joule (opcional, si se proporcionan datos de conductor)
        perdidas_joule_actuales = 0
        perdidas_joule_compensadas = 0
        if resistencia_conductor > 0 and longitud_conductor > 0:
            # P = √3 × I² × R (sistema trifásico)
            perdidas_joule_actuales = math.sqrt(3) * (i_actual ** 2) * resistencia_conductor * longitud_conductor / 1000  # kW
            perdidas_joule_compensadas = math.sqrt(3) * (i_compensada ** 2) * resistencia_conductor * longitud_conductor / 1000  # kW
        
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
        potencia_aparente_actual = math.sqrt(3) * tension * corriente / 1000  # kVA
        impedancia_actual = abs(reactancia_carga)
        impedancia_compensada = abs(x_total)
        
        # Corriente compensada (correcta para sistema trifásico)
        if impedancia_compensada > 0:
            i_compensada = math.sqrt(3) * tension / (math.sqrt(3) * impedancia_compensada)  # I = V/(√3×Z)
        else:
            i_compensada = corriente  # Sin cambio
        
        # Pérdidas realistas (basado en porcentaje de la potencia aparente)
        porcentaje_perdidas = 0.03  # 3% de pérdidas (típico industrial)
        perdidas_actuales = potencia_aparente_actual * porcentaje_perdidas  # kW
        perdidas_compensadas = (math.sqrt(3) * tension * i_compensada / 1000) * porcentaje_perdidas  # kW
        
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
        costo_kwh: float = None,
        multa_fp_bajo: float = None,
        corriente_actual: float = None,
        corriente_compensada: float = None,
        resistencia_conductor: float = 0.1,
        longitud_conductor: float = 1.0
    ) -> Dict:
        """
        Análisis económico mejorado con valores realistas
        
        Args:
            perdidas_actuales: Pérdidas actuales en kW
            perdidas_compensadas: Pérdidas compensadas en kW
            costo_componente: Costo del componente en USD
            horas_operacion_anual: Horas de operación anual
            costo_kwh: Costo por kWh (default: $0.12)
            multa_fp_bajo: Multa por FP bajo (default: $5.0/kW-mes)
            corriente_actual: Corriente actual en A
            corriente_compensada: Corriente compensada en A
            resistencia_conductor: Resistencia del conductor en Ω/km
            longitud_conductor: Longitud del conductor en km
            
        Returns:
            Diccionario con análisis económico completo
        """
        
        # Valores por defecto realistas
        if costo_kwh is None:
            costo_kwh = 0.12  # $0.12 USD/kWh (promedio industrial)
        if multa_fp_bajo is None:
            multa_fp_bajo = 5.0  # $5.0 USD/kW-mes (típico para FP < 0.9)
        
        # 1. Ahorro por reducción de pérdidas tradicionales
        # Las pérdidas reales suelen ser 1-5% de la carga total
        ahorro_tradicional_kwh = (perdidas_actuales - perdidas_compensadas) * horas_operacion_anual
        ahorro_tradicional_usd = ahorro_tradicional_kwh * costo_kwh
        
        # 2. Ahorro por reducción de pérdidas por efecto Joule (I²R)
        # Usando valores realistas: resistencia 0.1 Ω/km, longitud 1 km
        ahorro_joule_usd = 0
        if corriente_actual is not None and corriente_compensada is not None:
            # Pérdidas por efecto Joule: P = 3 * I² * R (sistema trifásico)
            # Usando valores realistas de resistencia y longitud
            perdidas_joule_actuales = 3 * (corriente_actual ** 2) * resistencia_conductor * longitud_conductor / 1000  # kW
            perdidas_joule_compensadas = 3 * (corriente_compensada ** 2) * resistencia_conductor * longitud_conductor / 1000  # kW
            
            ahorro_joule_kw = perdidas_joule_actuales - perdidas_joule_compensadas
            ahorro_joule_kwh = ahorro_joule_kw * horas_operacion_anual
            ahorro_joule_usd = ahorro_joule_kwh * costo_kwh
        
        # 3. Ahorro por multas de factor de potencia
        # Cálculo más realista basado en la potencia activa
        ahorro_multa_usd = 0
        if perdidas_actuales > 0 and perdidas_compensadas > 0:
            # Estimar potencia activa basada en pérdidas (asumiendo fp ≈ 0.8)
            potencia_activa_estimada = perdidas_actuales / 0.05  # Si pérdidas son 5% de P_activa
            fp_mejora = 0.02  # Mejora típica de FP
            
            # Cálculo de multa basado en la potencia activa
            multa_base = multa_fp_bajo * potencia_activa_estimada
            ahorro_multa_mensual = multa_base * fp_mejora * 0.3  # Factor conservador
            ahorro_multa_usd = ahorro_multa_mensual * 12  # Anual
        
        # 4. Ahorro total anual
        ahorro_anual_usd = ahorro_tradicional_usd + ahorro_joule_usd + ahorro_multa_usd
        ahorro_anual_kwh = ahorro_tradicional_kwh + (ahorro_joule_usd / costo_kwh if costo_kwh > 0 else 0)
        
        # 5. Cálculo de ROI y período de recuperación
        if ahorro_anual_usd > 0 and costo_componente > 0:
            periodo_recuperacion = costo_componente / ahorro_anual_usd
            roi_anual = (ahorro_anual_usd / costo_componente) * 100
        else:
            periodo_recuperacion = float('inf') if costo_componente > 0 else 0
            roi_anual = 0
        
        return {
            'ahorro_anual_kwh': ahorro_anual_kwh,
            'ahorro_anual_usd': ahorro_anual_usd,
            'ahorro_tradicional_usd': ahorro_tradicional_usd,
            'ahorro_joule_usd': ahorro_joule_usd,
            'ahorro_multa_usd': ahorro_multa_usd,
            'periodo_recuperacion': periodo_recuperacion,
            'roi_anual': roi_anual,
            'costo_componente': costo_componente,
            'horas_operacion_anual': horas_operacion_anual,
            'costo_kwh': costo_kwh,
            'multa_fp_bajo': multa_fp_bajo,
            'perdidas_joule_reducidas_kw': 3 * ((corriente_actual ** 2) - (corriente_compensada ** 2)) * resistencia_conductor * longitud_conductor / 1000 if corriente_actual is not None else 0
        }

class SolutionComparator:
    """Clase para comparar múltiples soluciones de compensación"""
    
    @staticmethod
    def compare_solutions(solutions: List[Dict]) -> Dict:
        """
        Compara múltiples soluciones de compensación
        
        Args:
            solutions: Lista de diccionarios con resultados de cálculos
            
        Returns:
            Diccionario con análisis comparativo
        """
        if not solutions or len(solutions) < 2:
            return {"error": "Se necesitan al menos 2 soluciones para comparar"}
        
        # Calcular scores para cada solución
        scored_solutions = []
        
        for i, sol in enumerate(solutions):
            # Score económico (menor costo = mejor score)
            max_cost = max([s.get('costo_estimado', 0) for s in solutions])
            min_cost = min([s.get('costo_estimado', 0) for s in solutions])
            
            if max_cost > min_cost:
                economic_score = 100 * (1 - (sol.get('costo_estimado', 0) - min_cost) / (max_cost - min_cost))
            else:
                economic_score = 100
            
            # Score técnico (basado en eficiencia y parametros)
            if sol.get('method') == 'paralelo':
                # Para compensación paralelo: mayor reducción de corriente = mejor
                reduction = ((sol.get('i_actual', 0) - sol.get('i_compensada', 0)) / sol.get('i_actual', 1)) * 100
                technical_score = min(100, reduction * 2)  # 50% reducción = 100 puntos
            else:
                # Para compensación serie: mayor reducción de reactancia = mejor
                reduction = sol.get('reduccion_porcentaje', 0)
                technical_score = min(100, reduction * 1.11)  # 90% reducción = 100 puntos
            
            # Score total (promedio ponderado)
            total_score = (economic_score * 0.6) + (technical_score * 0.4)
            
            # Agregar scores a la solución
            scored_sol = sol.copy()
            scored_sol.update({
                'economic_score': economic_score,
                'technical_score': technical_score,
                'total_score': total_score,
                'type': f"{sol.get('tipo_comp', 'Capacitiva')} {sol.get('method', 'paralelo').capitalize()}",
                'name': sol.get('name', f'Solución {i+1}')
            })
            
            scored_solutions.append(scored_sol)
        
        # Encontrar mejores soluciones
        best_economic = max(scored_solutions, key=lambda x: x['economic_score'])
        best_technical = max(scored_solutions, key=lambda x: x['technical_score'])
        best_overall = max(scored_solutions, key=lambda x: x['total_score'])
        
        return {
            'detailed_comparison': scored_solutions,
            'best_economic': best_economic,
            'best_technical': best_technical,
            'best_overall': best_overall,
            'total_solutions': len(solutions)
        }
