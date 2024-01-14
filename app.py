from typing import List, Union
from dotenv import load_dotenv, find_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import streamlit as st
import configparser


def read_config(file_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def init_page() -> None:
    st.set_page_config(
        page_title="Saurabh's Chat Assistant"
    )
    st.header("Saurabh's Chat Assistant")
    st.sidebar.title("Options")


def init_messages() -> None:
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content="You are a helpful AI assistant. Reply your answer in mardkown format.")
        ]
        st.session_state.costs = []


def select_llm() -> Union[ChatOpenAI, LlamaCpp]:
    
    config = read_config()
    openai_kay = config.get('Credentials', 'openaikay')
    llama_path = config.get('Credentials', 'llama_path')
    mistrl_path = config.get('Credentials', 'mistrl_path')


    model_name = st.sidebar.radio("Choose LLM:",
                                  ("gpt-3.5-turbo-0613", "gpt-4",
                                   "llama-2-7b-chat.Q4_K_M",'mistral-7b-v0.1.Q4_0'))
    temperature = st.sidebar.slider("Temperature:", min_value=0.0,
                                    max_value=1.0, value=0.0, step=0.01)
    if model_name.startswith("gpt-"):
        return ChatOpenAI(temperature=temperature, model_name=model_name,
                          openai_api_key=openai_kay)
    elif model_name.startswith("llama-2-"):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        return LlamaCpp(
                model_path=llama_path,
                temperature=temperature,
                max_tokens=100,
                top_p=1,
                callback_manager=callback_manager,
                verbose=True
                    )
    
    elif model_name.startswith("mistral"):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        return LlamaCpp(
                model_path=mistrl_path,
                temperature=temperature,
                max_tokens=100,
                top_p=1,
                callback_manager=callback_manager,
                verbose=True
                    )

def get_answer(llm, messages) -> tuple[str, float]:
    if isinstance(llm, ChatOpenAI):
        with get_openai_callback() as cb:
            answer = llm(messages)
        return answer.content, cb.total_cost
    if isinstance(llm, LlamaCpp):
        return llm(llama_v2_prompt(convert_langchainschema_to_dict(messages))), 0.0


def find_role(message: Union[SystemMessage, HumanMessage, AIMessage]) -> str:
    """
    Identify role name from langchain.schema object.
    """
    if isinstance(message, SystemMessage):
        return "system"
    if isinstance(message, HumanMessage):
        return "user"
    if isinstance(message, AIMessage):
        return "assistant"
    raise TypeError("Unknown message type.")


def convert_langchainschema_to_dict(
        messages: List[Union[SystemMessage, HumanMessage, AIMessage]]) \
        -> List[dict]:
    """
    Convert the chain of chat messages in list of langchain.schema format to
    list of dictionary format.
    """
    return [{"role": find_role(message),
             "content": message.content
             } for message in messages]


def llama_v2_prompt(messages: List[dict]) -> str:
    """
    Convert the messages in list of dictionary format to Llama2 compliant format.
    """
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    BOS, EOS = "<s>", "</s>"
    DEFAULT_SYSTEM_PROMPT = f"""You are a helpful, respectful and honest assistant. 
    Always answer as helpfully as possible, while being safe. 
    Please ensure that your responses are socially unbiased and positive in nature. 
    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
    If you don't know the answer to a question, please don't share false information."""

    if messages[0]["role"] != "system":
        messages = [
            {
                "role": "system",
                "content": DEFAULT_SYSTEM_PROMPT,
            }
        ] + messages
    messages = [
        {
            "role": messages[1]["role"],
            "content": B_SYS + messages[0]["content"] + E_SYS + messages[1]["content"],
        }
    ] + messages[2:]

    messages_list = [
        f"{BOS}{B_INST} {(prompt['content']).strip()} {E_INST} {(answer['content']).strip()} {EOS}"
        for prompt, answer in zip(messages[::2], messages[1::2])
    ]
    messages_list.append(
        f"{BOS}{B_INST} {(messages[-1]['content']).strip()} {E_INST}")

    return "".join(messages_list)


def main() -> None:
    _ = load_dotenv(find_dotenv())

    init_page()
    llm = select_llm()
    init_messages()

    # Supervise user input
    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Assistant is typing ..."):
            answer, cost = get_answer(llm, st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer))
        st.session_state.costs.append(cost)

    # Display chat history
    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

    costs = st.session_state.get("costs", [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


# streamlit run app.py
if __name__ == "__main__":
    main()