import streamlit as st
import utils


def main():
    st.set_page_config(
        page_title="My App",
        page_icon="🚀",
        layout="wide",
    )

    utils.init_prompt_inputs()

    # Render the sidebar
    with st.sidebar:
        # Ask the user for their OpenAI API key
        st.session_state["openai_api_key"] = st.text_input(
            "Enter your OpenAI API key", type="password")

    chat_tab, prompt_settings_tab = st.tabs(["Chat", "Settings"])

    with chat_tab:
        for message in st.session_state.get("messages", []):
            utils.print_message(message)

    with prompt_settings_tab:
        prompt_preview, prompt_settings_form = st.columns(2)
        with prompt_settings_form:
            utils.render_prompt_inputs_form()
        with prompt_preview:
            utils.render_prompt_preview()

if __name__ == "__main__":
    main()
