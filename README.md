# Домашнее задание 3. Асинхронность в Python

Установка зависимостей:
```bash
python -m pip install -r requirements.txt
```

Запуск:
```bash
python -m uvicorn main:app --reload
```

Проверка: открыть http://127.0.0.1:8000/docs
и отправить POST /calculate/ с данными:

```json
{
  "numbers": [5, 3, 10],
  "delays": [1, 2, 0.5]
}
```