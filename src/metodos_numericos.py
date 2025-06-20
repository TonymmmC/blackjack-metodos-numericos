import numpy as np
import math

class MetodosNumericos:
    """
    Implementación de métodos numéricos para la solución de ecuaciones no lineales.
    Incluye: Bisección, Newton-Raphson y Punto Fijo.
    """
    
    def __init__(self, tolerancia=1e-6, max_iteraciones=100):
        """
        Inicializa los parámetros de convergencia.
        
        Args:
            tolerancia (float): Error mínimo aceptable
            max_iteraciones (int): Número máximo de iteraciones
        """
        self.tolerancia = tolerancia
        self.max_iteraciones = max_iteraciones
    
    def biseccion(self, funcion, a, b, blackjack_obj=None):
        """
        Método de Bisección adaptado para funciones cuadráticas.
        
        Args:
            funcion: Función f(x) de la cual se busca la raíz
            a (float): Límite inferior del intervalo
            b (float): Límite superior del intervalo
            blackjack_obj: Objeto BlackjackMath para función modificada
            
        Returns:
            dict: Diccionario con resultados del método
        """
        # Usar función modificada para crear cambio de signo
        if blackjack_obj:
            funcion_uso = blackjack_obj.funcion_objetivo_biseccion
        else:
            funcion_uso = funcion
        
        # Verificar que existe cambio de signo
        try:
            fa = funcion_uso(a)
            fb = funcion_uso(b)
        except:
            return {
                'raiz': None,
                'iteraciones': 0,
                'convergencia': False,
                'error': float('inf'),
                'historial_x': [],
                'historial_error': [],
                'mensaje': 'Error al evaluar función en los límites'
            }
        
        if fa * fb >= 0:
            return {
                'raiz': None,
                'iteraciones': 0,
                'convergencia': False,
                'error': float('inf'),
                'historial_x': [],
                'historial_error': [],
                'mensaje': 'No se garantiza la existencia de raíz en el intervalo'
            }
        
        iteracion = 0
        error = float('inf')
        historial_x = []
        historial_error = []
        x_anterior = 0
        
        while iteracion < self.max_iteraciones and error > self.tolerancia:
            # Calcular punto medio
            c = (a + b) / 2
            historial_x.append(c)
            
            # Calcular error
            if iteracion > 0:
                error = abs(c - x_anterior)
            historial_error.append(error)
            
            # Evaluar función en el punto medio
            fc = funcion_uso(c)
            
            # Verificar si encontramos la raíz exacta
            if abs(fc) < self.tolerancia:
                return {
                    'raiz': c,
                    'iteraciones': iteracion + 1,
                    'convergencia': True,
                    'error': abs(fc),
                    'historial_x': historial_x,
                    'historial_error': historial_error,
                    'mensaje': 'Convergencia exitosa'
                }
            
            # Actualizar intervalo
            if funcion_uso(a) * fc < 0:
                b = c
            else:
                a = c
            
            x_anterior = c
            iteracion += 1
        
        # Resultado final
        c_final = (a + b) / 2
        return {
            'raiz': c_final,
            'iteraciones': iteracion,
            'convergencia': error <= self.tolerancia,
            'error': error,
            'historial_x': historial_x,
            'historial_error': historial_error,
            'mensaje': 'Convergencia exitosa' if error <= self.tolerancia else 'Máximo de iteraciones alcanzado'
        }
    
    def newton_raphson(self, funcion, derivada, x0):
        """
        Método de Newton-Raphson para encontrar raíces de ecuaciones no lineales.
        Modificado para manejar funciones cuadráticas donde f'(raíz) = 0.
        
        Args:
            funcion: Función f(x) de la cual se busca la raíz
            derivada: Derivada f'(x) de la función
            x0 (float): Aproximación inicial
            
        Returns:
            dict: Diccionario con resultados del método
        """
        iteracion = 0
        x_actual = x0
        error = float('inf')
        historial_x = [x0]
        historial_error = []
        
        while iteracion < self.max_iteraciones and error > self.tolerancia:
            # Evaluar función y derivada
            try:
                fx = funcion(x_actual)
                fpx = derivada(x_actual)
            except:
                return {
                    'raiz': x_actual,
                    'iteraciones': iteracion,
                    'convergencia': False,
                    'error': float('inf'),
                    'historial_x': historial_x,
                    'historial_error': historial_error,
                    'mensaje': 'Error al evaluar función o derivada'
                }
            
            # Para funciones cuadráticas, verificar si ya llegamos al mínimo
            if abs(fx) < self.tolerancia:
                return {
                    'raiz': x_actual,
                    'iteraciones': iteracion,
                    'convergencia': True,
                    'error': abs(fx),
                    'historial_x': historial_x,
                    'historial_error': historial_error,
                    'mensaje': 'Convergencia exitosa - mínimo encontrado'
                }
            
            # Verificar derivada muy pequeña (cerca del mínimo)
            if abs(fpx) < 1e-12:
                # Para funciones cuadráticas, si estamos muy cerca del mínimo
                if abs(fx) < 1e-6:
                    return {
                        'raiz': x_actual,
                        'iteraciones': iteracion,
                        'convergencia': True,
                        'error': abs(fx),
                        'historial_x': historial_x,
                        'historial_error': historial_error,
                        'mensaje': 'Convergencia exitosa - en el mínimo'
                    }
                else:
                    return {
                        'raiz': x_actual,
                        'iteraciones': iteracion,
                        'convergencia': False,
                        'error': float('inf'),
                        'historial_x': historial_x,
                        'historial_error': historial_error,
                        'mensaje': 'Derivada muy pequeña - posible punto crítico'
                    }
            
            # Fórmula de Newton-Raphson
            x_nuevo = x_actual - fx / fpx
            
            # Calcular error
            error = abs(x_nuevo - x_actual)
            historial_x.append(x_nuevo)
            historial_error.append(error)
            
            x_actual = x_nuevo
            iteracion += 1
        
        return {
            'raiz': x_actual,
            'iteraciones': iteracion,
            'convergencia': error <= self.tolerancia,
            'error': error,
            'historial_x': historial_x,
            'historial_error': historial_error,
            'mensaje': 'Convergencia exitosa' if error <= self.tolerancia else 'Máximo de iteraciones alcanzado'
        }
    
    def punto_fijo(self, g_funcion, x0):
        """
        Método de Punto Fijo para encontrar soluciones de la forma x = g(x).
        
        Args:
            g_funcion: Función g(x) tal que x = g(x)
            x0 (float): Aproximación inicial
            
        Returns:
            dict: Diccionario con resultados del método
        """
        iteracion = 0
        x_actual = x0
        error = float('inf')
        historial_x = [x0]
        historial_error = []
        
        while iteracion < self.max_iteraciones and error > self.tolerancia:
            # Aplicar iteración de punto fijo
            try:
                x_nuevo = g_funcion(x_actual)
            except:
                return {
                    'raiz': x_actual,
                    'iteraciones': iteracion,
                    'convergencia': False,
                    'error': float('inf'),
                    'historial_x': historial_x,
                    'historial_error': historial_error,
                    'mensaje': 'Error al evaluar función g(x)'
                }
            
            # Calcular error
            error = abs(x_nuevo - x_actual)
            historial_x.append(x_nuevo)
            historial_error.append(error)
            
            # Verificar convergencia
            if error < self.tolerancia:
                return {
                    'raiz': x_nuevo,
                    'iteraciones': iteracion + 1,
                    'convergencia': True,
                    'error': error,
                    'historial_x': historial_x,
                    'historial_error': historial_error,
                    'mensaje': 'Convergencia exitosa'
                }
            
            # Verificar divergencia
            if abs(x_nuevo) > 1e10:
                return {
                    'raiz': x_nuevo,
                    'iteraciones': iteracion + 1,
                    'convergencia': False,
                    'error': float('inf'),
                    'historial_x': historial_x,
                    'historial_error': historial_error,
                    'mensaje': 'Método divergente'
                }
            
            x_actual = x_nuevo
            iteracion += 1
        
        return {
            'raiz': x_actual,
            'iteraciones': iteracion,
            'convergencia': error <= self.tolerancia,
            'error': error,
            'historial_x': historial_x,
            'historial_error': historial_error,
            'mensaje': 'Convergencia exitosa' if error <= self.tolerancia else 'Máximo de iteraciones alcanzado'
        }