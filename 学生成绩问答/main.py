import streamlit as st
import pandas as pd
import requests

# Streamlit页面的标题
st.title("")

# 在Streamlit中创建一个文件上传组件
uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx", "xls"])

# ChatGPT API的URL
gpt_api_url = ""

# ChatGPT应用名称
app_name = "" 

def get_eval(user_prompt, context_data):
    messages = [{"role": "user", "content": user_prompt}]
    
    # 添加整个表格数据作为上下文信息
    messages.append({"role": "system", "content": context_data})
    
    task = {
        "app_name": app_name,
        "data": {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1000
        }
    }

    response = requests.post(gpt_api_url, json=task).json()
    content = response['data']['choices'][0]['message']['content']
    return content

if uploaded_file is not None:
    # 读取上传的Excel文件
    df = pd.read_excel(uploaded_file)

    # 将整个表格数据转换为JSON字符串，以便传递给ChatGPT
    context_data = df.to_json(orient="records", force_ascii=False)
   

    # 显示上传的数据
    st.write("上传的Excel数据：")
    st.write(df)

    # 使用ChatGPT接口生成答案
    prompt = st.text_input("请输入问题：")
    prompt = prompt + "不要使用代码。"
    if st.button("生成答案"):
        if prompt:
            # 调用get_eval函数并传递整个表格数据作为上下文信息
            answer = get_eval(prompt, context_data)
            st.write(f"答案：{answer}")
        else:
            st.write("请输入问题。")

