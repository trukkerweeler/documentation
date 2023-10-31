# Read DOCS_AVAIL database and find those that do not have a CTRL_DOC

import os
import sys
import utils
import re
ctrlpath = r'C:\Users\TimK\Documents\QMS'
distpath = r'K:\Quality'
foldersnotfound = []

def findInSpecialProcesses(form, dbPath):
    """This looks in the special processes folder for the form."""
    # for spl in ['C:\\Users\\TimK\Documents\\QMS\\08512 Validation and Control of Processes', 'K:\\Quality\\08512 - Special Process Control']:
    for folder in os.listdir(dbPath):
        if os.path.isdir(os.path.join(dbPath, folder)):
            for file in os.listdir(os.path.join(dbPath, folder)):
                if file.startswith(f"Form {form}") or file.startswith(f"{form} "):
                    #  fix the slashes
                    folder = folder.replace('\\', '\\\\')
                    fullpath = (dbPath.replace('\\', '\\\\') + "\\\\" + folder + "\\\\" + file)
                    print(fullpath)
                    if 'TimK' in dbPath:
                        print(f"Control path: {fullpath}")
                        utils.updateqms('CTRL_DOC', 'DOCS_AVAIL', fullpath, 'DOCUMENT_ID',form)
                    else:
                        print(f"Distribution path: {fullpath}")
                        utils.updateqms('DIST_DOC', 'DOCS_AVAIL', fullpath, 'DOCUMENT_ID',form)


def getUncontrolled():
    #Read DOCS_AVAIL table from DOCUMENTS table
    sql = "select da.*, d.REFERENCE from DOCS_AVAIL da left join DOCUMENTS d on da.DOCUMENT_ID = d.DOCUMENT_ID where (CTRL_DOC is null or CTRL_DOC = '' or DIST_DOC is null or DIST_DOC = '' and d.STATUS = 'C')"
    # sql = "select da.*, d.REFERENCE from DOCS_AVAIL da left join DOCUMENTS d on da.DOCUMENT_ID = d.DOCUMENT_ID"

    uncontrolled = utils.getDatabaseData(sql)
    #Find those that do not have a CTRL_DOC
    #Return a list of those that do not have a CTRL_DOC
    return uncontrolled

def lookin(folder, form, docType):
    # print(folder)
    print(form)
    for file in os.listdir(folder):
        if file.startswith(form):
            #  fix the slashes
            folder = folder.replace('\\', '\\\\')
            fullpath = (folder + "\\\\" + file)
            utils.updateqms(docType, 'DOCS_AVAIL', fullpath, 'DOCUMENT_ID',form)


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

def getDistributionFolders():
    """This gets the network folders in Quality"""
    # Create a dictionary of all the folders in the distribution folder
    distfolders = {}
    for folder in os.listdir(distpath):
        # if its a folder
        if os.path.isdir(os.path.join(distpath, folder)):
            # Find the control base number
            controlbase = re.search(r'[0-9]{4,5}[A-Q]{0,1}', folder)
            if controlbase:
                ctrlbase = controlbase.group()
                distfolders[ctrlbase] = folder
        # controlbase = re.search(r'[0-9]{4,5}', folder)
        # print(controlbase.group())
    # print(distfolders)
    return distfolders

def main():
    """This gets those without control documents and looks in the folder for the control document. If found it writes the path to DOC_AVAIL."""
    # Get the control folders
    ctrlfolders = getControlFolders()
    distfolders = getDistributionFolders()
    # print(ctrlfolders)
    print('+++++++++++++++++++++++++++++++')

    # Get those that do not have a CTRL_DOC

    uncontrolled = getUncontrolled()
    # print(uncontrolled)
    print('+++++++++++++++++++++++++++++++')
    if uncontrolled:
        for doc in uncontrolled:
            form = doc[0]
            ctrl = doc[1]
            dist = doc[2]
            spcl = doc[4]
            print("+------------------------------------+")
            arrPath = ['C:\\Users\\TimK\Documents\\QMS\\08512 Validation and Control of Processes', 'K:\\Quality\\08512 - Special Process Control']

            match spcl:
                case '08512':
                    print(f"{form} is a special process")
                    if ctrl is None:
                        print(f"Control path: {ctrl}")
                        specialprocesslocation = findInSpecialProcesses(form, arrPath[0])
                        # print(f"Special Process Location(s): {specialprocesslocation}")
                    if dist is None:
                        specialprocesslocation2 = findInSpecialProcesses(form, arrPath[1])
                        # print(f"Special Process Location(s): {specialprocesslocation2}")
                case _:
                    print(f"{form} is not a special process")                    
                    directfolder = re.search(r'[0-9]{4,5}[A-Q]{0,1}', form)
                    # print(f"Direct folder: {directfolder}")
                    baseID = directfolder.group()
                    parentID = round(int(baseID)/100)
                    parentID = '0' + str(parentID) + '00'
                    # parentID = parentID.split('.')[0]
                    print(f"Parent ID: {parentID}")
                    if baseID[0] != '1':
                        baseID = '0' + baseID
                    # print(value)

                    if ctrl is None:
                        if baseID in ctrlfolders:
                            print(ctrlfolders[baseID])
                            #append the folder name to the form name
                            proceduredir = os.path.join(ctrlpath, ctrlfolders[baseID])
                            print(proceduredir)

                            #Find the file in the folder
                            lookin(folder=proceduredir, form=form,docType='CTRL_DOC')

                        else:
                            if parentID in ctrlfolders:
                                print(f"Parent folder: {ctrlfolders[parentID]}")
                                #append the folder name to the form name
                                proceduredir = os.path.join(ctrlpath, ctrlfolders[parentID])
                                print(proceduredir)

                                #Find the file in the folder
                                lookin(folder=proceduredir, form=form, docType='CTRL_DOC')
                            else:
                                foldersnotfound.append(form)
                    
                    if dist is None:
                        if baseID in distfolders:
                            print(distfolders[baseID])
                            #append the folder name to the form name
                            proceduredir = os.path.join(distpath, distfolders[baseID])
                            print(proceduredir)

                            #Find the file in the folder
                            lookin(folder=proceduredir, form=form, docType='DIST_DOC')

                        else:
                            if parentID in distfolders:
                                print(f"Parent folder: {distfolders[parentID]}")
                                #append the folder name to the form name
                                proceduredir = os.path.join(distpath, distfolders[parentID])
                                print(proceduredir)

                                #Find the file in the folder
                                lookin(folder=proceduredir, form=form, docType='DIST_DOC')
                            else:
                                foldersnotfound.append(form)

if __name__ == '__main__':
    print("Starting FORMS Mgmt")
    main()
    print("Folders Not Found:")
    print(foldersnotfound)
    print("Done")
    # print(findInSpecialProcesses('T11'))