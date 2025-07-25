import gradio as gr
from nomollm_agent.client import get_completion


def llm_response(message, history):
    return get_completion(message)


if __name__ == "__main__":
    gr.ChatInterface(llm_response).launch()
