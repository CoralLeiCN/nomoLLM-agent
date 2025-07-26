from nomollm_agent.tools import extract_function_info


def test_extract_function_info_decorator_behavior():
    """
    Tests that the extract_function_info decorator correctly creates the info
    attribute and preserves the original function's behavior.
    """

    # 1. Define a sample function to be decorated
    def sample_function(name: str, count: int = 1) -> str:
        """A sample function with a docstring."""
        return f"Hello {name}" * count

    # 2. Apply the decorator
    decorated_function = extract_function_info(sample_function)

    # 3. Define the expected JSON schema
    expected_info = [
        {
            "type": "function",
            "name": "sample_function",
            "description": "A sample function with a docstring.",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string"}, "count": {"type": "number"}},
                "required": ["name"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    ]

    # 4. Assert that the .info attribute is correct
    assert hasattr(decorated_function, "info")
    assert decorated_function.info == expected_info

    # 5. Assert that the decorated function still works as expected
    assert decorated_function("World", count=2) == "Hello WorldHello World"
