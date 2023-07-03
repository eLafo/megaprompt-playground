import streamlit as st
import utils


def main():
    st.set_page_config(
        page_title="My App",
        page_icon="🚀",
        layout="wide",
    )

    utils.init_prompt_inputs()
    if not "messages" in st.session_state:
        st.session_state["messages"] = []
    # Render the sidebar
    with st.sidebar:            
        # Ask the user for their OpenAI API key
        st.session_state["openai_api_key"] = st.text_input(
            "Enter your OpenAI API key", type="password")

    prompt_settings_tab, chat_tab = st.tabs(["Settings", "Chat"])

    if st.session_state.get("openai_api_key"):
        if not utils.check_openai_api_key(st.session_state["openai_api_key"]):
            st.error("Invalid OpenAI API key")
            st.stop()
        if new_message := st.chat_input("Type a message...", key="message_input"):
            with st.spinner("Thinking..."):
                utils.generate_response(new_message)

    with chat_tab:
        for message in st.session_state.get("messages", []):
            utils.print_message(message)

    with prompt_settings_tab:
        prompt_preview, prompt_settings_form = st.columns(2)
        with prompt_settings_form:
            utils.render_prompt_inputs_form()
            st.header("Raw prompt")
            st.code(utils.get_system_message(), language="markdown")

        with prompt_preview:
            utils.render_prompt_preview()

if __name__ == "__main__":
    main()
