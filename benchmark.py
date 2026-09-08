import asyncio
import time
import os
import httpx
import logging
logging.getLogger("src.api.app").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Set dummy API key
os.environ["API_KEYS"] = "testkey"
# Ensure we don't use redis, so we hit the file read
os.environ["REDIS_HOST"] = "invalid_host"

from src.api.app import app

async def run_requests(client, num_requests):
    tasks = []
    for _ in range(num_requests):
        # Using a date that forces it to read the file
        tasks.append(client.get("/api/v1/check_holiday?year=2024&month=1&day=1", headers={"X-API-Key": "testkey"}))
    await asyncio.gather(*tasks)

async def benchmark():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Warmup
        await run_requests(client, 10)

        start_time = time.time()
        await run_requests(client, 1000)
        end_time = time.time()

        print(f"Total time for 1000 concurrent requests: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(benchmark())
