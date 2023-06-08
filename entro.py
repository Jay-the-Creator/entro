"""
entro.py
6/8/23

a text-based adventure game, terminal-based
beginner project
reference files in other files, python used
in order to progress the story

created by slugcat
used for beginner/intermediate python
developers to learn more about python
"""

#IMPORTS
import random #will be necessary later
import os #useful for save data
import json #char saving
import sys #exit file

#CONSTS
PATH=str(os.getcwd())

#VARS
menu="default"
char={}

#FUNCTIONS
def create_name(raw: str):
    #clean it up a little
    char_name = ''.join(char for char in raw if char.isalpha()).title()
    if char_name == "":
        #it's empty, we gotta fix that!
        for i in range(random.randint(3, 8)):
            char_name += random.choice("abcdefghijklmnopqrstuvwxyz")
        char_name = char_name.title()
    return char_name

def create_char(ranges: list | None, name: str | None):
    """
    expected ranges:
    
    0: hp/max_hp
    1: atk
    2: def
    3: mana
    """

    if ranges is None:
        hp = random.randint(10,100)
        atk = random.randint(1, 10)
        dfn = random.randint(1, 10) #* def is a keyword!
        mp = random.randint(25, 75)
    else:
        hp = ranges[0]
        atk = ranges[1]
        dfn = ranges[2]
        mp = ranges[3]

    return {"name": name, "hp": hp, "max_hp": hp, "atk": atk, "def": dfn, "mana": mp, "cur_file": "beginning.entro", "party": []}

def save_check(boot: bool):
    if (os.path.isfile(PATH+"\\save\\save1.entsv") is False) or (boot is False):
    #no save data! create new character, save
        while True:
            char_name = input("What is your name?\n>")
            try:
                char_name = create_name(char_name)
                c = input("Your name is %s. Is that okay?\n>" %char_name)
                if c in "yso":
                    break
            except:
                continue
        with open(PATH+"\\save\\save1.entsv", "w") as f:
            char = create_char(None, char_name)
            f.write(json.dumps(char))
            return char
        
    #save data found! let's check if it's good
    try:
        data = json.loads(open(PATH+"\\save\\save1.entsv", "r").read())
        if boot is True:
            c = input("This save has a character named %s. Is this your character?\n>" %data["name"])
            if c in "yso":
                return data
            else:
                return "notchar"
        
    except:
        print("[!!] - Save data failure!")
        #no good, default to making a new save
        while True:
            char_name = input("What is your name?\n>")
            try:
                char_name = create_name(char_name)
                c = input("Your name is %s. Is that okay?\n>" %char_name)
                if c in "yso":
                    break
            except:
                continue
        with open(PATH+"\\save\\save1.entsv", "w") as f:
            char = create_char(None, char_name)
            f.write(json.dumps(char))
            return char

def entro_file_format(raw_str: str):
    global char
    return raw_str.replace("<PLAYER>", char["name"]).replace("\\n", "\n")

def load_entro_file(filename: str):
    #automatically assume that filename is in /data/
    if os.path.isfile(PATH+"\\data\\%s" %filename) is False:
        print("[!*!] - ENTRO FILE %s DOES NOT EXIST IN \\data\\!" %filename)
        sys.exit()
    else:
        entro_file = open(PATH+"\\data\\%s" %filename, "r").read()
        entro_file = entro_file.splitlines()
        #entro files should always start with a q-, assume that to be the first line
        quote = entro_file[0]
        if quote.startswith("q-"):
            quote = quote.replace("q-", "")
            print(entro_file_format(quote))
        else:
            print("[!] - Entro file %s does not start with 'q-' keyword!" %filename)
            #search for q- keyword!!
            for line in entro_file:
                if line.startswith("q-"):
                    print(entro_file_format(line.replace("q-", "")))
    
    while True:
        choices = []
        returns = []
        for line in entro_file:
            if line.startswith("c-"):
                choices.append(line.replace("c-", ""))
            if line.startswith("r-"):
                returns.append(line.replace("r-", ""))
        keys = "asdfghjkl;zxcvbnm"
        choice_string = ""
        for ind, choice in enumerate(choices):
            choice_string += "%s: %s\n" %(keys[ind], choice)
        c = input(choice_string+">")
        if len(c) <= 0: #failsafe for empty string
            continue
        if c[0].lower() in keys:
            ind = keys.index(c[0].lower())
            if ind>len(choices)-1:
                continue
            char["cur_file"] = returns[ind]
            return

#get save data, if available
char = save_check(True)
if type(char) is str:
    sys.exit() #not us! exit
load_entro_file(char["cur_file"])