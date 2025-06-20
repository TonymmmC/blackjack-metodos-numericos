import json
import pickle
from datetime import datetime
import os

class AlmacenamientoResultados:
    """
    Clase para gestionar el almacenamiento y recuperación de resultados
    de los métodos numéricos aplicados al Blackjack.
    """
    
    def __init__(self, directorio_datos='data'):
        """
        Inicializa el gestor de almacenamiento.
        
        Args:
            directorio_datos (str): Directorio donde guardar los datos
        """
        self.directorio = directorio_datos
        self.crear_directorio()
    
    def crear_directorio(self):
        """Crea el directorio de datos si no existe."""
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)
    
    def guardar_sesion(self, resultados, parametros, nombre_sesion=None):
        """
        Guarda una sesión completa de resultados.
        
        Args:
            resultados (dict): Resultados de los métodos
            parametros (dict): Parámetros utilizados
            nombre_sesion (str): Nombre personalizado para la sesión
            
        Returns:
            str: Nombre del archivo guardado
        """
        if nombre_sesion is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_sesion = f"sesion_{timestamp}"
        
        datos_sesion = {
            'timestamp': datetime.now().isoformat(),
            'parametros': parametros,
            'resultados': resultados,
            'metadatos': {
                'version': '1.0',
                'tipo': 'blackjack_metodos_numericos'
            }
        }
        
        # Guardar en JSON (para legibilidad)
        archivo_json = os.path.join(self.directorio, f"{nombre_sesion}.json")
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(datos_sesion, f, indent=2, ensure_ascii=False, default=str)
        
        # Guardar en pickle (para objetos Python completos)
        archivo_pickle = os.path.join(self.directorio, f"{nombre_sesion}.pkl")
        with open(archivo_pickle, 'wb') as f:
            pickle.dump(datos_sesion, f)
        
        return nombre_sesion
    
    def cargar_sesion(self, nombre_sesion, formato='json'):
        """
        Carga una sesión guardada.
        
        Args:
            nombre_sesion (str): Nombre de la sesión
            formato (str): 'json' o 'pickle'
            
        Returns:
            dict: Datos de la sesión
        """
        if formato == 'json':
            archivo = os.path.join(self.directorio, f"{nombre_sesion}.json")
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif formato == 'pickle':
            archivo = os.path.join(self.directorio, f"{nombre_sesion}.pkl")
            with open(archivo, 'rb') as f:
                return pickle.load(f)
        else:
            raise ValueError("Formato debe ser 'json' o 'pickle'")
    
    def listar_sesiones(self):
        """
        Lista todas las sesiones guardadas.
        
        Returns:
            list: Lista de nombres de sesiones
        """
        archivos = os.listdir(self.directorio)
        sesiones_json = [f.replace('.json', '') for f in archivos if f.endswith('.json')]
        return sorted(sesiones_json)
    
    def guardar_comparacion_metodos(self, comparaciones):
        """
        Guarda comparaciones entre métodos para análisis posterior.
        
        Args:
            comparaciones (list): Lista de comparaciones
        """
        archivo = os.path.join(self.directorio, 'comparaciones_metodos.json')
        
        # Cargar comparaciones existentes si existen
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                datos_existentes = json.load(f)
        else:
            datos_existentes = {'comparaciones': []}
        
        # Agregar nuevas comparaciones
        datos_existentes['comparaciones'].extend(comparaciones)
        datos_existentes['ultima_actualizacion'] = datetime.now().isoformat()
        
        # Guardar
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_existentes, f, indent=2, ensure_ascii=False, default=str)
    
    def exportar_para_excel(self, nombre_sesion):
        """
        Exporta datos en formato compatible con Excel.
        
        Args:
            nombre_sesion (str): Nombre de la sesión
            
        Returns:
            dict: Datos formateados para Excel
        """
        datos = self.cargar_sesion(nombre_sesion)
        
        # Formatear para Excel
        excel_data = {
            'resumen': {
                'Fecha': datos['timestamp'],
                'Valor_Cartas': datos['parametros']['valor_cartas'],
                'Objetivo': datos['parametros']['objetivo'],
                'Tolerancia': datos['parametros']['tolerancia']
            },
            'resultados_detallados': []
        }
        
        for metodo, resultado in datos['resultados'].items():
            if metodo != 'tiempos':
                excel_data['resultados_detallados'].append({
                    'Método': metodo,
                    'Convergencia': resultado['convergencia'],
                    'Raíz': resultado['raiz'],
                    'Iteraciones': resultado['iteraciones'],
                    'Error': resultado['error']
                })
        
        return excel_data
    
    def generar_estadisticas_historicas(self):
        """
        Genera estadísticas de todas las sesiones guardadas.
        
        Returns:
            dict: Estadísticas históricas
        """
        sesiones = self.listar_sesiones()
        
        if not sesiones:
            return {'mensaje': 'No hay sesiones guardadas'}
        
        estadisticas = {
            'total_sesiones': len(sesiones),
            'metodos': {
                'biseccion': {'convergencias': 0, 'total_iteraciones': []},
                'newton': {'convergencias': 0, 'total_iteraciones': []},
                'punto_fijo': {'convergencias': 0, 'total_iteraciones': []}
            },
            'problemas_analizados': [],
            'fechas': []
        }
        
        for sesion in sesiones:
            try:
                datos = self.cargar_sesion(sesion)
                estadisticas['fechas'].append(datos['timestamp'])
                
                problema = f"{datos['parametros']['valor_cartas']} → {datos['parametros']['objetivo']}"
                estadisticas['problemas_analizados'].append(problema)
                
                for metodo, resultado in datos['resultados'].items():
                    if metodo in estadisticas['metodos'] and resultado['convergencia']:
                        estadisticas['metodos'][metodo]['convergencias'] += 1
                        estadisticas['metodos'][metodo]['total_iteraciones'].append(
                            resultado['iteraciones']
                        )
            except:
                continue  # Sesión corrupta, omitir
        
        # Calcular promedios
        for metodo in estadisticas['metodos']:
            iteraciones = estadisticas['metodos'][metodo]['total_iteraciones']
            if iteraciones:
                estadisticas['metodos'][metodo]['promedio_iteraciones'] = sum(iteraciones) / len(iteraciones)
                estadisticas['metodos'][metodo]['tasa_convergencia'] = (
                    estadisticas['metodos'][metodo]['convergencias'] / len(sesiones) * 100
                )
        
        return estadisticas

