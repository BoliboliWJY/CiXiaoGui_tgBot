import logging
import os
import json
from telebot import TeleBot
from model_api import call_large_model_api
from config import get_system_prompt

# 全局会话记录字典，区分不同用户
conversation_memory = {}


def save_conversation_to_file(chat_id):
    """
    将指定用户（chat_id）的会话历史记录写入本地文件。
    文件将保存在 conversation_history 目录下，文件名为 <chat_id>.json
    注意：这里只进行写入操作，不做读取。
    """
    try:
        directory = "conversation_history"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, f"{chat_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                conversation_memory.get(chat_id, []), f, ensure_ascii=False, indent=2
            )
    except Exception as e:
        logging.error("存储对话记录失败: %s", str(e))


def register_handlers(bot: TeleBot):
    """
    注册所有消息处理器到 bot。
    """

    @bot.message_handler(commands=["start", "hello"])
    def send_welcome(message):
        """
        处理 /start 或 /hello 命令，发送欢迎消息，并初始化对话记录。
        """
        logging.info(f"收到 {message.chat.id} 的 /start 或 /hello 命令")
        welcome_text = "唔嘿嘿，杂鱼你来啦❤~"
        bot.reply_to(message, welcome_text)
        # 初始化会话历史记录，并保存到本地文件
        conversation_memory[message.chat.id] = []
        save_conversation_to_file(message.chat.id)

    @bot.message_handler(commands=["help"])
    def send_help(message):
        """
        处理 /help 命令，发送帮助信息。
        """
        logging.info(f"收到 {message.chat.id} 的 /help 命令")
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
        处理所有普通文本消息，调用大模型 API 进行处理，
        并在本地保存会话记录（针对不同用户存于不同文件中）。
        """
        chat_id = message.chat.id
        logging.info(f"处理来自 {chat_id} 的消息：{message.text}")
        content = message.text.strip()

        # 如果当前用户未初始化对话历史，则先初始化
        if chat_id not in conversation_memory:
            conversation_memory[chat_id] = []

        # 将用户消息加入历史记录，并存储到本地
        conversation_memory[chat_id].append({"role": "user", "content": content})
        save_conversation_to_file(chat_id)

        # 构建发送给大模型 API 的消息列表：先添加系统预设，再添加会话历史
        system_prompt = get_system_prompt()
        messages_list = [
            {"role": "system", "content": system_prompt}
        ] + conversation_memory[chat_id]

        # 调用 API（传入完整的消息列表）
        response = call_large_model_api(messages_list)

        # 将模型响应加入历史记录，并更新存储
        conversation_memory[chat_id].append({"role": "assistant", "content": response})
        save_conversation_to_file(chat_id)

        bot.reply_to(message, response)
