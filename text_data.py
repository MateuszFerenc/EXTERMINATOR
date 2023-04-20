from lang_support import LangSupport


app_name = "EXTERMINATOR"
cmd_prefix = 'E>'

nonadmin_cmd_list = []
admin_cmd_list = []

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
    "verify_method": 0,
    "verify_depth": 5,
    "language": "EN_us",
    "verify_role": "None",
    "verify_new": "False",
    "do_ghost": "False",
    "do_warn": "False",
    "do_kick": "False",
    "pending_tasks": "None"
}
# < JSON data schemas section END

def prepare_help_page(langsupport_inst: LangSupport) -> str:
    assert isinstance(langsupport_inst, LangSupport)
    page = "{}\n".format(langsupport_inst.get_text('header_help', app_name, cmd_prefix))
    page += "\n{}\n".format(langsupport_inst.get_text('header_nac_H'))
    lkey = 'nac_H_help'
    page += "***{}*** : {}\n".format(lkey.replace('nac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'nac_H_hello'
    page += "***{}*** : {}\n".format(lkey.replace('nac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'nac_H_ping'
    page += "***{}*** : {}\n".format(lkey.replace('nac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'nac_H_whereami'
    page += "***{}*** : {}\n".format(lkey.replace('nac_H_', ''), langsupport_inst.get_text(lkey))
    page += "\n{}\n".format(langsupport_inst.get_text('header_ac_H'))
    lkey = 'ac_H_set_language'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey, langsupport_inst.lang_list))
    lkey = 'ac_H_set_verify_method'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey, return_verification_list(langsupport_inst)))
    lkey = 'ac_H_set_verify_depth'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey, ['null']))
    lkey = 'ac_H_set_verified_role'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'ac_H_set_verify_new'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'ac_H_verify_user'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'ac_H_verify_bulk'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'ac_H_reverify'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'ac_H_set_ghosting'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'ac_H_set_warning'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey))
    lkey = 'ac_H_set_kick'
    page += "***{}*** : {}\n".format(lkey.replace('ac_H_', ''), langsupport_inst.get_text(lkey))
    return page.replace(r'\n', '\n')

def return_verification_list(langsupport_inst):
    assert isinstance(langsupport_inst, LangSupport)
    keys_list = ['c_math', 'c_text']
    temp_list = []
    for k in keys_list:
        temp_list.append(langsupport_inst.get_text(k))
    return temp_list

def update_server_dict(langsupport_inst: LangSupport, lang: str) -> dict:
    assert isinstance(langsupport_inst, LangSupport)
    assert type(lang) is str
    assert lang in langsupport_inst.get_languages()
    return langsupport_inst.set_language(lang=lang, dump=True)
