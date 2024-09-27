import os

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