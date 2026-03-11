# RAG API

FastAPI Backend-проект з запитами Claude API для пошуку даних в документах за допомогою RAG
**Стек:** Python 3.12 · FastAPI · Claude API · ChromaDB

## Швидкий старт

```bash
git clone <repo>
cd rag_api

uvicorn main:app --reload
```


## Endpoints

| Назва | Метод | Навіщо |
|------|-----|--------|
| `/upload` | POST | Завантаження документів для пошуку |
| `/ask` |  POST | Відповіді на питання на основі заданого тексту |
| `/documents` | GET | перегляд завантажених документів |
| `/documents/{doc_id}` | DELETE | Видалення документу по ID |


## Особливості
- Векторний пошук по документу за допомогою RAG
- Claude API для аналізу і відповіді на питання
- Збереження документів на диск
