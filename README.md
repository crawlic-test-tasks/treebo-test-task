# Treebo test task

Тестовое задание в компанию [treebo.io](https://hh.ru/employer/4126648?hhtmFrom=vacancy)

## Как запустить:

1. Установить docker, docker-compose

2. Скопировать .env.example в .env, заполнить/поменять нужные переменные

3. Запустить проект через docker compose: 

```sh
docker compose up --build
```

Или можно просто запустить командой `make`

## Для тестов

1. Установить pytest + pytest_asyncio

```sh
pip install pytest pytest_asyncio
```

2. Запустить через make

```
make run-tests
```
