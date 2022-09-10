#import telegram.client
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, ChannelParticipantsSearch
from telethon.errors.rpcerrorlist import *
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest
import sys
import csv
import traceback
import time
import asyncio

import random


api_id_r=12369142
api_hash_r = '64830a510c2b86f53138f7174f6f4ede'

api_id_a1=15223906
api_hash_a1 = 'df1d9fc423ad02bf38c64c4951a4409e'

api_id_a2=12872821
api_hash_a2 = '8541c0a996efaf641cffffb6eaa6e154'


api_id = 12899094
api_hash = "335e73259ab7fe48c3d12e4139f6dfa0"

api_id45 = 16334723
api_hash45 = '33a1fd4e1fc89fc5e704d785fcd32e23'

api_id48 = 14940426
api_hash48 = 'a5e6221082b82f157025f48cc78692e2'

api_id47=19248905
api_hash47='876bddfdd4ee1d19e04f93fb8a6f781f'

api_id15 = 10686940
api_hash15 = '2f31a45c0ccb15049223ba40901dbe0c'


def scrap_members(client,username,filename):
    print('Fetching Members from @'+username)
    all_participants = []
    target_group = client.get_entity(username)
    try:
     all_participants = client.get_participants(target_group, aggressive=False)
     print('Saving In file ' + filename)
     with open(filename, "w", encoding='UTF-8') as f:
         writer = csv.writer(f, delimiter=",", lineterminator="\n")
         writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
         for user in all_participants:
             if user.username:
                 username = user.username
             else:
                 username = ""
             if user.first_name:
                 first_name = user.first_name
             else:
                 first_name = ""
             if user.last_name:
                 last_name = user.last_name
             else:
                 last_name = ""
             name = (first_name + ' ' + last_name).strip()
             writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
     print('Members scraped successfully.')
    except Exception as e:
        print(e)


def scrap_members_hack(client,username,filename):
    print('Fetching Members from @'+username)
    all_participants = []
    f=open('test.txt','w')
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
    f.close()

    target_group = client.get_entity(username)
    target_group_i = client.get_input_entity(username)
    try:

        limit = 10000
        total = 0
        all_participants = []
        previous_size=0
        ch='abcdefghijklmnopqrstuvwxyz'
        i=0
        participants=[]
        while(i<26):
          participants=[]
          all_participants=[]
          offset = 0
          print(str(i + 1) + ' of 26')
          while True:
            participants = client(GetParticipantsRequest(
                target_group_i, ChannelParticipantsSearch(ch[i]+'*'), offset, limit,
                hash=0
            ))

            if not participants.users:
                break
            if(i>=26):
                break
            all_participants.extend(participants.users)
            offset += len(participants.users)

          total += len(all_participants)
          print(str(total-previous_size) + ' users extracted from ' + ch[i] + '. Total: ' + str(
              total))
          previous_size = total
          t = random.randint(10, 20)
          print('Saving In file ' + filename)
          with open(filename, "a", encoding='UTF-8') as f:
              writer = csv.writer(f, delimiter=",", lineterminator="\n")
              #writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
              for user in all_participants:
                  if user.username:
                      username = user.username
                  else:
                      username = ""
                  if user.first_name:
                      first_name = user.first_name
                  else:
                      first_name = ""
                  if user.last_name:
                      last_name = user.last_name
                  else:
                      last_name = ""
                  name = (first_name + ' ' + last_name).strip()
                  writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
          print('Waiting for ' + str(t) + ' seconds...')
          i += 1

          time.sleep(t)




        print('Members scraped successfully.')
    except Exception as e:
        print(e)



def user_is_already_added(user,users_already):
    result=0
    if(user in users_already):
        result=1
    if(result==0):
        i=0
        while(i<len(users_already)):
            if(user['id']==users_already[i]['id']):
                result=1
                break
            i+=1

    return result

def user_has_failed_already(user,users_failed):
    result=0
    i = 0
    while (i < len(users_failed)):
        if (user['id'] == users_failed[i]):
            result = 1
            break
        i += 1

    return result

def add_to_group(client,user,group):
    res=0
    user_to_add = client.get_input_entity(user)
    target_group_entity = client.get_input_entity(group)
    print('Adding '+user+' to '+group+' ....')
    try:
     client(InviteToChannelRequest(target_group_entity, [user_to_add]))
     print(user + ' added to ' + group + ' successfully')
     res = 1
    except Exception as e:
        print(e)

    return res

