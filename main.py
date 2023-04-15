from threading import Thread
from datetime import datetime
import discord
from os import abort, path
import random
import atexit
import json
import text_data as txt

from lang_support import LangSupport
from datalogger import DataLogger

app_name = "EXTERMINATOR"
cmd_prefix = 'E>'

languages = LangSupport(path.basename(__file__).split(".")[0], ignore_file_error=True, ignore_key_error=True, ignore_dict_error=True)
dl = DataLogger(path.basename(__file__).split(".")[0], 'logs', debug=True)  # "debug=True" remove in future


def print_help():
    page = f"**{app_name}** commands help (Command prefix **{cmd_prefix}**):\n"
    page += "\n• Non Admin commands •\n"
    for command in txt.nonadmin_commands.keys():
        page += f"***{command}*** : {txt.nonadmin_commands[command]}\n"
    page += "\n• Admin commands •\n"
    for command in txt.admin_commands.keys():
        page += f"***{command}*** : {txt.admin_commands[command]}\n"
    return page


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
    for inst in DataLogger.instances:
        inst.end()
    print("Clean exit")


atexit.register(exit_handler)


def miniexterminator(client):
    print("miniexterminator thread created!")

    do_sth = False
    msg = ""
    while True:
        msg = input("enter superuser message")
        if not client.inuse and do_sth:
            client.superuser_message_send("1096800402369949796", msg)
            


class EXTERMINATOR(discord.Client):
    def __init__(self, *args, **kwargs):

        super(EXTERMINATOR, self).__init__(*args, **kwargs)

        # self.config = config
        self.ready = False
        self.name = app_name
        self.command_prefix = cmd_prefix
        self.inuse = False
        self.language = "english"
        self.msg_edit_interval = 180 # seconds
        
    async def superuser_message_send(self, channel, message):
        #channel = discord.utils.get(self.client.get_all_channels(), id=channel)
        channel = self.get_channel(channel)
        print(message)
        await channel.send(message)

    async def on_ready(self):
        print('Logged and ready as {0.user}'.format(self))
        print('Connected to:')
        for server in self.guilds:
            if server.name not in data_c:
                data_c[server.name] = [txt.data_container_schema]
            if server.name not in conf_c:
                conf_c[server.name] = [txt.config_container_schema]
            print("%s - %s" % (server.id, server.name))
        if not self.ready:
            Thread(target=miniexterminator, args=(self,), daemon=True).start()
        self.ready = True

    async def on_guild_join(self, guild):
        if not self.ready:
            return
        self.inuse = True
        print("{} has connected to {}".format(self.user, guild.name))
        data_c[guild.name] = [txt.data_container_schema]
        conf_c[guild.name] = [txt.config_container_schema]
        print("JSON scheme added.")
        self.inuse = False

    async def on_guild_remove(self, guild):
        if not self.ready:
            return
        self.inuse = True
        print("{} has left the {}".format(self.user, guild.name))
        del data_c[guild.name]
        del conf_c[guild.name]
        print("JSON scheme deleted.")
        self.inuse = False

    async def on_message(self, message):
        if not self.ready:
            return
        self.inuse = True
        await handle_message(self, message)
        self.inuse = False

    async def on_message_edit(self, before, after):
        if not self.ready:
            return
        self.inuse = True
        time_diff = after.edited_at - before.created_at
        if time_diff.total_seconds() < self.msg_edit_interval:
            await handle_message(self, after)
        self.inuse = False

    async def on_member_join(self, member):
        if not self.ready:
            return
        if member.name == ex.user:
            return
        self.inuse = True
        print('{} has joined {}!'.format(member.name, member.guild.name))
        channel = await member.create_dm()
        embed = discord.Embed(
            title=':smiley: Hello! {} :wave:'.format(member.name),
            description='We are glad to see you on {}.\n\nUntil you gain server access'
                        ', you need to pass verification.'.format(member.guild.name),
            color=0xC00000
        )
        await channel.send(embed=embed)
        await user_verify(self, member, channel)
        self.inuse = False

    async def on_member_remove(self, member):
        if not self.ready:
            return
        if member.name == ex.user:
            return
        self.inuse = True
        print('{} has left the {} server'.format(member.name, member.guild.name))
        await user_left_handler(self, member)
        self.inuse = False

    async def on_member_update(self, before, after):
        # before.name != after.name
        # before.role != after.role
        if not self.ready:
            return
        self.inuse = True

        self.inuse = False


