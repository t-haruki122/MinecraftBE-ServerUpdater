from Obj.WebManager import WebManager

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

if __name__ == "__main__":
    main()