```mermaid
sequenceDiagram
    Сервис генерации->>+Очередь задач: подписка на партицию
    Сервис архивации->>+Очередь задач: подписка на топик
    Flask-приложение->>+Очередь задач: задача на генерацию
    Очередь задач->>+Сервис генерации: задача на генерацию
    Сервис генерации->>+Основная БД: сохранение сгенерированных записей
    Flask-приложение->>+Очередь задач: задача на архивацию
    Очередь задач->>+Сервис архивации: задача на архивацию
    Сервис архивации->>+Основная БД: запрос данных
    Основная БД->>+Сервис архивации: получение данных
    Сервис архивации->>+Архивная БД: сохранение данных
    Flask-приложение->>+Архивная БД: запрос количества записей
    Архивная БД->>+Flask-приложение: получение ответа