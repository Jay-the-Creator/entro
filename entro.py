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

#get save data, if available
if os.path.isfile(PATH+"\\save1.entsv") is False:
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
    with open(PATH+"\\save1.entsv", "w") as f:
        f.write(char_name)