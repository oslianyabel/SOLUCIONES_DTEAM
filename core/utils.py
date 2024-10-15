import json
from app.models import *

def crear_generales(usuario, nombre_empresa, dir, mun, prov, email, tel, nombre, apellidos, cargo):
    try:
        generales = Generales.objects.get(usuario = usuario)
        Generales.objects.update(
            usuario=usuario,
            nombre_empresa=nombre_empresa,
            dir=dir,
            mun=mun,
            prov=prov,
            email=email,
            tel=tel,
            nombre=nombre,
            apellidos=apellidos,
            cargo=cargo
        )
        print("Generales actualizadas.")
    except Exception as error:
        Generales.objects.create(
            usuario=usuario,
            nombre_empresa=nombre_empresa,
            dir=dir,
            mun=mun,
            prov=prov,
            email=email,
            tel=tel,
            nombre=nombre,
            apellidos=apellidos,
            cargo=cargo
        )
        print("Generales creadas.")
        
        
def get_generales(usuario):
    try:
        generales = Generales.objects.get(usuario = usuario)
        print("Usuario con generales.")
        ans = {
            "usuario": generales.usuario,
            "nombre_empresa": generales.nombre_empresa,
            "dir": generales.dir,
            "mun": generales.mun,
            "prov": generales.prov,
            "email": generales.email,
            "tel": generales.tel,
            "nombre": generales.nombre,
            "apellidos": generales.apellidos,
            "cargo": generales.cargo
        }
        return json.dumps(ans)
    except Exception as error:
        print("Usuario sin generales.")
        return None
    
    
def Energux(
  usuario,
  cantidad_usuarios: int,
  entidad_consolidadora: bool,
  entidad_subordinada: bool,
  monedas_trabajo: list[str],
  centros_costo: int,
  tarjetas_combustibles: int,
  equipos: int,
  choferes: int,
  control_hojas_rutas: bool,
  plan_consumo_vehiculos: bool,
  modelo_portadores: str,
  sistema_contable_automatizado: bool,
  sistema_contable_utilizado: str,
  portadores: str,
  plan_mensual_portador: bool,
  registro_contadores_electricos: bool,
  registro_transformadores_electricos: bool,
  plan_consumo_electrico: bool,
  cuentas_control_combustible: str):
    generales = get_generales(usuario)
    if not generales:
        return "Usuario sin generales asociadas. Para crear la solicitud es necesario pedirle al usuario las generales de su empresa."
    
    datos = {
        "cantidad_usuarios": cantidad_usuarios,
        "entidad_consolidadora": entidad_consolidadora,
        "entidad_subordinada": entidad_subordinada,
        "monedas_trabajo": monedas_trabajo,
        "centros_costo": centros_costo,
        "tarjetas_combustibles": tarjetas_combustibles,
        "equipos": equipos,
        "choferes": choferes,
        "control_hojas_rutas": control_hojas_rutas,
        "plan_consumo_vehiculos": plan_consumo_vehiculos,
        "modelo_portadores": modelo_portadores,
        "sistema_contable_automatizado": sistema_contable_automatizado,
        "sistema_contable_utilizado": sistema_contable_utilizado,
        "portadores": portadores,
        "plan_mensual_portador": plan_mensual_portador,
        "registro_contadores_electricos": registro_contadores_electricos,
        "registro_transformadores_electricos": registro_transformadores_electricos,
        "plan_consumo_electrico": plan_consumo_electrico,
        "cuentas_control_combustible": cuentas_control_combustible
    }
    
    solicitud = Solicitud.objects.create(
        cliente = generales.usuario,
        empresa = generales.nombre_empresa,
        datos = json.dumps(datos),
        servicio = "EnerguX",
    )
    
    return "Solicitud enviada correctamente."


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})
    

def solicitud(servicio, usuario):
    Cliente_Pot.objects.create(
        cliente=usuario,
        servicio=servicio,
    )
    if servicio.nombre.lower() == "energux":
        return f'<p>Complete y envíe este <a href="/media/documentos/Cuestionario_Energux_5.0.doc">cuestionario</a> por correo a <a href="mailto:negocios.ssp@desoft.cu">negocios.ssp@desoft.cu</a>.</p> (Las etiquetas html envialas en formato html)'
    elif servicio.nombre.lower() == "myros":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Myros.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    elif servicio.nombre.lower() == "servidores":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Servidores.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    elif servicio.nombre.lower() == "fastos-pagus":
        return f'Complete y envíe este <a href="/media/documentos/Cuestionario_Fastos-Pagus.doc">cuestionario</a> por correo a negocios.ssp@desoft.cu'
    else:
        return "Servicio no disponible."
    