async def handle_message(self, message):
    if not self.ready:
        return
    self.inuse = True
    if message.author != ex.user:
        if message.guild is not None:
            if message.content.startswith("E>"):
                msg = message.content.replace('E>', '')

                # Users commands
                if msg == 'hello':
                    await message.channel.send('Hello!')

                if msg == 'ping':
                    ping = round(ex.latency, 1)
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
                    await send_embed_help(message, print_help())

                # Admin commands
                if message.author.guild_permissions.administrator:
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
    self.inuse = False


async def user_verify(self, user, channel):
    verify_emojis = []
    verify_emojis_raw = []
    for emoji in range(int(conf_c[user.guild.name]['verify_depth'])):
        emoji_raw = txt.verify_types[conf_c[user.guild.name]['verify_method']][
            random.randrange(0, len(txt.verify_types[conf_c[user.guild.name]['verify_method']]))]
        verify_emojis.append(":" + emoji_raw + ":")
        verify_emojis_raw.append(emoji_raw)

    embed = discord.Embed(
        title="Verification",
        description='Aby tego dokonać, musisz wypisać w tej samej kolejności nazwy tych emoji (po przecinku i po '
                    'angielsku!) \n{0}'.format(
            ' , '.join(verify_emojis)),
        color=0xC00000
    )
    await channel.send(embed=embed)
    data_c[user.guild.name]['Users2Verify'] = data_c[user.guild.name]['Users2Verify'] + 1
    updated = False
    for i in range(len(data_c[user.guild.name]['Users2VerifyData'])):
        if data_c['Users2VerifyData'][i]['uname'] is None:
            data_c['Users2VerifyData'][i]['uname'] = user.name
            data_c['Users2VerifyData'][i]['ujdate'] = user.joined_at.strftime('%Y-%m-%d-%H:%M')
            data_c['Users2VerifyData'][i]['ucode'] = verify_emojis_raw
            updated = True

    if not updated:
        data = {
            "uname": user.name,
            "ujdate": user.joined_at.strftime('%Y-%m-%d-%H:%M'),
            "ucode": verify_emojis_raw
        }
        data_c[user.guild.name]['Users2VerifyData'].append(data)
        print("user {} successfully added to database".format(user.name))


async def user_left_handler(self, member):
    for data_search in data_c[member.guild.name]:
        if 'UsersLeftData' in data_search:
            continue
        i = 0
        for data_user in data_search:
            if data_c[member.guild.name][data_search][i]['uname'] == member.name:
                data_c[member.guild.name][data_search][i]['uname'] = None
                data = {
                    "uname": member.name,
                    "ujdate": data_c[member.guild.name][data_search][i]['ujdate'],
                    "uldate": datetime.today().strftime('%Y-%m-%d-%H:%M')
                }
                data_c[member.guild.name]['UsersLeftData'].append(data)
                break
            i += 1
    print("user {} successfully removed from database".format(member.name))

if __name__ == "__main__":
    data_c = {}
    conf_c = {}
    token_c = {}

    try:
        with open("data_container.json", "r") as data_container:
            try:
                data_c = json.load(data_container)
            except json.JSONDecodeError:
                print("data_container.json is corrupted")
                abort()
            else:
                print("Data from data_container.json, successfully read")
    except FileNotFoundError:
        print("data_container.json file not found!\nNew data_container file will be created.")

    try:
        with open("config_container.json", "r") as config_container:
            try:
                conf_c = json.load(config_container)
            except json.JSONDecodeError:
                print("config_container.json is corrupted")
                abort()
            else:
                print("Data from config_container.json, successfully read")
    except FileNotFoundError:
        print("config_container.json file not found!\nNew config_container file will be created.")

    no_token = True
    try:
        with open("data_token.json", "r") as data_token:
            try:
                token_c = json.load(data_token)
            except json.JSONDecodeError:
                print("data_token.json is corrupted")
            else:
                no_token = False
                print("Token from data_token.json, successfully read")
    except FileNotFoundError:
        print("data_token.json, not found")

    if no_token:
        token_c['bot-token'] = input('No bot-token in data_token.json, enter it please\n>')

    if 'bot-token' not in token_c:
        token_c['bot-token'] = input('No bot-token in data_container.json, enter it please\n>')

    try:
        intents = discord.Intents.all()
        intents.members = True
        ex = EXTERMINATOR(intents=intents)
        ex.run(token_c['bot-token'])
    except Exception as exception:
        print(f"Program stopped due to {type(exception)}\n{exception}")
        exit()
