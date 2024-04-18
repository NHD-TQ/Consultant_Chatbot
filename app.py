import streamlit as st
from process import bot
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
