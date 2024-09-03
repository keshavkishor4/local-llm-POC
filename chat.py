from typing import List
import chainlit as cl
from ctransformers import AutoModelForCausalLM


# # LLAMA Model
# llm = AutoModelForCausalLM.from_pretrained(
#     "TheBloke/Llama-2-7b-Chat-GGUF", model_file="llama-2-7b-chat.Q5_K_M.gguf"
# )
# prompt = "Hey, How are you?"

# print(llm(prompt))

# prompt = "What is the name of the capital city of India. Please respond with the city name only and then stop talking. LLM answered: "
# print(prompt + llm(prompt))

def get_prompt(instruction: str, history: List[str] = None) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the question in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n"
    if len(history) > 0:
        prompt += f"This is the conversation history: {''.join(history)}. Now answer the question:-"
    prompt += f"{instruction}\n\n### Response:\n"
    # prompt = f"<s>[INST] <<SYS>>\n{system}\n<</SYS>>\n\n{instruction} [/INST]"
    print(f"Prompt created: {prompt}")
    return prompt

@cl.on_message
async def on_message(message: cl.Message):
    # response = f"Hello, you just sent: {message.content}!"
    message_history = cl.user_session.get("message_history")
    msg = cl.Message(content="")
    await msg.send()
    prompt = get_prompt(message.content, message_history)
    response = ""
    for word in llm(prompt, stream=True):
        await msg.stream_token(word)
        response += word
    await msg.update()
    message_history.append(response)
    # response = llm(prompt)
    # await cl.Message(response).send()

@cl.on_chat_start
def on_chat_start():
    # orca Model
    cl.user_session.set("message_history", [])
    global llm
    llm = AutoModelForCausalLM.from_pretrained(
        "zoltanctoth/orca_mini_3B-GGUF", model_file="orca-mini-3b.q4_0.gguf"
)
"""
def get_prompt(instruction: str, history: List[str] = None) -> str:
    system = "You are an AI assistant that gives helpful answers. You answer the question in a short and concise way."
    prompt = f"### System:\n{system}\n\n### User:\n"
    if history is not None:
        prompt += f"This is the conversation history: {''.join(history)}. Now answer the question:-"
    prompt += f"{instruction}\n\n### Response:\n"
    # prompt = f"<s>[INST] <<SYS>>\n{system}\n<</SYS>>\n\n{instruction} [/INST]"
    print(f"Prompt created: {prompt}")
    return prompt


history = []
question = "Which city is the capital of India?"
prompt = get_prompt(question)
answer = ""
for word in llm(prompt, stream=True):
    print(word, end="", flush=True)
    answer += word
history.append(answer)
print()

question = "And what  is the capital of united states?"
prompt = get_prompt(question, history)
for word in llm(prompt, stream=True):
    print(word, end="", flush=True)
print()

"""