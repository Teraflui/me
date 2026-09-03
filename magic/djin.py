import subprocess as s
import csv
import random

bros = [] #list for all characters
with open("data.csv", "r", encoding="utf-8") as f: #reading data.csv with all data
    readr = csv.DictReader(f) #save all data into the readr container
    for i in readr:
        bros.append(i)#write one person fo ieteration into the bros list

questions = {
    "is_real": "Is you character real?: ",
    "is_male": "Is your characters sex male: ",
    "isgreaterthan10000fw": "Have your character greater than 10000 followers?: ",
    "worked": "Is your character worked?: ",
    "ispornstar": "Is pornstar?: ",
    "rich": "Is rich?: ",
    "ismodel": "Is your character model?: ",
    "longhair": "Have your character long hair?: ",
    "is_robot": "Is your character robot?: ",
    "tineager": "Is your chaacter teneager?: ",
    "iscartoon": "Is your character from cartoon?: ",
    "smart": "Is your character very smart?: ",
    "veryold": "Is your character very old?: ",
    "isgood": "Is your character good?: "
} #all quesitons

def filter(broski, atribut, answer): #character filter
    if answer == "yes":
        return [c for c in broski if c[atribut] == "1"]
    else:
        return [c for c in broski if c[atribut] == "0"]

def bques(broski, ques):
    best_atrib = ques[0] #first qiestion is always IS YOUR CHARACTER REAL?
    best_diff = 999
    for attributs in ques:
        yes = 0
        for c in broski:
            if c[attributs] == "1":
                yes += 1
            no = len(broski) - yes
            diff = abs(yes - no)
            if diff < best_diff:
                best_diff = diff
                best_atrib = attributs
    return best_atrib


def program():
    global bros
    print("Welcome")
    qu = list(questions.keys()) #qu saved keys from questions dict
    while len(bros) > 1: #loop dauert bis zu 1 person bleibt
        if len(qu) == 0: #if questions schon fertig sind
            break #break from loop
        q = bques(bros, qu) #anderfalls calling we bques fuction die denkt welche question wird better
        eq = questions[q] #eq get humanize question text per key q
        print(f"{eq}", end="")
        ip = str(input()) #must be yes or no
        bros = filter(bros, q, ip)
        qu.remove(q) #delet question
    if len(bros) == 1: #if one person geblieben ist
        win = bros[0] #get the winner line
        path = f"photos/{win["photo"]}"#getting photo
        s.run(["xdg-open", path])#show photo
        print(f"This is: {win["name"]}!")#show name
        return#end
    else:
        print("Not found:(")#anderfalls enden wir das programm and write the Not Found error
        return


program()#calling the programm