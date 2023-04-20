import threading
from datetime import datetime
import discord
from discord.ext import tasks
from os import abort, path
import random
from atexit import register as atexit_method
import json
import text_data as txt
import asyncio 
from platform import python_version, system, release, architecture
from image_generator import captcha_math, captcha_text
import io

from lang_support import LangSupport
from datalogger import DataLogger

languages = LangSupport(path.basename(__file__).split(".")[0], ignore_file_error=True, ignore_key_error=True, ignore_dict_error=True)
dl = DataLogger(path.basename(__file__).split(".")[0], 'logs')

langs_dict = {}
exit_tasks = {}

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


atexit_method(exit_handler)


class MiniExterminator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.command_recieved = threading.Event()
        self.daemon = True
        intents = discord.Intents.all()
        intents.members = True
        self.ex = EXTERMINATOR(intents=intents)
        self.loop = asyncio.new_event_loop()
        self.closed = False
        
    def run(self):
        try:
            self.loop.run_until_complete(self.ex.start(token_c['bot-token']))
        except Exception as exception:
            dl.log(f"Program stopped due to {type(exception)} : {exception}", log_type=3)
        self.closed = True
    
    def recieve(self, command):
        dl.log(f"SuperUser command: {command}")
        if command == 'exit':
            try:
                asyncio.run_coroutine_threadsafe(asyncio.wait_for(self.ex.shutdown(), timeout=30), self.ex.loop)
                while not self.closed:
                    pass
                dl.log("Bot inactive.")
            except TimeoutError:
                dl.log("Bot shutdown timeout! Force quitting.", log_type=2)
            self.ex.loop.stop()
            self.loop.stop()
            self.join()
        elif command.startswith("su_send"):
            try:
                channel = int(command.split()[1])
                message = command.replace(f"su_send {str(channel)} ", "").replace(r'\n', '\n').replace(r'\t', '\t')
                if len(message):
                    asyncio.run_coroutine_threadsafe(self.ex.superuser_message_send(channel=channel, message=message), self.loop)
                else:
                    raise IndexError
            except IndexError:
                print("Should be: su_send <channel-id> <message>")
                dl.log("Should be: su_send <channel-id> <message>", log_type=2)
        elif command == "get_status":
            status = ["not ready", "ready"]
            print(f"Status: {status[self.ex.ready]}")
            dl.log(f"Status: {status[self.ex.ready]}")
        elif command.startswith("math"):
            try:
                channel = int(command.split()[1])
                channel = self.ex.get_channel(channel)
                img = captcha_math()
                with io.BytesIO() as image_binary:
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    asyncio.run_coroutine_threadsafe(channel.send(file=discord.File(fp=image_binary, filename='math.png')), self.loop)
            except IndexError:
                print("Should be: math <channel-id>")
                dl.log("Should be: math <channel-id>", log_type=2)
        elif command.startswith("dump_"):
            command = command.replace(f"dump_", "")
            dtype = command.split()[0]
            command = command.replace(f"{dtype}", "").strip().split()
            wrong = False
            data = None
            if dtype == "config":
                data = conf_c
            elif dtype == "data":
                data = data_c
            if len(command) == 0:
                dl.log(str(data))
                print(str(data))
            elif len(command) == 1:
                try:
                    dump = str(data[command[0]])
                    dl.log(dump)
                    print(dump)
                except IndexError:
                    wrong = True
            elif len(command) == 2:
                try:
                    dump = str(data[command[0]][0][command[1]])
                    dl.log(dump)
                    print(dump)
                except IndexError:
                    wrong = True
            else:
                wrong = True
            if wrong:
                print(f"Should be: dump_<data | config> [<server-name>] [<parameter>]")
                dl.log(f"Should be: dump_<data | config> [<server-name>] [<parameter>]", log_type=2)
        elif command.startswith("exec"):   # only for test purposes
            comand = command.replace("exec ", "")
            exec(str(comand))
        else:
            print(f"Command: {command} is unknown")
            dl.log(f"Command: {command} is unknown", log_type=1)


