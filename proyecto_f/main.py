from flask import Flask, render_template, request, jsonify
import requests
import math
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

app = Flask(__name__)

# ==================== COORDENADAS SAN MARCOS ====================
SAN_MARCOS_LAT = 21.8808
SAN_MARCOS_LON = -102.2918
SEARCH_RADIUS = 0.03  # ~3km
MAX_NODOS = 100

# ==================== DATOS REALES DE SAN MARCOS ====================
PUNTOS_SAN_MARCOS = [
    {"id": "osm_1", "nombre": "Jardín de San Marcos", "lat": 21.8808, "lon": -102.2918, "tipo": "Plaza", "descripcion": "Jardín público del barrio"},
    {"id": "osm_2", "nombre": "Palenque de la Feria", "lat": 21.8795, "lon": -102.2910, "tipo": "Plaza", "descripcion": "Palenque para conciertos"},
    {"id": "osm_3", "nombre": "Capilla de San Marcos", "lat": 21.8815, "lon": -102.2920, "tipo": "Centro", "descripcion": "Templo religioso"},
    {"id": "osm_4", "nombre": "Mercado de San Marcos", "lat": 21.8800, "lon": -102.2895, "tipo": "Mercado", "descripcion": "Mercado tradicional"},
    {"id": "osm_5", "nombre": "Fonda San Marcos", "lat": 21.8820, "lon": -102.2905, "tipo": "Restaurante", "descripcion": "Comida mexicana"},
    {"id": "osm_6", "nombre": "Farmacia San Marcos", "lat": 21.8810, "lon": -102.2925, "tipo": "Farmacia", "descripcion": "Servicios farmacéuticos"},
    {"id": "osm_7", "nombre": "Escuela Primaria San Marcos", "lat": 21.8790, "lon": -102.2940, "tipo": "Escuela", "descripcion": "Centro educativo"},
    {"id": "osm_8", "nombre": "Banco del Bajío", "lat": 21.8825, "lon": -102.2910, "tipo": "Banco", "descripcion": "Servicios bancarios"},
    {"id": "osm_9", "nombre": "Café San Marcos", "lat": 21.8812, "lon": -102.2930, "tipo": "Café", "descripcion": "Bebidas y desayunos"},
    {"id": "osm_10", "nombre": "Biblioteca Pública", "lat": 21.8805, "lon": -102.2885, "tipo": "Biblioteca", "descripcion": "Centro de lectura"},
    {"id": "osm_11", "nombre": "Parque Infantil", "lat": 21.8775, "lon": -102.2920, "tipo": "Parque", "descripcion": "Área recreativa"},
    {"id": "osm_12", "nombre": "Clínica San Marcos", "lat": 21.8830, "lon": -102.2900, "tipo": "Hospital", "descripcion": "Servicio médico"},
]

@dataclass
class PuntoInteres:
    """Clase para punto de interés"""
    id: str
    nombre: str
    lat: float
    lon: float
    tipo: str
    descripcion: str = ""
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "lat": self.lat,
            "lon": self.lon,
            "tipo": self.tipo,
            "descripcion": self.descripcion
        }

