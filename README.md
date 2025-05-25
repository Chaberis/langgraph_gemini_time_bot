# Установка и Запуск
```py
1. Клонирование
git clone https://github.com/Chaberis/langgraph_gemini_time_bot.git
cd langgraph_gemini_time_bot

2. Настройка окружения и зависимостей
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt

# 3. Настройка API ключа
# Создайте .env в корне проекта:
# GOOGLE_API_KEY="ВАШ_GOOGLE_API_КЛЮЧ"
# Добавьте .env в .gitignore:
# .env

# 4. Запуск LangGraph Playground
langgraph dev
```
