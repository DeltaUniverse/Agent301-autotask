import aiohttp
import aiofiles
import urllib.parse
from fake_useragent import UserAgent
import time
import json
import asyncio
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logger.log"),
        logging.StreamHandler()
    ]
)

# Function to extract the username from the authorization token or user data
def extract_username(authorization):
    try:
        # Parse the query string
        parsed_data = urllib.parse.parse_qs(authorization)
        user_data_json = parsed_data.get('user', [''])[0]

        # Decode URL-encoded string to JSON
        user_data = json.loads(urllib.parse.unquote(user_data_json))

        # Get the username from JSON
        username = user_data.get('username', 'unknown')
        return username
    except (json.JSONDecodeError, KeyError):
        return 'unknown'

# Function to read authorizations from a file asynchronously
async def load_authorizations_with_usernames(file_path):
    async with aiofiles.open(file_path, 'r') as file:
        authorizations = await file.readlines()

    auth_with_usernames = [{'authorization': auth.strip(), 'username': extract_username(auth)} for auth in authorizations]
    return auth_with_usernames

# Function to claim tasks asynchronously
async def claim_tasks(session, authorization, account_number, username):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'authorization': authorization.strip(),
        'origin': 'https://telegram.agent301.org',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    url_get_tasks = 'https://api.agent301.org/getMe'
    async with session.post(url_get_tasks, headers=headers) as response:
        if response.status == 200:
            json_response = await response.json()
            if json_response.get("ok"):
                result = json_response.get("result", {})
                balance = result.get("balance", 0)
                logging.info(f"#ACCOUNT {username} | BALANCE: {balance} AP")
                logging.info("STARTING AUTO CLAIM TASK...\n")

                tasks = result.get("tasks", [])
                for task in tasks:
                    task_type = task.get("type")
                    title = task.get("title")
                    reward = task.get("reward", 0)
                    is_claimed = task.get("is_claimed")
                    count = task.get("count", 0)
                    max_count = task.get("max_count")

                    if max_count is None and not is_claimed:
                        await claim_task(session, headers, task_type, title)

                    elif task_type == "video" and count < max_count:
                        while count < max_count:
                            logging.info(f"#TASK {task_type} - {title} PROGRESS: {count}/{max_count}")
                            if await claim_task(session, headers, task_type, title):
                                count += 1
                            else:
                                break

                    elif not is_claimed and count >= max_count:
                        await claim_task(session, headers, task_type, title)
                logging.info("\nALL TASKS COMPLETED!")
            else:
                logging.warning("FAILED TO RETRIEVE TASKS. PLEASE TRY AGAIN.")
        else:
            logging.error(f"# HTTP Error: {response.status}")

# Function to claim a single task asynchronously
async def claim_task(session, headers, task_type, title):
    url_complete_task = 'https://api.agent301.org/completeTask'
    claim_data = {"type": task_type}
    async with session.post(url_complete_task, headers=headers, json=claim_data) as response:
        if response.status == 200 and (await response.json()).get("ok"):
            result = (await response.json()).get("result", {})
            task_reward = result.get("reward", 0)
            balance = result.get("balance", 0)
            logging.info(f"#TASK {task_type} - {title} - REWARD {task_reward} AP - CURRENT BALANCE: {balance} AP")
            return True
        else:
            logging.error(f"#TASK {task_type} - {title} - CLAIM FAILED!")
            return False

# Main function to run the entire process
async def main():
    auth_data = await load_authorizations_with_usernames('query.txt')

    async with aiohttp.ClientSession() as session:
        try:
            while True:
                tasks = [
                    claim_tasks(session, data['authorization'], account_number, data['username'])
                    for account_number, data in enumerate(auth_data, start=1)
                ]
                
                await asyncio.gather(*tasks)

                logging.info("AUTO LOOPING AFTER 8 HOURS...")
                await asyncio.sleep(28800)  # 8 hours in seconds
        except KeyboardInterrupt:
            logging.info("Script interrupted by user. Exiting gracefully...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Program terminated by user.")