class RoutingService:
    """Servicio de enrutamiento con optimización por modo de transporte"""
    
    @staticmethod
    def obtener_ruta_real(lat_origen: float, lon_origen: float,
                         lat_destino: float, lon_destino: float,
                         modo: str = "car") -> Optional[Dict]:
        """
        Obtiene ruta usando OSRM optimizada por modo de transporte
        modo: "car" para carro, "foot" para pie
        """
        try:
            # Seleccionar perfil de OSRM según modo
            perfil = "driving" if modo == "car" else "foot"
            
            url = f"https://router.project-osrm.org/route/v1/{perfil}/{lon_origen},{lat_origen};{lon_destino},{lat_destino}"
            
            params = {
                "overview": "full",
                "geometries": "geojson",
                "steps": "true",
                "annotations": "duration,distance"
            }
            
            respuesta = requests.get(url, params=params, timeout=15)
            
            if respuesta.status_code != 200:
                print(f"Error OSRM {respuesta.status_code}")
                return None
            
            datos = respuesta.json()
            
            if not datos.get("routes"):
                return None
            
            ruta = datos["routes"][0]
            geometry = ruta.get("geometry")
            
            if not geometry or not geometry.get("coordinates"):
                return None
            
            distancia = ruta.get("distance", 0)
            duracion = ruta.get("duration", 0)
            
            # Calcular velocidad promedio
            velocidad_kmh = round((distancia / 1000) / (duracion / 3600), 1) if duracion > 0 else 0
            
            pasos = []
            try:
                legs = ruta.get("legs", [])
                for leg in legs:
                    for paso in leg.get("steps", []):
                        instruccion = paso.get("maneuver", {}).get("instruction", "Continuar")
                        pasos.append({
                            "instruccion": instruccion,
                            "distancia_m": round(paso.get("distance", 0), 2),
                            "duracion_s": round(paso.get("duration", 0), 1)
                        })
            except:
                pasos = []
            
            return {
                "coordenadas": geometry["coordinates"],
                "distancia_m": distancia,
                "distancia_km": round(distancia / 1000, 2),
                "tiempo_minutos": round(duracion / 60, 1),
                "tiempo_segundos": round(duracion, 0),
                "velocidad_kmh": velocidad_kmh,
                "pasos": pasos if pasos else [],
                "modo": modo,
                "perfil": perfil
            }
        
        except Exception as e:
            print(f"Error OSRM: {str(e)}")
            return None

class GrafoPuntos:
    """Almacén de puntos con caching"""
    def __init__(self):
        self.puntos: Dict[str, PuntoInteres] = {}
    
    def agregar_punto(self, punto: PuntoInteres):
        self.puntos[punto.id] = punto
    
    def agregar_puntos_batch(self, puntos_data: List[Dict]):
        """Agrega múltiples puntos respetando MAX_NODOS"""
        for p_data in puntos_data:
            if len(self.puntos) >= MAX_NODOS:
                break
            
            punto = PuntoInteres(
                id=p_data['id'],
                nombre=p_data['nombre'],
                lat=p_data['lat'],
                lon=p_data['lon'],
                tipo=p_data['tipo'],
                descripcion=p_data.get('descripcion', '')
            )
            self.agregar_punto(punto)
    
    def buscar_puntos(self, query: str) -> List[PuntoInteres]:
        """Búsqueda de puntos por nombre, tipo o descripción"""
        query_lower = query.lower().strip()
        
        if not query_lower:
            return list(self.puntos.values())
        
        resultados = []
        for punto in self.puntos.values():
            if query_lower in punto.nombre.lower():
                resultados.append(punto)
            elif query_lower in punto.tipo.lower():
                resultados.append(punto)
            elif query_lower in punto.descripcion.lower():
                resultados.append(punto)
        
        return sorted(resultados, key=lambda p: p.nombre)

# Instancia global
grafo = GrafoPuntos()

# ==================== RUTAS API ====================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/puntos", methods=["GET"])
def api_puntos():
    """Obtiene todos los puntos de San Marcos"""
    try:
        if grafo.puntos:
            puntos = [p.to_dict() for p in sorted(grafo.puntos.values(), key=lambda x: x.nombre)]
            return jsonify({
                "success": True,
                "data": puntos,
                "total": len(puntos),
                "maximo": MAX_NODOS,
                "fuente": "Cache Local"
            })
        
        # Si no hay en caché, usar datos locales
        grafo.agregar_puntos_batch(PUNTOS_SAN_MARCOS)
        puntos = [p.to_dict() for p in sorted(grafo.puntos.values(), key=lambda x: x.nombre)]
        
        return jsonify({
            "success": True,
            "data": puntos,
            "total": len(puntos),
            "maximo": MAX_NODOS,
            "fuente": "Base de Datos Local (San Marcos)"
        })
    
    except Exception as e:
        grafo.agregar_puntos_batch(PUNTOS_SAN_MARCOS)
        puntos = [p.to_dict() for p in sorted(grafo.puntos.values(), key=lambda x: x.nombre)]
        
        return jsonify({
            "success": True,
            "data": puntos,
            "total": len(puntos),
            "maximo": MAX_NODOS,
            "fuente": "Base de Datos Local"
        })

