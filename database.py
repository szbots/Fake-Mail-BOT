#=================================================================================================
# Copyright (C) 2022 by szsupunma@Github, < https://github.com/szsupunma >.
# Released under the "GNU v3.0 License Agreement".
# All rights reserved.
#=================================================================================================
import os
from motor.motor_asyncio import AsyncIOMotorClient

DATABASE = os.environ["DATABASE"]

mongo_client = AsyncIOMotorClient(DATABASE)
db = mongo_client.users
userdb = db.users

#===================== User database ================================

async def is_served_user(user_id: int) -> bool:
    user = await userdb.find_one({"bot_users": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users = userdb.find({"bot_users": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await userdb.insert_one({"bot_users": user_id})

async def remove_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await userdb.delete_one({"bot_users": user_id})

#===================== groups  database ================================

async def get_served_chats() -> list:
    chats = userdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    async for chat in userdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_served_chat(chat_id: int) -> bool:
    chat = await userdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True

async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await userdb.insert_one({"chat_id": chat_id})

async def remove_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return
    return await userdb.delete_one({"chat_id": chat_id})