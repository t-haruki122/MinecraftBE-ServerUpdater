# Get the new version of Minecraft Server Bedrock Edition and update it.

import requests
import random
import shutil
import os
import datetime

# ---------------------------------------------------------------

"""
Select the version of the server to download (ver)

[Release]
0 : Windows Release
1 : Linux Release

[Preview]
2 : Windows Preview
3 : Linux Preview
"""

ver = 1

# path
now_server_path = 'now_server'

# is replace old server
is_replace = True

# ---------------------------------------------------------------

def get_time():
    return datetime.datetime.now().strftime('%Y%m%d%H%M')

dl_filename = 'server_temp.zip'
old_server_path = f'old_server_{get_time()}'
backup_path = 'upd_backup'
dl_path = backup_path + '/' + dl_filename

RandNum = random.randint(1000, 9999)
ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.33 (KHTML, like Gecko) Chrome/90.0.{RandNum}.212 Safari/537.33"
headers = {'User-Agent': ua}

def get_latest_url():
    url = "https://www.minecraft.net/en-us/download/server/bedrock"
    response = requests.get(url, headers=headers, timeout = 10)
    print("response: ", response)
    content = str(response.text.encode('utf-8'))
    urls = serch_url(content, '<a href="https://minecraft.azureedge.net/', '.zip"')
    out = select_version(urls)
    return out

def serch_url(text, st, fn):
    out, ans = [], ''

    writing = False
    for k, i in enumerate(text):
        if i == st[0]: # start
            if text[k:k+len(st)] == st:
                writing = True
        if i == fn[0]: # finish
            if text[k:k+len(fn)] == fn:
                writing = False
                ans = (ans + fn).replace('<a href="', '').replace('"', '')
                out.append(ans)
                ans = ''
        if writing: # writing
            ans += i
    return out

def select_version(urls):
    global ver
    return urls[ver]

def download_file(url):
    global dl_path
    urlData = requests.get(url).content

    with open(dl_path, mode='wb') as f: # write binary
        f.write(urlData)

def unzip_file():
    global dl_path
    shutil.unpack_archive(dl_path, now_server_path)

def rename_old_file():
    os.rename(now_server_path, old_server_path)

def backup_file():
    # backup worlds & allowlist.json & server.properties
    global old_server_path, backup_path
    try:
        shutil.copytree(f'{old_server_path}/worlds', f'{backup_path}/worlds')
    except:
        print("Cannot copy Worlds data! (Maybe it's empty)")
    shutil.copy(f'{old_server_path}/allowlist.json', f'{backup_path}/allowlist.json')
    shutil.copy(f'{old_server_path}/server.properties', f'{backup_path}/server.properties')

def copy_new_file():
    global backup_path, now_server_path
    try:
        shutil.copytree(f'{backup_path}/worlds', f'{now_server_path}/worlds')
    except:
        print("Cannot copy Worlds data! (Maybe it's empty)")
    shutil.copy(f'{backup_path}/allowlist.json', f'{now_server_path}/allowlist.json')
    shutil.copy(f'{backup_path}/server.properties', f'{now_server_path}/server.properties')

def is_now_server_exist(now_server_path):
    return os.path.exists(now_server_path)

def check_now_version():
    # get version of now server
    global now_server_path

    files_list = os.listdir(f"{now_server_path}/behavior_packs")
    maxi = [0, 0, 0]
    for i in files_list:
        if i[:8] == "vanilla_":
            ver = i[8:].split(".")
            for j in range(len(ver)):
                if int(ver[j]) < maxi[j]:
                    break
                if int(ver[j]) > maxi[j]:
                    for k in range(len(ver)):
                        maxi[k] = int(ver[k])
                    break

    out = ".".join([str(i) for i in maxi])
    return out

def is_update_available(url):
    global now_server_path
    now_version = check_now_version()
    latest_version = ".".join(url.split("/")[-1][15:].replace(".zip", "").split(".")[0:3])
    print("*\nnow_version: ", now_version)
    print("latest_version: ", latest_version)
    return now_version != latest_version

test = True
if __name__ == '__main__' and test:
    if is_replace:
        if not is_now_server_exist(now_server_path):
            print("Server not found! Please put the server in the same directory as this file.")
            print("If you want a new server, please change 'is_place' to 'False'.")
            exit()
        else:
            print("Server directory found!")

    url = get_latest_url()
    print("URL detected!\n" + url)

    if is_replace:
        if not is_update_available(url):
            print("Looks like you're already using the latest version! \nThere's no need to update!")
            exit()
        else:
            print("Update is available!")

    print("*\nDownloading...")
    try:
        download_file(url)
    except:
        print("Download failed! Please try again later.")
        exit()
    print("Downloaded!")

    if not os.path.exists(backup_path):
        os.mkdir(backup_path)
        print("backup (temporary) directory created!")
    else:
        print("backup (temporary) directory found!")

    if is_replace:
        rename_old_file()
        print(f"Old Server Renamed! {now_server_path} -> {old_server_path}")

        backup_file()
        print("Game Data Backuped!")

    print("Unzipping downloaded file to directory...")
    unzip_file()
    print("Unzipped!")

    if is_replace:
        copy_new_file()
        print("Game Data Copied! (worlds & allowlist.json & server.properties)")

        shutil.rmtree(backup_path)
        print("Removed temporary file!")

    print("Process Completed!")