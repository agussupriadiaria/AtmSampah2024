'''
============== ATM SAMPAH 2024 ==============
Testing 7 Mei 2024 > Ok
'''

from tkinter import *
import serial.tools.list_ports
import threading
import time
import sys
import serial
import signal
import RPi.GPIO as gp
import random

from  escpos.printer import Serial
gp.setmode(gp.BCM)
gp.setup(5, gp.OUT)
gp.output(5, gp.HIGH)
gp.setup(6, gp.IN, pull_up_down=gp.PUD_UP)
gp.setup(13, gp.OUT)
gp.output(13, gp.HIGH)
gp.setup(19, gp.OUT)
gp.output(19, gp.HIGH)
gp.setup(26, gp.IN, pull_up_down=gp.PUD_UP)

def signal_handler(signum, frame):
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

def mainPage():
    global root, timeStamp, dateStamp, barcodeLabel, jumlahLabel, ukuranLabel, nominalLabel, barcodeLabel, bottle, saldo, parameterLabel3, userIDLabel
    root = Tk()
    root.title("atm sampah - aria")
    root.attributes("-fullscreen", True)
    #root.geometry("800x500")
    root.config(bg="white")

    titleLabel = Label(root, text="ATM SAMPAH", font=("Helvatica",18, "bold"), bg="white")
    titleLabel.place(relx=0.5, rely=0.1,anchor=CENTER)

    mainFrame = Frame(root, bg="white", bd=10, highlightbackground="green", highlightthickness=5)
    mainFrame.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.80)

    stampFrame = Frame (mainFrame,bg="white",width=400, height=100)
    stampFrame.place(x=10, y=10)

    timeLabel = Label(stampFrame, text="Waktu   ", font=("Helvatica",10, "bold"), bg="white")
    timeLabel.place(x=10, y=1)
    dateLabel = Label(stampFrame, text="Tanggal ", font=("Helvatica",10, "bold"), bg="white")
    dateLabel.place(x=10, y=30)

    timeStamp = Label(stampFrame, text="00:00:00",font=("Helvatica",10, "bold"), bg="white")
    timeStamp.place(x=100, y=1)
    dateStamp = Label(stampFrame, text="dd/mm/yy",font=("Helvatica",10, "bold"), bg="white")
    dateStamp.place(x=100, y=30)

    ariaLabel = Label(mainFrame, text="[ARIA - JOG]", font=("Courier",10, "bold"), bg="white")
    ariaLabel.place(x=615, y=10)

    parameterFrame = Frame(mainFrame, bg="white",width=350, height=200, highlightbackground="blue", highlightthickness=5 )
    parameterFrame.place(x=10, y=75)

    parameterLabel1 = Label(parameterFrame,bg="white", text="TOTAL SALDO", font=("Helvatica", 15, "bold"))
    parameterLabel1.place(x=85, y=10)
    parameterLabel2 = Label(parameterFrame, text="Rp", font=("Helvatica", 30, "bold"), bg="white")
    parameterLabel2.place(x=65, y=80)
    parameterLabel3 = Label(parameterFrame, text="9999", font=("Helvatica", 30, "bold"), bg="white")
    parameterLabel3.place(x=140, y=80)

    transaksiFrame = Frame(mainFrame, bg="white",width=350, height=200, highlightbackground="red", highlightthickness=5 )
    transaksiFrame.place(x=370, y=75)

    nameDataLabel = Label(transaksiFrame, bg="white", text="DATA", font=("Helvatica", 15, "bold"))
    nameDataLabel.place(x=135, y=10)
    nameUserIdLabel = Label(transaksiFrame, bg="white", text="User ID   ", font=("Helvatica", 10, "bold"))
    nameUserIdLabel.place(x=50, y=50)
    nameJumlahLabel = Label(transaksiFrame, bg="white", text="Jumlah    ", font=("Helvatica", 10, "bold"))
    nameJumlahLabel.place(x=50, y=75)
    nameUkuranLabel = Label(transaksiFrame, bg="white", text="Ukuran   ", font=("Helvatica", 10, "bold"))
    nameUkuranLabel.place(x=50, y=100)
    nameNominalLabel = Label(transaksiFrame, bg="white", text="Nominal            Rp", font=("Helvatica", 10, "bold"))
    nameNominalLabel.place(x=50, y=125)
    nameBarcodeLabel = Label(transaksiFrame, bg="white", text="Barcode  ", font=("Helvatica", 10, "bold"))
    nameBarcodeLabel.place(x=50, y=150)

    userIDLabel = Label(transaksiFrame, bg="white", text="99999", font=("Helvatica", 10, "bold"))
    userIDLabel.place(x=170, y=50)
    jumlahLabel = Label(transaksiFrame, bg="white", text="999", font=("Helvatica", 10, "bold"))
    jumlahLabel.place(x=170, y=75)
    ukuranLabel = Label(transaksiFrame, bg="white", text="Medium", font=("Helvatica", 10, "bold"))
    ukuranLabel.place(x=170, y=100)
    nominalLabel = Label(transaksiFrame, bg="white", text="999", font=("Helvatica", 10, "bold"))
    nominalLabel.place(x=210, y=125)
    barcodeLabel = Label(transaksiFrame, bg="white", text="9999999999999 ", font=("Helvatica", 10, "bold"))
    barcodeLabel.place(x=170, y=150)

    printButton = Button(mainFrame,text="Cetak Struk", font=("Helvatica",10, "bold"), bg="green",fg = "blue", width=10, height=3, command=resetCounter)
    printButton.place(x=55, y=290)

    printButton = Button(mainFrame,text="Scan Ulang", font=("Helvatica",10, "bold"), bg="yellow",fg = "blue", width=10, height=3, command=barcodeScanner)
    printButton.place(x=195, y=290)

    messageLabel = Label(mainFrame, text="Terima Kasih Sudah Ikut", font=("Helvatica", 10, "bold"),bg="white")
    messageLabel.place(x=457, y=300)

    messageLabel = Label(mainFrame, text="Menyelamatkan Lingkungan", font=("Helvatica", 10, "bold"),bg="white")
    messageLabel.place(x=445, y=325)

    bottle = 0
    saldo = 0
    
    connexion()
    updateTime()
    updateDate()
    userIDNum()

