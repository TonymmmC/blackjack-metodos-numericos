"""
Módulo principal del proyecto Blackjack - Métodos Numéricos.

Este paquete contiene la implementación de métodos numéricos para resolver
ecuaciones no lineales aplicadas al problema de optimización en Blackjack.

Módulos:
    metodos_numericos: Implementación de Bisección, Newton-Raphson y Punto Fijo
    blackjack_game: Lógica matemática del problema de Blackjack
    visualizaciones: Gráficas y visualizaciones de los métodos
"""

__version__ = "1.0.0"
__author__ = "Equipo Blackjack - Métodos Numéricos"

# Importaciones principales para facilitar el uso
from .metodos_numericos import MetodosNumericos
from .blackjack_game import BlackjackMath
from .visualizaciones import Visualizaciones

__all__ = [
    'MetodosNumericos',
    'BlackjackMath', 
    'Visualizaciones'
]