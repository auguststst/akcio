from pyrogram import Client

api_id = 127600233 
api_hash = "132337762a2554f293zx1736ead2804c9"
path = '/home/jamato/channels'

class Telegram:


    def __init__(self,title):
        self.title = title

    def no_casesensitive(self, word):
        word = str(word)
        return word.lower()

    def get_channels(self, file):
        channels = open(file,'r')
        return channels.readlines()

    def check_type_channel(self, array):
        ch = []
        for r in array:
            if "joinchat" in r:
                ch.append(r)
            else: 
                ch.append(r[13:])
    
        return ch 

    def get_telegram_channel(self, ch):
        with Client("my_account", api_id, api_hash) as app:
            x = 0
            while(x < len(ch)):
                id = app.get_chat(ch[x])["id"]

                for m in app.iter_history(chat_id=id):
                    if self.no_casesensitive(self.title) in self.no_casesensitive(m["caption"]) and m["video"] and m["video"]["duration"] > 3600:
                        app.forward_messages("me", id, m["message_id"])
                
                x = x + 1 

    def forward_to_the_channel(self):
        telegram_channels = self.get_channels(path)
        telegram_channels = self.check_type_channel(telegram_channels)
        return self.get_telegram_channel(telegram_channels)

    
title = str(input("Поиск: \t\t"))
t = Telegram(title)
t.forward_to_the_channel()

#telegram_channels = t.get_channels(path)
#telegram_channels = t.check_type_channel(telegram_channels)
#t.get_telegram_channel(telegram_channels)