def add_bulk_users_to_group(client,users_filename,group,members_already='members_already.csv',mode=1,min_delay=34,max_delay=43,start=1,scrap=True,amount=100):
    failed_users = []
    lines = open('failed_users.txt','r').readlines()
    for l in lines:
        s=l.removesuffix('\\n')
        failed_users.append(s)

    users = []
    with open(users_filename, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)
    if(scrap==True):
     scrap_members(client,group,members_already)

    users_already = []
    with open(members_already, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users_already.append(user)
    n=0
    w=1
    if(mode==1):
        print('Using username')
    else:
        print('Using id and hash')
    ggg = open('failed_users.txt','a')
    target_group_entity = client.get_input_entity(group)
    for user in users:
      n += 1
      if(n>=start):
        if(w>=random.randint(30,35) or w>amount):
            ma = open('last_index.txt', 'w')
            ma.write(str(n))
            ma.close()
            break
        try:
            print(str(n) + '. ' + str(w) + ". Adding {}".format(user['id']))
            if mode == 1:
                if user['username'] == "":
                    print('user doesnt have username. Skipping.')
                    continue
                #print(len(users_already))
                if (user_is_already_added(user, users_already)):
                    print('User already exists.Skipping.')
                    continue
                if (user_has_failed_already(user,failed_users)):
                    print('User already failed.Skipping.')
                    continue
                user_to_add = client.get_input_entity(user['username'])


            elif mode == 2:
                if (user_is_already_added(user,users_already)):
                    print('User already exists.Skipping.')
                    continue
                if (user_has_failed_already(user,failed_users)):
                    print('User already exists.Skipping.')
                    continue
                user_to_add = InputPeerUser(user['id'], user['access_hash'])


            else:
                sys.exit("Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))

            ma = open('last_index.txt', 'w')
            ma.write(str(n))
            ma.close()
            #writer = csv.writer(ma, delimiter=",", lineterminator="\n")
            #writer.writerow([user.username, user.id, user.access_hash, user.name, group.title, group.id])
            #ma.close()
            w += 1
            i = random.randrange(min_delay, max_delay)
            print("Waiting for " + str(i) + ' seconds.')
            time.sleep(i)
        except Exception as e:
            # traceback.print_exc()

            if (str(e).find('wait') != -1 or str(e).find('Too many requests') != -1 or str(e).find('flood') != -1):
                print(e)
                ma = open('last_index.txt', 'w')
                ma.write(str(n))
                ma.close()
                break
            else:
             print(e)

             ggg.write(str(user['id'])+'\n')
             continue

    ggg.close()
def authorize_client(client,f=False):
    client.connect()
    if not client.is_user_authorized():
        print('Not authorized')
        phone = input('Enter phone number: ')
        if(f==False):
         client.send_code_request(phone)
        else:
            client.send_code_request(phone,force_sms=True)
        client.sign_in(phone, input('Enter the code: '))
    else:
        print('Authorized')

def get_id_from_dialog(dl):
    dl=str(dl)
    i=dl.find('user_id')

    s=dl[i:i+20]

    s=s.removeprefix('user_id')
    j=0
    s2=''
    while(j<len(s)):
        if(s[j].isnumeric()):
            s2+=s[j]
        j+=1


    return s2


def get_telegram_dialog(dialogs):
    i=0
    for d in dialogs:
        #print(get_id_from_dialog(d))
        if(get_id_from_dialog(d)=='777000'):
            break
        i+=1
    return dialogs[i]

def get_last_message_from_telegram(dialogs):
    dialog = get_telegram_dialog(dialogs)
    s=str(dialog)
    i=s.find('message="')
    s=s[i+9:]
    j=0
    s2=''
    while(j<len(s)):
        if(s[j]=='"'):
          break
        s2+=s[j]
        j+=1
    return s2

#session_name_+251922372802



st = int(open('last_index.txt','r').read())
client = TelegramClient('session_name_+251922372802', api_id_r,api_hash_r)

authorize_client(client)

add_bulk_users_to_group(client,'free_cross_promotions+251922372802.csv','megaadvertisement',start=st,mode=2,scrap=True)

st = int(open('last_index.txt','r').read())
client = TelegramClient('session_name_15', api_id15,api_hash15)

authorize_client(client)

add_bulk_users_to_group(client,'free_cross_promotions15.csv','megaadvertisement',start=st,mode=2,scrap=True)

st = int(open('last_index.txt','r').read())
client = TelegramClient('session_name_45', api_id45,api_hash45)

authorize_client(client)

add_bulk_users_to_group(client,'free_cross_promotions45.csv','megaadvertisement',start=st,mode=2,scrap=True)







#dialogs = client.get_dialogs()

#print(get_last_message_from_telegram(dialogs))

#scrap_members(client,'megaadvertisement','members_already.csv')
#scrap_members(client,'free_cross_promotions','free_cross_promotions19.csv')
#scrap_members_hack(client,'zionhotsale','test.txt')
#target = client.get_input_entity('zionhotsale')


#add_to_group(client,'EIADGN','megaadvertisement')
#11




