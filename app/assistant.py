import json, os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

AVANGENIO_API_KEY = os.getenv('AVANGENIO_API_KEY')
client = OpenAI(
    base_url="https://apigateway.avangenio.net",
    api_key=AVANGENIO_API_KEY
)
model = "radiance"


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


def run_conversation(new_msg: str):
    messages = [
        {"role": "system", "content": "Eres un asistente virtual de la empresa SOLUCIONES DTEAM. Ayuda a los clientes en sus consultas."},
        {"role": "user", "content": new_msg}
    ]
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
        }
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if not tool_calls:
        return response_message.content
    else:
        print("Llamada a herramenta.")
        available_functions = {
            "get_current_weather": get_current_weather,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            print(function_name)
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print(function_args)
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )
        return second_response.choices[0].message.content


if __name__ == "__main__":
    print(run_conversation("dame la temperatura en Paris"))