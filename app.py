import gradio as gr

from nomollm_agent.client import chat_with_mistral
from nomollm_agent.tools import add, get_weather

tools = [add.info, get_weather.info]


def multi_turns_conversation(message, history):
    keys_to_keep = ["role", "content"]
    history = [{k: d[k] for k in keys_to_keep if k in d} for d in history]
    history.append({"role": "user", "content": message})

    # Get LLM response
    llm_response = chat_with_mistral(history, tools)
    return llm_response[-1].content


if __name__ == "__main__":
    # Remove type="messages" as it's not needed for the corrected implementation
    gr.ChatInterface(multi_turns_conversation, type="messages").launch()
