import streamlit as st
import openai
import yaml
import pyperclip

from langchain.llms import OpenAI
from prompts.application_prompt import prompt as application_prompt

ROLES_MAP = {
    "human": "user",
    "ai": "assistant",
    "system": "system"
}


def render_prompt_inputs_form():
    final_prompt = application_prompt.final_prompt
    pipeline_prompts = dict(application_prompt.pipeline_prompts)

    for input_variable in final_prompt.input_variables:
        inputs = {}
        with st.expander(input_variable):
            with st.form(input_variable):
                if input_variable in pipeline_prompts:
                    # inputs[input_variable] = {}
                    for input_variable_2 in pipeline_prompts[input_variable].input_variables:
                        inputs[input_variable_2] = st.text_area(
                            input_variable_2, value=get_prompt_input(input_variable_2))
                else:
                    inputs[input_variable] = st.text_area(
                        input_variable, value=get_prompt_input(input_variable))

                if st.form_submit_button("Submit"):
                    for key, value in inputs.items():
                        set_prompt_input(key, value)


def render_prompt_preview():
    prompt = application_prompt.format(**st.session_state["prompt_inputs"])
    print(prompt)
    st.markdown(prompt)
    if st.button("Copy to clipboard"):
        pyperclip.copy(prompt)


def init_prompt_inputs():
    if "prompt_inputs" not in st.session_state:
        st.session_state["prompt_inputs"] = {}

        with open("default_prompt_inputs.yaml", "r") as file:
            default_values = yaml.safe_load(file)

        final_prompt = application_prompt.final_prompt
        pipeline_prompts = dict(application_prompt.pipeline_prompts)

        st.header("Inputs")

        for input_variable in final_prompt.input_variables:
            if input_variable in pipeline_prompts:
                for input_variable_2 in pipeline_prompts[input_variable].input_variables:
                    set_prompt_input(input_variable_2,
                                     default_values[input_variable_2])
            else:
                set_prompt_input(
                    input_variable, default_values[input_variable])


def print_message(message):
    role = ROLES_MAP[message.type]

    if message.type != "system":
        st.chat_message(role).write(message.content)


def set_prompt_input(key, value):
    if "prompt_inputs" not in st.session_state:
        st.session_state["prompt_inputs"] = {}
    st.session_state["prompt_inputs"][key] = value


def get_prompt_input(key):
    return st.session_state.get("prompt_inputs", {key: None})[key]


def check_openai_api_key(openai_api_key):
    openai.api_key = openai_api_key
    try:
        openai.Engine.list()
        return True
    except openai.error.AuthenticationError:
        return False


def setup_llm(openai_api_key=None, temperature=0):
    return OpenAI(openai_api_key=openai_api_key, temperature=temperature)


def is_empty(variable):
    if variable is None:
        return True
    elif isinstance(variable, str) and variable.strip() == "":
        return True
    elif isinstance(variable, list) and len(variable) == 0:
        return True
    elif not variable:
        return True
    else:
        return False
