# Тестовое задание

1. Напишите калькулятор на Python который принимает на входе математическое выражение.
Например:

    2+2*5  
    12

2. (Не обязательно к выполнению, но будет большим плюсом) Интегрируйте его в telegram бота с авторизацией.

## Использование

Бот: <https://t.me/Saber_Test_Calculator_bot>  
Пароль: qwerty321

Команды:  
`/start`  
`/help`  
`/logout`  

## Установка
Используя Docker:  
`docker run -d \`  
`--name=saber-test-bot \`  
`-e TOKEN=YOUR_TELEGRAM_TOKEN \`  
`-e BOT_PASSWORD=YOUR_PASSWORD \`  
`--restart unless-stopped \`  
`kostikk/saber-test-bot`  

Или вручную:  
`git clone https://github.com/ikaktusz/saber-test-bot.git`  
`cd saber-test-bot`  
`pip install -r requirements.txt`  
В Linux:  
`export TOKEN=[ваш токен]`  
`export BOT_PASSWORD=[пароль для авторизации в боте]`  
В Windows:  
`set TOKEN=[ваш токен]`  
`set BOT_PASSWORD=[пароль для авторизации в боте]`  
Запуск:  
`python bot.py`
