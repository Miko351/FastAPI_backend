import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb+srv://mongodb-test:qwer1234@cluster0.douxnai.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

async def main():
    client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=8000)
    try:
        await client.admin.command("ping")
        print("Atlas 연결 성공 ✅")
    except Exception as e:
        print("Atlas 연결 실패 ❌:", e)

asyncio.run(main())