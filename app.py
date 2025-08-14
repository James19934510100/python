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
with open("python/style.css", encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
left, right = st.columns([0.3, 0.7])
with right: 
    st.title("通航小智")
    st.write("Welcome to our school!")
    css_style = """
        <style>
        .stApp {
            background-color: lightblue;
        }
        </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)

    # 聊天内容展示
    container = st.container()
    with container:
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.write(message['content'])
    # 接收用户的输入信息，存放在 session_state 中
    prompt = st.chat_input("您好，请问有什么可以帮助您的吗?")
    question_list = [
        '心情不好的时候怎么办？', '成绩不好的人会一事无成吗？', '父母经常拿自己和别人比较怎么办？',
        '为什么我们都去上课了，但是别的同学成绩比我高？'
    ]
    answer_list = [
        '''
            首先不能长时间低沉，会不利于心理健康噢~如果觉得不开心的话，
            就做点让自己能够开心的事，比如散步、睡觉、发呆或者和我聊聊天等等。
        ''',
        '''
            成绩和能力不会直接挂钩，成绩不好可能是上帝在创造你的时候忘记了赋予
            你这个天赋，但是它也许悄悄赋予了你别样的能力，只要你坚持正确的做事
            一定会有收获的。
        ''',
        '''
            尝试告诉父母，每个人都是独一无二的，每个人都有自己的来时路，
            在人生的康庄大道上，也许别人只是走得快，走的慢的你也一样会
            抵达属于自己的终点。你要相信你就是你自己，你有你的闪光点，
            别人亦是，也许你的闪光点还没有被发现。
        ''',
        '''
            成绩不代表一切，也许是别人在背后偷偷多刷了几道题，也许是他
            在课堂上积极互动，学习是双向的，你如果觉得也很努力了，那可
            以尝试着在课堂上多和老师互动，这样可以提高印象分。
        '''
    ]
    result = -1
    for i in range(len(question_list)):
        if str(prompt) == question_list[i]:
            result = i
            break

    if prompt:
        if result != -1:
            try:
                with container:
                    with st.chat_message("human"):
                        st.write(question_list[result])
                with container:
                    response = st.write(answer_list[result])
                st.session_state.messages.append(Message(content=response, role='human').model_dump())
            except:
                pass
        else:
            st.session_state.messages.append(Message(content=prompt, role="human").model_dump())
            with container:
                with st.chat_message("human"):
                    st.write(prompt)
            # 获取大模型的返回并展示
            with container:
                response = st.write_stream(chain.stream({'input': prompt, 'messages': st.session_state.messages}))
            st.session_state.messages.append(Message(content=response, role='ai').model_dump())


with left:
    pass









