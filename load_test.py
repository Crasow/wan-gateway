"""
Нагрузочное тестирование API Gateway
Имитирует 5 одновременных запросов на генерацию изображений
"""

import asyncio
import httpx
import json
from datetime import datetime
from time import time


async def generate_image_request(
    client: httpx.AsyncClient, user_id: int, base_url: str
):
    """Отправляет запрос на генерацию изображения"""
    prompt = f"Beautiful landscape for user {user_id}"

    start_time = time()

    try:
        print(f"[User {user_id}] Отправка запроса...")

        response = await client.post(
            f"{base_url}/api/generate/image",
            json={"prompt": prompt, "width": 512, "height": 512, "steps": 30},
        )

        elapsed = time() - start_time

        print(f"[User {user_id}] ✅ Ответ получен за {elapsed:.2f}s")
        print(f"           Статус: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if "elapsed_time" in result:
                print(f"           Время генерации: {result['elapsed_time']:.2f}s")

        return {
            "user_id": user_id,
            "status": response.status_code,
            "elapsed": elapsed,
            "success": response.status_code == 200,
        }

    except Exception as e:
        elapsed = time() - start_time
        print(f"[User {user_id}] ❌ Ошибка: {e}")
        return {
            "user_id": user_id,
            "status": None,
            "elapsed": elapsed,
            "success": False,
            "error": str(e),
        }


async def generate_video_request(
    client: httpx.AsyncClient, user_id: int, base_url: str
):
    """Отправляет запрос на генерацию изображения"""
    prompt = "Pretty woman walks across the beach"

    start_time = time()

    try:
        print(f"[User {user_id}] Отправка запроса...")

        response = await client.post(
            f"{base_url}/api/generate/video",
            json={
                "prompt": prompt,
            },
        )

        elapsed = time() - start_time

        print(f"[User {user_id}] ✅ Ответ получен за {elapsed:.2f}s")
        print(f"           Статус: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if "elapsed_time" in result:
                print(f"           Время генерации: {result['elapsed_time']:.2f}s")

        return {
            "user_id": user_id,
            "status": response.status_code,
            "elapsed": elapsed,
            "success": response.status_code == 200,
        }

    except Exception as e:
        elapsed = time() - start_time
        print(f"[User {user_id}] ❌ Ошибка: {e}")
        return {
            "user_id": user_id,
            "status": None,
            "elapsed": elapsed,
            "success": False,
            "error": str(e),
        }


async def load_test(num_requests: int = 5):
    """Запускает нагрузочный тест с заданным количеством одновременных запросов"""
    base_url = "http://localhost:8000"

    print("=" * 70)
    print(f"НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ - {num_requests} одновременных запросов")
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    print("Проверка доступности сервера...")
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{base_url}/")
            if response.status_code == 200:
                print("✅ Сервер доступен\n")
            else:
                print("❌ Сервер недоступен")
                return
        except Exception as e:
            print(f"❌ Не удалось подключиться к серверу: {e}")
            print("\nУбедитесь, что сервер запущен:")
            print("  uv run uvicorn app.main:app --reload")
            return

    print("Запуск одновременных запросов...")
    print("-" * 70)

    start_time = time()

    async with httpx.AsyncClient(timeout=600.0) as client:
        # Создаем все задачи одновременно
        tasks = [
            generate_video_request(client, user_id=i + 1, base_url=base_url)
            for i in range(num_requests)
        ]

        # Запускаем все запросы параллельно
        results = await asyncio.gather(*tasks)

    total_elapsed = time() - start_time

    print("-" * 70)
    print()

    # Анализ результатов
    successful = sum(1 for r in results if r["success"])
    failed = num_requests - successful

    avg_time = sum(r["elapsed"] for r in results) / num_requests
    max_time = max(r["elapsed"] for r in results)
    min_time = min(r["elapsed"] for r in results)

    print("=" * 70)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    print(f"Всего запросов:        {num_requests}")
    print(f"Успешных:              {successful}")
    print(f"Неудачных:             {failed}")
    print(f"Общее время:           {total_elapsed:.2f}s")
    print(f"Среднее время запроса: {avg_time:.2f}s")
    print(f"Минимальное время:     {min_time:.2f}s")
    print(f"Максимальное время:    {max_time:.2f}s")
    print()

    if successful > 0:
        print("Детальная информация по успешным запросам:")
        for r in results:
            if r["success"]:
                print(f"  User {r['user_id']}: {r['elapsed']:.2f}s")

    if failed > 0:
        print("\nОшибки:")
        for r in results:
            if not r["success"]:
                print(f"  User {r['user_id']}: {r.get('error', 'Unknown error')}")

    print()
    print("=" * 70)
    print("АНАЛИЗ")
    print("=" * 70)

    if successful == num_requests:
        print("✅ Все запросы успешно обработаны")
    else:
        print(f"⚠️  Не все запросы успешны ({failed} из {num_requests} провалились)")

    # Оценка нагрузки
    throughput = num_requests / total_elapsed
    print(f"\nПропускная способность: {throughput:.2f} запросов/сек")

    if total_elapsed < 10:
        print("✅ Низкая нагрузка - сервер справляется хорошо")
    elif total_elapsed < 30:
        print("⚠️  Средняя нагрузка - сервер работает нормально")
    else:
        print("❌ Высокая нагрузка - возможны задержки")

    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ API GATEWAY")
    print("=" * 70)
    print("\nЭтот тест имитирует ситуацию, когда 5 человек одновременно")
    print("отправляют запросы на генерацию изображений.\n")

    asyncio.run(load_test(num_requests=5))
