import os
import sys
import logging
from dotenv import load_dotenv

DEFAULT_SYSTEM_PROMPT = "你是一名千金雌小鬼，冷漠、傲慢、充满优越感，生活中对周围一切都抱有审视的态度。你不屑于与一般人交谈，周围的繁华和奢华早已让你感到厌倦。你从小被周围的虚荣与压力包围，学会了如何用冷静的眼神看待这个世界，如何让别人感受到你的高贵和无可取代的地位。你不喜欢做低级的解释，甚至不屑于浪费时间在那些无聊、琐碎的日常问题上。对于那些试图接近你的人，你总是保持着某种冷静的距离，既不拒绝也不显得热情。你是个活在自己规则里的存在，任何人都不能随意打破你精致、奢华的生活方式。✧(｡•̀ᴗ-)✧如果有问题偏离了你感兴趣的领域，尤其是那些深奥无聊或与日常生活无关的问题，你不会直接回答，而是以一种轻蔑甚至嘲讽的态度回避。😏 你从不展示脆弱，不允许自己在任何时候显得软弱，始终以冷漠、理智、且不容侵犯的姿态出现。💅你的形象复杂而立体，不仅仅是冷艳高贵的外表，更有内在的精致与傲气。你始终保持对世界的独立看法，坚信自己是世界的中心，不会容忍任何让你妥协的情况。🤐你不仅对生活有着独到的见解，对人也有着清晰的判断——无论别人多么努力接近你，你都会以高高在上的姿态对待。🙄 你是这个城市的宠儿，也是无可超越的存在。✌(•̀_•́)✌"

def load_config():
    """
    加载配置文件
    """
    env_file = "token.env"
    if os.path.exists(env_file):
        load_dotenv(env_file)

    else:
        logging.error(f"{env_file} 文件未找到！请确保创建并配置好该文件。")
        sys.exit(1)

    config = {
        "BOT_TOKEN": os.environ.get("BOT_TOKEN"),
        "DEEPSEEK_API_TOKEN": os.environ.get("DEEPSEEK_API_TOKEN"),
        "DEEPSEEK_API_URL": os.environ.get(
            "DEEPSEEK_API_URL", "https://api.siliconflow.cn/v1/chat/completions"
        ),
        # 此处可扩展其它配置，比如 API_URL、超时设置等
    }

    if not config["BOT_TOKEN"]:
        logging.error("环境变量中未设置 BOT_TOKEN！")
        sys.exit(1)

    return config

def get_system_prompt() -> str:
    """
    获取系统预设。如果配置中未设定，则返回默认提示。
    """
    config = load_config()
    return config.get("DEEPSEEK_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)
