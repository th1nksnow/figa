import re
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg
import os
import time
# from starlette_exporter import PrometheusMiddleware, handle_metrics

# import uvicorn

# api_port = os.environ['HISTORY_API_PORT']

regexp_pattern = "[а-яА-Яеё,. ]+"

# Глубина запроса к истории
history_count = 1
system_is_ready = False

# Забираем настройки из переменных окружения, всё по best practices
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']
db_login = os.environ['DB_LOGIN']
db_pass = os.environ['DB_PASS']

# Собираем строку подключения для удобства
db_connection_string = ('host=' + db_host +
                        ' port=' + db_port +
                        ' dbname=' + db_name +
                        ' user=' + db_login +
                        ' password=' + db_pass
                        )

# Создаём свой тип данных, чтобы загружать в него данные из запроса
class AppendRequest(BaseModel):
    original: str
    figalized: str

# Создаём API-интерфейс
app = FastAPI(
    # Так как API работает через реверс-прокси, необходимо поменять пути для автодокументации
    openapi_url = "/api/history/openapi.json",
    docs_url="/api/history/docs"
)

# Разрешаем обращение к API с любых доменов, так как внутри Kubernetes API будет недоступен снаружи
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API для запроса списка преобразованных слов из истории. У нас его использует фронтенд
# для генерации подсказки и отображения статистики
@app.get("/api/gethistory/", status_code=200)
async def get_history(response: Response):
    global system_is_ready
    # Пробуем выполнить запрос к БД
    try:
        async with await psycopg.AsyncConnection.connect(db_connection_string) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM history ORDER BY id DESC LIMIT %s",
                    (history_count,))
                result_list = [list(x) for x in await cur.fetchall()]
                print('Selection done')
    # Если не получилось, выставляем флаг неготовности системы
    except Exception as err:
        print ('Cannot get history', err)
        system_is_ready = False
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return
    else:
        system_is_ready = True
        return result_list
