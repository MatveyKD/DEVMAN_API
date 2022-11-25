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

    TG_BOT_TOKEN=5788475122:AAJGHKb7634gf70nOO7Q9wAZwa_AVJwQqPWmwKs
    TG_SERVICE_BOT_TOKEN=8754651:SUIEefUIHeCnISRx41Vdue_yniyfguv
    DEVMAN_API_TOKEN=47890ef6h9jd8t38ebcf7256784e3fynv7y8n9
    TG_USER_ID=1365827867

- TG_BOT_TOKEN - Токен зарегистрированного бота
- TG_BOT_TOKEN - Токен зарегистрированного бота для логирования
- DEVMAN_API_TOKEN - Токен пользователя на [Devman](https://dvmn.org/api/docs/)
- TG_USER_ID - Токен пользователя в [Telegram](https://telegram.me/userinfobot)

## Пример работы

Основной бот

![](https://github.com/MatveyKD/DEVMAN_API/blob/main/Gifs/main_bot.gif)

Бот для логирования

![](https://github.com/MatveyKD/DEVMAN_API/blob/main/Gifs/service_bot.gif)
