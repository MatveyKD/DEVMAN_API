# DEVMAN_API
Бот для уведомлений о проверки работ на Devman

## Как запустить

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- [Создайте бота](https://telegram.me/BotFather)
- Заполните `.env`
- Запустите код командой `python main.py`

### Переменные окружения
Код берет настройки из файла `.env`. Его содержимое должно быть похожим на это:

    BOT_TOKEN=5788475122:AAJGHKb7634gf70nOO7Q9wAZwa_AVJwQqPWmwKs
    API_TOKEN=47890ef6h9jd8t38ebcf7256784e3fynv7y8n9
    USER_ID=1365827867

- BOT_TOKEN - Токен зарегистрированного бота
- API_TOKEN - Токен пользователя на [Devman](https://dvmn.org/api/docs/)
- USER_ID - Токен пользователя в [Telegram](https://telegram.me/userinfobot)
