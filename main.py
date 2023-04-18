import threading
from datetime import datetime
import discord
from os import abort, path
import random
import atexit
import json
import text_data as txt
import asyncio 

from lang_support import LangSupport
from datalogger import DataLogger

languages = LangSupport(path.basename(__file__).split(".")[0], ignore_file_error=True, ignore_key_error=True, ignore_dict_error=True)
dl = DataLogger(path.basename(__file__).split(".")[0], 'logs')


async def send_embed_help(message, data):
    if data is None:
        return 3
    embed = discord.Embed(
        title="Help",
        description=data,
        color=0xC00000
    )
    await message.channel.send(embed=embed)


def exit_handler():
    with open("data_container.json", "w") as data_container_write:
        json.dump(data_c, data_container_write, indent=4)
    with open("data_token.json", "w") as data_token_write:
        json.dump(token_c, data_token_write, indent=4)
    with open("config_container.json", "w") as config_container_write:
        json.dump(conf_c, config_container_write, indent=4)
    dl.log("Clean exit")
    for inst in DataLogger.instances:
        inst.end()


atexit.register(exit_handler)


class MiniExterminator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.command_recieved = threading.Event()
        self.daemon = True
        intents = discord.Intents.all()
        intents.members = True
        self.ex = EXTERMINATOR(intents=intents)
        
    def run(self):
        try:
            self.ex.run(token_c['bot-token'], log_handler=None)
        except Exception as exception:
            dl.log(f"Program stopped due to {type(exception)} : {exception}", log_type=3)
            exit()
    
    def recieve(self, command):
        if command == 'exit':
            asyncio.run(self.ex.close())
            #loop = asyncio.get_running_loop()
            #asyncio.run_coroutine_threadsafe(self.ex.shutdown, self.ex.loop)
        if command.startswith("su_send"):
            asyncio.run(self.ex.superuser_message_send(channel=int(command.split()[1]), message=command.split()[2]))
            # 1096800402369949796



