import subprocess as s
import csv

bros = []
with open("data.csv", "r", encoding="utf-8") as f:
    readr = csv.DictReader(f)
    for i in readr:
        bros.append(i)

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
}
def filter(broski, atribut, answer):
    if answer == "yes":
        return [c for c in broski if c[atribut] == "1"]
    else:
        return [c for c in broski if c[atribut] == "0"]

def bques(broski, ques):
    best_atrib = ques[0]
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


def program(  ):
    global bros
    print("Welcome")
    qu = list(questions.keys())
    while len(bros) > 1:
        q = bques(bros, qu)
        eq = questions[q]
        print(f"{eq}", end="")
        ip = str(input()) #must be yes or no
        bros = filter(bros, q, ip)
        qu.remove(q)
    if len(bros) == 1:
        win = bros[0]
        path = f"photos/{win["photo"]}"
        s.run(["xdg-open", path])
        print(f"This is: {win["name"]}!")
        return
    else:
        print("Not found:(")
        return


program()