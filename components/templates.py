"""
Módulo de plantillas y preconfiguraciones para casos comunes
"""
import json
from typing import Dict, List

class TemplateManager:
    """Gestor de plantillas preconfiguradas"""
    
    @staticmethod
    def get_templates() -> Dict:
        """
        Retorna diccionario con todas las plantillas disponibles
        """
        return {
            "industrial": {
                "name": "Aplicaciones Industriales",
                "description": "Configuraciones típicas para entornos industriales",
                "templates": {
                    "motor_pequeno": {
                        "name": "Motor Eléctrico Pequeño (5-50 HP)",
                        "description": "Motor trifásico de pequeña potencia",
                        "icon": "⚙️",
                        "params": {
                            "potencia_activa": 15.0,
                            "fp_actual": 0.75,
                            "fp_deseado": 0.95,
                            "tension": 380,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [5, 50],
                            "fp_actual": [0.65, 0.85],
                            "tension": [220, 440]
                        }
                    },
                    "motor_grande": {
                        "name": "Motor Eléctrico Grande (100-500 HP)",
                        "description": "Motor trifásico de gran potencia",
                        "icon": "🏭",
                        "params": {
                            "potencia_activa": 200.0,
                            "fp_actual": 0.78,
                            "fp_deseado": 0.95,
                            "tension": 4160,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [100, 500],
                            "fp_actual": [0.70, 0.85],
                            "tension": [2300, 13800]
                        }
                    },
                    "soldadora": {
                        "name": "Equipo de Soldadura",
                        "description": "Máquina de soldar industrial",
                        "icon": "⚡",
                        "params": {
                            "potencia_activa": 25.0,
                            "fp_actual": 0.60,
                            "fp_deseado": 0.90,
                            "tension": 480,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [10, 100],
                            "fp_actual": [0.50, 0.70],
                            "tension": [208, 600]
                        }
                    }
                }
            },
            "commercial": {
                "name": "Aplicaciones Comerciales",
                "description": "Configuraciones para edificios y oficinas",
                "templates": {
                    "edificio_oficinas": {
                        "name": "Edificio de Oficinas",
                        "description": "Sistema de iluminación y equipos de oficina",
                        "icon": "🏢",
                        "params": {
                            "potencia_activa": 150.0,
                            "fp_actual": 0.85,
                            "fp_deseado": 0.95,
                            "tension": 220,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [50, 500],
                            "fp_actual": [0.75, 0.90],
                            "tension": [120, 480]
                        }
                    },
                    "centro_comercial": {
                        "name": "Centro Comercial",
                        "description": "Sistema mixto con iluminación y HVAC",
                        "icon": "🛍️",
                        "params": {
                            "potencia_activa": 500.0,
                            "fp_actual": 0.80,
                            "fp_deseado": 0.95,
                            "tension": 480,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [200, 2000],
                            "fp_actual": [0.70, 0.85],
                            "tension": [208, 600]
                        }
                    },
                    "hospital": {
                        "name": "Hospital/Centro Médico",
                        "description": "Equipos médicos y sistemas críticos",
                        "icon": "🏥",
                        "params": {
                            "potencia_activa": 800.0,
                            "fp_actual": 0.88,
                            "fp_deseado": 0.95,
                            "tension": 480,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [300, 3000],
                            "fp_actual": [0.80, 0.92],
                            "tension": [208, 13800]
                        }
                    }
                }
            },
            "residencial": {
                "name": "Aplicaciones Residenciales",
                "description": "Configuraciones para viviendas y condominios",
                "templates": {
                    "casa_familiar": {
                        "name": "Casa Familiar",
                        "description": "Sistema residencial típico",
                        "icon": "🏠",
                        "params": {
                            "potencia_activa": 8.0,
                            "fp_actual": 0.90,
                            "fp_deseado": 0.95,
                            "tension": 240,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [3, 20],
                            "fp_actual": [0.85, 0.95],
                            "tension": [120, 240]
                        }
                    },
                    "condominio": {
                        "name": "Edificio de Apartamentos",
                        "description": "Sistema para múltiples unidades residenciales",
                        "icon": "🏘️",
                        "params": {
                            "potencia_activa": 100.0,
                            "fp_actual": 0.85,
                            "fp_deseado": 0.95,
                            "tension": 240,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [50, 500],
                            "fp_actual": [0.80, 0.90],
                            "tension": [120, 480]
                        }
                    }
                }
            },
            "special": {
                "name": "Aplicaciones Especiales",
                "description": "Casos especiales y configuraciones avanzadas",
                "templates": {
                    "centro_datos": {
                        "name": "Centro de Datos",
                        "description": "Sistema para servidores y equipos TI",
                        "icon": "💾",
                        "params": {
                            "potencia_activa": 1000.0,
                            "fp_actual": 0.92,
                            "fp_deseado": 0.96,
                            "tension": 480,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [500, 5000],
                            "fp_actual": [0.88, 0.95],
                            "tension": [208, 13800]
                        }
                    },
                    "planta_tratamiento": {
                        "name": "Planta de Tratamiento de Agua",
                        "description": "Bombas y sistemas de control",
                        "icon": "💧",
                        "params": {
                            "potencia_activa": 300.0,
                            "fp_actual": 0.72,
                            "fp_deseado": 0.93,
                            "tension": 4160,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva"
                        },
                        "typical_range": {
                            "potencia_activa": [100, 2000],
                            "fp_actual": [0.65, 0.80],
                            "tension": [2300, 13800]
                        }
                    },
                    "linea_transmision": {
                        "name": "Línea de Transmisión",
                        "description": "Compensación serie para línea larga",
                        "icon": "🗼",
                        "params": {
                            "corriente": 500.0,
                            "reactancia_carga": 50.0,
                            "tension": 13800,
                            "frecuencia": 60,
                            "tipo_comp": "Capacitiva",
                            "reduccion_porcentaje": 60
                        },
                        "method": "serie",
                        "typical_range": {
                            "corriente": [100, 2000],
                            "reactancia_carga": [10, 200],
                            "tension": [4160, 345000]
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def get_template_by_id(category: str, template_id: str) -> Dict:
        """
        Obtiene una plantilla específica por categoría y ID
        
        Args:
            category: Categoría de la plantilla
            template_id: ID de la plantilla
            
        Returns:
            Diccionario con la plantilla o diccionario vacío si no existe
        """
        templates = TemplateManager.get_templates()
        
        if category in templates and template_id in templates[category]["templates"]:
            return templates[category]["templates"][template_id]
        
        return {}
    
    @staticmethod
    def get_all_templates_flat() -> List[Dict]:
        """
        Retorna todas las plantillas en una lista plana
        
        Returns:
            Lista de diccionarios con todas las plantillas
        """
        templates = TemplateManager.get_templates()
        flat_list = []
        
        for category_name, category_data in templates.items():
            for template_id, template_data in category_data["templates"].items():
                template = template_data.copy()
                template["category"] = category_name
                template["template_id"] = template_id
                template["category_name"] = category_data["name"]
                flat_list.append(template)
        
        return flat_list
    
    @staticmethod
    def search_templates(query: str) -> List[Dict]:
        """
        Busca plantillas por texto
        
        Args:
            query: Texto a buscar
            
        Returns:
            Lista de plantillas que coinciden con la búsqueda
        """
        all_templates = TemplateManager.get_all_templates_flat()
        query_lower = query.lower()
        
        results = []
        for template in all_templates:
            if (query_lower in template["name"].lower() or 
                query_lower in template["description"].lower()):
                results.append(template)
        
        return results
    
    @staticmethod
    def get_recommended_templates(potencia: float, tension: float) -> List[Dict]:
        """
        Recomienda plantillas basadas en potencia y tensión
        
        Args:
            potencia: Potencia activa en kW
            tension: Tensión en V
            
        Returns:
            Lista de plantillas recomendadas ordenadas por relevancia
        """
        all_templates = TemplateManager.get_all_templates_flat()
        
        # Filtrar solo plantillas paralelo (las que tienen potencia_activa)
        parallel_templates = [t for t in all_templates if "potencia_activa" in t["params"]]
        
        # Calcular score de relevancia
        scored_templates = []
        for template in parallel_templates:
            params = template["params"]
            typical_range = template.get("typical_range", {})
            
            # Score basado en qué tan cerca está de los rangos típicos
            score = 0
            
            # Score de potencia
            if "potencia_activa" in typical_range:
                min_p, max_p = typical_range["potencia_activa"]
                if min_p <= potencia <= max_p:
                    score += 50
                else:
                    # Penalización por distancia al rango
                    distance = min(abs(potencia - min_p), abs(potencia - max_p))
                    score -= min(distance / 10, 20)
            
            # Score de tensión
            if "tension" in typical_range:
                min_v, max_v = typical_range["tension"]
                if min_v <= tension <= max_v:
                    score += 50
                else:
                    # Penalización por distancia al rango
                    distance = min(abs(tension - min_v), abs(tension - max_v))
                    score -= min(distance / 1000, 20)
            
            scored_templates.append((score, template))
        
        # Ordenar por score (mayor a menor)
        scored_templates.sort(key=lambda x: x[0], reverse=True)
        
        # Retornar las 5 mejores recomendaciones
        return [template for score, template in scored_templates[:5] if score > 0]

class ComponentDatabase:
    """Base de datos de componentes comerciales"""
    
    @staticmethod
    def get_capacitor_bank_costs() -> Dict:
        """
        Retorna costos estimados de bancos de capacitores
        """
        return {
            "low_voltage": {
                "range": "208-600V",
                "units": [
                    {"kvar": 5, "cost_usd": 150, "brand": "Generic"},
                    {"kvar": 10, "cost_usd": 250, "brand": "Generic"},
                    {"kvar": 15, "cost_usd": 350, "brand": "Generic"},
                    {"kvar": 20, "cost_usd": 450, "brand": "Generic"},
                    {"kvar": 25, "cost_usd": 550, "brand": "Generic"},
                    {"kvar": 30, "cost_usd": 650, "brand": "Generic"},
                    {"kvar": 50, "cost_usd": 950, "brand": "Eaton"},
                    {"kvar": 75, "cost_usd": 1350, "brand": "Eaton"},
                    {"kvar": 100, "cost_usd": 1750, "brand": "Eaton"},
                    {"kvar": 150, "cost_usd": 2500, "brand": "Schneider"},
                    {"kvar": 200, "cost_usd": 3200, "brand": "Schneider"},
                    {"kvar": 300, "cost_usd": 4500, "brand": "Schneider"}
                ]
            },
            "medium_voltage": {
                "range": "4.16kV-34.5kV",
                "units": [
                    {"kvar": 300, "cost_usd": 8000, "brand": "GE"},
                    {"kvar": 600, "cost_usd": 14000, "brand": "GE"},
                    {"kvar": 900, "cost_usd": 20000, "brand": "ABB"},
                    {"kvar": 1200, "cost_usd": 26000, "brand": "ABB"},
                    {"kvar": 1800, "cost_usd": 38000, "brand": "Siemens"},
                    {"kvar": 2400, "cost_usd": 48000, "brand": "Siemens"},
                    {"kvar": 3600, "cost_usd": 70000, "brand": "Siemens"}
                ]
            }
        }
    
    @staticmethod
    def estimate_component_cost(q_compensacion: float, tension: float) -> float:
        """
        Estima el costo de un componente basado en kVAR y tensión
        
        Args:
            q_compensacion: Potencia reactiva en kVAR
            tension: Tensión en V
            
        Returns:
            Costo estimado en USD
        """
        costs = ComponentDatabase.get_capacitor_bank_costs()
        
        # Determinar categoría de tensión
        if tension <= 600:
            category = "low_voltage"
        else:
            category = "medium_voltage"
        
        units = costs[category]["units"]
        
        # Validar que haya unidades disponibles
        if not units:
            return 1000.0  # Costo por defecto
        
        # Encontrar la unidad más cercana
        closest_unit = min(units, key=lambda x: abs(x["kvar"] - q_compensacion))
        
        # Si el valor es muy pequeño o muy grande, usar el extremo más cercano
        if q_compensacion <= units[0]["kvar"]:
            return units[0]["cost_usd"] * 1.25
        
        if q_compensacion >= units[-1]["kvar"]:
            return units[-1]["cost_usd"] * 1.25
        
        # Encontrar unidades inferior y superior para interpolación
        lower_units = [u for u in units if u["kvar"] <= q_compensacion]
        upper_units = [u for u in units if u["kvar"] >= q_compensacion]
        
        if not lower_units:
            lower_unit = units[0]
        else:
            lower_unit = max(lower_units, key=lambda x: x["kvar"])
        
        if not upper_units:
            upper_unit = units[-1]
        else:
            upper_unit = min(upper_units, key=lambda x: x["kvar"])
        
        # Si son la misma unidad, retornar su costo
        if lower_unit == upper_unit:
            return lower_unit["cost_usd"] * 1.25
        
        # Interpolación lineal
        ratio = (q_compensacion - lower_unit["kvar"]) / (upper_unit["kvar"] - lower_unit["kvar"])
        interpolated_cost = lower_unit["cost_usd"] + ratio * (upper_unit["cost_usd"] - lower_unit["cost_usd"])
        
        # Agregar margen de instalación (25%)
        return interpolated_cost * 1.25
