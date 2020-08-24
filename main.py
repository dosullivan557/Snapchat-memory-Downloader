import glob
import zipfile
import requests
import os
from lxml import html
import re
import subprocess, platform

# List files

def clearTerminal():
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate() #I like to use this instead of subprocess.call since for multi-word commands you can just type it out, granted this is just cls and subprocess.call should work fine 
    else: #Linux and Mac
        print("\033c")

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r{0} |{1}| {2}% {3}'.format(prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total: 
        print()


def getFilePaths(dirName):
     
  # setup file paths variable
  filePaths = []
   
  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for filename in files:
        # Create the full filepath by using os module.
        filePath = os.path.join(root, filename)
        filePaths.append(filePath)
         
  # return all paths
  return filePaths
 
count=0
files=glob.glob('./*.zip')
if not os.path.exists('memories'):
    os.makedirs('memories')
for fileName in files:
    with zipfile.ZipFile(fileName, 'r') as zip_ref:
        newFileName= fileName[:-4]  
        zip_ref.extractall('./' + newFileName)
        fullPath=os.path.abspath(newFileName[2:] + '/html/memories_history.html')
        zip_file = zipfile.ZipFile('temp.zip', 'w')
        filePaths = getFilePaths('./memories')
        with open(fullPath, "r") as f:
            page = f.read()
            tree = html.fromstring(page)
            listOfLinks = tree.find('body').getchildren()[1].getchildren()[4].getchildren()[0].getchildren()
            for eachTag in listOfLinks:
                clearTerminal()
                printProgressBar(count, len(listOfLinks))
                name = eachTag.getchildren()[0].text
                type = eachTag.getchildren()[1].text
                link = eachTag.getchildren()[2].getchildren()[0].get("href")
                result = re.search(r'\((.*?)\)', str(link))
                if (result != None):
                    newVal = result.group(0)[2:-2]
                    res = requests.post(newVal)
                    imageUrl = res.text
                    if (type == "PHOTO"):
                        image = requests.get(imageUrl)
                        open('./memories/'+name +'.jpeg', 'wb').write(image.content)
                    elif (type == "VIDEO"):
                        video = requests.get(imageUrl)
                        open('./memories/'+name +'.mp4', 'wb').write(video.content)
                count += 1

            print(filePaths)
            for file in filePaths:
                zip_file.write(file)

            zip_file.close()
            os.rmdir(os.path.abspath(newFileName[2:]))
            print("Done")



            
            # print("Done")

                

