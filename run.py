import aiohttp
import asyncio
from appwrite.client import Client
from appwrite.services.databases import Databases

async def fetch_file_info(session, bot_token, file_id):
    url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    async with session.get(url) as response:
        return await response.json()

def get_ids():
    client = Client()

    (client
        .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
        .set_project('grace-cron') # Your project ID
        .set_key('e395ed05a7351d4f6dad840eca954a53c8fd713add863af127ba7d5c524c9b7fb85f4cf1cc8e6e9b2665ea0337abfa0e05cb6ccebb6a5e44801fab8d8f2368d3426adef6b00ba6c597d4a011acf05f424640a79af4c18c39a01370df644471759dda7a0c1059748556b3597aecc640235d9d7983877642ac89174c2bd840e63f') # Your secret API key
    )

    databases = Databases(client)

    result = databases.list_documents('grace-data', 'ids')
    # Extract file-ids from each document
    file_ids = [doc['file-id'] for doc in result['documents']]

    return file_ids

async def main(bot_token):
    async with aiohttp.ClientSession() as session:
        while True:
            file_ids = get_ids()
            for file_id in file_ids:
                file_info = await fetch_file_info(session, bot_token, file_id)
                print(f"File ID: {file_id}, File Info: {file_info}")

            # Introduce some delay between requests
            await asyncio.sleep(1)

if __name__ == "__main__":
    bot_token = "6361645598:AAF8Lioo2hS7tsGPXT0bTn5uT9pGF0gMAB8"

    asyncio.run(main(bot_token))

