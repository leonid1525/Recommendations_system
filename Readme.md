# Добро пожаловать в Recomendations_system!

## Введение

Этот проект реализует систему рекомендаций постов для пользователей вымышленной социальной сети. Алгоритм рекомендации основан на прогнозах того, какие публикации понравятся определенному пользователю в данный момент времени. Для предсказаний используется CatBoostClassifier. Для оценки сервиса использовалась упрощенная метрика hitrate@5. Эта метрика получает 5 рекомендаций для конкретного пользователя, после чего проверяет, есть ли хотя бы один пост из предложенных, который понравится пользователю. Удалось добиться значения данной метрики 0.607.

## Используемые библиотеки

![PANDAS](https://img.shields.io/badge/PANDAS-1.4.2-090909??style=flat-square&logo=PANDAS)
![NUMPY](https://img.shields.io/badge/NUMPY-1.22.4-090909??style=flat-square&logo=NUMPY)
![fastapi](https://img.shields.io/badge/FASTAPI-0.75.1-090909??style=flat-square&logo=fastapi)
![sqlalchemy](https://img.shields.io/badge/SQLALCHEMY-1.4.32-090909??style=flat-square&logo=sqlalchemy)
![catboost](https://img.shields.io/badge/CATBOOST-1.0.6-090909??style=flat-square&logo=catboost)
![pydantic](https://img.shields.io/badge/PYDANTIC-1.9.1-090909??style=flat-square&logo=pydantic)
![psycopg2](https://img.shields.io/badge/PSYCOPG2-2.9.3-090909??style=flat-square&logo=psycopg2)
![uvicorn](https://img.shields.io/badge/UVICORN-0.16.0-090909??style=flat-square&logo=uvicorn)

## Запуск

Для запуска приложения вам понадобятся:

<ul>
  <li>docker</li>
  <li>wsl</li>
  <li>Свободное место на жестком диске, примерно 5 гигабайт</li>
</ul>

Порядок действий для запуска:

<ol>
    <li>Загрузите docker-compose.yml из этого репозитория</li>
    <li>Поместите файл в каталог с вашим dockerfile</li>
    <li>Войдите в wsl. Убедитесь, что wsl находится в папке с docker-compose.yaml</li>
    <li>Введите команду docker-compose up (возможно, вам не нужно вставлять дефис)</li>
    <li>Дождитесь окончания сборки</li>
    <li>После сборки вы можете сделать запрос в браузере или в Postman</li>
</ol>

Шаблон запроса: http://0.0.0.0:8899/post/recommendations/?id=300&time=2021-11-12-22:57:45 В этом шаблоне запроса вы можете изменить идентификатор и время. Диапазон возможных идентификаторов: 199 < id < 163206.

## Различия между возможностями проекта при сборке контейнера и в стандартном режиме

Поскольку частные компьютеры очень ограничены в размере оперативной памяти, я сократил возможности приложения в контейнере до одной - предсказать 5 постов, которые с наибольшей вероятностью понравятся определенному пользователю.

Из контейнера в сборке были вырезаны методы:
<ul>
<li>@app.get("/user/{id}"...</li>
<li>@app.get("/post/{id}"...</li>
<li>@app.get("/user/{id}/feed"...</li>
<li>@app.get("/post/{id}/feed"...</li>
</ul>