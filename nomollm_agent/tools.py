import inspect
import functools


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

    tool_spec = [
        {
            "type": "function",
            "name": func_name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
            "strict": True,
        }
    ]

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.info = tool_spec
    return wrapper


@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b
