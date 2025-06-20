# Metodología - Métodos Numéricos para Blackjack

## Fundamento Teórico

### Problema Matemático
Resolver la ecuación no lineal:
```
f(x) = valor_cartas_actuales + x - objetivo = 0
```

**Objetivo:** Encontrar el valor `x` que representa cuánto valor adicional se necesita para alcanzar el objetivo en Blackjack.

### Métodos Implementados

#### 1. Método de Bisección

**Teorema del Valor Intermedio:** Si f es continua en [a,b] y f(a)·f(b) < 0, entonces existe al menos un c ∈ (a,b) tal que f(c) = 0.

**Algoritmo:**
1. Verificar que f(a)·f(b) < 0
2. Calcular punto medio: c = (a+b)/2
3. Evaluar f(c)
4. Si f(a)·f(c) < 0, entonces b = c; sino a = c
5. Repetir hasta convergencia

**Convergencia:** 
- Lineal con razón 1/2
- Error acotado: |e_n| ≤ (b-a)/2^n
- Convergencia garantizada

**Ventajas:**
- Siempre converge si existe raíz en el intervalo
- Robusto y estable
- No requiere derivadas

**Desventajas:**
- Convergencia lenta
- Requiere intervalo inicial válido

#### 2. Método de Newton-Raphson

**Fórmula:** x_{n+1} = x_n - f(x_n)/f'(x_n)

**Derivada para nuestro problema:** f'(x) = 1

**Algoritmo:**
1. Partir de aproximación inicial x_0
2. Calcular x_{n+1} = x_n - f(x_n)/f'(x_n)
3. Repetir hasta convergencia

