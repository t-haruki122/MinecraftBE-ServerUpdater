import re

from Obj.Downloader import Downloader, ServerDownloader
from Obj.File import Writer


class WebManager():
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
        content = self.downloadSiteUrl.getContent().decode("utf-8")
        a_tags = re.findall("(https.*.zip)", str(content))
        urls = [re.findall("(https.*.zip)", str(a_tag))[0] for a_tag in a_tags]
        urls = [ServerDownloader(url) for url in urls]
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

