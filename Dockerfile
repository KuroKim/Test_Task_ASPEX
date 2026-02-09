# Используем легкий образ Python
FROM python:3.10-slim

# Отключаем создание .pyc файлов и буферизацию вывода (чтобы логи летели сразу в консоль)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Обновляем pip до последней версии перед установкой библиотек
RUN pip install --upgrade pip

# Сначала копируем только requirements, чтобы использовать кэш Докера
# Если requirements не менялись, этот шаг пропустится при пересборке
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта
COPY . .

# Открываем порт (для документации)
EXPOSE 8000

# Команда запуска по умолчанию (но мы переопределим её в docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]