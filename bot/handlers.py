import logging
from telebot import TeleBot

from config.config import get_system_prompt
from api.model_api import call_large_model_api


def register_handlers(bot: TeleBot, conv_manager):
    """
    注册所有消息处理器到 bot。
    conv_manager: 用于管理用户对话记录。
    """

    @bot.message_handler(commands=["start", "hello"])
    def send_welcome(message):
        """
        处理 /start 或 /hello 命令，发送欢迎信息，并初始化对话记录。
        """
        chat_id = message.chat.id
        logging.info(f"收到 {chat_id} 的 /start 或 /hello 命令")
        welcome_text = "唔嘿嘿，杂鱼你来啦❤~"
        bot.reply_to(message, welcome_text)
        conv_manager.init_conversation(chat_id)

    @bot.message_handler(commands=["help"])
    def send_help(message):
        """
        处理 /help 命令，发送帮助信息。
        """
        chat_id = message.chat.id
        logging.info(f"收到 {chat_id} 的 /help 命令")
        help_text = (
            "欢迎使用本机器人，您可以使用以下命令：\n"
            "/start 或 /hello - 发送问候信息\n"
            "/help - 获取帮助信息\n"
            "/preset - 查看当前模型预设\n"
            "直接输入消息即可调用大模型进行处理。"
        )
        bot.reply_to(message, help_text)

    @bot.message_handler(commands=["preset"])
    def send_preset(message):
        """
        处理 /preset 命令，显示当前大模型的系统预设。
        """
        prompt = get_system_prompt()
        bot.reply_to(message, f"当前模型预设：{prompt}")

    @bot.message_handler(func=lambda msg: True)
    def process_message(message):
        """
        处理所有普通文本消息。
        将用户消息添加至对话记录，调用大模型 API，更新对话记录，然后回复用户。
        """
        chat_id = message.chat.id
        logging.info(f"处理来自 {chat_id} 的消息：{message.text}")

        content = message.text.strip()
        conv_manager.add_message(chat_id, role="user", content=content)

        # 构建发送给大模型 API 的消息列表：
        # 先添加系统预设，再添加用户与机器人的对话历史
        system_prompt = get_system_prompt()
        messages_list = [
            {"role": "system", "content": system_prompt}
        ] + conv_manager.get_conversation(chat_id)

        # 调用大模型 API
        response = call_large_model_api(messages_list)
        conv_manager.add_message(chat_id, role="assistant", content=response)

        bot.reply_to(message, response)
