import sys
import signal
import logging
import time
from telebot import TeleBot

from config.config import load_config
from bot.handlers import register_handlers
from storage.conversation_manager import ConversationManager

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def graceful_stop(signum, frame):
    """
    捕获中断信号后，优雅地结束 bot polling。
    """
    logging.info("收到停止信号，正在退出…")
    bot.stop_polling()
    sys.exit(0)


if __name__ == "__main__":
    # 加载配置信息
    config = load_config()
    BOT_TOKEN = config["BOT_TOKEN"]

    # 创建 TeleBot 实例
    bot = TeleBot(BOT_TOKEN)
    # 移除可能存在的 webhook
    bot.remove_webhook()

    # 初始化对话记录管理器
    conv_manager = ConversationManager(storage_dir="conversation_history")

    # 注册所有消息处理器，并传入对话管理器实例
    register_handlers(bot, conv_manager)

    # 注册信号处理（Ctrl+C 或 kill）
    signal.signal(signal.SIGINT, graceful_stop)
    signal.signal(signal.SIGTERM, graceful_stop)

    logging.info("开始启动机器人轮询……")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error("轮询过程中出现异常：%s", str(e))
            # 暂停几秒再重试轮询
            time.sleep(5)
