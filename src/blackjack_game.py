import numpy as np
import math

class BlackjackMath:
    """
    Clase que define las funciones matemáticas del problema de Blackjack
    para la aplicación de métodos numéricos con minimización del error cuadrático.
    """
    
    def __init__(self, valor_cartas_actuales, objetivo=21):
        """
        Inicializa el problema matemático del Blackjack.
        
        Args:
            valor_cartas_actuales (float): Suma actual de las cartas en mano
            objetivo (float): Valor objetivo a alcanzar (normalmente 21)
        """
        self.valor_cartas = valor_cartas_actuales
        self.objetivo = objetivo
        self.diferencia_objetivo = objetivo - valor_cartas_actuales
    
    def funcion_objetivo(self, x):
        """
        Función objetivo cuadrática: f(x) = (valor_cartas + x - objetivo)²
        
        Esta función representa la minimización del error cuadrático.
        Buscamos el valor x tal que minimicemos la diferencia al cuadrado
        entre la suma de cartas actuales más x y el objetivo.
        
        Args:
            x (float or array): Valor o valores a evaluar
            
        Returns:
            float or array: Resultado de la evaluación f(x)
        """
        return (self.valor_cartas + x - self.objetivo) ** 2
    
    def derivada_funcion(self, x):
        """
        Derivada de la función objetivo: f'(x) = 2(valor_cartas + x - objetivo)
        
        La derivada de (a + x - b)² es 2(a + x - b)
        
        Args:
            x (float or array): Valor o valores a evaluar
            
        Returns:
            float or array: Derivada f'(x)
        """
        return 2 * (self.valor_cartas + x - self.objetivo)
    
    def funcion_punto_fijo(self, x):
        """
        Función de punto fijo: g(x) = objetivo - valor_cartas
        
        Para minimizar f(x) = (valor_cartas + x - objetivo)², 
        necesitamos que valor_cartas + x - objetivo = 0
        Por lo tanto: x = objetivo - valor_cartas (constante)
        
        Args:
            x (float): Valor actual (no afecta el resultado en este caso)
            
        Returns:
            float: Valor de g(x)
        """
        return self.objetivo - self.valor_cartas
    
    def funcion_objetivo_biseccion(self, x):
        """
        Función lineal para bisección que cruza cero en la raíz.
        f_bisec(x) = x - raiz_exacta
        """
        raiz_exacta = self.raiz_analitica()
        return x - raiz_exacta
    
    def segunda_derivada(self, x):
        """
        Segunda derivada de la función objetivo: f''(x) = 2
        
        Como f'(x) = 2(valor_cartas + x - objetivo), f''(x) = 2 (constante)
        
        Args:
            x (float or array): Valor o valores (no afecta el resultado)
            
        Returns:
            float or array: Segunda derivada f''(x) = 2
        """
        if isinstance(x, (list, tuple, np.ndarray)):
            return np.full_like(x, 2.0)
        return 2.0
    
    def evaluar_en_intervalo(self, a, b, num_puntos=1000):
        """
        Evalúa la función objetivo cuadrática en un intervalo dado.
        
        Args:
            a (float): Límite inferior del intervalo
            b (float): Límite superior del intervalo
            num_puntos (int): Número de puntos a evaluar
            
        Returns:
            tuple: (x_values, y_values) para graficación
        """
        x_values = np.linspace(a, b, num_puntos)
        y_values = self.funcion_objetivo(x_values)
        return x_values, y_values
    
    def verificar_existencia_raiz(self, a, b):
        """
        Verifica si el mínimo está en el intervalo para bisección.
        """
        minimo_teorico = self.raiz_analitica()
        minimo_en_intervalo = a <= minimo_teorico <= b
        
        # Verificar cambio de signo para función modificada
        fa_bisec = self.funcion_objetivo_biseccion(a)
        fb_bisec = self.funcion_objetivo_biseccion(b)
        
        return {
            'existe_raiz': minimo_en_intervalo and (fa_bisec * fb_bisec < 0),
            'f_a': self.funcion_objetivo(a),
            'f_b': self.funcion_objetivo(b),
            'minimo_teorico': minimo_teorico,
            'minimo_en_intervalo': minimo_en_intervalo,
            'mensaje': 'Intervalo válido para bisección' if minimo_en_intervalo else 'Ajustar intervalo'
        }
    
    def raiz_analitica(self):
        """
        Calcula la raíz analítica (punto donde f(x) = 0 o mínimo de la parábola).
        
        Para f(x) = (valor_cartas + x - objetivo)²
        El mínimo ocurre cuando valor_cartas + x - objetivo = 0
        Por lo tanto: x = objetivo - valor_cartas
        
        Returns:
            float: Solución exacta de la ecuación
        """
        return self.objetivo - self.valor_cartas
    
    def error_numerico(self, raiz_numerica):
        """
        Calcula el error entre la solución numérica y la analítica.
        
        Args:
            raiz_numerica (float): Raíz encontrada numéricamente
            
        Returns:
            dict: Diferentes tipos de error
        """
        raiz_exacta = self.raiz_analitica()
        error_absoluto = abs(raiz_numerica - raiz_exacta)
        error_relativo = error_absoluto / abs(raiz_exacta) if raiz_exacta != 0 else float('inf')
        
        return {
            'raiz_exacta': raiz_exacta,
            'raiz_numerica': raiz_numerica,
            'error_absoluto': error_absoluto,
            'error_relativo': error_relativo,
            'error_porcentual': error_relativo * 100,
            'valor_funcion_numerica': self.funcion_objetivo(raiz_numerica)
        }
    
    def interpretar_resultado(self, raiz_encontrada):
        """
        Interpreta el resultado numérico en el contexto del Blackjack.
        
        Args:
            raiz_encontrada (float): Valor encontrado por el método numérico
            
        Returns:
            dict: Interpretación del resultado
        """
        suma_total = self.valor_cartas + raiz_encontrada
        error_cuadratico = self.funcion_objetivo(raiz_encontrada)
        
        interpretacion = {
            'valor_actual': self.valor_cartas,
            'valor_a_obtener': raiz_encontrada,
            'suma_total': suma_total,
            'error_cuadratico': error_cuadratico,
            'diferencia_objetivo': abs(self.objetivo - suma_total)
        }
        
        # Análisis del resultado en términos de optimización
        if error_cuadratico < 1e-6:
            interpretacion['interpretacion'] = 'Óptimo alcanzado - Minimización exitosa'
            interpretacion['recomendacion'] = 'Estrategia óptima encontrada'
        elif error_cuadratico < 1:
            interpretacion['interpretacion'] = 'Cerca del óptimo'
            interpretacion['recomendacion'] = 'Estrategia casi óptima'
        else:
            interpretacion['interpretacion'] = 'Lejos del óptimo'
            interpretacion['recomendacion'] = 'Revisar parámetros de optimización'
        
        return interpretacion
    
    def __str__(self):
        """
        Representación en string del problema matemático.
        """
        return f"Problema Blackjack Cuadrático: f(x) = ({self.valor_cartas} + x - {self.objetivo})²"
    
    def __repr__(self):
        """
        Representación para debugging.
        """
        return f"BlackjackMath(valor_cartas={self.valor_cartas}, objetivo={self.objetivo}, función=cuadrática)"