import bs4
import requests
import random
import re
import os


class web_manager():
    def __init__(self):
        # 初期化をする
        self.urls = []

        # ダウンロードサイト(トップ)のURL
        self.downloadSiteUrl = Downloader("https://www.minecraft.net/en-us/download/server/bedrock")

        # ダウンロードバージョンの設定
        self.downloadOsVersionList = [
            "win",
            "linux",
            "win-preview",
            "linux-preview"
        ]
        self.downloadOsVersion = 0

        # 一時ファイルの設定
        self.downloadFileName = "server_temp.zip"
        self.temporaryDownloadPath = "./temp/" + self.downloadFileName

        return


    def setDownloadOsVersion(self, osVersion: int):
        # ダウンロードするOSのバージョンを設定
        # 0: windows Release
        # 1: Linux Release
        # 2: Windows Preview
        # 3: Linux Preview

        if osVersion < 0 or osVersion > 3:
            raise ValueError("Invalid osVersion")

        self.downloadOsVersion = osVersion
        return


    def getDownloadOsVersion(self):
        # ダウンロードするOSのバージョンを取得
        # 引数: なし
        # 返り値: [osVersion, osVersionName]
        return [self.downloadOsVersion, self.downloadOsVersionList[self.downloadOsVersion]]


    def getLatestUrl(self):
        # 最新のURLを取得
        # 引数: なし
        # 返り値: URLのリスト

        self.downloadSiteUrl.download()

        content = bs4.BeautifulSoup(self.downloadSiteUrl.getContent(), "html.parser")
        a_tags = content.select("a[href$='.zip']")
        urls = [re.findall('(https.*.zip)', str(a_tag))[0] for a_tag in a_tags]
        urls = [Downloader(url) for url in urls]
        self.urls = urls

        return urls


    def downloadServer(self):
        # サーバーをダウンロード
        # 引数: なし
        # 返り値: なし

        for url in self.urls:
            if url.getVersion()[0] == self.downloadOsVersionList[self.downloadOsVersion]:
                url.download()
                content = url.getContent()
                break
        else:
            raise ValueError("No such version")

        w = Writer(self.temporaryDownloadPath)
        w.write(content)

        return



class Writer():
    def __init__(self, path: str):
        # 初期化をする
        self.path = path
        return


    def __str__(self):
        # ファイルパスを返す
        return self.path


    def isExist(self):
        # ファイルが存在するかどうかを返す
        return os.path.exists(self.path)


    def write(self, content: bytes):
        print(f"writing to file : {self.path}")
        with open(self.path, "wb") as f:
            f.write(content)
        return



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


    def getVersion(self):
        # URLからバージョンを取得
        # 引数: なし
        # 返り値: OSバージョン，ゲームバージョン
        osVersion = re.findall('bin-(.*)/', self.url)[0]
        gameVersion = re.findall('server-(.*).zip', self.url)[0]
        return osVersion, gameVersion


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
            response = requests.get(self.url, headers = self.headers, timeout = 10)
            if response.status_code == 200:
                break
        else:
            raise RuntimeError("Failed to get the latest version! Please try again later.")

        self.content = response.content
        print(f"statusCode : <{response.status_code}>")

        return response.status_code



def pprint(lis):
    for i in lis:
        print(i)
    return

if __name__ == "__main__":
    web = web_manager()
    web.setDownloadOsVersion(0)
    print(web.getDownloadOsVersion())
    urls = web.getLatestUrl()
    pprint(urls)
    for i in urls:
        print(i.getVersion())
    pass