class EXTERMINATOR(discord.Client):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.ready = False
        self.name = txt.app_name
        self.command_prefix = txt.cmd_prefix
        self.language = languages.language
        self.msg_edit_interval = 180 # seconds
        
    async def superuser_message_send(self, channel, message):
        #channel = discord.utils.get(self.client.get_all_channels(), id=channel)
        channel = self.get_channel(channel)
        print(message)
        await channel.send(message)
        
    async def shutdown(self):
        print("shuttingdown")
        await self.close()
        print("Bot offline")

    async def on_ready(self):
        dl.log(f"Logged and ready as {self.user}")
        dl.log("Connected to:")
        for server in self.guilds:
            if server.name not in data_c:
                data_c[server.name] = [txt.data_container_schema]
            if server.name not in conf_c:
                conf_c[server.name] = [txt.config_container_schema]
            dl.log(f"{server.id} - {server.name}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f" {languages.get_text('bot_activity_prompt', txt.cmd_prefix)}"))
        self.ready = True

    async def on_guild_join(self, guild):
        if self.ready:
            dl.log(f"{self.user} has connected to {guild.name}")
            data_c[guild.name] = [txt.data_container_schema]
            conf_c[guild.name] = [txt.config_container_schema]
            dl.log("JSON scheme added.")

    async def on_guild_remove(self, guild):
        if self.ready:
            dl.log(f"{self.user} has left the {guild.name}")
            del data_c[guild.name]
            del conf_c[guild.name]
            dl.log("JSON scheme deleted.")

    async def on_message(self, message):
        if self.ready:
            await handle_message(self, message)

    async def on_message_edit(self, before, after):
        if self.ready:
            time_diff = after.edited_at - before.created_at
            if time_diff.total_seconds() < self.msg_edit_interval:
                await handle_message(self, after)

    async def on_member_join(self, member):
        if self.ready:
            if member.name != self.user:
                dl.log(f"{member.name} has joined {member.guild.name}")
                channel = await member.create_dm()
                embed = discord.Embed(
                    title=f":smiley: Hello! {member.name} :wave:",
                    description="User verification is temporarily unavailable, for further"
                                "information please contact the Server Administration.",
                    color=0xC00000
                )
                await channel.send(embed=embed)
            else:
                dl.log(f"{member.name} was added to {member.guild.name}")

    async def on_member_remove(self, member):
        if self.ready:
            if member.name != self.user:
                dl.log(f"{member.name} has left the {member.guild.name} server")
            else:
                dl.log(f"{member.name} was removed from the {member.guild.name} server")

    async def on_member_update(self, before, after):
        # before.name != after.name
        # before.role != after.role
        if not self.ready:
            return


async def handle_message(self, message):
    if self.ready:
        if message.author != self.user:
            if message.guild is not None:
                if message.content.startswith("E>"):
                    msg = message.content.replace('E>', '')
                    if message.author.guild_permissions.administrator:
                        pass #print("Admin!")
                    if message.author == message.guild.owner:
                        pass #print("Owner!")
                    # Users commands
                    if msg == 'hello':
                        await message.channel.send('Hello!')

                    if msg == 'ping':
                        ping = round(self.latency, 1)
                        speed = ''
                        if ping <= 10:
                            speed = 'Super fast :rocket:'
                        elif ping <= 30:
                            speed = 'Quite fast :rabbit:'
                        elif ping <= 100:
                            speed = 'Sloow :turtle:'
                        else:
                            speed = 'Terrible :sob:'
                        await message.channel.send('pong! \n{0} {1} ms'.format(speed, ping))

                    if msg == '':
                        await message.channel.send('Yep that\'s me')

                    if msg == 'whereami':
                        await message.channel.send('You are on {} server!'.format(message.guild.name))

                    if msg == 'help':
                        await send_embed_help(message, txt.prepare_help_page(langsupport_inst=languages))

                    # Admin commands
                    if message.author.guild_permissions.administrator or message.author.id == self.guild.owner.id:
                        if message.content == 'hello':
                            await message.channel.send('Hi Admin!')
                        if 'set_verify_method' in msg:
                            cmd, val = list(msg.split())
                            if msg[1] in txt.verify_types_str:
                                conf_c[message.guild.name]['verify_method'] = txt.verify_types_str.index(val)
                                await message.channel.send('Verification method set to {0}'.format(val))
                            else:
                                await message.channel.send(
                                    ':octagonal_sign:  ERROR!  :octagonal_sign: \nInvalid argument => {0} <='.format(
                                        val))
                        if 'set_verify_depth' in msg:
                            cmd, val = list(msg.split())
                            if int(val) in list(range(1, txt.verify_obj_count)):
                                conf_c[message.guild.name]['verify_depth'] = int(val)
                                await message.channel.send('Verification depth set to {0}'.format(val))
                            else:
                                await message.channel.send(
                                    ':octagonal_sign:  ERROR!  :octagonal_sign: \nInvalid value => {0} <='.format(
                                        val))
                        if 'set_verified_role' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'set_verify_new' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'verify_user' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'verify_bulk' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'set_ghosting' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'set_warning' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
                        if 'set_kick' in msg:
                            await message.channel.send(
                                ':construction: Under construction :construction: \nSoon available :construction_worker:')
            else:
                if message.content != "":
                    channel = await message.author.create_dm()
                    await channel.send(
                        ':construction: Under construction :construction: \nSoon available :construction_worker:')


if __name__ == "__main__":
    data_c = {}
    conf_c = {}
    token_c = {}

    try:
        with open("data_container.json", "r") as data_container:
            try:
                data_c = json.load(data_container)
            except json.JSONDecodeError:
                dl.log("data_container.json is corrupted", log_type=3)
                abort()
            else:
                dl.log("Data from data_container.json, successfully read")
    except FileNotFoundError:
        dl.log("data_container.json file not found! New data_container file will be created.", log_type=1)

    try:
        with open("config_container.json", "r") as config_container:
            try:
                conf_c = json.load(config_container)
            except json.JSONDecodeError:
                dl.log("config_container.json is corrupted", log_type=3)
                abort()
            else:
                dl.log("Data from config_container.json, successfully read")
    except FileNotFoundError:
        dl.log("config_container.json file not found! New config_container file will be created.", log_type=1)

    no_token = True
    try:
        with open("data_token.json", "r") as data_token:
            try:
                token_c = json.load(data_token)
            except json.JSONDecodeError:
                dl.log("data_token.json is corrupted", log_type=3)
            else:
                no_token = False
                dl.log("Token from data_token.json, successfully read")
    except FileNotFoundError:
        dl.log("data_token.json, not found", log_type=1)

    if no_token:
        token_c['bot-token'] = input('No bot-token in data_token.json, enter it please\n>')

    if 'bot-token' not in token_c:
        token_c['bot-token'] = input('No bot-token in data_container.json, enter it please\n>')

    miniex = MiniExterminator()
    miniex.start()
    
    while 1:
        c = input("\n>")
        miniex.recieve(command = c)
        if c == 'exit':
            break
        if c == 'h':
            print("no help yet..")

    dl.log("MiniExterminator thread has been killed")
