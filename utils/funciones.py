import numpy as np
import math

class Funciones:
    """
    Clase con funciones matemáticas auxiliares para métodos numéricos.
    """
    
    @staticmethod
    def validar_intervalo(funcion, a, b):
        """
        Valida si un intervalo es apropiado para el método de bisección.
        
        Args:
            funcion: Función a evaluar
            a, b: Límites del intervalo
            
        Returns:
            dict: Resultado de la validación
        """
        try:
            fa = funcion(a)
            fb = funcion(b)
            producto = fa * fb
            
            return {
                'valido': producto < 0,
                'f_a': fa,
                'f_b': fb,
                'producto': producto,
                'mensaje': 'Intervalo válido' if producto < 0 else 'No garantiza raíz'
            }
        except Exception as e:
            return {
                'valido': False,
                'error': str(e),
                'mensaje': 'Error al evaluar función'
            }
    
    @staticmethod
    def calcular_error_absoluto(x_nuevo, x_anterior):
        """Calcula error absoluto entre dos valores."""
        return abs(x_nuevo - x_anterior)
    
    @staticmethod
    def calcular_error_relativo(x_nuevo, x_anterior):
        """Calcula error relativo entre dos valores."""
        if abs(x_anterior) < 1e-15:
            return float('inf')
        return abs(x_nuevo - x_anterior) / abs(x_anterior)
    
    @staticmethod
    def estimar_orden_convergencia(errores):
        """
        Estima el orden de convergencia basado en errores sucesivos.
        
        Args:
            errores (list): Lista de errores absolutos
            
        Returns:
            float: Orden de convergencia estimado
        """
        if len(errores) < 3:
            return None
        
        try:
            ratios = []
            for i in range(1, len(errores) - 1):
                if errores[i] > 0 and errores[i+1] > 0 and errores[i-1] > 0:
                    ratio = math.log(errores[i+1] / errores[i]) / math.log(errores[i] / errores[i-1])
                    ratios.append(ratio)
            
            return np.mean(ratios) if ratios else None
        except:
            return None
    
    @staticmethod
    def generar_intervalo_biseccion(funcion, x_centro, radio=10):
        """
        Genera un intervalo válido para bisección alrededor de un punto.
        
        Args:
            funcion: Función objetivo
            x_centro: Punto central
            radio: Radio de búsqueda
            
        Returns:
            tuple: (a, b) intervalo válido o None
        """
        for r in np.linspace(0.1, radio, 100):
            a = x_centro - r
            b = x_centro + r
            
            try:
                if funcion(a) * funcion(b) < 0:
                    return a, b
            except:
                continue
        
        return None, None
    
    @staticmethod
    def verificar_derivada_no_cero(derivada, x, tolerancia=1e-15):
        """
        Verifica que la derivada no sea cero en un punto.
        
        Args:
            derivada: Función derivada
            x: Punto a evaluar
            tolerancia: Tolerancia para considerar cero
            
        Returns:
            bool: True si la derivada es válida
        """
        try:
            fx_prima = derivada(x)
            return abs(fx_prima) > tolerancia
        except:
            return False
    
    @staticmethod
    def analizar_convergencia_punto_fijo(g_funcion, g_derivada, x):
        """
        Analiza condiciones de convergencia para punto fijo.
        
        Args:
            g_funcion: Función g(x)
            g_derivada: Derivada g'(x)
            x: Punto a evaluar
            
        Returns:
            dict: Análisis de convergencia
        """
        try:
            g_prima = g_derivada(x)
            convergencia = abs(g_prima) < 1
            
            return {
                'g_prima': g_prima,
                'convergencia_local': convergencia,
                'tipo': 'Convergente' if convergencia else 'Divergente'
            }
        except:
            return {
                'g_prima': None,
                'convergencia_local': False,
                'tipo': 'Error en evaluación'
            }
    
    @staticmethod
    def formatear_numero_cientifico(numero, decimales=2):
        """Formatea número en notación científica."""
        if numero == 0:
            return "0"
        elif abs(numero) >= 1e-3 and abs(numero) < 1e3:
            return f"{numero:.{decimales}f}"
        else:
            return f"{numero:.{decimales}e}"
    
    @staticmethod
    def crear_tabla_iteraciones(historial_x, historial_error, metodo):
        """
        Crea tabla formateada de iteraciones.
        
        Args:
            historial_x: Lista de valores x
            historial_error: Lista de errores
            metodo: Nombre del método
            
        Returns:
            list: Lista de diccionarios para tabla
        """
        tabla = []
        for i, (x, error) in enumerate(zip(historial_x, historial_error)):
            tabla.append({
                'Iteración': i,
                'x': f"{x:.8f}",
                'Error': Funciones.formatear_numero_cientifico(error),
                'Método': metodo
            })
        return tabla