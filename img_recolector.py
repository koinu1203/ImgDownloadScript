import errno
import requests 
import os 
import colorama
import logging
from urllib import request
from bs4 import BeautifulSoup as bs, ResultSet

logging.basicConfig(level=logging.DEBUG,format= '%(message)s')

#
#   TO USE ONLY CHANGE THE SITE URL AND RUN WITH THE COMMANT "py ./img_recolector.py" | "python3 ./img_recolector.py"
#

def main():
    site=getSite()
    soup=getSoup(site)
    capTitle=getTitle(soup)
    folderName=createFolder(capTitle)
    download(folderName,capTitle,soup)
    openFolder(folderName)

def getSite():
    params("Insert URL (www.tapas.io): ")
    site= getInput(1,27)
    if "tapas.io" in site:
        debug("Site URL >>> "+ site)
        return site
    error(site+" is not a permited site")

def getSoup(site:str):
    print(colorama.Fore.MAGENTA)
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
    response= requests.get(url=site, headers=head)
    warm("Estatus Code RESPONSE: "+str(response.status_code))
    return bs(response.text,'html.parser')

def createFolder(titleName):
    warm("Scanning existing directories")
    dir, subdirs, archivos = next(os.walk('.'))
    debug("valid directories founds \n"+str(subdirs))
    dirArray=[]
    for subdir in subdirs:
        if 'Cap' in subdir:
            try: 
                dirArray.append(int(subdir[4:6]))
            except:
                warm("Unvalid Dir " + subdir)
    dirArray.sort()
    capNum= 1 if not dirArray else dirArray.pop()+1
    folderName= "Cap "+str(capNum)+" - "+titleName
    try:
        os.mkdir(folderName)
    except OSError as e:
        if e.errno!=errno.EEXIST:
            raise
    finally:
        params(">>>>>>>>>>>> Folder create with name "+folderName)
    return folderName


def getTitle(soup:bs):
    soupTitle=soup.find_all('div',attrs={ "class":"viewer__header"})
    htmlTitleContainer=str(soupTitle[0])
    titleContainer=bs(htmlTitleContainer,'html.parser')
    for title in titleContainer.find_all("p",attrs={"class":"title"}):
        debug("Cap Title: "+title.text)
        return title.text


def download(folderName,titleName:str,soup:bs):
    path="./"+folderName+"/"
    i=0
    for link in soup.find_all('img',{'content__img'}):
        filename= "img_0" if i<9 else "img_"
        filename+=str(i+1)+".png"
        saveImg(link,filename,path,'data-src')
        i+=1

    pPictureName= folderName+".png"
    for link in soup.find_all('img',attrs={ "alt":titleName}):
        saveImg(link,pPictureName,path,'src')
    params('>>>>>>>>>>>> DONWLOAD FINISHED')

def saveImg(link:ResultSet,filename,path,src):
    url=link.get(src) 
    debug(str(url)+" >>>>> "+str(filename))
    if not filename:
        print('No imagen')
    else: 
        try:
            request.urlretrieve(url,path+filename)
        except Exception as e:
            pass    

def openFolder(folderName: str):
    path="./"+folderName+"/"
    realpath = os.path.realpath(path)
    params("Images save in " +realpath)
    os.startfile(realpath)

def debug(msg:str):
    pre="DEBUG - "
    logging.debug(colorama.Fore.GREEN + pre + msg)
    resetColor()

def warm(msg:str):
    pre="WARNING - "
    logging.warning(colorama.Fore.YELLOW + pre + msg)
    resetColor()

def error(msg:str):
    pre="ERROR - "
    logging.error(colorama.Fore.RED+pre+msg)
    resetColor()

def params(msg:str):
    print(colorama.Fore.LIGHTBLUE_EX+msg)
    resetColor()

def getInput(up:int=0,forward:int=0):
    return input(colorama.Fore.RESET + colorama.Cursor.UP(up)+colorama.Cursor.FORWARD(forward))

def resetColor():
    print(colorama.Fore.RESET)
    print(colorama.Cursor.UP(2))

if __name__ == "__main__":
    main()