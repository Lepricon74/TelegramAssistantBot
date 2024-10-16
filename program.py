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
    # dbRepository.initTables()
    assistantBot = AssistantBot(dbRepository)
    targetChannelIds = dbRepository.getTargetChannelUsernames()
    logging.info('MODE: realtimeObservation')
    for targetChannelId in targetChannelIds:
        await assistantBot.processOldMessages(targetChannelId)


asyncio.run(main())


# def main():
#     logging.basicConfig(
#         level=logging.INFO,
#         filename="{:%d-%m-%Y}".format(datetime.now()) + '.log',
#         filemode='w')
#     dbRepository = DbRepository('assistant_database.db')
#     assistantBot = AssistantBot(dbRepository)
#     logging.info('MODE: realtimeObservation')
#     assistantBot.beginObservation()
#
#
# main()
