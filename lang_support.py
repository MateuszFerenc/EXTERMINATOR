from os import listdir, path
from re import match
from datalogger import DataLogger


class LangSupport:
    def __init__(self, directory=None, ignore_file_error=False, ignore_key_error=False, ignore_dict_error=False):
        if directory is None:
            exit(3)
        self.dl = DataLogger(f"{path.basename(__file__).split('.')[0]}<<{directory}", 'logs', debug=True)  # "debug=True" remove in future
        self.lang_list = []
        self.language = "EN_us"  # default language
        self.dictionary = {}  # language dictionary
        self.path = path.dirname(__file__)
        self.directory = path.join(self.path, directory)

        self.ignore_file_error = ignore_file_error
        self.ignore_key_error = ignore_key_error
        self.ignore_dict_error = ignore_dict_error

        self.get_languages()  # initialise available languages
        self.set_language(self.language)

    def get_languages(self):
        files = None
        try:
            files = listdir(self.directory)
        except FileNotFoundError:
            self.dl.log(f"Fatal error! Directory {self.directory} does not exist")
            exit(3)
        self.lang_list = []
        for Lang in files:
            if match('^[A-Z]{2}_[a-z]{2}$', str(Lang)) is not None:  # add only files in name format 'XX_yy'
                self.lang_list.append(Lang)
        return self.lang_list

    def set_language(self, lang):
        if len(self.lang_list):
            if lang not in self.lang_list:
                self.dl.log(f"Warning! {lang} language not found.")
            self.language = lang
        else:
            self.dl.log(f"Error! Languages not indexed or not present in directory!")
            return None
        try:
            with open(path.join(self.directory, self.language), "r", encoding="utf-8") as lang_data:
                self.dictionary = {}
                for line in lang_data:
                    if not line.startswith(".."):  # double-dotted lines are not interpreted comment lines
                        split_line = line.strip().split("#", 1)  # separate parameters from values
                        # and remove escaping
                        self.dictionary[split_line[0]] = split_line[1]  # enter values by keys into dictionary
                lang_data.close()
        except FileNotFoundError:
            self.dl.log(f"Fatal error! File not found!")
            if not self.ignore_file_error:
                exit(3)
            self.dl.log(f"Exit disabled by ignore_file_error flag.")

    def get_text(self, dict_key, *args):
        text = None
        try:
            text = str(self.dictionary[dict_key])  # get text value based on key
        except KeyError:
            if len(self.dictionary):
                self.dl.log(f"Error! {dict_key} key not found in {self.language} language file.")
                if self.ignore_key_error:
                    self.dl.log(f"Error disabled by ignore_key_error flag.")
                    return dict_key
            else:
                self.dl.log(f"Fatal error! Language: {self.language} not loaded!")
                if self.ignore_dict_error:
                    self.dl.log(f"Exit disabled by ignore_dict_error flag.")
                    return dict_key
            exit(3)
        try:
            text = text.format(*args)   # try to format text with arguments, if any specified
        except IndexError:
            pass
        return text


if __name__ == "__main__":
    print("Fatal error! This file could not be ran standalone")
    exit(3)

# example usage
# l = LangSupport()
# print(l.get_languages())
# print(l.dictionary)
# print(l.get_text("siminfo2", "Alfa 0.0"))
# l.set_language("PL_pl")
# print(l.get_text("siminfo2", "Alfa 0.0"))
