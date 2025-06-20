import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

class Visualizaciones:
    """
    Clase para generar visualizaciones de los métodos numéricos aplicados al Blackjack.
    """
    
    def __init__(self):
        """
        Inicializa la clase con configuraciones de estilo predeterminadas.
        """
        self.colores = {
            'biseccion': '#1f77b4',
            'newton': '#ff7f0e', 
            'punto_fijo': '#2ca02c',
            'funcion': '#d62728',
            'raiz': '#9467bd'
        }
        
        self.config_layout = {
            'font': dict(size=12),
            'showlegend': True,
            'hovermode': 'x unified',
            'template': 'plotly_white'
        }
    
    def grafica_convergencia(self, resultados):
        """
        Crea una gráfica comparativa de la convergencia de los métodos.
        
        Args:
            resultados (dict): Resultados de los métodos numéricos
            
        Returns:
            plotly.graph_objects.Figure: Gráfica de convergencia
        """
        fig = go.Figure()
        
        for metodo, resultado in resultados.items():
            if metodo == 'tiempos':
                continue
                
            if resultado['convergencia'] and resultado['historial_x']:
                iteraciones = list(range(len(resultado['historial_x'])))
                
                fig.add_trace(go.Scatter(
                    x=iteraciones,
                    y=resultado['historial_x'],
                    mode='lines+markers',
                    name=metodo.replace('_', ' ').title(),
                    line=dict(color=self.colores.get(metodo, '#000000'), width=2),
                    marker=dict(size=6),
                    hovertemplate=f'<b>{metodo.title()}</b><br>' +
                                'Iteración: %{x}<br>' +
                                'Valor: %{y:.6f}<br>' +
                                '<extra></extra>'
                ))
        
        fig.update_layout(
            title='Convergencia de los Métodos Numéricos',
            xaxis_title='Número de Iteración',
            yaxis_title='Valor de x',
            **self.config_layout
        )
        
        return fig
    
    def grafica_error(self, resultados):
        """
        Crea una gráfica del error absoluto vs iteraciones.
        
        Args:
            resultados (dict): Resultados de los métodos numéricos
            
        Returns:
            plotly.graph_objects.Figure: Gráfica de error
        """
        fig = go.Figure()
        
        for metodo, resultado in resultados.items():
            if metodo == 'tiempos':
                continue
                
            if resultado['convergencia'] and resultado['historial_error']:
                iteraciones = list(range(1, len(resultado['historial_error']) + 1))
                errores_filtrados = [e for e in resultado['historial_error'] if e != float('inf')]
                iter_filtradas = iteraciones[:len(errores_filtrados)]
                
                if errores_filtrados:
                    fig.add_trace(go.Scatter(
                        x=iter_filtradas,
                        y=errores_filtrados,
                        mode='lines+markers',
                        name=metodo.replace('_', ' ').title(),
                        line=dict(color=self.colores.get(metodo, '#000000'), width=2),
                        marker=dict(size=6),
                        hovertemplate=f'<b>{metodo.title()}</b><br>' +
                                    'Iteración: %{x}<br>' +
                                    'Error: %{y:.2e}<br>' +
                                    '<extra></extra>'
                    ))
        
        fig.update_layout(
            title='Error Absoluto vs Iteraciones',
            xaxis_title='Número de Iteración',
            yaxis_title='Error Absoluto',
            yaxis_type='log',
            **self.config_layout
        )
        
        return fig
    
    def visualizar_biseccion(self, funcion, resultado, a, b):
        """
        Visualiza el comportamiento del método de bisección.
        
        Args:
            funcion: Función objetivo
            resultado (dict): Resultado del método de bisección
            a, b (float): Intervalo inicial
            
        Returns:
            plotly.graph_objects.Figure: Visualización de bisección
        """
        # Generar puntos para la función
        x_func = np.linspace(a - 2, b + 2, 1000)
        y_func = funcion(x_func)
        
        fig = go.Figure()
        
        # Graficar función
        fig.add_trace(go.Scatter(
            x=x_func,
            y=y_func,
            mode='lines',
            name='f(x)',
            line=dict(color=self.colores['funcion'], width=2)
        ))
        
        # Línea y = 0
        fig.add_hline(y=0, line_dash="dash", line_color="black", 
                     annotation_text="y = 0")
        
        # Puntos de convergencia
        if resultado['historial_x']:
            fig.add_trace(go.Scatter(
                x=resultado['historial_x'],
                y=[funcion(x) for x in resultado['historial_x']],
                mode='markers',
                name='Puntos de Bisección',
                marker=dict(
                    color=self.colores['biseccion'],
                    size=8,
                    symbol='diamond'
                ),
                hovertemplate='Iteración: %{pointNumber}<br>' +
                            'x: %{x:.6f}<br>' +
                            'f(x): %{y:.6f}<br>' +
                            '<extra></extra>'
            ))
        
        # Raíz final
        if resultado['convergencia']:
            fig.add_trace(go.Scatter(
                x=[resultado['raiz']],
                y=[funcion(resultado['raiz'])],
                mode='markers',
                name='Raíz Encontrada',
                marker=dict(
                    color=self.colores['raiz'],
                    size=12,
                    symbol='star'
                )
            ))
        
        fig.update_layout(
            title='Método de Bisección - Convergencia',
            xaxis_title='x',
            yaxis_title='f(x)',
            **self.config_layout
        )
        
        return fig
    
    def visualizar_newton_raphson(self, funcion, derivada, resultado, x0):
        """
        Visualiza el comportamiento del método de Newton-Raphson.
        
        Args:
            funcion: Función objetivo
            derivada: Derivada de la función
            resultado (dict): Resultado del método Newton-Raphson
            x0 (float): Valor inicial
            
        Returns:
            plotly.graph_objects.Figure: Visualización de Newton-Raphson
        """
        if not resultado['historial_x']:
            return go.Figure()
        
        # Determinar rango para la gráfica
        x_min = min(resultado['historial_x']) - 2
        x_max = max(resultado['historial_x']) + 2
        x_func = np.linspace(x_min, x_max, 1000)
        y_func = funcion(x_func)
        
        fig = go.Figure()
        
        # Graficar función
        fig.add_trace(go.Scatter(
            x=x_func,
            y=y_func,
            mode='lines',
            name='f(x)',
            line=dict(color=self.colores['funcion'], width=2)
        ))
        
        # Línea y = 0
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        
        # Tangentes y puntos de iteración
        for i, x_i in enumerate(resultado['historial_x'][:-1]):
            fx_i = funcion(x_i)
            fpx_i = derivada(x_i)
            
            # Punto de iteración
            fig.add_trace(go.Scatter(
                x=[x_i],
                y=[fx_i],
                mode='markers',
                marker=dict(color=self.colores['newton'], size=8),
                name=f'Iteración {i}' if i == 0 else None,
                showlegend=i == 0,
                hovertemplate=f'Iteración {i}<br>' +
                            f'x: {x_i:.6f}<br>' +
                            f'f(x): {fx_i:.6f}<br>' +
                            '<extra></extra>'
            ))
            
            # Línea tangente
            if abs(fpx_i) > 1e-15:
                x_tangent = np.array([x_min, x_max])
                y_tangent = fx_i + fpx_i * (x_tangent - x_i)
                
                fig.add_trace(go.Scatter(
                    x=x_tangent,
                    y=y_tangent,
                    mode='lines',
                    line=dict(color=self.colores['newton'], width=1, dash='dot'),
                    name='Tangentes' if i == 0 else None,
                    showlegend=i == 0,
                    opacity=0.7
                ))
        
        # Raíz final
        if resultado['convergencia']:
            fig.add_trace(go.Scatter(
                x=[resultado['raiz']],
                y=[funcion(resultado['raiz'])],
                mode='markers',
                name='Raíz Encontrada',
                marker=dict(
                    color=self.colores['raiz'],
                    size=12,
                    symbol='star'
                )
            ))
        
        fig.update_layout(
            title='Método de Newton-Raphson - Tangentes',
            xaxis_title='x',
            yaxis_title='f(x)',
            **self.config_layout
        )
        
        return fig
    
    def visualizar_punto_fijo(self, g_funcion, resultado, x0):
        """
        Visualiza el comportamiento del método de punto fijo.
        
        Args:
            g_funcion: Función g(x) para punto fijo
            resultado (dict): Resultado del método punto fijo
            x0 (float): Valor inicial
            
        Returns:
            plotly.graph_objects.Figure: Visualización de punto fijo
        """
        if not resultado['historial_x']:
            return go.Figure()
        
        # Rango para la gráfica
        x_min = min(resultado['historial_x']) - 1
        x_max = max(resultado['historial_x']) + 1
        x_range = np.linspace(x_min, x_max, 1000)
        
        fig = go.Figure()
        
        # Función g(x)
        try:
            y_g = [g_funcion(x) for x in x_range]
            fig.add_trace(go.Scatter(
                x=x_range,
                y=y_g,
                mode='lines',
                name='g(x)',
                line=dict(color=self.colores['punto_fijo'], width=2)
            ))
        except:
            # Si g(x) es constante
            g_val = g_funcion(x0)
            fig.add_hline(y=g_val, line_color=self.colores['punto_fijo'], 
                         line_width=2, annotation_text=f"g(x) = {g_val:.3f}")
        
        # Línea y = x
        fig.add_trace(go.Scatter(
            x=x_range,
            y=x_range,
            mode='lines',
            name='y = x',
            line=dict(color='gray', width=1, dash='dash')
        ))
        
        # Iteraciones
        for i, x_i in enumerate(resultado['historial_x']):
            g_x_i = g_funcion(x_i)
            
            fig.add_trace(go.Scatter(
                x=[x_i],
                y=[g_x_i],
                mode='markers',
                marker=dict(color=self.colores['punto_fijo'], size=8),
                name=f'Iteración {i}' if i == 0 else None,
                showlegend=i == 0,
                hovertemplate=f'Iteración {i}<br>' +
                            f'x: {x_i:.6f}<br>' +
                            f'g(x): {g_x_i:.6f}<br>' +
                            '<extra></extra>'
            ))
        
        # Punto fijo final
        if resultado['convergencia']:
            fig.add_trace(go.Scatter(
                x=[resultado['raiz']],
                y=[resultado['raiz']],
                mode='markers',
                name='Punto Fijo',
                marker=dict(
                    color=self.colores['raiz'],
                    size=12,
                    symbol='star'
                )
            ))
        
        fig.update_layout(
            title='Método de Punto Fijo - Iteraciones',
            xaxis_title='x',
            yaxis_title='g(x)',
            **self.config_layout
        )
        
        return fig
    
    def tabla_comparativa(self, resultados):
        """
        Crea una tabla comparativa de los resultados.
        
        Args:
            resultados (dict): Resultados de todos los métodos
            
        Returns:
            pd.DataFrame: Tabla con comparación
        """
        datos = []
        
        for metodo, resultado in resultados.items():
            if metodo == 'tiempos':
                continue
                
            datos.append({
                'Método': metodo.replace('_', ' ').title(),
                'Raíz': f"{resultado['raiz']:.8f}" if resultado['raiz'] is not None else "N/A",
                'Iteraciones': resultado['iteraciones'],
                'Error Final': f"{resultado['error']:.2e}" if resultado['error'] != float('inf') else "∞",
                'Convergencia': '✅' if resultado['convergencia'] else '❌',
                'Mensaje': resultado['mensaje']
            })
        
        return pd.DataFrame(datos)
    
    def grafica_barras_comparativa(self, resultados, metrica='iteraciones'):
        """
        Crea gráfica de barras para comparar métricas.
        
        Args:
            resultados (dict): Resultados de los métodos
            metrica (str): Métrica a comparar ('iteraciones', 'error', 'tiempo')
            
        Returns:
            plotly.graph_objects.Figure: Gráfica de barras
        """
        metodos = []
        valores = []
        
        for metodo, resultado in resultados.items():
            if metodo == 'tiempos':
                continue
                
            if resultado['convergencia']:
                metodos.append(metodo.replace('_', ' ').title())
                
                if metrica == 'iteraciones':
                    valores.append(resultado['iteraciones'])
                elif metrica == 'error':
                    valores.append(resultado['error'])
                elif metrica == 'tiempo' and 'tiempos' in resultados:
                    valores.append(resultados['tiempos'][metodo])
        
        fig = go.Figure(data=[
            go.Bar(
                x=metodos,
                y=valores,
                marker_color=[self.colores.get(m.lower().replace(' ', '_'), '#000000') 
                            for m in metodos],
                text=[f'{v:.2e}' if metrica == 'error' else f'{v}' for v in valores],
                textposition='auto'
            )
        ])
        
        titulo_metrica = {
            'iteraciones': 'Número de Iteraciones',
            'error': 'Error Final',
            'tiempo': 'Tiempo de Ejecución (s)'
        }
        
        fig.update_layout(
            title=f'Comparación - {titulo_metrica.get(metrica, metrica)}',
            xaxis_title='Método',
            yaxis_title=titulo_metrica.get(metrica, metrica),
            **self.config_layout
        )
        
        if metrica == 'error':
            fig.update_yaxis(type='log')
        
        return fig
    
    def dashboard_completo(self, resultados, funcion, derivada, g_funcion, a, b, x0):
        """
        Crea un dashboard completo con todas las visualizaciones.
        
        Args:
            resultados (dict): Resultados de todos los métodos
            funcion: Función objetivo
            derivada: Derivada de la función
            g_funcion: Función de punto fijo
            a, b (float): Intervalo para bisección
            x0 (float): Valor inicial
            
        Returns:
            plotly.graph_objects.Figure: Dashboard completo
        """
        # Crear subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Convergencia', 'Error vs Iteraciones', 
                          'Bisección', 'Newton-Raphson'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Agregar gráficas de convergencia y error
        fig_conv = self.grafica_convergencia(resultados)
        fig_error = self.grafica_error(resultados)
        
        for trace in fig_conv.data:
            fig.add_trace(trace, row=1, col=1)
        
        for trace in fig_error.data:
            fig.add_trace(trace, row=1, col=2)
        
        # Agregar visualizaciones específicas de métodos
        if 'biseccion' in resultados and resultados['biseccion']['convergencia']:
            fig_bisec = self.visualizar_biseccion(funcion, resultados['biseccion'], a, b)
            for trace in fig_bisec.data:
                fig.add_trace(trace, row=2, col=1)
        
        if 'newton' in resultados and resultados['newton']['convergencia']:
            fig_newton = self.visualizar_newton_raphson(funcion, derivada, resultados['newton'], x0)
            for trace in fig_newton.data:
                fig.add_trace(trace, row=2, col=2)
        
        fig.update_layout(
            height=800,
            title_text="Dashboard Completo - Métodos Numéricos",
            showlegend=True
        )
        
        return fig