# Get the new version of Minecraft Server Bedrock Edition and update it.

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os
import re
import sys
import random
import shutil
import datetime
import platform

# ---------------------------------------------------------------

# path (todo: auto detect)
now_server_path = 'now_server'

# About is_replace
# True: Replace the existing server
# False: Place a new server
is_replace = False

# ---------------------------------------------------------------

# Get mode from argument
# 0 : Check whether the latest version is available
#     returns 0 if the latest version is already installed, 1 if not installed and -1 if an error occurs
# 1 : Update the server to the latest version (default)
mode = 1
if len(sys.argv) > 1:
    mode = int(sys.argv[1])
else:
    print("No version argument provided. Using default version 1.")


def get_time():
    return datetime.datetime.now().strftime('%Y%m%d%H%M')

# Variables
dl_filename = 'server_temp.zip'
old_server_path = f'old_server_{get_time()}'
backup_path = 'upd_backup'
dl_path = backup_path + '/' + dl_filename
max_retry = 5

# Consts
st = '<a href="https://www.minecraft.net/bedrockdedicatedserver/'
fn = '.zip"'
dl_page_url = "https://www.minecraft.net/en-us/download/server/bedrock"


# User-Agent
RandNum = random.randint(1000, 9999)
ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.33 (KHTML, like Gecko) Chrome/90.0.{RandNum}.212 Safari/537.33"
headers = {'User-Agent': ua}


def get_serverZip_url(ver) -> str:
    global max_retry, st, fn, dl_page_url, headers
    for try_count in range(max_retry):
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument(f'user-agent={ua}')  # uaは既存のUser-Agent文字列
            driver = webdriver.Chrome(options=options)
            driver.get(dl_page_url)
            content = driver.page_source
            driver.quit()
        except Exception as e:
            print(f"Failed to get page content! (retry {try_count+1}/{max_retry})", e)
            continue
    dl_pattern = re.escape(st + ver + "/") + r'(.*?)' + re.escape(fn)
    serverZip_urls = []
    for m in re.findall(dl_pattern, content):
        url = st + ver + "/" + m + fn
        if url.startswith('<a href="'):
            url = url[len('<a href="'):]
        if url.endswith('"'):
            url = url[:-1]
        serverZip_urls.append(url)
    print("Detected URLs: ", serverZip_urls)
    if len(serverZip_urls) == 0:
        raise RuntimeError("Failed to get the latest version! Please try again later.")
    return serverZip_urls[0]


def download_serverZip(url) -> None:
    global dl_path, max_retry
    for i in range(max_retry):
        response = requests.get(url, headers=headers, timeout = 10)
        if response.status_code == 200:
            break
        print(f"Failed to download! (retry {i+1}/{max_retry})")
    else:
        raise RuntimeError("Failed to download! Please try again later.")
    print("response: ", response)
    urlData = response.content

    with open(dl_path, mode='wb') as f: # write binary
        f.write(urlData)


def backup_mcdata():
    # backup minecraft server data
    # Folders: worlds
    # Files: allowlist.json, server.properties, permissions.json
    global old_server_path, backup_path

    folders = ['worlds']
    for folder in folders:
        try:
            shutil.copytree(f'{old_server_path}/{folder}', f'{backup_path}/{folder}')
            print(f"Folder copied: {folder}")
        except FileNotFoundError as e:
            print(f"Cannot copy: {folder} (Maybe it's empty) :", e)
    
    files = ['allowlist.json', 'server.properties', 'permissions.json']
    for file in files:
        try:
            shutil.copy(f'{old_server_path}/{file}', f'{backup_path}/{file}')
            print(f"File copied: {file}")
        except FileNotFoundError as e:
            print(f"Cannot copy: {file} :", e)
    
    print("Backup Completed!")


def restore_mcdata():
    global backup_path, now_server_path
    try:
        shutil.copytree(f'{backup_path}/worlds', f'{now_server_path}/worlds')
    except FileNotFoundError as e:
        print("Cannot copy Worlds data! (Maybe it's empty) :", e)
    shutil.copy(f'{backup_path}/allowlist.json', f'{now_server_path}/allowlist.json')
    shutil.copy(f'{backup_path}/server.properties', f'{now_server_path}/server.properties')


def get_local_version():
    # function to get version of local server
    global now_server_path

    files_list = os.listdir(f"{now_server_path}/behavior_packs")
    maxi = [0, 0, 0]

    # search maximum version in behavior_packs
    for i in files_list:
        if i[:8] != "vanilla_":
            continue
        version = i[8:].split(".")
        for serch_index, version_part in enumerate(version):
            if int(version_part) < maxi[serch_index]:
                break
            if int(version_part) > maxi[serch_index]:
                # バージョンコピー
                for k in range(len(version)):
                    maxi[k] = int(version[k])
                break
            continue # 同じだった場合は次の桁へ

    out = ".".join([str(i) for i in maxi])
    return out


def get_os():
    os_name = platform.system()
    if os_name == "Windows":
        return "bin-win"
    elif os_name == "Linux":
        return "bin-linux"
    else:
        raise RuntimeError("Unsupported OS! Only Windows and Linux are supported.")


def is_update_available(url):
    global now_server_path
    local_version = get_local_version()
    latest_version = ".".join(url.split("/")[-1][15:].replace(".zip", "").split(".")[0:3])
    print("*\nlocal_version: ", local_version)
    print("latest_version: ", latest_version)
    return local_version != latest_version


if __name__ == '__main__' and mode == 0:
    ver = get_os()
    if not os.path.exists(now_server_path):
        print("-1")
        exit()
    url = get_serverZip_url(ver)
    print("1" if is_update_available(url) else "0")


if __name__ == '__main__' and mode == 1:
    if is_replace:
        if not os.path.exists(now_server_path):
            print("Server not found! Please put the server in the same directory as this file.")
            print("If you want a new server, change variable 'is_place' to 'False'.")
            print("If you want to replace without any name changes, modify variable 'now_server_path' to appropriate value")
            exit()
        else:
            print("Server directory found!")

    ver = get_os()
    print(f"Platform: {ver}")

    url = get_serverZip_url(ver)
    print("URL detected!\n" + url)

    if is_replace:
        if not is_update_available(url):
            print("Looks like you're already using the latest version! \nThere's no need to update!")
            exit()
        else:
            print("Update is available!")

    if not os.path.exists(backup_path):
        os.mkdir(backup_path)
        print("backup (temporary) directory created!")
    else:
        print("backup (temporary) directory found!")

    print("*\nDownloading...")
    try:
        download_serverZip(url)
    except RuntimeError as e:
        print("Download failed! Please try again later.", e)
        exit()
    print("Downloaded!")

    if is_replace:
        os.rename(now_server_path, old_server_path)
        print(f"Old Server Renamed! {now_server_path} -> {old_server_path}")

        backup_mcdata()
        print("Game Data Backuped!")

    print("Unzipping downloaded file to directory...")
    shutil.unpack_archive(dl_path, now_server_path)
    print("Unzipped!")

    if is_replace:
        restore_mcdata()
        print("Game Data Copied! (worlds & allowlist.json & server.properties)")

        shutil.rmtree(backup_path)
        print("Removed temporary file!")

    print("Process Completed!")
