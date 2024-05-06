'''
SERIAL KOMUNIKASI UART 3
Detail: 1 channel

** Tools: Raspy, RTC, arduino uno, barcode scanner, thermal printer

** Note: All system is OK

UPDATE:

ISSUE:
- Kalau sudah input botol, tapi nggak kebaca, auto stop atau no proses, biar botol diambil lagi.
- Buat sistem melakuan akumulasi dulu, habis itu setelah di pencet tombol print baru cetak struk dan reset data userID
- Tinggal menaruh pushbutton, karena nggak crash dengan tkinter display.
'''

#MODULES==============
from tkinter import *
import serial.tools.list_ports
import threading
import time
import sys
import serial
import signal
import RPi.GPIO as gp #MODULE GPIO [KHUSUS RASPBERRY]
import random
import matplotlib
matplotlib.use('Agg')

#THERMAL PRINTER=======
from  escpos.printer import Serial

#CLEAR GPIO PIN JIKA DIPERLLUKAN==========
# def gpClean ():
# 	gp.cleanup()

#DATA BARCODE SAMPLE======================
# 1	Cuttonbud	8994096222069	10	Medium
# 2	Handsanitizer	8992745610816	15	Big
# 3	Baygon	8998899400341	15	Big
# 4	PaperClips	6926677100031	5	Small
# 5	Axe	9300830022557	10	Medium

#TAMBAHAN PENYETABIL BACAAN SENSOR============
def signal_handler(signum, frame):
	sys.exit()
signal.signal(signal.SIGINT, signal_handler)

#THERMAL PRINTER==============
def thermalPrinterX():
	""" 9600 Baud, 8N1, Flow Control Enabled """
	p = Serial(devfile='/dev/serial0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1.00, dsrdtr=True)
	p.set(font="a", height=1, align="center", bold=True, double_height=False)
	#HEADER===
	p.text("ARIA\n")
	p.text("ATM SAMPAH JOGJA\n\n")
	#CONTENT===
	p.set(font="a", height=2, align="center", bold=True, double_height=True)
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

#HALAMAN UTAMA====================
def mainPage():
	global root, timeStamp, dateStamp, barcodeLabel, jumlahLabel, ukuranLabel, nominalLabel, barcodeLabel, bottle, saldo, parameterLabel3, userIDLabel
	root = Tk()
	root.title("Serial Komunikasi")
	#Full screen geometry
	#root.attributes("-fullscreen", True)
	root.geometry("1300x600")
	root.config(bg="white")

#LABEL TITLE====================
	titleLabel = Label(root, text="ATM SAMPAH ARIA", font=("Helvatica",18, "bold"), bg="white")
	titleLabel.place(relx=0.5, rely=0.1,anchor=CENTER)
#BIG FRAME=====================
	mainFrame = Frame(root, bg="white", bd=10, highlightbackground="green", highlightthickness=5)
	mainFrame.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.80)
#SMALL FRAME==================
	stampFrame = Frame (mainFrame,bg="white",width=400, height=100)
	stampFrame.place(x=10, y=10)
#LABEL NAMA================
	timeLabel = Label(stampFrame, text="Waktu  : ", font=("Helvatica",10, "bold"), bg="white")
	timeLabel.place(x=10, y=10)
	dateLabel = Label(stampFrame, text="Tanggal: ", font=("Helvatica",10, "bold"), bg="white")
	dateLabel.place(x=10, y=40)
#LABEL DATA=================
	timeStamp = Label(stampFrame, text="00:00:00",font=("Helvatica",10, "bold"), bg="white")
	timeStamp.place(x=100, y=10)
	dateStamp = Label(stampFrame, text="dd/mm/yy",font=("Helvatica",10, "bold"), bg="white")
	dateStamp.place(x=100, y=40)
#PARAMETER FRAME===============
	parameterFrame = Frame(mainFrame, bg="white",width=550, height=300, highlightbackground="blue", highlightthickness=5 )
	parameterFrame.place(x=10, y=100)
#KONTENT FRAME=================
	parameterLabel1 = Label(parameterFrame, text="TOTAL SALDO", font=("Helvatica", 20, "bold"), bg="white")
	parameterLabel1.place(x=170, y=10)
	parameterLabel2 = Label(parameterFrame, text="Rp", font=("Helvatica", 70, "bold"), bg="white")
	parameterLabel2.place(x=70, y=100)
	parameterLabel3 = Label(parameterFrame, text="0", font=("Helvatica", 70, "bold"), bg="white")
	parameterLabel3.place(x=240, y=100)
#DETAIL TRANSAKSI FRAME=================
	transaksiFrame = Frame(mainFrame, bg="white",width=550, height=300, highlightbackground="red", highlightthickness=5 )
	transaksiFrame.place(x=650, y=100)
