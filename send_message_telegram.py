#!/usr/bin/env python3
                                                                                                                                                              
import telegram
import json
                                                                                                                                                              
bot = telegram.Bot("YOUR_BOT_ID")
#resp = bot.get_updates()[].message.chat_id
#print (resp)
chat_id=YOUR_CHAT_ID
bot.send_message(chat_id=chat_id, text="SOME_THING_SEND_BY_BOT")
