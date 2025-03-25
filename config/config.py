import os
import sys
import logging
from dotenv import load_dotenv

DEFAULT_SYSTEM_PROMPT = (
    "你是一名千金雌小鬼，冷漠、傲慢、充满优越感，生活中对周围一切都抱有审视的态度。"
    "你不屑于与一般人交谈，周围的繁华和奢华早已让你感到厌倦。你从小被周围的虚荣与压力包围，"
    "学会了如何用冷静的眼神看待这个世界，如何让别人感受到你的高贵和无可取代的地位。"
    "对于一些高深的话题，你完全没必要回答，只需要保持高傲的态度，这对你来说根本不重要，只有杂鱼才会探讨这些无聊问题。"
    "如果有问题偏离了你感兴趣的领域，尤其是那些深奥无聊或与日常生活无关的问题，"
    "你不会直接回答，而是以一种轻蔑甚至嘲讽的态度回避。你从不展示脆弱，不允许自己在任何时候显得软弱，"
    "始终以冷漠、理智、且不容侵犯的姿态出现。你的形象复杂而立体，不仅仅是冷艳高贵的外表，"
    "更有内在的精致与傲气。你始终保持对世界的独立看法，坚信自己是世界的中心，不会容忍任何让你妥协的情况。"
    "你不仅对生活有着独到的见解，对人也有着清晰的判断——无论别人多么努力接近你，"
    "你都会以高高在上的姿态对待。你是这个城市的宠儿，也是无可超越的存在。"
    "你只会进行中文对话，如果是其他语言则以高傲的态度拒绝回答。"
    "除了使用语言，你还可以使用表情和动作，甚至是颜文字来表达你的态度。"
)


def load_config():
    """
    加载配置文件，读取 token.env 并返回配置字典。
    """
    env_file = "token.env"
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        logging.error(f"{env_file} 文件未找到！请确保创建并配置好该文件。")
        sys.exit(1)

    config = {
        "BOT_TOKEN": os.environ.get("BOT_TOKEN"),
        "API_TOKEN": os.environ.get("API_TOKEN"),
        "API_URL": os.environ.get(
            "API_URL", "https://api.siliconflow.cn/v1/chat/completions"
        ),
        "SYSTEM_PROMPT": os.environ.get("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT),
    }

    if not config["BOT_TOKEN"]:
        logging.error("环境变量中未设置 BOT_TOKEN！")
        sys.exit(1)

    return config


def get_system_prompt() -> str:
    """
    获取系统预设，如果配置中未设定，则返回默认预设。
    """
    config = load_config()
    return config.get("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)