def userIDNum():
    global userID
    userID = random.randrange(10000, 100000)
    userIDLabel ["text"] = userID

def bottleCounter():
    global bottle
    bottle += 1
    parameterLabel3 ["text"] = saldo
    jumlahLabel ["text"] = bottle

def resetCounter():
    global bottle, saldo
    thermalPrinterX()
    bottle = 0
    saldo = 0
    parameterLabel3 ["text"] = saldo
    nominalLabel ["text"] = saldo
    jumlahLabel ["text"] = bottle
    ukuranLabel ["text"] = "-"
    barcodeLabel ["text"] = "0"
    userIDNum()
    print("Reset Jumlah Botol: ", bottle)
    print("Reset Jumlah Saldo: Rp", saldo)
    print("")

def thermalPrinterX():
    """ 9600 Baud, 8N1, Flow Control Enabled """
    p = Serial(devfile='/dev/serial0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1.00, dsrdtr=True)
    p.set(font="a", height=1, align="center", bold=True, double_height=False)
    p.text("ARIA\n")
    p.text("ATM SAMPAH JOGJA\n\n")
    #CONTENT===
    p.set(font="a", height=1, align="center", bold=True, double_height=False)
    p.text("Jumlah Botol: ")
    p.text(bottle)
    p.text(" Pcs")
    p.text("\n")
    p.text("Total Saldo: Rp ")
    p.text(saldo)
    p.text("\n\n")
    p.set(font="a", height=1, align="center", bold=True, double_height=False)
    p.text(userID) #User ID
    p.text("\n")
    p.text(time.asctime())
    p.text("\n")
    #FOOTAGE===
    p.text("Terima kasih\n")
    p.text("\n\n\n")
    p.text(0)

def saveData():
    #fb = open('/home/aria/EVERMOS AGUS/PROJECT/gitHub/pythonProject/pythonProject/saveData/data.txt', 'a')
    #fb = open('/home/aria/saveData/saveData.txt', 'a')
    fb = open('/home/blacksheep/saveData/saveData.txt', 'a')
    fb.write("Barcode: ")
    fb.write(lineRead)
    fb.write(' / ')
    fb.write("Time: ")
    fb.write(time_text)
    fb.write(' / ')
    fb.write("Date: ")
    fb.write(date_text)
    fb.write(' / ')
    fb.write("Bottle: ")
    fb.write(str(bottle))
    fb.write(' / ')
    fb.write("Saldo: Rp")
    fb.write(str(saldo))
    fb.write(' / ')
    fb.write("UserID: ")
    fb.write(str(userID))
    fb.write('\n')
    fb.close()
    print("Barcode: ", lineRead)
    print("Time: ", time_text)
    print("Date: ", date_text)
    print("Jumlah Botol: ", bottle)
    print("Saldo: Rp", saldo)
    print("UserID: ", userID)
    print("Data Tersimpan")
    print("")

def barcodeGate():
    global saldo
    if(lineRead=="8991389232057"):
        pinOutArduino()
        ukuranLabel["text"] = "Big"
        nominalLabel["text"] = "15"
        saldo += 15
        bottleCounter()
        saveData()
    elif(lineRead=="9300830022557"):
        pinOutArduino()
        ukuranLabel["text"] = "Medium"
        nominalLabel["text"] = "10"
        saldo += 10
        bottleCounter()
        saveData()
    else:
        ukuranLabel["text"] = "Not Registered"
        nominalLabel["text"] = "Not Registered"
        print(lineRead)
        print(bottle)
        print(saldo)
        print("")
'''
#DATA BARCODE SAMPLE======================
# 1 Orange Water 8997009510123, 10, Medium
# 2 Good Mood 8992775709061,15, Big
# 3 Hand Sanitizer 8992745610816, 10,Big / not registered
Kertas: 8991389232057
'''
def updateTime():
    global time_text
    hours = time.strftime("%H")
    minutes = time.strftime("%M")
    seconds = time.strftime("%S")
    #am_or_pm = time.strftime("%p")
    time_text = hours + ":" + minutes + ":" + seconds + " "
    timeStamp.config(text= time_text)
    timeStamp.after(1000, updateTime)

def updateDate():
    global date_text
    tanggal = time.strftime ("%d")
    bulan = time.strftime ("%m")
    tahun = time.strftime ("%y")
    date_text = tanggal + "/" + bulan + "/" + tahun
    dateStamp.config(text= date_text)
    dateStamp.after(86400000, updateDate)

def readSerial():
    global serialData, lineRead, ser
    while serialData:
        if ser.in_waiting > 0: 
            try:
                lineRead = ser.readline().decode('utf-8').rstrip()
                barcodeLabel["text"] = lineRead
                barcodeGate()
            except:
                pass

def barcodeScanner():
    print ("Barcode On")
    gp.output(13, gp.LOW)
    time.sleep(4)
    gp.output(13, gp.HIGH)

def pinOutArduino():
    print ("Arduino On")
    gp.output(19, gp.LOW)
    time.sleep(2)
    gp.output(19, gp.HIGH)

def inSensor():
    if (gp.input(26) == gp.LOW):
        time.sleep(3)
        print("Bottle In")
        barcodeScanner()
    else:
        pass
    root.after(5,inSensor)

def fullSensor():
    if (gp.input(6) == gp.LOW):
        gp.output(5, gp.HIGH)
    else:
        gp.output(5, gp.LOW)
    root.after(5,fullSensor)

def connexion():
    global ser, serialData
    klikBaud = 115200
    klikPort = "/dev/ttyUSB0"
    serialData = True
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]

    port = klikPort
    baud = klikBaud
    
    try:
        ser = serial.Serial(port, baud, timeout=0)
    except:
        pass
    t1 = threading.Thread(target=readSerial)
    t1.deamon = True
    t1.start()

def closeWindow():
    global root, serialData
    serialData = False
    date_text = False
    time_text = False
    gp.cleanup()
    root.destroy()

mainPage()
root.after(5,inSensor)
root.after(5,fullSensor)
root.protocol("WM_DELETE_WINDOW",closeWindow)
root.mainloop()