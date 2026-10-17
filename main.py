import asyncio
from time import perf_counter

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Данные запроса
class RequestData(BaseModel):
    numbers: list[float]
    delays: list[float]


# Результат одного вычисления
class Result(BaseModel):
    number: float
    square: float
    delay: float
    time: float


# Данные ответа
class ResponseData(BaseModel):
    results: list[Result]
    total_time: float
    parallel_faster_than_sequential: bool
    
    
# Вычисление квадрата с заданной задержкой
async def square(number: float, delay: float) -> Result:
    start = perf_counter()
    await asyncio.sleep(delay)
    value = number * number
    elapsed = perf_counter() - start
    return Result(
        number=number,
        square=value,
        delay=delay,
        time=elapsed
    )
    
    
# Обработка запроса на вычисление квадратов
@app.post("/calculate/", response_model=ResponseData)
async def calculate(data: RequestData) -> ResponseData:
    if len(data.numbers) != len(data.delays):
        raise HTTPException(
            status_code=422,
            detail="Количество чисел и задержек должно совпадать"
        )
    for delay in data.delays:
        if delay < 0:
            raise HTTPException(
                status_code=422,
                detail="Задержка не может быть отрицательной"
            )
    start = perf_counter()
    tasks = []
    for number, delay in zip(data.numbers, data.delays):
        tasks.append(square(number, delay))
    results = await asyncio.gather(*tasks)
    total_time = perf_counter() - start
    sequential_time = sum(data.delays)
    return ResponseData(
        results=results,
        total_time=total_time,
        parallel_faster_than_sequential=total_time < sequential_time
    )