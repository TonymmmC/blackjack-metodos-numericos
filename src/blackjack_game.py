import numpy as np
import math

class BlackjackMath:
    """
    Clase que define las funciones matemáticas del problema de Blackjack
    para la aplicación de métodos numéricos.
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
        Función objetivo: f(x) = valor_cartas + x - objetivo = 0
        
        Esta función representa la ecuación no lineal que queremos resolver.
        Buscamos el valor x tal que la suma de cartas actuales más x sea igual al objetivo.
        
        Args:
            x (float or array): Valor o valores a evaluar
            
        Returns:
            float or array: Resultado de la evaluación f(x)
        """
        return self.valor_cartas + x - self.objetivo
    
    def derivada_funcion(self, x):
        """
        Derivada de la función objetivo: f'(x) = 1
        
        Como f(x) = valor_cartas + x - objetivo es lineal en x,
        su derivada es constante igual a 1.
        
        Args:
            x (float or array): Valor o valores (no afecta el resultado)
            
        Returns:
            float or array: Derivada f'(x) = 1
        """
        if isinstance(x, (list, tuple, np.ndarray)):
            return np.ones_like(x)
        return 1.0
    
    def funcion_punto_fijo(self, x):
        """
        Función de punto fijo: g(x) = objetivo - valor_cartas
        
        Transformamos f(x) = valor_cartas + x - objetivo = 0
        a la forma x = g(x) donde g(x) = objetivo - valor_cartas
        
        Args:
            x (float): Valor actual (no afecta el resultado en este caso)
            
        Returns:
            float: Valor de g(x)
        """
        return self.objetivo - self.valor_cartas
    
    def segunda_derivada(self, x):
        """
        Segunda derivada de la función objetivo: f''(x) = 0
        
        Como f'(x) = 1 es constante, su derivada es cero.
        
        Args:
            x (float or array): Valor o valores (no afecta el resultado)
            
        Returns:
            float or array: Segunda derivada f''(x) = 0
        """
        if isinstance(x, (list, tuple, np.ndarray)):
            return np.zeros_like(x)
        return 0.0
    
    def evaluar_en_intervalo(self, a, b, num_puntos=1000):
        """
        Evalúa la función objetivo en un intervalo dado.
        
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
        Verifica si existe una raíz en el intervalo [a, b] usando el
        Teorema del Valor Intermedio.
        
        Args:
            a (float): Límite inferior
            b (float): Límite superior
            
        Returns:
            dict: Información sobre la existencia de raíz
        """
        fa = self.funcion_objetivo(a)
        fb = self.funcion_objetivo(b)
        producto = fa * fb
        
        return {
            'existe_raiz': producto < 0,
            'f_a': fa,
            'f_b': fb,
            'producto': producto,
            'mensaje': 'Existe al menos una raíz en el intervalo' if producto < 0 
                      else 'No se garantiza la existencia de raíz'
        }
    
    def raiz_analitica(self):
        """
        Calcula la raíz analítica de la ecuación lineal.
        
        Para f(x) = valor_cartas + x - objetivo = 0
        La solución es x = objetivo - valor_cartas
        
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
            'error_porcentual': error_relativo * 100
        }
    
    def generar_casos_prueba(self):
        """
        Genera casos de prueba típicos para el problema de Blackjack.
        
        Returns:
            list: Lista de diccionarios con casos de prueba
        """
        casos = [
            {
                'nombre': 'Mano Baja',
                'valor_cartas': 6,
                'descripcion': 'As(1) + 5 = 6, necesita llegar a 21',
                'raiz_esperada': 15
            },
            {
                'nombre': 'Mano Media',
                'valor_cartas': 17,
                'descripcion': '10 + 7 = 17, necesita llegar a 21',
                'raiz_esperada': 4
            },
            {
                'nombre': 'Mano Alta',
                'valor_cartas': 19,
                'descripcion': '9 + 10 = 19, necesita llegar a 21',
                'raiz_esperada': 2
            },
            {
                'nombre': 'Mano Crítica',
                'valor_cartas': 20,
                'descripcion': '10 + 10 = 20, necesita exactamente 1',
                'raiz_esperada': 1
            }
        ]
        
        return casos
    
    def analizar_convergencia_punto_fijo(self):
        """
        Analiza las condiciones de convergencia para el método de punto fijo.
        
        Para g(x) = objetivo - valor_cartas (constante),
        g'(x) = 0, por lo que |g'(x)| < 1 siempre se cumple.
        
        Returns:
            dict: Análisis de convergencia
        """
        return {
            'g_prima': 0,
            'convergencia_garantizada': True,
            'tipo_convergencia': 'Convergencia en una iteración',
            'razon': 'g(x) es constante, por lo que g\'(x) = 0 < 1'
        }
    
    def condicion_newton_raphson(self, x):
        """
        Analiza las condiciones para Newton-Raphson.
        
        Args:
            x (float): Punto a analizar
            
        Returns:
            dict: Análisis de las condiciones
        """
        fx = self.funcion_objetivo(x)
        fpx = self.derivada_funcion(x)
        fppx = self.segunda_derivada(x)
        
        return {
            'f_x': fx,
            'f_prima_x': fpx,
            'f_segunda_x': fppx,
            'derivada_no_cero': abs(fpx) > 1e-15,
            'multiplicidad': 1,  # Raíz simple para función lineal
            'convergencia_esperada': 'Cuadrática (en una iteración para función lineal)'
        }
    
    def interpretar_resultado(self, raiz_encontrada):
        """
        Interpreta el resultado numérico en el contexto del Blackjack.
        
        Args:
            raiz_encontrada (float): Valor encontrado por el método numérico
            
        Returns:
            dict: Interpretación del resultado
        """
        interpretacion = {
            'valor_a_obtener': raiz_encontrada,
            'suma_total': self.valor_cartas + raiz_encontrada,
            'diferencia_objetivo': abs(self.objetivo - (self.valor_cartas + raiz_encontrada))
        }
        
        # Análisis del resultado en términos de juego
        if raiz_encontrada < 0:
            interpretacion['interpretacion'] = 'Se pasó del objetivo (bust)'
            interpretacion['recomendacion'] = 'No tomar más cartas'
        elif raiz_encontrada == 0:
            interpretacion['interpretacion'] = 'Ya alcanzó el objetivo exacto'
            interpretacion['recomendacion'] = 'Mantenerse (stand)'
        elif raiz_encontrada <= 11:
            interpretacion['interpretacion'] = 'Puede tomar cartas sin riesgo de pasarse'
            interpretacion['recomendacion'] = 'Continuar jugando (hit)'
        else:
            interpretacion['interpretacion'] = 'Alto riesgo de pasarse del objetivo'
            interpretacion['recomendacion'] = 'Evaluar cuidadosamente el siguiente movimiento'
        
        return interpretacion
    
    def generar_funcion_modificada(self, parametro_dificultad=1):
        """
        Genera una versión más compleja del problema para pruebas avanzadas.
        
        Args:
            parametro_dificultad (float): Factor que modifica la complejidad
            
        Returns:
            function: Función objetivo modificada
        """
        def funcion_compleja(x):
            # Función no lineal más realista
            base = self.valor_cartas + x - self.objetivo
            return base + parametro_dificultad * np.sin(x / 10) * np.exp(-x / 20)
        
        return funcion_compleja
    
    def __str__(self):
        """
        Representación en string del problema matemático.
        """
        return f"Problema Blackjack: f(x) = {self.valor_cartas} + x - {self.objetivo} = 0"
    
    def __repr__(self):
        """
        Representación para debugging.
        """
        return f"BlackjackMath(valor_cartas={self.valor_cartas}, objetivo={self.objetivo})"