**Convergencia:**
- Cuadrática (cuando converge)
- Error: e_{n+1} ≈ (f''(ξ)/(2f'(x*)))e_n²
- Para función lineal: converge en 1 iteración

**Ventajas:**
- Convergencia muy rápida
- Pocas iteraciones requeridas
- Excelente para funciones suaves

**Desventajas:**
- Requiere calcular derivada
- Puede no converger con mal x_0
- Problemas si f'(x) ≈ 0

#### 3. Método de Punto Fijo

**Transformación:** x = g(x) donde g(x) = objetivo - valor_cartas

**Algoritmo:**
1. Partir de x_0
2. Calcular x_{n+1} = g(x_n)
3. Repetir hasta convergencia

**Condición de Convergencia:** |g'(x)| < 1 en el intervalo de interés

**Para nuestro problema:** g'(x) = 0, por lo que converge en 1 iteración

**Ventajas:**
- Simple de implementar
- Para nuestro caso específico: convergencia inmediata
- No requiere derivadas de f(x)

**Desventajas:**
- Convergencia depende de g'(x)
- Puede diverger fácilmente
- Convergencia típicamente lineal

## Análisis Específico del Problema Blackjack

### Naturaleza de la Función
La función f(x) = valor_cartas + x - objetivo es **lineal** en x, lo que implica:

1. **Derivada constante:** f'(x) = 1
2. **Segunda derivada nula:** f''(x) = 0
3. **Solución analítica:** x = objetivo - valor_cartas

### Comportamiento Esperado de los Métodos

#### Bisección
- Convergencia lineal estándar
- Aproximadamente 20 iteraciones para tolerancia 1e-6
- Intervalo sugerido: [0, objetivo - valor_cartas + margen]

#### Newton-Raphson
- **Convergencia en 1 iteración** (función lineal)
- Independiente del valor inicial x_0
- Método óptimo para este problema

#### Punto Fijo
- **Convergencia en 1 iteración** (g(x) constante)
- g'(x) = 0 < 1, cumple condición de convergencia
- Resultado independiente de x_0

### Casos de Prueba Estándar

#### Caso 1: Mano Baja
- **Entrada:** valor_cartas = 6, objetivo = 21
- **Ecuación:** f(x) = 6 + x - 21 = 0
- **Solución:** x = 15
- **Interpretación:** Necesita 15 puntos adicionales

#### Caso 2: Mano Media
- **Entrada:** valor_cartas = 17, objetivo = 21
- **Ecuación:** f(x) = 17 + x - 21 = 0
- **Solución:** x = 4
- **Interpretación:** Necesita 4 puntos adicionales

#### Caso 3: Mano Alta
- **Entrada:** valor_cartas = 19, objetivo = 21
- **Ecuación:** f(x) = 19 + x - 21 = 0
- **Solución:** x = 2
- **Interpretación:** Necesita 2 puntos adicionales

## Criterios de Convergencia

### Error Absoluto
```
|x_{n+1} - x_n| < ε
```

### Error Relativo
```
|x_{n+1} - x_n| / |x_n| < ε
```

### Error de Función
```
|f(x_n)| < ε
```

**Tolerancia recomendada:** ε = 1×10^{-6}

## Métricas de Evaluación

### 1. Número de Iteraciones
- Medida de eficiencia computacional
- Newton-Raphson: 1 iteración (óptimo)
- Punto Fijo: 1 iteración
- Bisección: ~20 iteraciones

### 2. Precisión Final
- Error absoluto respecto a solución analítica
- Todos los métodos deben alcanzar tolerancia especificada

### 3. Tiempo de Ejecución
- Medición en microsegundos
- Newton-Raphson: más rápido
- Bisección: más lento debido a iteraciones

### 4. Estabilidad Numérica
- Sensibilidad a condiciones iniciales
- Robustez ante errores de redondeo

## Implementación Computacional

### Estructura de Datos
```python
resultado = {
    'raiz': float,           # Solución encontrada
    'iteraciones': int,      # Número de iteraciones
    'convergencia': bool,    # Si convergió o no
    'error': float,          # Error final
    'historial_x': list,     # Valores de x en cada iteración
    'historial_error': list, # Errores en cada iteración
    'mensaje': str           # Descripción del resultado
}
```

### Criterios de Parada
1. **Convergencia:** Error < tolerancia
2. **Máximo de iteraciones:** Prevenir bucles infinitos
3. **Error de función:** |f(x)| < tolerancia
4. **Divergencia detectada:** |x| > límite_grande

## Análisis de Complejidad

### Complejidad Temporal
- **Bisección:** O(log((b-a)/ε))
- **Newton-Raphson:** O(1) para función lineal
- **Punto Fijo:** O(1) para g(x) constante

### Complejidad Espacial
- Todos los métodos: O(n) donde n = número de iteraciones
- Almacenamiento del historial para análisis

## Validación y Verificación

### Verificación Analítica
- Comparar con solución exacta: x = objetivo - valor_cartas
- Error numérico debe ser < tolerancia

### Casos Límite
1. **valor_cartas = objetivo:** x = 0
2. **valor_cartas muy bajo:** x grande
3. **valor_cartas > objetivo:** x negativo (situación bust)

### Pruebas de Robustez
- Diferentes valores iniciales
- Tolerancias variables
- Intervalos extremos para bisección

## Interpretación de Resultados

### Contexto del Blackjack
- **x > 0:** Valor adicional necesario
- **x = 0:** Ya en el objetivo
- **x < 0:** Se pasó del objetivo (bust)

### Recomendaciones de Juego
- **x ≤ 11:** Seguro tomar carta (As no causa bust)
- **x = 10:** Buscar carta de valor 10
- **x < 5:** Alto riesgo, evaluar probabilidades

## Conclusiones Metodológicas

### Mejor Método para Este Problema
**Newton-Raphson** es óptimo porque:
1. Converge en 1 iteración
2. No requiere intervalo inicial
3. Máxima eficiencia computacional

### Aplicabilidad General
Esta metodología se extiende a:
- Otros juegos de cartas
- Problemas de optimización lineal
- Sistemas de ecuaciones simples

### Limitaciones
- Función objetivo lineal (caso especial)
- No aplicable a sistemas no lineales complejos
- Requiere función continua y derivable