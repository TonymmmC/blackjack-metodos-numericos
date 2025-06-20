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
    
    st.markdown('<h1 class="main-header">Minimización del Error Cuadrático - Blackjack</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d;">Aplicación de Métodos Numéricos para Ecuaciones No Lineales</p>', unsafe_allow_html=True)
    
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
    raiz_teorica = objetivo - valor_cartas
    a = st.sidebar.number_input("Límite inferior (a)", value=float(max(0.0, raiz_teorica - 5)), step=0.1)
    b = st.sidebar.number_input("Límite superior (b)", value=float(raiz_teorica + 5), step=0.1)
    
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
            st.markdown("### Ecuación No Lineal (Cuadrática)")
            st.latex(r"f(x) = (\text{valor\_cartas} + x - \text{objetivo})^2")
            
            st.markdown("### Función Específica")
            st.latex(f"f(x) = ({valor_cartas} + x - {objetivo})^2")
            
            st.markdown("### Derivada (para Newton-Raphson)")
            st.latex(f"f'(x) = 2({valor_cartas} + x - {objetivo})")
            
            st.markdown("### Función de Punto Fijo")
            st.latex(f"g(x) = {objetivo} - {valor_cartas} = {objetivo - valor_cartas}")
            
        with col2:
            st.markdown('<div class="method-card">', unsafe_allow_html=True)
            st.markdown("**Interpretación del Problema:**")
            st.write(f"- Cartas actuales: {valor_cartas}")
            st.write(f"- Objetivo: {objetivo}")
            st.write(f"- Mínimo teórico: {objetivo - valor_cartas}")
            st.write(f"- Error cuadrático mínimo: 0")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Evaluación de la función
        st.subheader("Evaluación de la Función Cuadrática")
        x_eval = np.linspace(raiz_teorica - 10, raiz_teorica + 10, 1000)
        y_eval = blackjack.funcion_objetivo(x_eval)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_eval, 
            y=y_eval, 
            mode='lines',
            name='f(x) = (suma + x - 21)²',
            line=dict(color='blue', width=2)
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="y = 0")
        fig.add_vline(x=raiz_teorica, line_dash="dash", line_color="green", 
                     annotation_text=f"Mínimo: x = {raiz_teorica}")
        
        fig.update_layout(
            title="Gráfica de la Función Objetivo Cuadrática",
            xaxis_title="x",
            yaxis_title="f(x)",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Implementación de Métodos Numéricos")
        
        # Verificar intervalo para bisección
        verification = blackjack.verificar_existencia_raiz(a, b)
        if not verification['minimo_en_intervalo']:
            st.warning(f"El mínimo teórico ({raiz_teorica:.3f}) está fuera del intervalo [{a}, {b}]")
        
        # Ejecutar métodos
        if st.button("Ejecutar Todos los Métodos", type="primary"):
            
            with st.spinner("Ejecutando métodos numéricos..."):
                # Método de Bisección
                st.subheader("1. Método de Bisección")
                start_time = time.time()
                resultado_biseccion = metodos.biseccion(blackjack.funcion_objetivo, a, b, blackjack)
                tiempo_biseccion = time.time() - start_time
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if resultado_biseccion['raiz'] is not None:
                        st.metric("Raíz encontrada", f"{resultado_biseccion['raiz']:.6f}")
                    else:
                        st.metric("Raíz encontrada", "No converge")
                with col2:
                    st.metric("Iteraciones", resultado_biseccion['iteraciones'])
                with col3:
                    st.metric("Tiempo (s)", f"{tiempo_biseccion:.4f}")
                
                if resultado_biseccion['convergencia']:
                    st.success(f"Convergió con error: {resultado_biseccion['error']:.2e}")
                else:
                    st.error(f"No convergió: {resultado_biseccion['mensaje']}")
                
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
                    if resultado_newton['raiz'] is not None:
                        st.metric("Raíz encontrada", f"{resultado_newton['raiz']:.6f}")
                    else:
                        st.metric("Raíz encontrada", "No converge")
                with col2:
                    st.metric("Iteraciones", resultado_newton['iteraciones'])
                with col3:
                    st.metric("Tiempo (s)", f"{tiempo_newton:.4f}")
                
                if resultado_newton['convergencia']:
                    st.success(f"Convergió con error: {resultado_newton['error']:.2e}")
                else:
                    st.error(f"No convergió: {resultado_newton['mensaje']}")
                
                # Método de Punto Fijo
                st.subheader("3. Método de Punto Fijo")
                start_time = time.time()
                resultado_punto_fijo = metodos.punto_fijo(blackjack.funcion_punto_fijo, x0)
                tiempo_punto_fijo = time.time() - start_time
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if resultado_punto_fijo['raiz'] is not None:
                        st.metric("Punto fijo", f"{resultado_punto_fijo['raiz']:.6f}")
                    else:
                        st.metric("Punto fijo", "No converge")
                with col2:
                    st.metric("Iteraciones", resultado_punto_fijo['iteraciones'])
                with col3:
                    st.metric("Tiempo (s)", f"{tiempo_punto_fijo:.4f}")
                
                if resultado_punto_fijo['convergencia']:
                    st.success(f"Convergió con error: {resultado_punto_fijo['error']:.2e}")
                else:
                    st.error(f"No convergió: {resultado_punto_fijo['mensaje']}")
                
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
                        blackjack.funcion_objetivo_biseccion, 
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
                        'Raíz': f"{resultado['raiz']:.8f}" if resultado['raiz'] is not None else "No converge",
                        'Iteraciones': resultado['iteraciones'],
                        'Error Final': f"{resultado['error']:.2e}" if resultado['error'] != float('inf') else "∞",
                        'Tiempo (s)': f"{tiempos[metodo]:.6f}",
                        'Convergencia': '✅' if resultado['convergencia'] else '❌'
                    })
            
            df_comparacion = pd.DataFrame(datos_comparacion)
            st.subheader("Tabla Comparativa de Resultados")
            st.dataframe(df_comparacion, use_container_width=True)
            
            # Análisis de resultados
            st.subheader("Análisis de Resultados")
            convergentes = [r for r in [resultados['biseccion'], resultados['newton'], resultados['punto_fijo']] if r['convergencia']]
            
            if convergentes:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    mejor_precision = min([r['error'] for r in convergentes])
                    st.metric("Mejor Precisión", f"{mejor_precision:.2e}")
                
                with col2:
                    mejor_tiempo = min(tiempos.values())
                    st.metric("Menor Tiempo", f"{mejor_tiempo:.6f} s")
                
                with col3:
                    menos_iteraciones = min([r['iteraciones'] for r in convergentes])
                    st.metric("Menos Iteraciones", menos_iteraciones)
                
                # Interpretación para Blackjack
                st.subheader("Interpretación en Blackjack")
                raiz_promedio = np.mean([r['raiz'] for r in convergentes])
                interpretacion = blackjack.interpretar_resultado(raiz_promedio)
                
                st.markdown(f"""
                **Análisis Estratégico:**
                - Valor actual de cartas: {interpretacion['valor_actual']}
                - Valor óptimo a obtener: {interpretacion['valor_a_obtener']:.3f}
                - Suma total resultante: {interpretacion['suma_total']:.3f}
                - Error cuadrático: {interpretacion['error_cuadratico']:.6f}
                
                **Recomendación:** {interpretacion['recomendacion']}
                """)
                
                # Gráficas comparativas
                col1, col2 = st.columns(2)
                
                with col1:
                    # Comparación de iteraciones (solo convergentes)
                    metodos_conv = [m for m in ['biseccion', 'newton', 'punto_fijo'] if resultados[m]['convergencia']]
                    if metodos_conv:
                        iteraciones_data = {
                            'Método': [m.replace('_', ' ').title() for m in metodos_conv],
                            'Iteraciones': [resultados[m]['iteraciones'] for m in metodos_conv]
                        }
                        fig_iter = px.bar(
                            iteraciones_data, 
                            x='Método', 
                            y='Iteraciones',
                            title='Iteraciones por Método (Convergentes)',
                            color='Método'
                        )
                        st.plotly_chart(fig_iter, use_container_width=True)
                
                with col2:
                    # Comparación de tiempos
                    tiempos_data = {
                        'Método': [k.replace('_', ' ').title() for k in tiempos.keys()],
                        'Tiempo': list(tiempos.values())
                    }
                    fig_tiempo = px.bar(
                        tiempos_data, 
                        x='Método', 
                        y='Tiempo',
                        title='Tiempo de Ejecución por Método',
                        color='Método'
                    )
                    st.plotly_chart(fig_tiempo, use_container_width=True)
            
            else:
                st.error("Ningún método convergió. Revisa los parámetros del problema.")
                
        else:
            st.info("Ejecuta los métodos para ver la comparación")
    
    # Footer
    st.markdown("---")
    st.markdown("**Proyecto:** Métodos Numéricos aplicados a Blackjack | **Función:** Minimización del Error Cuadrático")

if __name__ == "__main__":
    main()