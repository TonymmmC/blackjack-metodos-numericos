import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

# Importar módulos del proyecto
from src.metodos_numericos import MetodosNumericos
from src.blackjack_game import BlackjackMath
from src.visualizaciones import Visualizaciones
from utils.funciones import Funciones
from utils.helpers import Helpers

def main():
    st.set_page_config(
        page_title="Blackjack - Métodos Numéricos",
        page_icon="🃏",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personalizado
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .method-card {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">Solución de Ecuaciones No Lineales - Blackjack</h1>', unsafe_allow_html=True)
    
    # Sidebar - Configuración
    st.sidebar.header("Configuración del Problema")
    
    # Valor inicial de cartas
    valor_cartas = st.sidebar.number_input(
        "Valor actual de cartas",
        min_value=2,
        max_value=20,
        value=10,
        step=1,
        help="Suma actual de las cartas en mano"
    )
    
    # Objetivo (normalmente 21 en Blackjack)
    objetivo = st.sidebar.number_input(
        "Valor objetivo",
        min_value=15,
        max_value=25,
        value=21,
        step=1,
        help="Valor objetivo a alcanzar"
    )
    
    # Parámetros numéricos
    st.sidebar.subheader("Parámetros Numéricos")
    
    tolerancia = st.sidebar.selectbox(
        "Tolerancia (ε)",
        [1e-6, 1e-8, 1e-10],
        index=0,
        format_func=lambda x: f"{x:.0e}"
    )
    
    max_iter = st.sidebar.number_input(
        "Máximo de iteraciones",
        min_value=10,
        max_value=1000,
        value=100,
        step=10
    )
    
    # Valor inicial para Newton-Raphson y Punto Fijo
    x0 = st.sidebar.number_input(
        "Valor inicial (x₀)",
        min_value=0.1,
        max_value=50.0,
        value=float(objetivo - valor_cartas),
        step=0.1,
        help="Aproximación inicial para Newton-Raphson y Punto Fijo"
    )
    
    # Intervalo para Bisección
    st.sidebar.subheader("Intervalo para Bisección")
    a = st.sidebar.number_input("Límite inferior (a)", value=0.0, step=0.1)
    b = st.sidebar.number_input("Límite superior (b)", value=float(objetivo - valor_cartas + 5), step=0.1)
    
    # Instanciar clases
    metodos = MetodosNumericos(tolerancia, max_iter)
    blackjack = BlackjackMath(valor_cartas, objetivo)
    viz = Visualizaciones()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Análisis del Problema", 
        "🔢 Métodos Numéricos", 
        "📈 Visualizaciones", 
        "📋 Comparación"
    ])
    
    with tab1:
        st.header("Definición del Problema Matemático")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Ecuación No Lineal")
            st.latex(r"f(x) = \text{valor\_cartas} + x - \text{objetivo} = 0")
            
            st.markdown("### Función Específica")
            st.latex(f"f(x) = {valor_cartas} + x - {objetivo} = 0")
            
            st.markdown("### Derivada (para Newton-Raphson)")
            st.latex(r"f'(x) = 1")
            
            st.markdown("### Función de Punto Fijo")
            st.latex(f"g(x) = {objetivo} - {valor_cartas} = {objetivo - valor_cartas}")
            
        with col2:
            st.markdown('<div class="method-card">', unsafe_allow_html=True)
            st.markdown("**Interpretación del Problema:**")
            st.write(f"- Cartas actuales: {valor_cartas}")
            st.write(f"- Objetivo: {objetivo}")
            st.write(f"- Valor a encontrar: {objetivo - valor_cartas}")
            st.write(f"- Diferencia actual: {abs(objetivo - valor_cartas)}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Evaluación de la función
        st.subheader("Evaluación de la Función")
        x_eval = np.linspace(-5, objetivo - valor_cartas + 10, 1000)
        y_eval = blackjack.funcion_objetivo(x_eval)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_eval, 
            y=y_eval, 
            mode='lines',
            name='f(x)',
            line=dict(color='blue', width=2)
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="y = 0")
        fig.add_vline(x=objetivo - valor_cartas, line_dash="dash", line_color="green", 
                     annotation_text=f"Raíz teórica: x = {objetivo - valor_cartas}")
        
        fig.update_layout(
            title="Gráfica de la Función Objetivo",
            xaxis_title="x",
            yaxis_title="f(x)",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Implementación de Métodos Numéricos")
        
        # Validaciones
        if blackjack.funcion_objetivo(a) * blackjack.funcion_objetivo(b) >= 0:
            st.warning(f"Para Bisección: f({a}) × f({b}) = {blackjack.funcion_objetivo(a) * blackjack.funcion_objetivo(b):.4f} ≥ 0. No se garantiza la existencia de raíz en el intervalo.")
        
        # Ejecutar métodos
        if st.button("Ejecutar Todos los Métodos", type="primary"):
            
            with st.spinner("Ejecutando métodos numéricos..."):
                # Método de Bisección
                st.subheader("1. Método de Bisección")
                start_time = time.time()
                resultado_biseccion = metodos.biseccion(blackjack.funcion_objetivo, a, b)
                tiempo_biseccion = time.time() - start_time
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Raíz encontrada", f"{resultado_biseccion['raiz']:.6f}")
                with col2:
                    st.metric("Iteraciones", resultado_biseccion['iteraciones'])
                with col3:
                    st.metric("Tiempo (s)", f"{tiempo_biseccion:.4f}")
                
                if resultado_biseccion['convergencia']:
                    st.success(f"Convergió con error: {resultado_biseccion['error']:.2e}")
                else:
                    st.error("No convergió")
                
                # Método de Newton-Raphson
                st.subheader("2. Método de Newton-Raphson")
                start_time = time.time()
                resultado_newton = metodos.newton_raphson(
                    blackjack.funcion_objetivo, 
                    blackjack.derivada_funcion, 
                    x0
                )
                tiempo_newton = time.time() - start_time
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Raíz encontrada", f"{resultado_newton['raiz']:.6f}")
                with col2:
                    st.metric("Iteraciones", resultado_newton['iteraciones'])
                with col3:
                    st.metric("Tiempo (s)", f"{tiempo_newton:.4f}")
                
                if resultado_newton['convergencia']:
                    st.success(f"Convergió con error: {resultado_newton['error']:.2e}")
                else:
                    st.error("No convergió")
                
                # Método de Punto Fijo
                st.subheader("3. Método de Punto Fijo")
                start_time = time.time()
                resultado_punto_fijo = metodos.punto_fijo(blackjack.funcion_punto_fijo, x0)
                tiempo_punto_fijo = time.time() - start_time
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Punto fijo", f"{resultado_punto_fijo['raiz']:.6f}")
                with col2:
                    st.metric("Iteraciones", resultado_punto_fijo['iteraciones'])
                with col3:
                    st.metric("Tiempo (s)", f"{tiempo_punto_fijo:.4f}")
                
                if resultado_punto_fijo['convergencia']:
                    st.success(f"Convergió con error: {resultado_punto_fijo['error']:.2e}")
                else:
                    st.error("No convergió")
                
                # Guardar resultados en session_state para otras tabs
                st.session_state['resultados'] = {
                    'biseccion': resultado_biseccion,
                    'newton': resultado_newton,
                    'punto_fijo': resultado_punto_fijo,
                    'tiempos': {
                        'biseccion': tiempo_biseccion,
                        'newton': tiempo_newton,
                        'punto_fijo': tiempo_punto_fijo
                    }
                }
    
    with tab3:
        st.header("Visualizaciones de Convergencia")
        
        if 'resultados' in st.session_state:
            resultados = st.session_state['resultados']
            
            # Gráfica de convergencia
            fig = viz.grafica_convergencia(resultados)
            st.plotly_chart(fig, use_container_width=True)
            
            # Gráfica de error
            fig_error = viz.grafica_error(resultados)
            st.plotly_chart(fig_error, use_container_width=True)
            
            # Visualización del comportamiento de cada método
            st.subheader("Comportamiento de los Métodos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Bisección - Convergencia del intervalo
                if resultados['biseccion']['convergencia']:
                    fig_bisec = viz.visualizar_biseccion(
                        blackjack.funcion_objetivo, 
                        resultados['biseccion'], 
                        a, b
                    )
                    st.plotly_chart(fig_bisec, use_container_width=True)
            
            with col2:
                # Newton-Raphson - Tangentes
                if resultados['newton']['convergencia']:
                    fig_newton = viz.visualizar_newton_raphson(
                        blackjack.funcion_objetivo,
                        blackjack.derivada_funcion,
                        resultados['newton'],
                        x0
                    )
                    st.plotly_chart(fig_newton, use_container_width=True)
        
        else:
            st.info("Ejecuta los métodos en la pestaña anterior para ver las visualizaciones")
    
    with tab4:
        st.header("Comparación de Métodos")
        
        if 'resultados' in st.session_state:
            resultados = st.session_state['resultados']
            tiempos = st.session_state['resultados']['tiempos']
            
            # Tabla comparativa
            datos_comparacion = []
            for metodo, resultado in resultados.items():
                if metodo != 'tiempos':
                    datos_comparacion.append({
                        'Método': metodo.replace('_', ' ').title(),
                        'Raíz': f"{resultado['raiz']:.8f}",
                        'Iteraciones': resultado['iteraciones'],
                        'Error Final': f"{resultado['error']:.2e}",
                        'Tiempo (s)': f"{tiempos[metodo]:.6f}",
                        'Convergencia': 'Correcta' if resultado['convergencia'] else '❌'
                    })
            
            df_comparacion = pd.DataFrame(datos_comparacion)
            st.subheader("Tabla Comparativa de Resultados")
            st.dataframe(df_comparacion, use_container_width=True)
            
            # Gráficas comparativas
            col1, col2 = st.columns(2)
            
            with col1:
                # Comparación de iteraciones
                fig_iter = px.bar(
                    df_comparacion, 
                    x='Método', 
                    y='Iteraciones',
                    title='Número de Iteraciones por Método',
                    color='Método'
                )
                st.plotly_chart(fig_iter, use_container_width=True)
            
            with col2:
                # Comparación de tiempos
                tiempos_df = pd.DataFrame({
                    'Método': [k.replace('_', ' ').title() for k in tiempos.keys()],
                    'Tiempo': list(tiempos.values())
                })
                fig_tiempo = px.bar(
                    tiempos_df, 
                    x='Método', 
                    y='Tiempo',
                    title='Tiempo de Ejecución por Método',
                    color='Método'
                )
                st.plotly_chart(fig_tiempo, use_container_width=True)
            
            # Análisis de eficiencia
            st.subheader("Análisis de Eficiencia")
            
            mejor_precision = min([r['error'] for r in [resultados['biseccion'], resultados['newton'], resultados['punto_fijo']] if r['convergencia']])
            mejor_tiempo = min(tiempos.values())
            menos_iteraciones = min([r['iteraciones'] for r in [resultados['biseccion'], resultados['newton'], resultados['punto_fijo']] if r['convergencia']])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mejor Precisión", f"{mejor_precision:.2e}")
            with col2:
                st.metric("Menor Tiempo", f"{mejor_tiempo:.6f} s")
            with col3:
                st.metric("Menos Iteraciones", menos_iteraciones)
                
        else:
            st.info("Ejecuta los métodos para ver la comparación")
    
    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()