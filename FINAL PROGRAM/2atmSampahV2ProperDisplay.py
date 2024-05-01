'''
Testing hahaha

SERIAL KOMUNIKASI UART 3
Spec: Raspberry pi 3 or 4
Detail: 1 channel
**Tools: Raspy, RTC, arduino uno, barcode scanner, thermal printer
**Note: All system is OK
**Series: Pushbutton on display.
**GPIO: Active
===================
Source:
- Raspy to RTC:
https://www.youtube.com/watch?v=Eqzw994ImUo&ab_channel=FuzzThePiGuy
https://fuzzthepiguy.tech/rtc/
- Raspy thermal printer:
https://circuitdigest.com/microcontroller-projects/thermal-printer-interfacing-with-raspberry-pi-zero-to-print-text-images-and-bar-codes

===================
PINS
* RASPBERRY <> ARDUINO MEGA [barcode scanner]
Koneksi dengan UART

* RASPBERRY <> ARDUINO UNO [] ---?
GPIO 19 (out)
GPIO 26 (in)

* RASPBERRY <> RTC [time]
5Volt - VCC
PIN 6 - GND
PIN 3 - SDA
PIN 5 - SCL

RASPBERRY <> THERMAL PRINTER

===================
toDo:
- Coba relay dan LED dipisah koneksinya
- Coba main2 dengan mindah2 urutan program high dan low GPIO
===================
ISSUE:
- Kalau sudah input botol, tapi nggak kebaca, auto stop atau no proses, biar botol diambil lagi.
- Buat sistem melakuan akumulasi dulu, habis itu setelah di pencet tombol print baru cetak struk dan reset data userID
- Relay nggak bisa kerja dengan baik, normali open/close nggak jalan, kemungkinan kendala dibagian pin input.
===================
History:
- 1 Mei 2024 > testing lagi

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

#THERMAL PRINTER=======
from  escpos.printer import Serial

gp.setmode(gp.BCM)
gp.setup(19, gp.OUT)
gp.setup(26, gp.IN, pull_up_down=gp.PUD_UP)

#TAMBAHAN PENYETABIL BACAAN SENSOR============
def signal_handler(signum, frame):
	sys.exit()
signal.signal(signal.SIGINT, signal_handler)

#HALAMAN UTAMA====================
def mainPage():
	global root, timeStamp, dateStamp, barcodeLabel, jumlahLabel, ukuranLabel, nominalLabel, barcodeLabel, bottle, saldo, parameterLabel3, userIDLabel
	root = Tk()
	root.title("atm sampah - aria")
	#Full screen geometry
	#root.attributes("-fullscreen", True)
	root.geometry("800x500")
	root.config(bg="white")

#LABEL TITLE====================
	titleLabel = Label(root, text="ATM SAMPAH", font=("Helvatica",18, "bold"), bg="white")
	titleLabel.place(relx=0.5, rely=0.1,anchor=CENTER)
#BIG FRAME=====================
	mainFrame = Frame(root, bg="white", bd=10, highlightbackground="green", highlightthickness=5)
	mainFrame.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.80)
#SMALL FRAME==================
	stampFrame = Frame (mainFrame,bg="white",width=400, height=100)
	stampFrame.place(x=10, y=10)
#LABEL NAMA================
	timeLabel = Label(stampFrame, text="Waktu   ", font=("Helvatica",10, "bold"), bg="white")
	timeLabel.place(x=10, y=1)
	dateLabel = Label(stampFrame, text="Tanggal ", font=("Helvatica",10, "bold"), bg="white")
	dateLabel.place(x=10, y=30)
#LABEL DATA=================
	timeStamp = Label(stampFrame, text="00:00:00",font=("Helvatica",10, "bold"), bg="white")
	timeStamp.place(x=100, y=1)
	dateStamp = Label(stampFrame, text="dd/mm/yy",font=("Helvatica",10, "bold"), bg="white")
	dateStamp.place(x=100, y=30)
#PARAMETER FRAME===============
	parameterFrame = Frame(mainFrame, bg="white",width=270, height=200, highlightbackground="blue", highlightthickness=5 )
	parameterFrame.place(x=10, y=75)
#KONTENT FRAME=================
	parameterLabel1 = Label(parameterFrame,bg="white", text="TOTAL SALDO", font=("Helvatica", 15, "bold"))
	parameterLabel1.place(x=55, y=10)
	parameterLabel2 = Label(parameterFrame, text="Rp", font=("Helvatica", 30, "bold"), bg="white")
	parameterLabel2.place(x=35, y=80)
	parameterLabel3 = Label(parameterFrame, text="9999", font=("Helvatica", 30, "bold"), bg="white")
	parameterLabel3.place(x=110, y=80)
#DETAIL TRANSAKSI FRAME=================
	transaksiFrame = Frame(mainFrame, bg="white",width=270, height=200, highlightbackground="red", highlightthickness=5 )
	transaksiFrame.place(x=300, y=75)
#KONTENT FRAME================
	nameDataLabel = Label(transaksiFrame, bg="white", text="DATA", font=("Helvatica", 15, "bold"))
	nameDataLabel.place(x=95, y=10)
	nameUserIdLabel = Label(transaksiFrame, bg="white", text="User ID   ", font=("Helvatica", 10, "bold"))
	nameUserIdLabel.place(x=10, y=50)
	nameJumlahLabel = Label(transaksiFrame, bg="white", text="Jumlah    ", font=("Helvatica", 10, "bold"))
	nameJumlahLabel.place(x=10, y=75)
	nameUkuranLabel = Label(transaksiFrame, bg="white", text="Ukuran   ", font=("Helvatica", 10, "bold"))
	nameUkuranLabel.place(x=10, y=100)
	nameNominalLabel = Label(transaksiFrame, bg="white", text="Nominal            Rp", font=("Helvatica", 10, "bold"))
	nameNominalLabel.place(x=10, y=125)
	nameBarcodeLabel = Label(transaksiFrame, bg="white", text="Barcode  ", font=("Helvatica", 10, "bold"))
	nameBarcodeLabel.place(x=10, y=150)

	userIDLabel = Label(transaksiFrame, bg="white", text="99999", font=("Helvatica", 10, "bold"))
	userIDLabel.place(x=130, y=50)
	jumlahLabel = Label(transaksiFrame, bg="white", text="999", font=("Helvatica", 10, "bold"))
	jumlahLabel.place(x=130, y=75)
	ukuranLabel = Label(transaksiFrame, bg="white", text="Medium", font=("Helvatica", 10, "bold"))
	ukuranLabel.place(x=130, y=100)
	nominalLabel = Label(transaksiFrame, bg="white", text="999", font=("Helvatica", 10, "bold"))
	nominalLabel.place(x=170, y=125)
	barcodeLabel = Label(transaksiFrame, bg="white", text="9999999999999 ", font=("Helvatica", 10, "bold"))
	barcodeLabel.place(x=130, y=150)
#BUTTON PRINT=============
#Bisa dihilangkan sesuai dengan penggunaan, apakah ingin touchscreen atau sensor IR.
	printButton = Button(mainFrame,text="Cetak Struk", font=("Helvatica",10, "bold"), bg="green",fg = "white", width=10, height=3, command=resetCounter)
	printButton.place(x=10, y=290)

	# contohButton = Button()
#MESSAGES LABEL======================
	messageLabel = Label(mainFrame, text="Terima Kasih Sudah Ikut Menyelamatkan Lingkungan", font=("Helvatica", 10, "bold"),bg="white")
	messageLabel.place(x=165, y=300)
#LABEL ARIA==============
	ariaLabel = Label(mainFrame, text="[ARIA - JOG]", font=("Courier",10, "bold"), bg="white")
	ariaLabel.place(x=470, y=330)

#VARIABEL BOTTLE COUNTER=============
	bottle = 0
	saldo = 0
	
#AUTO CALL ALL COMMAND DISINI======================
	connexion()
	updateTime()
	updateDate()
	userIDNum()

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

#THERMAL PRINTER==============
def thermalPrinterX():
	""" 9600 Baud, 8N1, Flow Control Enabled """
	p = Serial(devfile='/dev/serial0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1.00, dsrdtr=True)
	p.set(font="a", height=1, align="center", bold=True, double_height=False)
	#HEADER===
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
	if(lineRead=="8992775709061"):
		ukuranLabel["text"] = "Big"
		nominalLabel["text"] = "15"
		saldo += 15
		bottleCounter()
		saveData()
	elif(lineRead=="8997009510123"):
		ukuranLabel["text"] = "Medium"
		nominalLabel["text"] = "10"
		saldo += 10
		bottleCounter()
		saveData()
		pushButton() #INI JANGAN DITARUH DISINI, JADI DIBIKIN INDEPENDEN, ditaruh di mainPage====================
	else:
		ukuranLabel["text"] = "Not Registered"
		nominalLabel["text"] = "Not Registered"
		print(bottle)
		print(saldo)
		print("")
'''
8997009510123
8992775709061
8992745610816'''
#DATA BARCODE SAMPLE======================
# 1	Orange Water	8997009510123	10	Medium
# 2	Good Mood	8992775709061	15	Big
# 3	Hand Sanitizer	8992745610816	10	Big / not registered

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

#INPUT BUTTON===========
def lampuNyala():
#Coba ini nanti dipisah antara LED dan relay, apakah bisa on/off dengan normal
	print ("Lighting up LED")
	gp.output(19, gp.HIGH) #Coba main2 di bagian ini, harusnya pin nya bisa clear.===============
	time.sleep(5)
	gp.output(19, gp.LOW)
	resetCounter()

#OUTPUT BUTTON===========
def pushButton():
	if (gp.input(26) == gp.LOW):
		print("Button Pressed")
		lampuNyala()
	else:
		pass
	root.after(10,pushButton)#Ini coba dihilangin bisa tetap jalan atau nggak?=======================

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
	date_text = False
	time_text = False
	gp.cleanup()
	root.destroy()

#RUN PROGRAM LOOP====================================
mainPage()
root.protocol("WM_DELETE_WINDOW",closeWindow) #Stop running loop ketika nggak sengaja ter close
root.after(10,pushButton)
root.mainloop()