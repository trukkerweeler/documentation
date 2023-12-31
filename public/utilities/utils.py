import os, sys
from datetime import datetime, timedelta


def ranToday(script):
    match script:
        case "sysdoc":
            print(f"{script} script")
            sysdocFile = "C:\\Users\\timk\\Documents\\Python\\sysdoc\\sysdoc.txt"
            if os.path.exists(sysdocFile):
                with open(sysdocFile, "r") as f:
                    lastRun = f.readline()
                if lastRun == str(datetime.now().date()):
                    return True
                else:
                    with open(sysdocFile, "w") as f:
                        f.write(str(datetime.now().date()))
                    return False
            else:
                with open(sysdocFile, "w") as f:
                    f.write(str(datetime.now().date()))
                return False
        case default:
            return True



def getDatabaseData(sql):
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(host='ciqms.chgubqsqxrvz.us-east-2.rds.amazonaws.com',
                                             database='quality',
                                             user='admin',
                                             password='A1rplane$$$')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            return records

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def sendMail(to_email, subject, message, from_email="quality@ci-aviation.com", cc_email=""):
    import smtplib, ssl
    from email.message import EmailMessage
    PORT = 465
    SERVER = "sh10.nethosting.com"
    CONTEXT = ssl.create_default_context()
    if from_email == "tim":
        USERNAME = "tim.kent@ci-aviation.com"
        PASSWORD = "#A1rplane23"

    else:
        USERNAME = "quality@ci-aviation.com"
        PASSWORD = "#A1rplane2023"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = USERNAME
    msg["To"] = to_email
    msg["Cc"] = cc_email
    msg.set_content(message)
    server = smtplib.SMTP_SSL(SERVER, PORT, context=CONTEXT)
    server.login(USERNAME, PASSWORD)
    server.send_message(msg)
    server.quit()


def updateDatabaseData(sql):
    # print(sql)
    table = sql.split()[2]
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(host='ciqms.chgubqsqxrvz.us-east-2.rds.amazonaws.com',
                                              database='quality',
                                              user='admin',
                                              password='A1rplane$$$')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            # print(f"Inserted into {table}")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            connection.close()


def emailAddress(name):
    import mysql.connector
    from mysql.connector import Error
    sql = f"select WORK_EMAIL_ADDRESS from PEOPLE where PEOPLE_ID = '{name}'"
    # print(sql)
    try:
        connection = mysql.connector.connect(host='ciqms.chgubqsqxrvz.us-east-2.rds.amazonaws.com',
                                              database='quality',
                                              user='admin',
                                              password='A1rplane$$$')
        if connection.is_connected():
            cursor = connection.cursor(buffered=True)
            cursor.execute(sql)
            # connection.commit()
            email = cursor.fetchone()
            # print(email)
            return email[0]
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            connection.close()

def setLastSentFile(file):
    """Set the date in the last sent file."""
    lastSentFile = file + "Lastsent.txt"
    with open(lastSentFile, "w") as f:
        f.write(str(datetime.today()))
        
        
def getLastSentFile(file):
    """Get the date from the last sent file, add 12 days to it."""
    lastSentFile = file + "Lastsent.txt"
    # print(lastSentFile)
    if os.path.exists(lastSentFile):
        with open(lastSentFile, "r") as f:
            lastSentDate = f.read().split()[0]
            lastSentDate = datetime.strptime(lastSentDate, '%Y-%m-%d') + timedelta(days=10)
    else:
        lastSentDate = datetime.today() - timedelta(days=10)
    return lastSentDate

def getNextSysid(description):
    """Get the next sysid from the database."""
    sql = "select CURRENT_ID from SYSTEM_IDS where DESCRIPTION = '{description}'".format (description=description)
    # print(sql)
    sysid = getDatabaseData(sql)
    # convert to number
    sysid = int(sysid[0][0])
    # increment
    sysid += 1
    #prepends with zeros
    while len(str(sysid)) < 7:
        sysid = "0" + str(sysid)
    # increment in database
    sql = "update SYSTEM_IDS set CURRENT_ID = '{sysid}' where DESCRIPTION = '{description}'".format(sysid=sysid, description=description)
    updateDatabaseData(sql)
    return sysid

def getProjectName(projectid):
    """Get the project name from the database."""
    sql = "select NAME from PROJECT where PROJECT_ID = '{projectid}'".format(projectid=projectid)
    # print(sql)
    projectname = getDatabaseData(sql)

    return projectname


def getProjectId(iid):
    """Get the project id from the database."""
    sql = "select PROJECT_ID from PEOPLE_INPUT where INPUT_ID = '{iid}'".format(iid=iid)
    # print(sql)
    projectid = getDatabaseData(sql)
    return projectid[0][0]


def getAttachmentPath(sysid, recType):
    """Get the attachment from the records directory."""
    match recType:
        case "sysdoc": 
            path = "C:\\Users\\timk\\Documents\\Python\\sysdoc\\records\\"
        case "corrective":
            path = "\\\\fs1\\Quality - Records\\10200C - Corrective Actions\\2023\\"
            path = "K:\\Quality - Records\\10200C - Corrective Actions\\2023\\"
            
        case default:
            path = ""
    # print(path)
    if path != "":
        for folder in os.listdir(path):
            # print(f"folder: {folder}")
            if folder.startswith(sysid):
                for file in os.listdir(path + folder):
                    # print(os.path.join(path, folder, file))
                    if file.endswith(".pdf") and file.startswith(sysid) and not file.endswith("closeout.pdf"):
                        attachment = path + folder + "\\" + file
                        return attachment                        
    else:
        return None


def updateqms(field, table, value, id_name, id_value):
    # print(f'utils: {field}, {table}, {value}, {id_name}, {id_value}')
    sql = f"update {table} set {field} = '{value}' where {id_name} = '{id_value}'"
    print(sql)
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(host='ciqms.chgubqsqxrvz.us-east-2.rds.amazonaws.com',
                                              database='quality',
                                              user='admin',
                                              password='A1rplane$$$')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            # print(f"Inserted into {table}")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            connection.close()


if __name__ == '__main__':
    # print(getNextSysid("INPUT_ID"))
    # print(getProjectName("0000055"))
    # print(getProjectId("0000055"))
    print(getAttachmentPath("0001219", "corrective"))

