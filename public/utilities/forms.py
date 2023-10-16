# Read DOCS_AVAIL database and find those that do not have a CTRL_DOC

import os
import sys
import utils
import re
ctrlpath = r'C:\Users\TimK\Documents\QMS'
foldersnotfound = []

def getUncontrolled():
    #Read DOCS_AVAIL table from DOCUMENTS table
    sql = "select * from DOCS_AVAIL where (CTRL_DOC is null or CTRL_DOC = '')"
    uncontrolled = utils.getDatabaseData(sql)
    #Find those that do not have a CTRL_DOC
    #Return a list of those that do not have a CTRL_DOC
    return uncontrolled

def lookin(folder, form):
    # print(folder)
    print(form)
    for file in os.listdir(folder):
        if file.startswith(form):
            #  fix the slashes
            folder = folder.replace('\\', '\\\\')
            fullpath = (folder + "\\\\" + file)
            utils.updateqms('CTRL_DOC', 'DOCS_AVAIL', fullpath, 'DOCUMENT_ID',form)


def getControlFolders():
    """This gets the control folders and returns a dictionary of the folder name and the control base number."""
    # Create a dictionary of all the folders in the CTRL_DOC folder
    ctrlfolders = {}
    for folder in os.listdir(ctrlpath):
        # if its a folder
        if os.path.isdir(os.path.join(ctrlpath, folder)):
            # Find the control base number
            controlbase = re.search(r'[0-9]{4,5}[A-Q]{0,1}', folder)
            if controlbase:
                ctrlbase = controlbase.group()
                ctrlfolders[ctrlbase] = folder
        # controlbase = re.search(r'[0-9]{4,5}', folder)
        # print(controlbase.group())
    # print(ctrlfolders)
    return ctrlfolders

def main():
    """This gets those without control documents and looks in the folder for the control document. If found it writes the path to DOC_AVAIL."""
    # Get the control folders
    ctrlfolders = getControlFolders()
    # print(ctrlfolders)

    # Get those that do not have a CTRL_DOC
    uncontrolled = getUncontrolled()
    
    for doc in uncontrolled:
        print("+------------------------------------+")
        form = doc[0]
        directfolder = re.search(r'[0-9]{4,5}[A-Q]{0,1}', form)
        baseID = directfolder.group()
        if baseID[0] != '1':
            baseID = '0' + baseID
        # print(value)

        if baseID in ctrlfolders:
            print(ctrlfolders[baseID])
            #append the folder name to the form name
            proceduredir = os.path.join(ctrlpath, ctrlfolders[baseID])
            print(proceduredir)

            #Find the file in the folder
            lookin(folder=proceduredir, form=form)

        else:
            foldersnotfound.append(form)

if __name__ == '__main__':
    main()
    print("Folders Not Found:")
    print(foldersnotfound)
    print("Done")