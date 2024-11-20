import json

import streamlit as st
from openai import OpenAI
from tools import available_tools, functions

from utils import display_message

# define model
MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful assistant with tool calling capabilities. When you receive a tool call response, use the output to format an answer to the orginal use question.",
}

client = OpenAI(
    base_url="http://127.0.0.1:8001/v1",
    api_key="lit",
)

st.title("Chat with an AI Assistant.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add input field for system prompt
st.sidebar.header("System Prompt")
system_prompt = st.sidebar.text_area(
    label="Modify the prompt here.", value=SYSTEM_MESSAGE["content"], height=200
)
SYSTEM_MESSAGE["content"] = system_prompt


# Add checkboxes to the sidebar
st.sidebar.header("Available Tools")
selected_tools = [
    tool["function"]["name"]
    for tool in available_tools
    if st.sidebar.checkbox(tool["function"]["name"], value=True)
]

# Filter available tools based on selected tools
tools = [tool for tool in available_tools if tool["function"]["name"] in selected_tools]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    display_message(message)

# Accept user input
if prompt := st.chat_input("Ask anything?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        messages = [SYSTEM_MESSAGE, *st.session_state.messages]
        if not tools:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            spinner = st.spinner("Thinking...")
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=available_tools,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            if tool_calls:
                with st.status("Thinking...", expanded=True) as status:
                    st.session_state.messages.append(response_message)
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        tool = functions[function_name]
                        args = json.loads(tool_call.function.arguments)
                        st.write(f"Calling {function_name}... with args: {args}")
                        tool_response = tool(**args)
                        st.session_state.messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "ipython",
                                "content": tool_response,
                                "name": function_name,
                            }
                        )
                        status.update(
                            label=f"Running {function_name}... Done!",
                            state="complete",
                            expanded=False,
                        )
                stream = client.chat.completions.create(
                    model=MODEL, messages=st.session_state.messages, stream=True
                )
                response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            else:
                response = response.choices[0].message
                st.write(response.content)
                st.session_state.messages.append(response)
