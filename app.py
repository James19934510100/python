import os
os.environ['DASHSCOPE_API_KEY'] = 'sk-7df6ff73bfd54925938c58eb83e3e5d6'

import streamlit as st

# 聊天机器人页面，可视化展示内容和大模型的聊天记录
from pydantic import BaseModel

# 构建和大模型聊天chain

# 1. 使用通义大模型
from langchain_community.chat_models.tongyi import ChatTongyi
# 2. 构建聊天机制并保存聊天记录
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
# 3. 保存角色输入的内容
from langchain.schema import HumanMessage, AIMessage


# 设置背景
import streamlit as st
 
with open(r"C:\Users\49033\Desktop\AItest\style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.title("通航小智")
st.write("Welcome to our school!")
st.image(r'C:\Users\49033\Desktop\AItest\pic01.jpg')

# 定义大模型
model = ChatTongyi(model_name='qwen-max', streaming=True)

# 获取聊天记录的来源
memory_key = 'history'

# 定义题词模板
prompt = ChatPromptTemplate.from_messages(
    # 用来转化用户和大模型的聊天历史
    [
        MessagesPlaceholder(variable_name = memory_key),
        ('human', '{input}')
    ]
)

class Message(BaseModel):
    # 保存用户或大模型输入的内容
    content: str
    # 区分是大模型还是用户输出的内容
    role: str


# 保存用户和大模型的聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 接收 st.session_state.messages 的信息
def to_message_place_holder(messages):
    return [
        AIMessage(content=message['content']) if message['role'] == "ai" else HumanMessage(content=message['content'])
        for message in messages
    ]

chain = {
    'input': lambda x: x['input'],
    'history': lambda x: to_message_place_holder(x['messages'])
} | prompt | model | StrOutputParser()



# 构建页面
# 页面的左边展示聊天内容，右边展示聊天记录
left, right = st.columns([0.99, 0.01])
with left: 
    # 聊天内容展示
    container = st.container()
    with container:
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.write(message['content'])
    # 接收用户的输入信息，存放在 session_state 中
    prompt = st.chat_input("您好，请问有什么可以帮助您的吗?")
    if prompt:
        st.session_state.messages.append(Message(content=prompt, role="human").model_dump())
        with container:
            with st.chat_message("human"):
                st.write(prompt)
        # 获取大模型的返回并展示
        with container:
            response = st.write_stream(chain.stream({'input': prompt, 'messages': st.session_state.messages}))
        st.session_state.messages.append(Message(content=response, role='ai').model_dump())

# with right:
#     # 聊天记录展示
#     st.json(st.session_state.messages)





# def chatBoot():
#     st.title("通航小智")
#     st.write("Welcome to our school!")

#     # 用于展示聊天内容
#     st.write("Chatboot content goes here")

#     # 用于展示聊天内容
#     st.write("Chatboot history goes here")




