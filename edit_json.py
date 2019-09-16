import json

def open_data():
    global data
    f = open('data.json', 'r')
    data = json.loads(f.read())
    f.close()

def close_data():
    global data
    f = open('data.json', 'w')
    f.write(json.dumps(data, sort_keys=True, indent=4))
    f.close()

def save_data():
    close_data()
    open_data()

#TODO migliora dialogo
#TODO controlla che la gente non metta: folder "folder_name"

properties = ['username'] #TODO
commands = {
    'help' : [0, 'display this help message'],
    'sources_list' : [0, 'list sources'],
    'folder_info' : [0, 'show the path of the folder where files are currently saved'],
    'source_info' : [1, 'show arg1 source\'s data'],
    'folder' : [1, 'set folder to arg1'],
    'username' : [2, 'set in source arg1 username arg2'],
    'add' : [1, 'add new source arg1'],
    'exit': [0, 'close the editor']
}

data = {}
open_data()
print('info... \ntype "help" to dislpay the commands')

print('DEBUG: '+str(data))

if 'folder' not in data:
    data['folder'] = ""
if 'sources' not in data:
    data['sources'] = {}

while True:

    print('>>', end=' ')
    user_input = input().strip().split(" ")


    if user_input[0] not in commands:
        print(user_input[0]+' is not a valid command')
    elif len(user_input) != commands[user_input[0]][0]+1:
        print(user_input[0]+' needs '+str(commands[user_input[0]][0])+' parameters')

    elif user_input[0] == 'help':
        for c in commands:
            print(c, end=' ')
            for i in range(commands[c][0]):
                print('arg'+str(i+1), end=' ')
            print('\t', end='')
            print(commands[c][1])

    elif user_input[0] == 'sources_list':
        if len(data['sources']):
            print(data['sources'].keys())
        else:
            print('no sources yet')

    elif user_input[0] == 'folder_info':
        if data['folder'] != "":
            print('your current folder is: '+data['folder'])
        else:
            print('folder not set yet')

    elif user_input[0] == 'source_info':
        if user_input[1] in data['sources']:
            print(data['sources'][user_input[1]])
        else:
            print(user_input[1]+' is not a valid source')

    elif user_input[0] == 'folder':
        data['folder'] = user_input[1]

    elif user_input[0] == 'username':
        if user_input[1] not in data['sources']:
            print(user_input[1]+' is not a valid source')
        else:
            data['sources'][user_input[1]]['username'] = user_input[2]

    elif user_input[0] == 'add':
        if user_input[1] in data['sources']:
            print('source '+user_input[1]+' already exists')
        else:
            data['sources'][user_input[1]] = {}
            for p in properties:
                print(p+':')
                data['sources'][user_input[1]][p] = input()

    elif user_input[0] == 'exit':
        exit(0)

    save_data()


#TODO
#   controlla siti
#   pagina web

#   nome_funzione (funzioni precedenti necessarie) [info da cercare su data.json]

#funzioni che serve fare:

#   _username [username]
#   max_page (_username) [link, javascript]
#   submissions_per_page (_username) [page_number, link, javascript]
#   solved_problems
#   submissions (max_page, submissions_per_page) []

#a questo punto ho tutte le submissions (id, tempo, problema) (l'id contiene il sito e il problem id)

#   submission_id (submissions) []

#   get_code (submission_id) [link, javascript]

#INSTALLATION
#   download https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-linux64.tar.gz to bin
#   tar -zxvf geckodriver-v0.25.0-linux64.tar.gz
#   pip3 install selenium

#WEBSITES

#codeforces

#codechef
#oj.uz
#sphere
#wcipeg
#acm.timus.ru
#onlinejudge.org
#judge.u-aizu.ac.jp
