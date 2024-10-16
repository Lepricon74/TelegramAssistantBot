from datetime import datetime
from pyrogram import Client, filters
from decouple import config
from pyrogram.types import Message
from dbRepository import DbRepository
from regexHelper import getPrice, getRoomCount
import logging
import asyncio
import re


class AssistantBot:
    searchToDate = datetime(2024, 10, 12, 1, 0, 0)
    forwardChatTitle = 'ApartmentSearchAssistant'
    forwardChat = None
    telegramClient = None

    isInit = False

    dbRepository: DbRepository = None

    def __init__(self, dbRepository: DbRepository):
        self.telegramClient = Client(name=config('LOGIN'),
                                     api_id=config('API_ID'),
                                     api_hash=config('API_HASH'),
                                     phone_number=config('PHONE'))
        self.dbRepository = dbRepository

    async def initBot(self):
        await self.telegramClient.start()
        async for dialog in self.telegramClient.get_dialogs():
            if (dialog.chat.title == self.forwardChatTitle):
                self.forwardChat = dialog.chat
                break
        if (self.forwardChat == None):
            logging.error(f'Could not find chat to forward with title {self.forwardChatTitle}')
            return
        await self.telegramClient.stop()

    def isMessageValid(self, message: Message) -> bool:
        if (message.caption is None):
            return False
        rows = re.split(";|,|\n", message.caption)
        price = 10000
        roomsCount = ""
        for row in rows:
            priceOrNone = getPrice(row)
            if (priceOrNone): price = priceOrNone
            roomsCountOrNone = getRoomCount(row)
            if (roomsCountOrNone): roomsCount = roomsCountOrNone
        if (price >= 600 and price <= 1000 and (
                roomsCount == '3' or roomsCount == '2в3')): return True;
        return False

    async def processMessage(self, message: Message) -> bool:
        if self.isMessageValid(message):
            messageDbKey = str(message.id) + '@' + message.chat.username
            if (self.dbRepository.checkMessageIdExist(messageDbKey)): return
            mediaGroupMessages = await self.telegramClient.get_media_group(message.chat.username, message.id)
            messagesIdsToForward = list(map(lambda x: x.id, mediaGroupMessages))
            await self.telegramClient.forward_messages(
                chat_id=self.forwardChat.id,
                from_chat_id=message.chat.id,
                message_ids=messagesIdsToForward
            )
            await self.telegramClient.send_message(self.forwardChat.id,
                                                   f'Дата публикации: {message.date:%Y-%m-%d %H:%M:%S%z}')
            self.dbRepository.addMessageId(messageDbKey)
            return True
        return False

    async def processOldMessages(self, targetChatId: str):
        if self.isInit == False: await self.initBot()
        await self.telegramClient.start()
        async for message in self.telegramClient.get_chat_history(targetChatId):
            if (message.date < self.searchToDate): break
            messageWasForward = await self.processMessage(message)
            if(messageWasForward): await asyncio.sleep(15)
        await self.telegramClient.stop()

    def beginObservation(self):
        @self.telegramClient.on_message(filters.channel)
        async def echo_handler(client: Client, message: Message):
            messageWasForward = await self.processMessage(message)
            if (messageWasForward): await asyncio.sleep(2)
        self.telegramClient.run()
