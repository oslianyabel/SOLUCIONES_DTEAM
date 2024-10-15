import json, os
from dotenv import load_dotenv
from openai import OpenAI
from app.models import *
from core import utils

load_dotenv()

AVANGENIO_API_KEY = os.getenv('AVANGENIO_API_KEY')
client = OpenAI(
    base_url="https://apigateway.avangenio.net",
    api_key=AVANGENIO_API_KEY
)
model = "radiance"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Consulta la temperatura de una ubicacion.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "La ciudad y el estado, ej. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "solicitud",
            "description": "Guía al usuario a realizar una solicitud de contrato para adquirir un servicio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "servicio": {
                        "type": "string",
                        "description": "nombre del servicio solicitado, ej. EnerguX",
                    },
                },
                "required": ["servicio"],
            },
        },
    }
]


def get_sys_prompt():
    chatbot = ChatBot.objects.filter(activo = True)[0]
    sys_prompt = chatbot.sys_prompt
    sys_prompt += "A continuación se listan las redes sociales de SOLUCIONES DTEAM. Entrégaselas al usuario en formato html: \n"
    sys_prompt += f"{chatbot.facebook} \n"
    sys_prompt += f"{chatbot.instagram} \n"
    sys_prompt += f"{chatbot.X} \n"
    sys_prompt += f"{chatbot.telegram} \n"
    sys_prompt += f"{chatbot.whatsapp} \n"
    
    sys_prompt += "A continuación se muestra información detallada de la empresa: \n"
    sn = SobreNosotros.objects.filter(activo = True)[0]
    sys_prompt += f"{sn.parrafo} \n {sn.parrafo2} \n"
    
    sys_prompt += "A continuación se listan los nombres, categorías, descripciones, cantidad de votos y puntuación promedio de los servicios que ofrece SOLUCIONES DTEAM:\n"
    servicios = Servicio.objects.filter(activo = True)
    for s in servicios:
        sys_prompt += f"- Nombre:{s.nombre}, Categoria: {s.categoria}, Descripción: {s.descripcion}, Votos: {s.votos}, Rating: {s.puntos_promedio} \n"
        
    sys_prompt += "A continuación se listas las preguntas frecuentes con sus respuestas: \n"
    preguntas = PreguntaFrecuente.objects.filter(activo = True)
    for pf in preguntas:
        sys_prompt += f"Pregunta: {pf.pregunta} Respuesta: {pf.respuesta} \n"
        
    contacto = Contacto.objects.filter(activo = True)[0]
    sys_prompt += f"Esta es la dirección de la empresa: {contacto.direccion} \n"
    sys_prompt += f"Este es el correo de la empresa: {contacto.correo} \n"
    sys_prompt += f"Este es el teléfono fijo de la empresa: {contacto.telefono_fijo} \n"
    sys_prompt += f"Este es el teléfono móvil o celular de la empresa: {contacto.telefono_movil} \n"
    
    return sys_prompt
    
    
def run_conversation(usuario, new_msg: str, messages=None):
    if not messages:
        sys_prompt = get_sys_prompt()
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": new_msg}
        ]
    else:
        messages.append({"role": "user", "content": new_msg})
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
    except Exception as error:
        print(error)
        return "Lo sentimos, ha ocurrido un error, realice la consulta más tarde.", False
    tool_calls = response_message.tool_calls
    if not tool_calls:
        return response_message.content, True
    else:
        ok = True
        print("Llamada a herramenta.")
        available_functions = {
            "get_current_weather": utils.get_current_weather,
            "solicitud": utils.solicitud,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            try:
                function_name = tool_call.function.name
                print(function_name)
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print(function_args)
                
                if function_name == 'get_current_weather':
                    function_response = function_to_call(**function_args)
                elif function_name == 'solicitud':
                    nombre_serv = function_args["servicio"]
                    try:
                        servicio = Servicio.objects.filter(nombre = nombre_serv)[0]
                        function_response = function_to_call(servicio=servicio, usuario=usuario)
                    except Exception as error:
                        print(f"El servicio no existe: {error}")
                        function_response = "El servicio no existe."
                else:
                    function_response = "Herramienta desconocida."
                    print("Herramienta desconocida.")
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                print("Respuesta de la herramienta enviada al modelo.")
            except Exception as error:
                ok = False
                print(f"Error al ejecutar la herramienta: {error}")
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": "Error al ejecutar la herramienta.",
                    }
                )
        second_response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )
        print("Respuesta del modelo generada.")
        return second_response.choices[0].message.content, ok


if __name__ == "__main__":
    print(run_conversation("dame la temperatura en Paris"))