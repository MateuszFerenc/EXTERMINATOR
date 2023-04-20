from lang_support import LangSupport


app_name = "EXTERMINATOR"
cmd_prefix = 'E>'

nonadmin_cmd_list = ['help', 'hello', 'ping', 'whereami']
admin_cmd_list = ['set_language', 'get_language', 'set_verify_method', 
                'get_verify_methods', 'get_bot_stats', 'set_verified_role',
                'set_verify_new', 'verify_user', 'verify_bulk', 
                'reverify', 'set_ghosting', 'set_warning', 
                'set_kick', 'hello']

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
    "member_since": "",
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

def prepare_help_page(langsupport_inst: LangSupport, lang_dict: dict) -> str:
    assert isinstance(langsupport_inst, LangSupport)
    page = "{}\n".format(langsupport_inst.ext_text(lang_dict, 'header_help', app_name, cmd_prefix))
    page += "\n{}\n".format(langsupport_inst.ext_text(lang_dict, 'header_nac_H'))
    for c in nonadmin_cmd_list:
        page += "***{}*** : {}\n".format(c, langsupport_inst.ext_text(lang_dict, f"nac_H_{c}"))
    page += "\n{}\n".format(langsupport_inst.ext_text(lang_dict, 'header_ac_H'))
    for c in admin_cmd_list:
        page += "***{}*** : {}\n".format(c, langsupport_inst.ext_text(lang_dict, f"ac_H_{c}"))
    return page.replace(r'\n', '\n')

def return_verification_list(langsupport_inst: LangSupport, lang_dict: dict) -> list:
    assert isinstance(langsupport_inst, LangSupport)
    keys_list = ['c_math', 'c_text']
    temp_list = []
    for k in keys_list:
        temp_list.append(langsupport_inst.ext_text(lang_dict, k))
    return temp_list

def update_server_dict(langsupport_inst: LangSupport, lang: str) -> dict:
    assert isinstance(langsupport_inst, LangSupport)
    assert type(lang) is str
    assert lang in langsupport_inst.get_languages()
    return langsupport_inst.set_language(lang=lang, dump=True)