class EXTERMINATOR(discord.Client):
    task_loop_seconds = 60

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
        await channel.send(message)
        
    async def shutdown(self):
        dl.log(f"Shuttingdown {self.user}...")
        await self.loop.stop()
        await self.loop.close()
        dl.log(f"{self.user} offline")

    async def on_ready(self):
        dl.log(f"Logged in and ready as {self.user}")
        dl.log(f"discord.py API version: {discord.__version__}")
        dl.log(f"Python version: {python_version()}")
        dl.log(f"Hosted on {system()} {release()} {architecture()[0]}")
        dl.log("Connected to:")
        for server in self.guilds:
            if server.name not in data_c:
                data_c[server.name] = [txt.data_container_schema]
            if server.name not in conf_c:
                conf_c[server.name] = [txt.config_container_schema]
            lang = conf_c[server.name][0]['language']
            langs_dict[server.name] = txt.update_server_dict(languages, lang)
            dl.log(f"{server.id} - {server.name}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"extermination | {txt.cmd_prefix}help for commands"))
        self.periodic_task.start()
        self.ready = True

    @tasks.loop(seconds=task_loop_seconds)
    async def periodic_task(self):
        pass

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
        if self.ready and not message.author.bot:
            await handle_message(self, message)

    async def on_message_edit(self, before, after):
        if self.ready:
            time_diff = after.edited_at - before.created_at
            if time_diff.total_seconds() < self.msg_edit_interval:
                await handle_message(self, after)

    async def on_member_join(self, member):
        if self.ready:
            if member.name != self.user and not member.bot:
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
            if member.name != self.user and not member.bot:
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
                if message.content.startswith(txt.cmd_prefix):
                    msg = message.content.replace(f"{txt.cmd_prefix}", "")
                    cmd = msg.split()[0].strip()
                    msg = msg.replace(f"{cmd}", "")

                    is_admin = message.author.guild_permissions.administrator
                    is_owner = message.author == message.guild.owner

                    # check if command exist and user priviliges
                    if cmd in txt.admin_cmd_list:
                        # check if message author is a admin or owner
                        if is_admin or is_owner:
                            # Admin commands
                            await handle_ac(cmd, msg, message)
                        else:
                            # if not priviliged, check if command exists also as non admin 
                            if cmd in txt.nonadmin_cmd_list:
                                await handle_nac(cmd, msg, message)
                            else:
                                await message.channel.send(languages.ext_text(langs_dict[message.guild.name], 'notprivileged_command', cmd))
                    elif cmd in txt.nonadmin_cmd_list:
                        # Non Admin commands
                        await handle_nac(cmd, msg, message)
                    else:
                        await message.channel.send(languages.ext_text(langs_dict[message.guild.name], 'unknown_command', cmd))
            else:
                if message.content != "":
                    channel = await message.author.create_dm()
                    await channel.send(languages.ext_text(langs_dict[message.guild.name], 'under_construction'))


async def handle_nac(command: str, msg: str, message):
    if command == 'ping':
        ping = round(miniex.ex.latency, 1)
        speed = ''
        if ping <= 10:
            speed = languages.ext_text(langs_dict[message.guild.name], 'ping_sfast')
        elif ping <= 30:
            speed = languages.ext_text(langs_dict[message.guild.name], 'ping_fast')
        elif ping <= 100:
            speed = languages.ext_text(langs_dict[message.guild.name], 'ping_slow')
        else:
            speed = languages.ext_text(langs_dict[message.guild.name], 'ping_tslow')
        await message.channel.send(f"pong! \n{speed} {ping} ms")
    elif command == 'whereami':
        await message.channel.send(languages.ext_text(langs_dict[message.guild.name], 'whereme', message.guild.name))
    elif command == 'help':
        await send_embed_help(message, txt.prepare_help_page(languages, langs_dict[message.guild.name]))
    elif command == 'hello':
        await message.channel.send(languages.ext_text(langs_dict[message.guild.name], 'greet_user', message.author.split('#')[0]))
    else:
        await message.channel.send(languages.ext_text(langs_dict[message.guild.name], 'under_construction'))

async def handle_ac(command: str, msg: str, message):
    if command == 'hello':
        await message.channel.send(languages.ext_text(langs_dict[message.guild.name], 'greet_admin'))
    elif command == 'set_language':
        if msg not in languages.get_languages():
            await message.channel.send(languages.ext_text(langs_dict[message.guild.name], 'wrong_lang', msg))
        else:
            dict_ = txt.update_server_dict(languages, msg)
            langs_dict[message.guild.name] = dict_
            conf_c[message.guild.name][0]['language'] = msg
    else:
        await message.channel.send(languages.ext_text(langs_dict[message.guild.name], 'under_construction'))

async def send_embed_help(message, data):
    if data is None:
        return 3
    embed = discord.Embed(
        title="Help",
        description=data,
        color=0xC00000
    )
    await message.channel.send(embed=embed)


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
        try:
            c = input(">")
        except EOFError:
            c = "exit"
        miniex.recieve(command = c)
        if c == 'exit':
            break
        if c == 'h':
            print("no help yet..")

    miniex.join()
    dl.log("MiniExterminator thread has been killed")
