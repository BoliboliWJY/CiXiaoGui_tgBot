# Deepseek Telegram Bot

A lightweight Telegram bot that integrates with the Deepseek large model API. This bot uses the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) to handle Telegram messages, forwards user messages to the Deepseek API for processing, and stores conversation history in local JSON files.

## Features

- **Commands**:
  - `/start` or `/hello` — Sends a welcome message and initializes the conversation history.
  - `/help` — Displays a help message with available commands.
  - `/preset` — Shows the currently used system prompt (preset) for the Deepseek API.
- **Conversation History**:
  - Maintains per-user message history in a global in-memory dictionary.
  - Saves conversation history as JSON files in the `conversation_history` directory.
- **Deepseek API Integration**:
  - Sends user messages along with a system preset prompt to the Deepseek API.
  - Returns and logs model responses that are also appended to the user’s conversation history.

## Prerequisites

- Python 3.7+
- Libraries:
  - `pyTelegramBotAPI` (telebot)
  - `requests`
  - `python-dotenv`
  
You can install the required dependencies with: