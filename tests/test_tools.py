from nomollm_agent.tools import tool


def test_extract_function_info_decorator_behavior():
    """
    Tests that the extract_function_info decorator correctly creates the info
    attribute and preserves the original function's behavior.
    """

    # 1. Define a sample function to be decorated
    @tool
    def sample_function(name: str, count: int = 1) -> str:
        """A sample function with a docstring."""
        return f"Hello {name}" * count

    # 2. Apply the decorator
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
    assert hasattr(sample_function, "info")
    assert sample_function.info == expected_info

    # 5. Assert that the decorated function still works as expected
    assert sample_function("World", count=2) == "Hello WorldHello World"
