from datetime import datetime
from assistantBot import AssistantBot
from dbRepository import DbRepository
from decouple import config
import logging
import asyncio

async def main():
    logging.basicConfig(
        level=logging.INFO,
        filename="{:%d-%m-%Y}".format(datetime.now()) + '.log',
        filemode='w')
    dbRepository = DbRepository('assistant_database.db')
    #dbRepository.initTables()
    assistantBot = AssistantBot(dbRepository)
    processOld = config('PROCESS_OLD')
    if(processOld):
        targetChannelIds = dbRepository.getTargetChannelUsernames()
        for targetChannelId in targetChannelIds:
            await assistantBot.processOldMessages(targetChannelId)

asyncio.run(main())
