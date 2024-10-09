from Obj.WebManager import WebManager
from Obj.File import Directory

def pprint(lis):
    for i in lis:
        print(i)
    return


def main():
    web = WebManager()
    web.setDownloadOsVersion(0)
    print(web.getDownloadOsVersion())
    urls = web.getLatestUrl()
    pprint(urls)
    for i in urls:
        print(i.getVersion())
    pass

def main2():
    d = Directory("Obj")
    print(d)
    print(d.getPath())
    print(d.getPathList())
    print(d.getFileList())
    pass


if __name__ == "__main__":
    main2()