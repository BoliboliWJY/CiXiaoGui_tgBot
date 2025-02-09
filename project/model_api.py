import logging
import requests
from config import load_config, get_system_prompt


def call_large_model_api(messages) -> str:
    """
    调用 Deepseek 大模型 API 进行处理。
    该函数根据传入的消息列表构建请求，发送 API 请求，
    并返回模型生成的响应文本。
    """
    # 加载配置获取 Deepseek 的 API token、URL
    config = load_config()
    deepseek_token = config.get("DEEPSEEK_API_TOKEN")
    deepseek_url = config.get("DEEPSEEK_API_URL")

    if not deepseek_token:
        logging.error("未配置 API token！")
        return "API token 缺失！"

    headers = {
        "Authorization": f"Bearer {deepseek_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": messages,
        "stream": False,
        "max_tokens": 4096,
        "stop": ["null"],
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
        "tools": [
            {
                "type": "function",
                "function": {
                    "description": "<string>",
                    "name": "<string>",
                    "parameters": {},
                    "strict": False,
                },
            }
        ],
    }

    try:
        response = requests.post(deepseek_url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and data["choices"]:
                message = data["choices"][0].get("message", {})
                content = message.get("content")
                if content:
                    return content
                else:
                    return "API 响应中未能解析出内容。"
            else:
                return "API 响应格式异常。"
        else:
            logging.error("API 错误: %s", response.text)
            return f"API 错误: 状态码 {response.status_code}"
    except Exception as e:
        logging.exception("调用 API 时发生异常")
        return f"调用 API 异常: {str(e)}"
