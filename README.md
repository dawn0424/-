# 赛博算命大师

这是一个使用 Streamlit 和 DashScope 通义千问 API 制作的赛博算命网页。

## 运行

```bash
pip install -r requirements.txt
export DASHSCOPE_API_KEY="你的 API Key"
streamlit run web_chat.py
```

部署到 Streamlit Community Cloud 时，请在 App 的 Secrets 中配置：

```toml
DASHSCOPE_API_KEY = "你的 API Key"
```
