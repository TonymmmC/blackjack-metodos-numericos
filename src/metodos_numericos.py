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
    
    def biseccion(self, funcion, a, b):
        """
        Método de Bisección para encontrar raíces de ecuaciones no lineales.
        
        Args:
            funcion: Función f(x) de la cual se busca la raíz
            a (float): Límite inferior del intervalo
            b (float): Límite superior del intervalo
            
        Returns:
            dict: Diccionario con resultados del método
        """
        # Verificar que existe raíz en el intervalo
        if funcion(a) * funcion(b) >= 0:
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
            fc = funcion(c)
            
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
            if funcion(a) * fc < 0:
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
            fx = funcion(x_actual)
            fpx = derivada(x_actual)
            
            # Verificar que la derivada no sea cero
            if abs(fpx) < 1e-15:
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
            
            # Verificar convergencia por valor de función
            if abs(funcion(x_nuevo)) < self.tolerancia:
                return {
                    'raiz': x_nuevo,
                    'iteraciones': iteracion + 1,
                    'convergencia': True,
                    'error': error,
                    'historial_x': historial_x,
                    'historial_error': historial_error,
                    'mensaje': 'Convergencia exitosa'
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
            x_nuevo = g_funcion(x_actual)
            
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
    
    def comparar_metodos(self, funcion, derivada, g_funcion, a, b, x0):
        """
        Ejecuta y compara los tres métodos numéricos.
        
        Args:
            funcion: Función f(x) objetivo
            derivada: Derivada f'(x)
            g_funcion: Función g(x) para punto fijo
            a, b: Intervalo para bisección
            x0: Valor inicial para Newton-Raphson y Punto Fijo
            
        Returns:
            dict: Comparación completa de los métodos
        """
        resultados = {}
        
        # Ejecutar Bisección
        resultados['biseccion'] = self.biseccion(funcion, a, b)
        
        # Ejecutar Newton-Raphson
        resultados['newton_raphson'] = self.newton_raphson(funcion, derivada, x0)
        
        # Ejecutar Punto Fijo
        resultados['punto_fijo'] = self.punto_fijo(g_funcion, x0)
        
        # Análisis comparativo
        metodos_convergentes = {k: v for k, v in resultados.items() if v['convergencia']}
        
        if metodos_convergentes:
            # Encontrar el más eficiente
            mejor_iteraciones = min(metodos_convergentes.values(), key=lambda x: x['iteraciones'])
            mejor_precision = min(metodos_convergentes.values(), key=lambda x: x['error'])
            
            resultados['analisis'] = {
                'metodos_convergentes': list(metodos_convergentes.keys()),
                'mejor_iteraciones': mejor_iteraciones,
                'mejor_precision': mejor_precision,
                'raiz_teorica': None  # Se puede calcular analíticamente si es necesario
            }
        else:
            resultados['analisis'] = {
                'metodos_convergentes': [],
                'mejor_iteraciones': None,
                'mejor_precision': None,
                'raiz_teorica': None
            }
        
        return resultados
    
    def analizar_convergencia(self, resultado):
        """
        Analiza las propiedades de convergencia de un método.
        
        Args:
            resultado (dict): Resultado de un método numérico
            
        Returns:
            dict: Análisis de convergencia
        """
        if not resultado['convergencia'] or len(resultado['historial_error']) < 2:
            return {
                'tipo_convergencia': 'No convergente',
                'orden_convergencia': None,
                'factor_convergencia': None
            }
        
        errores = resultado['historial_error'][1:]  # Excluir el primer error (inf)
        
        # Estimar orden de convergencia
        if len(errores) >= 3:
            try:
                # Método para estimar orden de convergencia
                ratios = []
                for i in range(1, len(errores) - 1):
                    if errores[i] > 0 and errores[i+1] > 0 and errores[i-1] > 0:
                        ratio = math.log(errores[i+1] / errores[i]) / math.log(errores[i] / errores[i-1])
                        ratios.append(ratio)
                
                if ratios:
                    orden_estimado = np.mean(ratios)
                    
                    if orden_estimado < 1.5:
                        tipo = 'Lineal'
                    elif orden_estimado < 2.5:
                        tipo = 'Cuadrática'
                    else:
                        tipo = 'Superlineal'
                    
                    return {
                        'tipo_convergencia': tipo,
                        'orden_convergencia': orden_estimado,
                        'factor_convergencia': errores[-1] / errores[-2] if len(errores) >= 2 else None
                    }
            except:
                pass
        
        # Análisis básico si no se puede estimar el orden
        factor = errores[-1] / errores[-2] if len(errores) >= 2 else None
        
        if factor and factor < 0.1:
            tipo = 'Rápida'
        elif factor and factor < 0.5:
            tipo = 'Moderada'
        else:
            tipo = 'Lenta'
        
        return {
            'tipo_convergencia': tipo,
            'orden_convergencia': None,
            'factor_convergencia': factor
        }