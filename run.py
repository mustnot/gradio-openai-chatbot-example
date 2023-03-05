import os

import openai
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_messages(messages: list):
    result = []
    for index in range(0, len(messages)-1, 2):
        result.append([messages[index]["content"], messages[index+1]["content"]])
    return result


def answer(input, history=[]):
    history.append(
        {"role": "user", "content": input}
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
    )
    response_content = response["choices"][-1]["message"]["content"].strip()

    history.append(
        {"role": "assistant", "content": response_content}
    )

    messages = generate_messages(history)
    return messages, history


def reset(chatbot, state):
    return [], []


with gr.Blocks() as app:
    state = gr.State([])
    chatbot = gr.Chatbot()
    
    textbox = gr.Textbox(show_label=False, placeholder="질문을 해주세요.").style(container=False)
    reset_button = gr.Button(value="초기화")

    textbox.submit(answer, [textbox, state], [chatbot, state])
    reset_button.click(reset, [chatbot, state], [chatbot, state])


if __name__ == "__main__":
    app.launch()
