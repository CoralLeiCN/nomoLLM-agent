import functools
import inspect

import requests

# Global registry to store available tools
TOOL_REGISTRY = {}


def tool(func):
    """
    A decorator that inspects a function and creates a JSON schema representation for it.
    """
    sig = inspect.signature(func)
    func_name = func.__name__
    description = func.__doc__.strip() if func.__doc__ else ""

    # Map Python types to JSON schema types
    type_mapping = {
        int: "number",
        float: "number",
        str: "string",
        bool: "boolean",
    }

    properties = {}
    required = []

    for name, param in sig.parameters.items():
        if param.annotation in type_mapping:
            properties[name] = {"type": type_mapping[param.annotation]}
        if param.default is inspect.Parameter.empty:
            required.append(name)

    tool_spec = {
        "type": "function",
        "function": {
            "name": func_name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
    TOOL_REGISTRY[func_name] = func

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.info = tool_spec
    return wrapper


@tool
def get_weather(latitude: float, longitude: float) -> float:
    """
    "Get current temperature for provided coordinates in celsius.",

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
    Returns:
        float: The current temperature in Celsius.
    """
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]["temperature_2m"]


@tool
def add(a: int, b: int) -> int:
    """
    Adds two integers together.

    Args:
        a (int): The first integer to add.
        b (int): The second integer to add.

    Returns:
        int: The sum of a and b.
    """
    return a + b


def call_function(name, args):
    if name in TOOL_REGISTRY:
        print(f"Find function {name} in TOOL_REGISTRY")
        return TOOL_REGISTRY[name](**args)
