from lang_support import LangSupport
from datetime import datetime

app_name = "EXTERMINATOR"
cmd_prefix = 'E>'

nonadmin_cmd_list = ['help', 'hello', 'ping', 'whereami']
admin_cmd_list = ['set_language', 'get_languages', 'set_verify_method', 
                'get_verify_methods', 'get_bot_stats', 'set_verified_role',
                'set_verify_new', 'verify_user', 'verify_bulk', 
                'reverify', 'set_ghosting', 'set_warning', 
                'set_kick', 'hello']

limited_commands = {
    'set_language': "w0:d4",
    'set_verify_new': "w0:d2",
    'reverify': "w1:d0"
}

verification_list = ['cptmath', 'cpttext']
version = "0.00.21 (Alfa)"

# < JSON data schemas section START
data_container_schema = {
    "Users2Verify": 0,
    "Users2VerifyData": [],
    "UsersVerified": 0,
    "UsersVerifiedData": [],
    "Users2GHOST": 0,
    "Users2GHOSTData": [],
    "UsersGHOSTED": 0,
    "UsersGHOSTEDData": [],
    "Users2Warn": 0,
    "Users2WarnData": [],
    "UsersWarned": 0,
    "UsersWarnedData": [],
    "Users2Kick": 0,
    "Users2KickData": [],
    "UsersLeft": 0,
    "UsersLeftData": []
}

config_container_schema = {
    "member_since": None,
    "verify_method": "",
    "language": "EN_us",
    "verify_role": None,
    "verify_new": False,
    "do_ghost": False,
    "do_warn": False,
    "do_kick": False,
    "pending_tasks": None
}
# < JSON data schemas section END

def prepare_help_page(lang_dict: dict) -> str:
    page = "{}\n".format(LangSupport.ext_text(lang_dict, 'header_help', app_name, cmd_prefix))
    page += "\n{}\n".format(LangSupport.ext_text(lang_dict, 'header_nac_H'))
    for c in nonadmin_cmd_list:
        page += "➤  ***{}*** : {}\n".format(c, LangSupport.ext_text(lang_dict, f"nac_H_{c}"))
    page += "\n{}\n".format(LangSupport.ext_text(lang_dict, 'header_ac_H'))
    for c in admin_cmd_list:
        page += "➤  ***{}*** : {}\n".format(c, LangSupport.ext_text(lang_dict, f"ac_H_{c}"))
    return page.replace(r'\n', '\n')

def update_server_dict(langsupport_inst: LangSupport, lang: str) -> dict:
    assert isinstance(langsupport_inst, LangSupport)
    assert type(lang) is str
    assert lang in langsupport_inst.get_languages()
    return langsupport_inst.set_language(lang=lang, dump=True)

def get_time_limit(command: str):
    week = int(limited_commands[command].split(":")[0].replace("w", ""))
    day = int(limited_commands[command].split(":")[1].replace("d", ""))
    week_inc = 1 if week > 0 else 0
    day_inc = 1 if day > 0 else 0
    return week, day, week_inc, day_inc

def get_limit_name(langs_dict: dict, command: str):
    dat = list(get_time_limit(command))
    times = 0
    kind = ""
    if dat[0]:
        kind = LangSupport.ext_text(langs_dict, 'weekly')
        times = dat[0]
    else:
        kind = LangSupport.ext_text(langs_dict, 'daily')
        times = dat[1]
    return kind, times
    
def is_command_limited(config_cointainer: dict, server_name: str, command: str):
    week, day, week_inc, day_inc = get_time_limit(command)
    if command in config_cointainer[server_name][0]:
        _week = int(config_cointainer[server_name][0][command][0]['count'].split(":")[0].replace("w", ""))
        _day = int(config_cointainer[server_name][0][command][0]['count'].split(":")[1].replace("d", ""))
        if _week < week or _day < day:
            config_cointainer[server_name][0][command][0]['count'] = f"w{week_inc + _week}:d{day_inc + _day}"
        else:
            return True
    else:
        now_time = datetime.now().strftime('%H:%M:%d:%m:%y')
        config_cointainer[server_name][0][command] = []
        data = {
            'count': f"w{week_inc}:d{day_inc}",
            'datetime': now_time
        }
        config_cointainer[server_name][0][command].append(data)
    return False

def decision_bool(yes: list, no: list, s: str) -> bool:
    s = s.lower()
    if s == yes or s == 1:
        return True
    elif s == no or s == 0:
        return False
    else:
        raise TypeError()
