import os
import json
import logging


class ConversationManager:
    def __init__(self, storage_dir="conversation_history"):
        self.storage_dir = storage_dir
        self.conversations = {}

    def init_conversation(self, chat_id):
        """
        初始化用户对话记录。
        """
        self.conversations[chat_id] = []
        self._save_conversation(chat_id)

    def add_message(self, chat_id, role, content):
        """
        添加消息至对话记录，并存储到本地。
        """
        if chat_id not in self.conversations:
            self.conversations[chat_id] = []
        self.conversations[chat_id].append({"role": role, "content": content})
        self._save_conversation(chat_id)

    def get_conversation(self, chat_id):
        """
        获取指定用户的对话记录。
        """
        return self.conversations.get(chat_id, [])

    def _save_conversation(self, chat_id):
        """
        将对话记录写入本地 JSON 文件。
        """
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            file_path = os.path.join(self.storage_dir, f"{chat_id}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    self.conversations.get(chat_id, []), f, ensure_ascii=False, indent=2
                )
        except Exception as e:
            logging.error("保存对话记录失败：%s", str(e))
