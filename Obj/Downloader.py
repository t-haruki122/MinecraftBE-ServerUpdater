import requests
import random
import re

class Downloader():
    def __init__(self, url: str):
        # 初期化をする関数
        # 引数: url (str)
        # 返り値: なし
        self.content = None
        self.downloadAttemptTimes = 5

        self.setUrl(url)

        # User-Agentの設定
        self.RandNum = random.randint(1000, 9999)
        self.ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.33 (KHTML, like Gecko) Chrome/90.0.{self.RandNum}.212 Safari/537.33"
        self.headers = {'User-Agent': self.ua}

        return


    def __str__(self):
        return self.url


    def setUrl(self, url: str):
        if url == "":
            raise ValueError("Invalid url")
        self.url = url
        return


    def getContent(self):
        return self.content


    def download(self):
        # URLからダウンロード
        # 引数: なし
        # 返り値: ステータスコード (200:成功)

        print(f"downloading : {self.__str__()}")
        for i in range(self.downloadAttemptTimes):
            print(f"Attempt: {i+1} / {self.downloadAttemptTimes}")
            try:
                response = requests.get(self.url, headers = self.headers, timeout = 10)
                print(f"statusCode : <{response.status_code}>")
                if response.status_code == 200:
                    print("Downloaded successfully.")
                    break
                else:
                    print(f"Failed to download. Status code: {response.status_code}")
            except KeyboardInterrupt as e:
                print("KEYBOARD INTERRUPT")
                exit()
            except Exception as e:
                print("SOMETHING WENT WRONG")
                print(e)

        else:
            raise RuntimeError("Failed to download! Please try again later.")

        self.content = response.content
        return response.status_code



class ServerDownloader(Downloader):
    def getVersion(self):
        # URLからバージョンを取得
        # 引数: なし
        # 返り値: OSバージョン，ゲームバージョン
        osVersion = re.findall('bin-(.*)/', self.url)[0]
        gameVersion = re.findall('server-(.*).zip', self.url)[0]
        return osVersion, gameVersion