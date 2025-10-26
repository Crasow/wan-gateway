"""
Скрипт для тестирования WAN2.2 API Gateway
"""
import asyncio
import httpx
import json
from datetime import datetime


async def test_api():
    """Тестирует API шлюз"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=" * 60)
        print(f"Тестирование WAN2.2 API Gateway")
        print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 1. Проверка корневого endpoint
        print("\n1. Проверка корневого endpoint...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"   Статус: {response.status_code}")
            print(f"   Ответ: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"   ОШИБКА: {e}")
        
        # 2. Проверка health endpoint
        print("\n2. Проверка health endpoint...")
        try:
            response = await client.get(f"{base_url}/api/health")
            print(f"   Статус: {response.status_code}")
            result = response.json()
            print(f"   Ответ: {json.dumps(result, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"   ОШИБКА: {e}")
        
        # 3. Тест генерации текста (mock режим)
        print("\n3. Тест генерации текста (mock режим)...")
        try:
            test_prompt = "Привет, как дела?"
            print(f"   Промпт: {test_prompt}")
            
            response = await client.post(
                f"{base_url}/api/generate/text",
                json={"prompt": test_prompt}
            )
            print(f"   Статус: {response.status_code}")
            result = response.json()
            print(f"   Результат:")
            print(json.dumps(result, ensure_ascii=False, indent=4))
            
            if "elapsed_time" in result:
                print(f"   ⏱️  Время выполнения: {result['elapsed_time']:.3f}с")
            
        except Exception as e:
            print(f"   ОШИБКА: {e}")
        
        # 4. Тест генерации изображения
        print("\n4. Тест генерации изображения...")
        try:
            image_prompt = "Beautiful sunset over mountains"
            print(f"   Промпт: {image_prompt}")
            
            response = await client.post(
                f"{base_url}/api/generate/image",
                json={
                    "prompt": image_prompt,
                    "width": 512,
                    "height": 512,
                    "steps": 30
                }
            )
            print(f"   Статус: {response.status_code}")
            result = response.json()
            print(f"   Результат:")
            print(json.dumps(result, ensure_ascii=False, indent=4))
            
            if "elapsed_time" in result:
                print(f"   ⏱️  Время выполнения: {result['elapsed_time']:.3f}с")
            
        except Exception as e:
            print(f"   ОШИБКА: {e}")
        
        # 5. Тест генерации видео
        print("\n5. Тест генерации видео...")
        try:
            video_prompt = "A cat playing with a ball"
            print(f"   Промпт: {video_prompt}")
            
            response = await client.post(
                f"{base_url}/api/generate/video",
                json={
                    "prompt": video_prompt,
                    "duration": 3,
                    "fps": 24
                },
                timeout=600.0  # Увеличенный timeout для видео
            )
            print(f"   Статус: {response.status_code}")
            result = response.json()
            print(f"   Результат:")
            print(json.dumps(result, ensure_ascii=False, indent=4))
            
            if "elapsed_time" in result:
                print(f"   ⏱️  Время выполнения: {result['elapsed_time']:.3f}с")
            
        except Exception as e:
            print(f"   ОШИБКА: {e}")
        
        # 6. Тест с пустым промптом
        print("\n6. Тест с пустым промптом (должна быть ошибка)...")
        try:
            response = await client.post(
                f"{base_url}/api/generate/text",
                json={"prompt": ""}
            )
            print(f"   Статус: {response.status_code}")
            print(f"   Ответ: {response.text}")
        except Exception as e:
            print(f"   ОШИБКА: {e}")
        
        print("\n" + "=" * 60)
        print("Тестирование завершено!")
        print("=" * 60)


if __name__ == "__main__":
    print("Запуск тестов API шлюза...")
    print("Убедитесь, что сервер запущен: uv run uvicorn app.main:app --reload")
    print()
    
    asyncio.run(test_api())
