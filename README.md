# Speech2Text Bot

![](https://img.shields.io/github/actions/workflow/status/appxpy/Speech2Text-For-Telegram/pipeline.yml?branch=main&style=flat-square)
![](https://img.shields.io/badge/coverage-100%25-brightgreen?style=flat-square)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/appxpy/speech2text-for-telegram/main?style=flat-square)


Speech2Text Bot это **простой** бот для **быстрого** распознавания ваших голосовых сообщений прямо в [чате Telegram](https://t.me/sp2txtbot).

## Содержание
- [Speech2Text Bot](#speech2text-bot)
  - [Содержание](#содержание)
  - [Описание](#описание)
  - [Стэк используемых технологий](#стэк-используемых-технологий)
  - [Архитектура проекта](#архитектура-проекта)

## Описание
Бывало ли у вас такое, что вам отправили голосовое сообщение в телеграме, а вы не можете его послушать? У телеграма уже есть встроенное решение для распознавания текста, но оно доступно только обладателям платных аккаунтов. Этот бот позволяет вам распознать голосовое сообщение и получить его текстовую расшифровку совершенно бесплатно!

## Стэк используемых технологий

- **Python 3.10**
  
  Каркас на базе которого постоен бот, поддерживает синтаксис `async/await`, является сравнительно свежей версией python.


- **aiogram**

  [Превосходная библиотека](https://github.com/aiogram/aiogram) для работы с Telegram. Является асинхронной, в следствии чего очень быстрой.


- **tortoise-orm**
  
  Простая, но в тоже время функциональная и полностью асинхронная orm. Одной из причин её выбора была большая схожесть с хорошо себя зарекомендовавшим ORM фреймворка Django. [Её GitHub (тык)](https://github.com/tortoise/tortoise-orm)

- **Yandex Speechkit**

  Для распознавания голосовых сообщений используется сервис Yandex SpeechKit. Сервис имеет возможность асинхронного распознавания и вполне неплохо справляется со своей задачей. Помимо этого, в проекте используется [неофициальная SDK](https://github.com/TikhonP/yandex-speechkit-lib-python) для работы с сервисом в python.

- **Пунктуация**

  Для добавления пунктуации в расшифровку аудио-сообщения используется библиотека **aiohttp**, которая отправляет запрос на сайт [textovod.ru](https://textovod.ru), где расшифровка голосового сообщения обрабатывается и возвращается с пунктуацией.

- **Docker**

  Для удобства развертывания и запуска бота используется Docker. Все зависимости устанавливаются в контейнере, а для запуска используется docker-compose.

---

## Архитектура проекта

![](https://i.imgur.com/WyF4euF.jpg)

---

made with ❤️ by [@appxpy](https://github.com/appxpy) and [@brazenoptimist](https://github.com/brazenoptimist)