# Instancia global para uso en la aplicación
almacenamiento = AlmacenamientoResultados()

# Datos predefinidos para casos de prueba
CASOS_PRUEBA_PREDEFINIDOS = [
    {
        'nombre': 'Caso Básico - Mano 10',
        'parametros': {
            'valor_cartas': 10,
            'objetivo': 21,
            'tolerancia': 1e-6,
            'max_iter': 100,
            'x0': 11,
            'a': 0,
            'b': 20
        },
        'raiz_esperada': 11,
        'descripcion': 'Caso estándar con mano de valor 10'
    },
    {
        'nombre': 'Mano Baja - Valor 6',
        'parametros': {
            'valor_cartas': 6,
            'objetivo': 21,
            'tolerancia': 1e-6,
            'max_iter': 100,
            'x0': 15,
            'a': 0,
            'b': 20
        },
        'raiz_esperada': 15,
        'descripcion': 'Mano baja, necesita mucho valor adicional'
    },
    {
        'nombre': 'Mano Alta - Valor 19',
        'parametros': {
            'valor_cartas': 19,
            'objetivo': 21,
            'tolerancia': 1e-6,
            'max_iter': 100,
            'x0': 2,
            'a': 0,
            'b': 5
        },
        'raiz_esperada': 2,
        'descripción': 'Mano alta, solo necesita poco valor'
    }
]

def obtener_caso_prueba(nombre):
    """
    Obtiene un caso de prueba predefinido por nombre.
    
    Args:
        nombre (str): Nombre del caso
        
    Returns:
        dict: Caso de prueba o None si no existe
    """
    for caso in CASOS_PRUEBA_PREDEFINIDOS:
        if caso['nombre'] == nombre:
            return caso
    return None

def listar_casos_prueba():
    """
    Lista todos los casos de prueba disponibles.
    
    Returns:
        list: Lista de nombres de casos
    """
    return [caso['nombre'] for caso in CASOS_PRUEBA_PREDEFINIDOS]