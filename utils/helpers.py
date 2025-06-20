import time
import numpy as np
import pandas as pd
from datetime import datetime

class Helpers:
    """
    Funciones auxiliares para la aplicación de Blackjack con métodos numéricos.
    """
    
    @staticmethod
    def cronometrar_ejecucion(func):
        """
        Decorador para medir tiempo de ejecución de funciones.
        
        Args:
            func: Función a cronometrar
            
        Returns:
            tuple: (resultado, tiempo_ejecucion)
        """
        def wrapper(*args, **kwargs):
            inicio = time.time()
            resultado = func(*args, **kwargs)
            fin = time.time()
            tiempo = fin - inicio
            return resultado, tiempo
        return wrapper
    
    @staticmethod
    def generar_reporte_convergencia(resultados):
        """
        Genera reporte detallado de convergencia.
        
        Args:
            resultados (dict): Resultados de métodos numéricos
            
        Returns:
            dict: Reporte estructurado
        """
        reporte = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'metodos_ejecutados': [],
            'convergentes': [],
            'no_convergentes': [],
            'estadisticas': {}
        }
        
        for metodo, resultado in resultados.items():
            if metodo == 'tiempos':
                continue
                
            reporte['metodos_ejecutados'].append(metodo)
            
            if resultado['convergencia']:
                reporte['convergentes'].append({
                    'metodo': metodo,
                    'raiz': resultado['raiz'],
                    'iteraciones': resultado['iteraciones'],
                    'error': resultado['error']
                })
            else:
                reporte['no_convergentes'].append({
                    'metodo': metodo,
                    'razon': resultado['mensaje']
                })
        
        # Estadísticas comparativas
        if reporte['convergentes']:
            iteraciones = [m['iteraciones'] for m in reporte['convergentes']]
            errores = [m['error'] for m in reporte['convergentes']]
            
            reporte['estadisticas'] = {
                'total_convergentes': len(reporte['convergentes']),
                'promedio_iteraciones': np.mean(iteraciones),
                'min_iteraciones': min(iteraciones),
                'max_iteraciones': max(iteraciones),
                'mejor_precision': min(errores),
                'peor_precision': max(errores)
            }
        
        return reporte
    
    @staticmethod
    def validar_parametros_entrada(valor_cartas, objetivo, tolerancia, max_iter, x0, a, b):
        """
        Valida parámetros de entrada de la aplicación.
        
        Returns:
            dict: Resultado de validación
        """
        errores = []
        
        # Validar valor de cartas
        if not 2 <= valor_cartas <= 20:
            errores.append("Valor de cartas debe estar entre 2 y 20")
        
        # Validar objetivo
        if not 15 <= objetivo <= 25:
            errores.append("Objetivo debe estar entre 15 y 25")
        
        # Validar tolerancia
        if not 1e-15 <= tolerancia <= 1e-1:
            errores.append("Tolerancia debe estar entre 1e-15 y 1e-1")
        
        # Validar iteraciones
        if not 1 <= max_iter <= 1000:
            errores.append("Máximo de iteraciones debe estar entre 1 y 1000")
        
        # Validar intervalo
        if a >= b:
            errores.append("Límite inferior debe ser menor que límite superior")
        
        # Validar x0
        if not -100 <= x0 <= 100:
            errores.append("Valor inicial x0 debe estar entre -100 y 100")
        
        return {
            'valido': len(errores) == 0,
            'errores': errores
        }
    
    @staticmethod
    def formatear_resultado_metodo(resultado, metodo):
        """
        Formatea resultado de método para presentación.
        
        Args:
            resultado (dict): Resultado del método
            metodo (str): Nombre del método
            
        Returns:
            dict: Resultado formateado
        """
        if not resultado['convergencia']:
            return {
                'metodo': metodo.title(),
                'estado': 'No Convergió',
                'raiz': 'N/A',
                'iteraciones': resultado['iteraciones'],
                'error': 'N/A',
                'mensaje': resultado['mensaje']
            }
        
        return {
            'metodo': metodo.title(),
            'estado': 'Convergió',
            'raiz': f"{resultado['raiz']:.8f}",
            'iteraciones': resultado['iteraciones'],
            'error': f"{resultado['error']:.2e}",
            'mensaje': resultado['mensaje']
        }
    
    @staticmethod
    def generar_casos_prueba_automaticos():
        """
        Genera casos de prueba predefinidos para validación.
        
        Returns:
            list: Lista de casos de prueba
        """
        return [
            {
                'nombre': 'Caso Básico',
                'valor_cartas': 10,
                'objetivo': 21,
                'x0': 11,
                'a': 0,
                'b': 20,
                'raiz_esperada': 11
            },
            {
                'nombre': 'Mano Baja',
                'valor_cartas': 6,
                'objetivo': 21,
                'x0': 15,
                'a': 0,
                'b': 20,
                'raiz_esperada': 15
            },
            {
                'nombre': 'Mano Alta',
                'valor_cartas': 19,
                'objetivo': 21,
                'x0': 2,
                'a': 0,
                'b': 5,
                'raiz_esperada': 2
            }
        ]
    
    @staticmethod
    def calcular_metricas_rendimiento(resultados, tiempos):
        """
        Calcula métricas de rendimiento comparativo.
        
        Args:
            resultados (dict): Resultados de métodos
            tiempos (dict): Tiempos de ejecución
            
        Returns:
            dict: Métricas de rendimiento
        """
        metricas = {
            'eficiencia_iteraciones': {},
            'eficiencia_tiempo': {},
            'precision': {},
            'robustez': {}
        }
        
        # Métodos que convergieron
        convergentes = {k: v for k, v in resultados.items() 
                      if k != 'tiempos' and v['convergencia']}
        
        if not convergentes:
            return metricas
        
        # Eficiencia en iteraciones
        iteraciones = {k: v['iteraciones'] for k, v in convergentes.items()}
        min_iter = min(iteraciones.values())
        
        for metodo, iter_count in iteraciones.items():
            metricas['eficiencia_iteraciones'][metodo] = min_iter / iter_count
        
        # Eficiencia en tiempo
        if tiempos:
            tiempos_convergentes = {k: v for k, v in tiempos.items() if k in convergentes}
            min_tiempo = min(tiempos_convergentes.values())
            
            for metodo, tiempo in tiempos_convergentes.items():
                metricas['eficiencia_tiempo'][metodo] = min_tiempo / tiempo
        
        # Precisión
        errores = {k: v['error'] for k, v in convergentes.items()}
        min_error = min(errores.values())
        
        for metodo, error in errores.items():
            metricas['precision'][metodo] = min_error / error if error > 0 else 1
        
        # Robustez (% de convergencia en múltiples ejecuciones)
        for metodo in convergentes.keys():
            metricas['robustez'][metodo] = 1.0  # Simplificado para este ejemplo
        
        return metricas
    
    @staticmethod
    def exportar_resultados_csv(resultados, filename=None):
        """
        Exporta resultados a archivo CSV.
        
        Args:
            resultados (dict): Resultados de métodos
            filename (str): Nombre del archivo
            
        Returns:
            str: Nombre del archivo generado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resultados_blackjack_{timestamp}.csv"
        
        datos = []
        for metodo, resultado in resultados.items():
            if metodo == 'tiempos':
                continue
                
            datos.append({
                'Método': metodo,
                'Convergencia': resultado['convergencia'],
                'Raíz': resultado['raiz'],
                'Iteraciones': resultado['iteraciones'],
                'Error': resultado['error'],
                'Mensaje': resultado['mensaje']
            })
        
        df = pd.DataFrame(datos)
        df.to_csv(filename, index=False)
        return filename
    
    @staticmethod
    def interpretar_blackjack(valor_cartas, raiz_encontrada, objetivo=21):
        """
        Interpreta el resultado en términos del juego Blackjack.
        
        Args:
            valor_cartas (float): Valor actual de cartas
            raiz_encontrada (float): Solución encontrada
            objetivo (float): Valor objetivo
            
        Returns:
            dict: Interpretación del resultado
        """
        suma_total = valor_cartas + raiz_encontrada
        
        interpretacion = {
            'valor_actual': valor_cartas,
            'valor_a_obtener': raiz_encontrada,
            'suma_total': suma_total,
            'diferencia_objetivo': abs(objetivo - suma_total)
        }
        
        # Análisis estratégico
        if suma_total < objetivo:
            diferencia = objetivo - suma_total
            if diferencia <= 10:
                interpretacion['recomendacion'] = 'Considerar tomar una carta más'
                interpretacion['riesgo'] = 'Bajo'
            else:
                interpretacion['recomendacion'] = 'Definitivamente tomar cartas'
                interpretacion['riesgo'] = 'Muy bajo'
        elif suma_total == objetivo:
            interpretacion['recomendacion'] = 'Perfecto - Mantenerse (Stand)'
            interpretacion['riesgo'] = 'Ninguno'
        else:
            interpretacion['recomendacion'] = 'Se pasó del objetivo (Bust)'
            interpretacion['riesgo'] = 'Máximo'
        
        return interpretacion
    
    @staticmethod
    def generar_resumen_ejecutivo(resultados, parametros):
        """
        Genera resumen ejecutivo del análisis.
        
        Args:
            resultados (dict): Resultados de métodos
            parametros (dict): Parámetros utilizados
            
        Returns:
            str: Resumen en formato texto
        """
        convergentes = [k for k, v in resultados.items() 
                       if k != 'tiempos' and v['convergencia']]
        
        resumen = f"""
RESUMEN EJECUTIVO - ANÁLISIS BLACKJACK
=====================================

Problema: f(x) = {parametros['valor_cartas']} + x - {parametros['objetivo']} = 0
Solución teórica: x = {parametros['objetivo'] - parametros['valor_cartas']}

RESULTADOS:
- Métodos convergentes: {len(convergentes)}/3
- Métodos: {', '.join(convergentes)}

"""
        
        if convergentes:
            mejor_iteraciones = min([resultados[m]['iteraciones'] for m in convergentes])
            mejor_precision = min([resultados[m]['error'] for m in convergentes])
            
            resumen += f"""
MEJOR RENDIMIENTO:
- Menos iteraciones: {mejor_iteraciones}
- Mejor precisión: {mejor_precision:.2e}

RECOMENDACIÓN:
El método más eficiente para este tipo de problemas lineales es Newton-Raphson,
que converge en una sola iteración debido a la naturaleza lineal de la función.
"""
        
        return resumen