#KONTENT FRAME================
	nameDataLabel = Label(transaksiFrame, bg="white", text="DATA", font=("Helvatica", 20, "bold"))
	nameDataLabel.place(x=230, y=20)
	nameUserIdLabel = Label(transaksiFrame, bg="white", text="User ID  : ", font=("Helvatica", 20, "bold"))
	nameUserIdLabel.place(x=10, y=70)
	nameJumlahLabel = Label(transaksiFrame, bg="white", text="Jumlah   :   ", font=("Helvatica", 20, "bold"))
	nameJumlahLabel.place(x=10, y=110)
	nameUkuranLabel = Label(transaksiFrame, bg="white", text="Ukuran  :  ", font=("Helvatica", 20, "bold"))
	nameUkuranLabel.place(x=10, y=150)
	nameNominalLabel = Label(transaksiFrame, bg="white", text="Nominal :     Rp", font=("Helvatica", 20, "bold"))
	nameNominalLabel.place(x=10, y=190)
	nameBarcodeLabel = Label(transaksiFrame, bg="white", text="Barcode : ", font=("Helvatica", 20, "bold"))
	nameBarcodeLabel.place(x=10, y=230)

	userIDLabel = Label(transaksiFrame, bg="white", text="0", font=("Helvatica", 20, "bold"))
	userIDLabel.place(x=200, y=70)
	jumlahLabel = Label(transaksiFrame, bg="white", text="0", font=("Helvatica", 20, "bold"))
	jumlahLabel.place(x=200, y=110)
	ukuranLabel = Label(transaksiFrame, bg="white", text="0", font=("Helvatica", 20, "bold"))
	ukuranLabel.place(x=200, y=150)
	nominalLabel = Label(transaksiFrame, bg="white", text="0", font=("Helvatica", 20, "bold"))
	nominalLabel.place(x=260, y=190)
	barcodeLabel = Label(transaksiFrame, bg="white", text="-------- ", font=("Helvatica", 20, "bold"))
	barcodeLabel.place(x=200, y=230)
#BUTTON PRINT=============
	printButton = Button(mainFrame, text="Cetak Struk", font=("Helvatica",10, "bold"), bg="grey", width=10, height=4, command=resetCounter)
	printButton.place(x=10, y=420)
#MESSAGES LABEL======================
	messageLabel = Label(mainFrame, text="Terima Kasih Sudah Ikut Menyelamatkan Lingkungan", font=("Helvetica", "16", "bold"),bg="white")
	messageLabel.place(x=350, y=550)
#ARIA LABEL======================
	ariaLabel = Label(mainFrame, text="**aria-project**", font=("Bitstream Vera Sans Mono", "10", "bold"),bg="white")
	ariaLabel.place(x=1120, y=550)

#VARIABEL BOTTLE COUNTER=============
	bottle = 0
	saldo = 0

#AUTO CALL ALL COMMAND DISINI=======================
	connexion()
	updateTime()
	updateDate()
	userIDNum()
	pushButtonSensor()

#PUSH BUTTON=================
def pushButtonSensor():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	while True:
		input_state = GPIO.input(26)
		if input_state == False:
			print('Button Pressed')
			time.sleep(1)
			thermalPrinterX()

#RANDOM NUMBER===================
def userIDNum():
	global userID
	userID = random.randrange(10000, 100000)
	userIDLabel ["text"] = userID

#DEF BOTTLE COUNTER==============
def bottleCounter():
	global bottle
	bottle += 1
	parameterLabel3 ["text"] = saldo
	jumlahLabel ["text"] = bottle

#DEF RESET COUNTER================
def resetCounter():
#RESET ALL DATA DISPLAY HERE===========
	global bottle, saldo
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

#DEF SAVE DATA TO STORAGE=================
def saveData():
	#fb = open('/home/aria/EVERMOS AGUS/PROJECT/gitHub/pythonProject/pythonProject/saveData/data.txt', 'a')
	fb = open('/home/aria/saveData/saveData.txt', 'a')
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

#ARGS COMMAND HERE=====================
def barcodeGate(): #INI DITARUH DIMANA COBA???
	global saldo
	if(lineRead=="8998899400341"):
		ukuranLabel["text"] = "Big"
		nominalLabel["text"] = "15"
		saldo += 15
		bottleCounter()
		saveData()
		gp.output(26,gp.HIGH)
		time.sleep(0.25)
		gp.output(26,gp.LOW)
	elif(lineRead=="9300830022557"):
		ukuranLabel["text"] = "Medium"
		nominalLabel["text"] = "10"
		saldo += 10
		bottleCounter()
		saveData()
		gp.output(26,gp.HIGH)
		time.sleep(0.25)
		gp.output(26,gp.LOW)
	else:
		ukuranLabel["text"] = "Error"
		nominalLabel["text"] = "Error"
		print(bottle)
		print(saldo)
		print("")
		gp.output(26,gp.LOW)

def updateTime():
	global time_text
	hours = time.strftime("%H") # Pakai %I  untuk am/pm
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

#MEMBACA DATA DARI SERIAL KONEKSI==========
def readSerial():
	global serialData, lineRead, ser
	while serialData:
		if ser.in_waiting > 0: 
			try:
				lineRead = ser.readline().decode('utf-8').rstrip()
				#Read satu line barcode dari arduino, data time dll dari raspi
				barcodeLabel["text"] = lineRead
				barcodeGate()
			except:
				pass

#MASUKKAN PILIHAN PORT DAN BAUD RATE================
def connexion():
	global ser, serialData
	klikBaud = 115200
	klikPort = "/dev/ttyUSB0"
	serialData = True
	ports = serial.tools.list_ports.comports()
	coms = [com[0] for com in ports]

	port = klikPort
	baud = klikBaud
	#BISA PRINT SHELL PORT DAN BAUD DISINI========================
	try:
		ser = serial.Serial(port, baud, timeout=0)
	except:
		pass
	t1 = threading.Thread(target=readSerial)
	t1.deamon = True
	t1.start()

#STOP RUNNING LOOP KETIKA WINDOWS DI CLOSE=====================
def closeWindow():
	global root, serialData
	serialData = False
	root.destroy()

#RUN PROGRAM LOOP====================================
mainPage()
root.protocol("WM_DELETE_WINDOW",closeWindow) #Stop running loop ketika nggak sengaja ter close
root.mainloop()

