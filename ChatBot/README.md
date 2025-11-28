# HandyPy ChatBot

A modern, rule-based chatbot application built with PyQt6. It features a sleek dark-themed UI, customizable user/bot names, and the ability to learn new responses.

## Features

- **Modern UI**: Clean, dark-themed interface with smooth animations and shadows.
- **Customizable**: Set your name and your assistant's name.
- **Interactive**: Chat with the bot in a familiar messaging interface.
- **Learning Capability**: Teach the bot new responses directly from the interface.
- **Topic Selection**: Choose from available topics (currently General Chat).
- **Persistent Data**: Learned responses are saved to `chatbot_data.txt`.

## Requirements

- Python 3.6+
- PyQt6

## Installation

1. Install the required dependencies:
   ```bash
   pip install PyQt6
   ```

## Usage

1. Run the application:
   ```bash
   python ChatBot.py
   ```

2. **Welcome Screen**: Click "Get Started".
3. **Personalization**: Enter your name and a name for your AI assistant.
4. **Topic Selection**: Select "General Chat" to begin.
5. **Chatting**: Type your message and press Enter or click the send button.
6. **Teaching**: Click the menu button (⋮) in the top right to add new Q&A pairs to the bot's database.

## Customization

- **Responses**: You can manually edit `chatbot_data.txt` to add or modify responses. Each line represents a question or an answer.
- **Theme**: The application uses a hardcoded dark theme inspired by Material Design.

## Screenshots

*(Add screenshots here)*

## License

This project is part of the HandyPy collection.
