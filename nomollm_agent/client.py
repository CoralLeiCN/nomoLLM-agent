from openai import OpenAI
import os
from dotenv import load_dotenv
from nomollm_agent.prompt.prompts import system_prompt

load_dotenv()


# Configure OpenAI client to use Mistral AI
client = OpenAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    base_url="https://api.mistral.ai/v1",
)


def chat_with_mistral(messages, model="mistral-medium-latest", **kwargs):
    """
    Send a chat completion request to Mistral AI using the OpenAI client interface.

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        model: Mistral model to use (e.g., "mistral-small-latest", "mistral-medium-latest", "mistral-large-latest")
        **kwargs: Additional parameters like temperature, max_tokens, etc.

    Returns:
        OpenAI ChatCompletion response object
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": messages},
    ]
    response = client.chat.completions.create(model=model, messages=messages, **kwargs)
    return response


def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
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
