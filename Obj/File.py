import os
import shutil


class File():
    def __init__(self, path: str) -> None:
        # 初期化をする
        self.setPath(path)
        return


    def __str__(self) -> str:
        # ファイル名を文字列で返す
        return self.pathList[-1]


    def getPath(self) -> str:
        # ファイルパスを文字列で返す
        return self.path


    def getPathList(self) -> list[str]:
        # ファイルパスをリストで返す
        return self.pathList


    def getDirPath(self) -> str:
        # ファイルが存在するディレクトリのパスを文字列で返す
        return "/".join(self.getPathList()[:-1])


    def setPath(self, path: str) -> None:
        # ファイルパスを設定する
        if path == "":
            raise ValueError("Invalid path: it's empty")
        self.path = path
        self.pathList = path.split("/")
        return


    def isPathExist(self) -> bool:
        # ファイルが存在するかどうかを返す
        return os.path.exists(self.getPath())


    def remove(self) -> None:
        # ファイルを削除する
        if self.isPathExist():
            os.remove(self.getPath())
            print(f"File removed: {self.getPath()}")
        return



class Writer(File):
    def __init__(self, path: str) -> None:
        # 初期化をする
        super().__init__(path)
        return


    def writeBinary(self, content: bytes):
        # ファイルに書き込む
        print(f"writing to file : {self.path}")
        with open(self.path, "wb") as f:
            f.write(content)
        return



class Zip(File):
    def __init__(self, path: str) -> None:
        # 初期化をする
        super().__init__(path)


    def unzip(self, toPath: str) -> None:
        # ファイルを解凍する
        shutil.unpack_archive(self.path, toPath)
        return