# temp verifications objects
animals = ["cow", "dog", "cat", "mouse", "hamster", "rabbit", "fox", "bear", "koala", "tiger", "lion", "pig", "frog",
           "monkey", "chicken", "penguin", "bird", "duck", "eagle", "owl", "bat", "wolf", "horse", "hedgehog"]

vegetables = ["watermelon", "banana", "pear", "orange", "apple", "lemon", "grapes", "blueberries", "strawberry",
              "melon", "cherries", "peach", "mango", "pineapple", "coconut", "kiwi", "tomato", "avocado", "carrot",
              "garlic", "onion", "potato", "corn", "broccoli"]

verify_obj_count = 24  # counting from 1

verify_types = [animals, vegetables]
verify_types_str = ["animals", "vegetables"]

# commands help (non admin)
nonadmin_commands = {
    "help": "Prints bot commands and its description",
    "hello": "Greets user with \"Hello!\"",
    "ping": "Do I hear Ping-Pong? Lets check the connection latency",
    "whereami": "Prints guild/server name"
}

# commands help (admin)
admin_commands = {
    "DATA TYPES": " -> <integer> <bool><text><text_multi>",
    "set_verify_method": " <text> : Set user verification method to <text>\nAvailable methods: {}".format(
        ", ".join(verify_types_str)),
    "set_verify_depth": " <integer> : Set user verification method to <integer> depth\n<integer> must vary between <1, {}>".format(
        verify_obj_count),
    "set_verified_role": " <text> : Set <text> to role of verified user",
    "set_verify_new": " <bool> : <bool> 0 - new users won't be verified | 1 - new users will be verified",
    "verify_user": " <text> : Verifies user <text>",
    "verify_bulk": " <text_multi> : Verifies multiple users on given conditions in <text>\nexample: verify_bulk @everyone not @role0 and not @role1",
    "set_ghosting": " <bool> : <bool> 0 - non verified users ghosting disabled | 1 - enabled\n<integer> represents days to ghost user",
    "set_warning": " <bool> : <bool> 0 - non verified users warn before kick disabled | 1 - enabled\n<integer> represents days to warn user",
    "set_kick": " <bool> : <bool> 0 - non verified users kick disabled | 1 - enabled\n<integer> represents days to kick user",
}

# JSON data schemas
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
    "verify_depth": 5
}
