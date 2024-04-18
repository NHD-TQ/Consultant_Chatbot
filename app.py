import streamlit as st
# from process import bot

from llama_index.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent,
)
from llama_index.query_engine.pandas import PandasInstructionParser
from llama_index.llms import OpenAI
from llama_index.prompts import PromptTemplate
import os
import pandas as pd

# define api_key
os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']

# read data.
df = pd.read_csv("data/data.csv")

# defile module.
def bot(input):
    instruction_str = (
        "You are a sales consultant.\n"
        "1. Convert the query to executable Python code using Pandas.\n"
        "2. The final line of code should be a Python expression that can be called with the `eval()` function.\n"
        "3. The code should represent a solution to the query.\n"
        "4. PRINT ONLY THE EXPRESSION.\n"
        "5. Do not quote the expression.\n"
    )

    pandas_prompt_str = (
        "You are working with a pandas dataframe in Python.\n"
        "The name of the dataframe is `df`.\n"
        "This is the result of `print(df.head())`:\n"
        "{df_str}\n\n"
        "Follow these instructions:\n"
        "{instruction_str}\n"
        "Query: {query_str}\n\n"
        "Expression:"
    )
    response_synthesis_prompt_str = (
        "Given an input question, synthesize a response from the query results.\n"
        "Query: {query_str}\n\n"
        "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
        "Pandas Output: {pandas_output}\n\n"
        "If the query is not valid for pandas dataframe then respond like a sales consultant.\n"
        "You must answer all questions in Vietnamese.\n"
        "Response: "
    )

    pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
        instruction_str=instruction_str, df_str=df
    )
    pandas_output_parser = PandasInstructionParser(df)
    response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_str)
    llm = OpenAI(model="gpt-3.5-turbo")

    # build query pipeline.
    qp = QP(
        modules={
            "input": InputComponent(),
            "pandas_prompt": pandas_prompt,
            "llm1": llm,
            "pandas_output_parser": pandas_output_parser,
            "response_synthesis_prompt": response_synthesis_prompt,
            "llm2": llm,
        },
        verbose=True,
    )
    qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])
    qp.add_links(
        [
            Link("input", "response_synthesis_prompt", dest_key="query_str"),
            Link(
                "llm1", "response_synthesis_prompt", dest_key="pandas_instructions"
            ),
            Link(
                "pandas_output_parser",
                "response_synthesis_prompt",
                dest_key="pandas_output",
            ),
        ]
    )
    # add link from response synthesis prompt to llm2
    qp.add_link("response_synthesis_prompt", "llm2")

    response = qp.run(
        query_str=input,
    )

    return response.message.content








# App title
st.set_page_config(page_title="🦙💬 Chatbot - Beta")

with st.sidebar:
    st.title('Chatbot - Beta')

# Store LLM generated response
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Chào mừng bạn đến với cửa hàng của chúng tôi ! Bạn cần tìm hiểu thông tin về sản phẩm nào trong cửa hàng ?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message['content'])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Chào mừng bạn đến với cửa hàng của chúng tôi ! Bạn cần tìm hiểu thông tin về sản phẩm nào trong cửa hàng ?"}]
st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

# Create the LLM response generation function
def generate_responses(prompt_input):
    output = bot(prompt_input)
    return output

if prompt := st.chat_input(): # Kiểm tra xem replicate api đã tồn tại hay chưa nếu rồi thì gán prompt = st.chat_input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new LLM response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            response = generate_responses(prompt)
            print(response)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response) # Chuyển đổi response thành định dạng có thể display trên giao diện web
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
