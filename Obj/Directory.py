import shutil
import os

from Obj.File import File


class Directory():
    def __init__(self, path) -> None:
        # 初期化をする
        self.setPath(path)
        self.dirPathList = []
        return


    def __str__(self) -> str:
        # ディレクトリ名を文字列で返す
        return self.getPathList()[-1]


    def getPath(self) -> str:
        # ディレクトリパスを文字列で返す
        return self.path


    def getPathList(self) -> list[str]:
        # ディレクトリパスをリストで返す
        return self.pathList


    def setPath(self, path: str) -> None:
        # ディレクトリパスを設定する
        if path == "":
            raise ValueError("Invalid path: it's empty")
        self.path = path
        self.pathList = path.split("/")
        self.reloadFileList()
        return


    def reloadFileList(self) -> None:
        # ディレクトリ内のファイルリストを再取得する
        if self.isPathExist():
            self.dirPathList = [f"{self.path}/{i}" for i in os.listdir(self.path)]
        else:
            self.dirPathList = []
        return


    def isPathExist(self) -> bool:
        # ディレクトリが存在するかどうかを返す
        return os.path.exists(self.path)


    def makeDir(self) -> bool:
        # ディレクトリを作成する
        if not self.isPathExist():
            os.makedirs(self.path)
            print(f"Directory created: {self.path}")
            return True
        else:
            print(f"Directory already exists: {self.path}")
        return False


    def removeDir(self) -> bool:
        # ディレクトリを削除する
        # 使用注意: ディレクトリ内のファイルも削除される
        if self.isPathExist():
            # 使うときにコメントアウトを外す
            # shutil.rmtree(self.path)
            print(f"Directory removed: {self.path}")
            return True
        else:
            print(f"Directory doesn't exist: {self.path}")
        return False


    def renameDir(self, newName: str) -> bool:
        # ディレクトリ名を変更する
        if self.isPathExist():
            os.rename(self.path, f"{self.getPath()}/{newName}")
            print(f"Directory renamed: {self.path} -> {newName}")
            return True
        else:
            print(f"Directory doesn't exist: {self.path}")
        return False



class MinecraftServerDirectory(Directory):
    def __init__(self, path) -> None:
        # 初期化をする
        super().__init__(path)
        return


    def getVersion(self):
        # behavior_packsの中に存在している
        # vanilla_[version] を確認し，
        # 最新のバージョンを返す
        version = [0, 0, 0]
        self.reloadFileList()
        for i in self.getFileList():
            if "vanilla_" in i.getPath():
                version = [int(j) for j in i.getPath().split("_")[-1].split(".")]
                # これじゃ動かない 変える