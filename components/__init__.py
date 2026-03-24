"""
Paquete de componentes para la calculadora de compensación de reactivos
"""

from .calculators import PowerCalculator, SolutionComparator
from .templates import TemplateManager, ComponentDatabase
from .visualizers import ChartGenerator
from .exporters import PDFExporter, ReportGenerator

__all__ = [
    'PowerCalculator',
    'SolutionComparator', 
    'TemplateManager',
    'ComponentDatabase',
    'ChartGenerator',
    'PDFExporter',
    'ReportGenerator'
]
