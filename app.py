import gradio as gr

from nomollm_agent.client import chat_with_mistral
from nomollm_agent.tools import add, get_weather

tools = [add.info, get_weather.info]

# Separate variable to maintain chat history
chat_history = []


def multi_turns_conversation(message, history):
    keys_to_keep = ["role", "content"]
    history = [{k: d[k] for k in keys_to_keep if k in d} for d in history]
    history.append({"role": "user", "content": message})

    # Get LLM response
    llm_response = chat_with_mistral(history, tools)
    return llm_response[-1].content


def customised_multi_turns_conversation(message, history):
    """
    Handle conversation with separate history management.

    Args:
        message: Current user message (dict with 'role' and 'content')
        history: Gradio's display history (we'll ignore this)

    Returns:
        Updated history for display
    """
    global chat_history

    # Add user message to our separate history
    user_message = {"role": "user", "content": message}
    chat_history.append(user_message)

    # Get LLM response using our separate history
    chat_history = chat_with_mistral(chat_history, tools)
    # Return the updated history for Gradio to display
    return chat_history[-1].content


if __name__ == "__main__":
    gr.ChatInterface(customised_multi_turns_conversation, type="messages").launch()
