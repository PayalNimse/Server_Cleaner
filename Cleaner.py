""" SERVER CLEANER (Duplicate Files Remover :)
This is An Automation Project which Scans The Directory and gather All Duplicate files after users confirmation :
    
"""

from sys import *
import os
import hashlib
import pyttsx3
import datetime,time
import schedule
import smtplib,ssl
from email.message import EmailMessage

engine=pyttsx3.init()               #it is only for indiaction purpose we can ommite this part
engine.setProperty("rate", 150)
voices = engine.getProperty("voices")
engine.setProperty('voice', voices [1].id)

def engine_talk(text):
	engine.say(text)
	engine.runAndWait()

def write_log(Dups_file,log_info):
    Exists=os.path.isdir('Loggs')         # Existance of directory 
    logdir=os.path.join(os.getcwd(),'Loggs')
    if not Exists:
        os.mkdir(logdir)
    filename= str(datetime.datetime.today().strftime("%B_%d_%Y_%I_%M.txt"))
    filepath=os.path.join(logdir,filename)
    with open(filepath,'w',encoding='UTF-8') as logg:
        for i in Dups_file:
            logg.write("%s  %s\n"%(i[0],i[1]))
        logg.close()
    send_Email(filepath,argv[3],log_info)
    return filepath

def send_Email(pathh,reciver,log_info):
    msg = EmailMessage()
    msg["From"] = "gaurav.arun.pekhale@gmail.com"
    msg["Subject"] = ' '.join(['Logg File of ',str(datetime.date.today())])
    msg["To"] = reciver
    msg.set_content(log_info)
    msg.add_attachment(open(pathh, "r").read(), filename="loggfile.txt")

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls(context=ssl.create_default_context())
    try:
        s.login("gaurav.arun.pekhale@gmail.com","11June2001")
        s.send_message(msg)
        print('Mail Sent Succesfully')
        engine_talk('Mail Sent Succesfully')
    except Exception as E:
        print(E)



def Hashfile(paths,blocksize=1024): #default size is 1 kb 
    file_obj=open(paths,'rb')   # To find chechsum file must be in binary mode 
    try :
        hasher=hashlib.md5()
        buf=file_obj.read(blocksize)

        while len(buf)>0:
            hasher.update(buf)
            buf = file_obj.read(blocksize)

    except Exception as E:
        print("Exception Occured While Finding Checksum ")

    finally:
        file_obj.close()
        return hasher.hexdigest()


def File_checker(dir_path):
    engine_talk('Scanning.....')
    print('Scanning.....')
    if not os.path.isabs(dir_path):             # Converting Relative path into Absulute path
        dir_path=os.path.abspath(dir_path)

    if not os.path.exists(dir_path):            #Existance of DIrectory
        print("Invallide Path")
        exit(0)
    dups_file=list()
    files_info=dict()
    try:    
        for (root,dirs,files) in os.walk(dir_path, topdown=True):
            for file_name in files:
                file_path=os.path.join(root,file_name)
                Checksum=Hashfile(file_path)
                
                files_info.setdefault(Checksum, [])
                files_info[Checksum].append([file_path,file_name])
        """  here we used nested list as dictionary value, if there will be multiple 
        file then number of nested list incresed and that dictionary having more than
        one nested list then there is duplication occures  
        """
        for val in files_info.values():
            if len(val)>1 :
                while(len(val)!=1):
                    dups_file.append(val.pop())

        for i in dups_file:
            os.remove(i[0])

    except Exception as E:
        print("Excaption Occured wihile Scanning files : ",E)

    log_info='Start Time of Scanning :%s \nTotal Files Scanned : %d Files\nDuplicate Files Found :%d FIles'%(datetime.datetime.today().strftime('%I:%M:%S'),len(files_info),len(dups_file))
    if(len(dups_file)!=0):
        write_log(dups_file,log_info)
    else:
        engine_talk("No Duplicate File Found")
        print("No Duplicate File Found")

def main():
    print("------- Automation :Directory Cleaner  ----------") #header 
    print("Application name :",argv[0])
    
    if (len(argv)<4):
        print("Error : Invalide Number of Arguments")
        print("Please Give Flag '-u' for Usage and '-h' for Help")
        exit(0)
    if argv[1] == '-h' or argv[1] == '-H':
        print("HELP : This Script designed for Deleting Duplicate Files and deleted data will be written in Logs and that logs transfered to user via Email")
        exit(0)
    if argv[1] == '-u' or argv[1] == '-U':
        print("Usage : Application_name     Directory_Path     Time_Interval(in minutes)    Mail_id")
        exit(0)

    schedule.every(int(argv[2])).minutes.do(File_checker,argv[1])
    while True:
        schedule.run_pending()
        time.sleep(2)
    
if __name__ == "__main__":
    main()
