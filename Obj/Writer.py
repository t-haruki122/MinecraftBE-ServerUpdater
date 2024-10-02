import os

class Writer():
    def __init__(self, path: str):
        # 初期化をする
        self.setPath(path)
        return


    def __str__(self):
        # ファイルパスを文字列で返す
        return self.path


    def getPathList(self):
        # ファイルパスをリストで返す
        return self.pathList


    def getDirPath(self):
        # ディレクトリパスを文字列で返す
        return "/".join(self.pathList[:-1])


    def setPath(self, path: str):
        # ファイルパスを設定する
        if path == "":
            raise ValueError("Invalid path: it's empty")
        self.path = path
        self.pathList = path.split("/")
        return


    def isDirPathExist(self):
        # ディレクトリが存在しているか返す
        return os.path.exists(self.getDirPath())


    def isFilePathExist(self):
        # ファイルが存在するかどうかを返す
        return os.path.exists(self.path)


    def write(self, content: bytes):
        print(f"writing to file : {self.path}")
        with open(self.path, "wb") as f:
            f.write(content)
        return