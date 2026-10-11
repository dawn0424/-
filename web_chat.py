import streamlit as st
import sys
import os

# ==========================================
# 🔮 赛博修仙老者 - 网页版启动器
# ==========================================

# 设置网页标题和图标
st.set_page_config(page_title="赛博算命大师", page_icon="🔮")
st.title("🔮 赛博修仙老者在线算命")
st.caption("命运服务器连接中... ERROR 404... 算了，凑合用吧。")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 如果网站部署在 Streamlit Cloud，API Key 通常放在 st.secrets 中。
# 这里把 Secrets 中的值转成环境变量，供 master.py 读取。
try:
    if "DASHSCOPE_API_KEY" in st.secrets:
        os.environ["DASHSCOPE_API_KEY"] = st.secrets["DASHSCOPE_API_KEY"]
except Exception:
    # 如果本地没有配置 Streamlit Secrets，就继续运行；
    # 本地环境可以直接使用系统环境变量。
    pass

# 🚨 核心逻辑：调用你原来的 master.py 里的函数
# 假设你的 master.py 和这个文件在同一个文件夹
# 我们需要把 master.py 当作模块导入进来
sys.path.append(os.path.dirname(__file__))

try:
    # 导入你原来的代码文件 (去掉 .py 后缀)
    from master import ask_master 
except ImportError:
    st.error("⚠️ 找不到 master.py 文件！请确保它和 web_chat.py 在同一个文件夹里。")
    st.stop()

# 处理用户输入
if prompt := st.chat_input("请输入你的问题（例如：我和他...）"):
    # 1. 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 调用你的 AI 函数
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 获取回答
        # 注意：这里直接调用了你 master.py 里的 ask_master 函数
        response = ask_master(prompt) 
        
        # 模拟打字机效果（可选，为了更酷）
        full_response = response
        message_placeholder.markdown(full_response)
    
    # 3. 保存助手回复
    st.session_state.messages.append({"role": "assistant", "content": full_response})