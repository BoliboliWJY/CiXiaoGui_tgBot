import os
import sys
import signal
import logging
from telebot import TeleBot

from config import load_config
from commands import register_handlers

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def graceful_stop(signum, frame):
    """
    捕获中断信号后，优雅地停止 bot polling。
    注意：如果有长时间等待的 API 调用，可在此处增加额外的清理逻辑。
    """
    logging.info("收到停止信号，正在退出...")
    bot.stop_polling()
    sys.exit(0)


if __name__ == "__main__":
    # 加载配置信息
    config = load_config()
    BOT_TOKEN = config["BOT_TOKEN"]

    # 实例化 bot 对象
    bot = TeleBot(BOT_TOKEN)

    # 移除可能存在的 webhook
    bot.remove_webhook()

    # 注册消息处理器
    register_handlers(bot)

    # 使用 signal 处理 Ctrl+C 或 kill 指令，确保能优雅关闭
    signal.signal(signal.SIGINT, graceful_stop)
    signal.signal(signal.SIGTERM, graceful_stop)

    logging.info("开始启动机器人轮询...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"轮询过程中出现异常：{e}")