@app.route("/api/buscar", methods=["POST"])
def api_buscar():
    """Búsqueda rápida de lugares"""
    try:
        data = request.json
        query = data.get("query", "").strip()
        
        if not query or len(query) < 1:
            return jsonify({
                "success": False,
                "error": "Mínimo 1 carácter"
            }), 400
        
        resultados = grafo.buscar_puntos(query)
        
        return jsonify({
            "success": True,
            "data": [p.to_dict() for p in resultados],
            "total": len(resultados)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error: {str(e)}"
        }), 500

@app.route("/api/ruta", methods=["POST"])
def api_ruta():
    """
    Calcula ruta optimizada por modo de transporte
    Parámetros: origen, destino, modo ("car" o "foot")
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({"success": False, "error": "Body JSON requerido"}), 400
        
        origen_id = data.get("origen")
        destino_id = data.get("destino")
        modo = data.get("modo", "car").lower()  # "car" o "foot"
        
        # Validar modo
        if modo not in ["car", "foot"]:
            modo = "car"
        
        if not origen_id or not destino_id:
            return jsonify({"success": False, "error": "Se requieren origen y destino"}), 400
        
        origen = grafo.puntos.get(origen_id)
        destino = grafo.puntos.get(destino_id)
        
        if not origen or not destino:
            return jsonify({"success": False, "error": "Puntos no encontrados"}), 404
        
        if origen_id == destino_id:
            return jsonify({"success": False, "error": "Deben ser diferentes"}), 400
        
        # Obtener ruta con modo específico
        ruta_info = RoutingService.obtener_ruta_real(
            origen.lat, origen.lon,
            destino.lat, destino.lon,
            modo=modo  # Pasar el modo de transporte
        )
        
        if not ruta_info:
            return jsonify({"success": False, "error": "No se pudo calcular la ruta"}), 503
        
        pasos = ruta_info.get("pasos", [])
        if not isinstance(pasos, list):
            pasos = []
        
        return jsonify({
            "success": True,
            "data": {
                "origen_id": origen_id,
                "destino_id": destino_id,
                "origen_nombre": origen.nombre,
                "destino_nombre": destino.nombre,
                "origen_lat": origen.lat,
                "origen_lon": origen.lon,
                "destino_lat": destino.lat,
                "destino_lon": destino.lon,
                "coordenadas": ruta_info["coordenadas"],
                "distancia_km": ruta_info["distancia_km"],
                "tiempo_minutos": ruta_info["tiempo_minutos"],
                "tiempo_segundos": ruta_info["tiempo_segundos"],
                "velocidad_kmh": ruta_info["velocidad_kmh"],
                "modo": ruta_info["modo"],
                "modo_label": "A pie" if ruta_info["modo"] == "foot" else "En carro",
                "pasos": pasos[:15]
            }
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"success": False, "error": f"Error: {str(e)}"}), 500

@app.route("/api/info", methods=["GET"])
def api_info():
    """Información del sistema"""
    return jsonify({
        "success": True,
        "data": {
            "ciudad": "Aguascalientes",
            "barrio": "San Marcos",
            "puntos_cargados": len(grafo.puntos),
            "maximo_nodos": MAX_NODOS,
            "modos_transporte": ["car", "foot"]
        }
    })

@app.errorhandler(404)
def no_encontrado(e):
    return jsonify({"success": False, "error": "No encontrado"}), 404

@app.errorhandler(500)
def error_interno(e):
    return jsonify({"success": False, "error": "Error interno"}), 500

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    print("\n" + "="*70)
    print("🎪 NAVEGADOR DE RUTAS - SAN MARCOS (VERSIÓN FINAL)")
    print("="*70)
    print(f"📍 Ubicación: Barrio San Marcos, Aguascalientes")
    print(f"🌐 URL: http://localhost:5001")
    print(f"🚗 Modos: A pie / En carro")
    print(f"📦 Máximo de nodos: {MAX_NODOS}")
    print("="*70 + "\n")
    app.run(debug=True, port=5001, host="0.0.0.0")