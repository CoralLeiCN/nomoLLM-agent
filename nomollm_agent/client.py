import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from nomollm_agent.prompt.prompts import system_prompt
from nomollm_agent.tools import call_function

load_dotenv()


# Configure OpenAI client to use Mistral AI
client = OpenAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    base_url="https://api.mistral.ai/v1",
)


def chat_with_mistral(messages, tools, model="mistral-medium-latest", **kwargs):
    """
    Send a chat completion request to Mistral AI using the OpenAI client interface.

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        tools: List of tool specifications to be used in the chat
        model: Mistral model to use (e.g., "mistral-small-latest", "mistral-medium-latest", "mistral-large-latest")
        **kwargs: Additional parameters like temperature, max_tokens, etc.

    Returns:
        List of messages including the model's response and any tool call results.
    """

    completion = client.chat.completions.create(
        model=model, messages=messages, tools=tools, **kwargs
    )

    # if function calls are present, execute them
    if completion.choices[0].message.tool_calls:
        messages.append(
            completion.choices[0].message
        )  # append model's function call message

        print(len(completion.choices[0].message.tool_calls), "tool calls found")
        for tool_call in completion.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"Calling function: {name} with args: {args}")
            result = call_function(name, args)
            print(f"Function {name} returned: {result}")

            messages.append(
                {  # append result message
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )
    else:
        print("No tool calls found")
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )
    messages.append(completion.choices[0].message)

    return messages


def get_completion(prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    response = chat_with_mistral(messages)
    return response.choices[0].message.content


# Example usage function
def example_chat():
    messages = [{"role": "user", "content": "Hello! How are you today?"}]

    response = chat_with_mistral(messages)
    return response.choices[0].message.content


if __name__ == "__main__":
    # Example usage
    try:
        result = example_chat()
        print("Mistral AI Response:", result)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your MISTRAL_API_KEY environment variable")
