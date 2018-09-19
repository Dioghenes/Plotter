#******************************************************
 # Dioghenes
 # Polytechnic of Turin
 # 2016
 # Plotter v0.5
#******************************************************

from Tkinter import *
from ttk import *
from serial import *
from tkMessageBox import *
from threading import *
import os
import time


"""
	All global variables start with '_' to highlight their properties.
	All global variables are declared and initialized here.
"""
global _version
global _defaultPathVar
global _defaultPort
global _defaultBaud
global _RUN



_version = "Plotter v0.5"
if os.name == "posix":
	_defaultPathVar = str(os.getcwd()+"/Plots/")
	_defaultPort = "/dev/ttyACM0"
elif os.name == "nt":
	_defaultPathVar = str("C:\\")
	_defaultPort = "COM3"
_defaultBaud = "9600"
_RUN = 0



"""
	Main class
"""
class Plotter:
	

	"""
		Draw the window and initialize the variables
	"""
	def __init__(self):		

		global _NTRACES		

		self.mainApp = Tk()
		self.mainApp.title(_version)
		self.mainApp.resizable(False,False)


		"""
			All variables that are strictly connected to a Tkinter widget 
			are written with all characters capitalized and are preceeded by _.
			Variables of this kind are:
			 - StringVar()
			 - IntVar()
			 - FloatVar()
			All these variables are created inside the main class, in the __init_ method.
			They will be initialized in the __init__ method, after the creation of
			the instance Tk().
		"""
		self._BAUDVAR = StringVar()				#Baudrate for the serial communication
		self._PORTVAR = StringVar()				#Port on which Arduino is sending datas
		self._SAVEVAR = IntVar()				#1 - Save datas on a file. 0 - Plot without saving
		self._PATHVAR = StringVar()				#Path where you save your data file
		self._FILEVAR = StringVar()				#Name of the file that you can choose
		self._RELTVAR = IntVar()				#1 - Use a zoomed scale to plot the signal. 0 - Use default scale (0-5)V
		self._MINABSVAR = StringVar()			        #Beta function
		self._MAXABSVAR = StringVar()			        #Beta function
		self._MINVOLTVAR = StringVar()                          #
		self._MAXVOLTVAR = StringVar()                          #
		self._WORKVAR = ""						#String containing path+filename. 
		self._NOISVAR = IntVar()				#Noise reduction level 1
		self._NOISVAR2 = IntVar()				#Noise reduction level 2
		self._STATUSVAR = StringVar()   		#Variable for the status of the program.
		self._NTRACES = IntVar()				#Variable for the number of traces plotted on the screen		
		self._TRACETOPLOT = IntVar()			#Datum to plot in the array of data received
		
		self._PORTVAR.set(_defaultPort)
		self._BAUDVAR.set(_defaultBaud)
		self._SAVEVAR.set(0)
		self._PATHVAR.set(_defaultPathVar)
		self._FILEVAR.set("")
		self._RELTVAR.set(0)
		self._MINABSVAR.set("0")
		self._MAXABSVAR.set("5")
		self._MINVOLTVAR.set("0")
		self._MAXVOLTVAR.set("5")
		self._NOISVAR.set(0)
		self._NOISVAR2.set(0)
		self._STATUSVAR.set("Initialization")
		self._NTRACES.set(1)
		self._TRACETOPLOT.set(-1)

		self.mainFrame = Frame(self.mainApp,height=1000,width=1200)
		self.mainFrame.pack(expand=1,fill=BOTH)
		

		"""
			Frames definition
		"""
		self.leftFrame = Frame(self.mainFrame)
		self.leftFrame.pack(side=LEFT,expand=1,fill=BOTH)
		self.centerFrame = LabelFrame(self.mainFrame,text="Plot")
		self.centerFrame.pack(side=LEFT,expand=1,fill=BOTH,pady=4)
		self.rightFrame = Frame(self.mainFrame)
		self.rightFrame.pack(side=LEFT,expand=1,fill=BOTH)


		"""
			Left Frame design
		"""
		#Port and baud
		self.leftFrame1 = LabelFrame(self.leftFrame,text="Port settings")
		self.leftFrame1.pack(side=TOP,expand=1,fill=BOTH,pady=4)
		self.portLabel = Label(self.leftFrame1,text="Port: ")
		self.portLabel.grid(column=0,row=0,pady=10)
		self.portEntry = Entry(self.leftFrame1,textvariable=self._PORTVAR)
		self.portEntry.grid(column=1,row=0,pady=10)
		self.baudLabel = Label(self.leftFrame1,text="Baud: ")
		self.baudLabel.grid(column=0,row=1,pady=10)
		self.baudEntry = Entry(self.leftFrame1,textvariable=self._BAUDVAR)
		self.baudEntry.grid(column=1,row=1,pady=10)

		#Number of traces
		self.leftFrame2 = LabelFrame(self.leftFrame,text="Traces")
		self.leftFrame2.pack(side=TOP,expand=1,fill=BOTH,pady=4)
		self.nTracesLabel = Label(self.leftFrame2,text="N of traces: ")
		self.nTracesLabel.grid(column=0,row=0,pady=10)
		self.nTracesEntry = Entry(self.leftFrame2,textvariable=self._NTRACES)
		self.nTracesEntry.grid(column=1,row=0,pady=10)
		self.startTraceLabel = Label(self.leftFrame2,text="Trace to plot: ")
		self.startTraceLabel.grid(column=0,row=1,pady=10)
		self.startTraceEntry = Entry(self.leftFrame2,textvariable=self._TRACETOPLOT)
		self.startTraceEntry.grid(column=1,row=1,pady=10)	
		
		#Personalized scale
		self.leftFrame3 = LabelFrame(self.leftFrame,text="Set scale")
		self.leftFrame3.pack(side=TOP,expand=1,fill=BOTH,pady=4)

		self.relChkButton = Checkbutton(self.leftFrame3,text="Use advanced functions")
		self.relChkButton["variable"] = self._RELTVAR
		self.relChkButton["command"] = self.relativeScale
		self.relChkButton.grid(row=0,columnspan=3,pady=10)

		self.labA = Label(self.leftFrame3,text="Zoom scale")
		self.labA.grid(row=1,column=1,pady=10)
		self.labB = Label(self.leftFrame3,text="ADC V range")
		self.labB.grid(row=1,column=2,pady=10)

		self.scaleLabelM = Label(self.leftFrame3,text="Max: ")
		self.scaleLabelM.grid(row=2,column=0,pady=10)
		self.scEntryMA = Entry(self.leftFrame3,textvariable=self._MAXABSVAR,state=DISABLED,width=12)
		self.scEntryMA.grid(row=2,column=1,pady=10)
		self.scEntryMB = Entry(self.leftFrame3,textvariable=self._MAXVOLTVAR,state=DISABLED,width=12)
		self.scEntryMB.grid(row=2,column=2,pady=10)

		self.scaleLabelm = Label(self.leftFrame3,text="Min: ")
		self.scaleLabelm.grid(row=3,column=0,pady=10)
		self.scEntrymA = Entry(self.leftFrame3,textvariable=self._MINABSVAR,state=DISABLED,width=12)
		self.scEntrymA.grid(row=3,column=1,pady=10)
		self.scEntrymB = Entry(self.leftFrame3,textvariable=self._MINVOLTVAR,state=DISABLED,width=12)
		self.scEntrymB.grid(row=3,column=2,pady=10)
		
		self.noiseChkButton = Checkbutton(self.leftFrame3,text="Enable Anti-Noise",variable=self._NOISVAR)
		self.noiseChkButton["state"] = DISABLED
		self.noiseChkButton.grid(row=4,columnspan=3,pady=10)

		self.UnoiseChkButton = Checkbutton(self.leftFrame3,text="Enable Ultra-AntiNoise",variable=self._NOISVAR2)
		self.UnoiseChkButton["state"] = DISABLED
		self.UnoiseChkButton.grid(row=5,columnspan=3,pady=10)
		
		
		#Start, stop and default buttons
		self.leftFrame4 = LabelFrame(self.leftFrame,text="Commands")
		self.leftFrame4.pack(side=TOP,expand=1,fill=BOTH,pady=4)
		self.startButton = Button(self.leftFrame4,text="Start Sampling",state=ACTIVE)
		self.startButton["command"] = self.start
		self.startButton.pack(side=TOP,expand=1,fill=BOTH)
		self.stopButton = Button(self.leftFrame4,text="Stop Sampling",state=DISABLED)
		self.stopButton["command"] = self.stop
		self.stopButton.pack(side=TOP,expand=1,fill=BOTH)
		
		Separator(self.leftFrame4,orient=HORIZONTAL).pack(side=TOP,expand=1,fill=BOTH)
		
		self.restoreDefaultButton = Button(self.leftFrame4,text="Restore Default")
		self.restoreDefaultButton["command"] = self.restoreDefault
		self.restoreDefaultButton.pack(side=TOP,expand=1,fill=BOTH)


		"""
			Center Frame design
		"""
		self.drawCanva = Canvas(self.centerFrame,bg="#FFFFFF",height=530,width=870)
		self.drawCanva.pack(expand=1,fill=BOTH)
		self.drawAxis()


		"""
			Right Frame design
		"""
		self.topFrame2 = LabelFrame(self.rightFrame,text="Save data")
		self.topFrame2.pack(expand=1,fill=BOTH,side=TOP,pady=4)
		self.pathButton = Button(self.topFrame2,text="Select path...",state=ACTIVE)
		self.pathButton["command"] = self.definePath
		self.pathButton.pack(side=TOP)
		self.saveChkButton = Checkbutton(self.topFrame2,text="Save data",variable=self._SAVEVAR)
		self.saveChkButton["state"] = DISABLED
		self.saveChkButton.pack(fill=X,expand=1)

		self.topFrame3 = LabelFrame(self.rightFrame,text="Read data")
		self.topFrame3.pack(expand=1,fill=BOTH,side=TOP,pady=4)
		self.readDataButt = Button(self.topFrame3,text="Read data",state=ACTIVE)
		self.readDataButt.pack(fill=X,expand=1)


		"""
				Bottom Frame design
		"""
		self.bottomFrame = Frame(self.mainApp)
		self.bottomFrame.pack(fill=BOTH,expand=1,side=BOTTOM)
		Separator(self.bottomFrame,orient=HORIZONTAL).pack(side=TOP,expand=1,fill=BOTH)
		self.statusLabel = Label(self.bottomFrame,textvariable=self._STATUSVAR)
		self.statusLabel.pack(expand=1,fill=BOTH)
		self._STATUSVAR.set("Ready")
		
		self.mainApp.bind_all("<Control-C>",self.restoreDefaultHandler)
		self.mainApp.mainloop()



	"""
		Draw the main axis on the canva. DO NOT CHANGE NUMERICAL VALUES!
	"""
	def drawAxis(self):

		#y relative voltage axis
		self.drawCanva.create_line(840,510,840,10,arrow=LAST,arrowshape=(8,10,3))

		#y absolute value axis
		self.drawCanva.create_line(40,510,40,10,arrow=LAST,arrowshape=(8,10,3))

		#x axis
		self.drawCanva.create_line(40,510,840,510,arrow=LAST,arrowshape=(8,10,3)) 

		#Draw a scale on the x axis 
		x = 40
		while x<840:
			self.drawCanva.create_line(x,510,x,515)
			x += 30

		#Analog values
		x = 510.0
		nums = 0
		while x>10.0:
			self.drawCanva.create_line(35,x,40,x)
			self.drawCanva.create_text(20,x,text=str(nums),fill="#2222CC")
			nums += 100
			x -= 48.83

		#Draw a scale on the y axes for values and voltages
		#Default mode
		if self._RELTVAR.get() == 0:
			#Voltages
			x = 510.0
			nums = 0.0
			while x>5:
				self.drawCanva.create_line(840,x,845,x)
				self.drawCanva.create_line(40,x,840,x,dash=(7,1,1,1),fill="#BBBBBB")
				self.drawCanva.create_text(860,x,text=str(nums),fill="#CC2222")
				x -= 100.0
				nums += 1.0
				
		#Re-scaled mode
		else:
			try:
				#Central point of the y axis
				medium = (float(self._MINABSVAR.get())+float(self._MAXABSVAR.get()))/2.0
				#Coefficient that says how many points are contained in 50 pixels
				coeff = (abs(float(self._MINABSVAR.get())-float(self._MAXABSVAR.get()))*25.0/500.0)
			except:
				showwarning(title="Invalid values",message="Invalid scaling parameters. Check and change them.")	
				return "ERR"		
			x = 260.0
			nums = medium
			color = "#BBBBBB"
			while x>=10:
				self.drawCanva.create_line(840,x,845,x)
				if x == 260.0 and nums != 2.5:
					self.drawCanva.create_line(40,x,840,x,dash=(7,1,1,1),fill="#DD2288")
				else:
					self.drawCanva.create_line(40,x,840,x,dash=(7,1,1,1),fill=color)
				self.drawCanva.create_text(860,x,text=str(round(nums,2)),fill="#CC2222")
				x -= 25.0
				nums += coeff

			x = 285.0
			nums = medium-coeff
			while x<=510:
				self.drawCanva.create_line(840,x,845,x)
				self.drawCanva.create_line(40,x,840,x,dash=(7,1,1,1),fill=color)
				self.drawCanva.create_text(860,x,text=str(round(nums,2)),fill="#CC2222")
				x += 25.0
				nums -= coeff



	"""
		Enable/disable commands according to the state of reltvar
	"""
	def relativeScale(self):
		if self._RELTVAR.get() == 0:
			self.scEntryMA["state"] = DISABLED
			self.scEntrymA["state"] = DISABLED
			self.scEntryMB["state"] = DISABLED
			self.scEntrymB["state"] = DISABLED
			self.noiseChkButton["state"] = DISABLED
			self.UnoiseChkButton["state"] = DISABLED
		elif self._RELTVAR.get() == 1:
			self.scEntryMA["state"] = ACTIVE
			self.scEntrymA["state"] = ACTIVE
			self.scEntryMB["state"] = ACTIVE
			self.scEntrymB["state"] = ACTIVE
			self.noiseChkButton["state"] = ACTIVE
			self.UnoiseChkButton["state"] = ACTIVE



	"""
		Start the sampling operation		
	"""
	def start(self):
		global _RUN

		self.drawCanva.delete("all")
		if self.drawAxis()=="ERR":
			return
		try:			
			self.serialComm = Serial(self._PORTVAR.get(),int(self._BAUDVAR.get()))
			self.stopButton["state"] = ACTIVE
			self.startButton["state"] = DISABLED
			self.baudEntry["state"] = DISABLED
			self.portEntry["state"] = DISABLED
			self.relChkButton["state"] = DISABLED
			self.restoreDefaultButton["state"] = DISABLED
			self.pathButton["state"] = DISABLED
			self.saveChkButton["state"] = DISABLED
			self.scEntryMA["state"] = DISABLED
			self.scEntrymA["state"] = DISABLED
			self.scEntryMB["state"] = DISABLED
			self.scEntrymB["state"] = DISABLED
			self.noiseChkButton["state"] = DISABLED
			self.UnoiseChkButton["state"] = DISABLED
		
			self.fp = None
			if self._SAVEVAR.get() == 1:
				self.fp = file(self._WORKVAR,'w')
			noise1 = self._NOISVAR.get()
			noise2 = self._NOISVAR2.get()
			minVol= float(self.scEntrymA.get())
			maxVol = float(self.scEntryMA.get())
			maxvadc = float(self.scEntryMB.get())
			ntraces = self._NTRACES.get()
			traceToPlot = self._TRACETOPLOT.get()
			if traceToPlot >= ntraces:
				tmp = "Trace to plot must be a number comprised between 0 and N. of traces-1."
				showerror(title="Input Error",message=tmp)
				self.restoreDefault()
				return
			self._STATUSVAR.set("Sampling")
			if traceToPlot==-1:
				self.sTh = serialThread(self.drawCanva,self._STATUSVAR,self.serialComm,self.fp,noise1,noise2,minVol,maxVol,maxvadc,ntraces,traceToPlot)
				_RUN = 1
				self.sTh.runMulti()
			else:
				self.sTh = serialThread(self.drawCanva,self._STATUSVAR,self.serialComm,self.fp,noise1,noise2,minVol,maxVol,maxvadc,ntraces,traceToPlot)
				_RUN = 1
				self.sTh.runSingle()
		except SerialException:
			tmp = "Unable to open the serial port. Default values will be restored."
			showerror(title="Serial Error",message=tmp)
			self.restoreDefault()
			return
		except:
			tmp = "Invalid input values. Check the parameters you have just entered."
			showerror(title="Input Error",message=tmp)
			self.restoreDefault()
			return



	"""
		Stop the sampling operation
	"""	
	def stop(self):
		global _RUN

		_RUN = 0
		if self.fp != None:
			self.fp.close()
		else:
			self.fp = None
		self.startButton["state"] = ACTIVE
		self.stopButton["state"] = DISABLED
		self.baudEntry["state"] = ACTIVE
		self.portEntry["state"] = ACTIVE
		self.restoreDefaultButton["state"] = ACTIVE
		self.pathButton["state"] = ACTIVE
		self.relChkButton["state"] = ACTIVE
		if self._RELTVAR.get() == 1:
			self.scEntryMA["state"] = ACTIVE
			self.scEntrymA["state"] = ACTIVE 
			self.scEntryMB["state"] = ACTIVE
			self.scEntrymB["state"] = ACTIVE 
			self.noiseChkButton["state"] = ACTIVE
			self.UnoiseChkButton["state"] = ACTIVE
		else:
			self.scEntryMA["state"] = DISABLED
			self.scEntrymA["state"] = DISABLED
			self.scEntryMB["state"] = DISABLED
			self.scEntrymB["state"] = DISABLED 
			self.noiseChkButton["state"] = DISABLED
			self.UnoiseChkButton["state"] = DISABLED
		self._STATUSVAR.set("Ready")
		self.saveChkButton["state"] = DISABLED
		
		self.serialComm.close()
	
	
	
	"""
		Restore default parameters and default button states. Handler for critical events.
	"""
	def restoreDefaultHandler(self,handler):
		global _RUN
		_RUN = 0
		self.startButton["state"] = ACTIVE
		self.stopButton["state"] = DISABLED
		self.baudEntry["state"] = ACTIVE
		self.portEntry["state"] = ACTIVE
		self.restoreDefaultButton["state"] = ACTIVE
		self.pathButton["state"] = ACTIVE
		self.relChkButton["state"] = ACTIVE
		self.saveChkButton["state"] = DISABLED
		self.scEntryMA["state"] = DISABLED
		self.scEntrymA["state"] = DISABLED
		self.scEntryMB["state"] = DISABLED
		self.scEntrymB["state"] = DISABLED
		self.noiseChkButton["state"] = DISABLED
		self.UnoiseChkButton["state"] = DISABLED

		self._SAVEVAR.set(0)
		self._BAUDVAR.set(_defaultBaud)
		self._PORTVAR.set(_defaultPort)
		self._PATHVAR.set(_defaultPathVar)
		self._FILEVAR.set("")
		self._WORKVAR = "" 
		self._RELTVAR.set(0)
		self._MINABSVAR.set("0")
		self._MAXABSVAR.set("5")
		self._MINVOLTVAR.set("0")
		self._MAXVOLTVAR.set("5")
		self._NOISVAR.set(0)
		self._NOISVAR2.set(0)
		self._STATUSVAR.set("Ready")
		self._NTRACES.set(1)
		self._TRACETOPLOT.set(-1)



	"""
		Restore default parameters and default button states
	"""
	def restoreDefault(self):
		global _RUN
		_RUN = 0
		self.startButton["state"] = ACTIVE
		self.stopButton["state"] = DISABLED
		self.baudEntry["state"] = ACTIVE
		self.portEntry["state"] = ACTIVE
		self.restoreDefaultButton["state"] = ACTIVE
		self.pathButton["state"] = ACTIVE
		self.relChkButton["state"] = ACTIVE
		self.saveChkButton["state"] = DISABLED
		self.scEntryMA["state"] = DISABLED
		self.scEntrymA["state"] = DISABLED
		self.scEntryMB["state"] = DISABLED
		self.scEntrymB["state"] = DISABLED
		self.noiseChkButton["state"] = DISABLED
		self.UnoiseChkButton["state"] = DISABLED

		self._SAVEVAR.set(0)
		self._BAUDVAR.set(_defaultBaud)
		self._PORTVAR.set(_defaultPort)
		self._PATHVAR.set(_defaultPathVar)
		self._FILEVAR.set("")
		self._WORKVAR = "" 
		self._RELTVAR.set(0)
		self._MINABSVAR.set("0")
		self._MAXABSVAR.set("5")
		self._MINVOLTVAR.set("0")
		self._MAXVOLTVAR.set("5")
		self._NOISVAR.set(0)
		self._NOISVAR2.set(0)
		self._STATUSVAR.set("Ready")
		self._NTRACES.set(1)
		self._TRACETOPLOT.set(-1)



	"""
		Define path to save the sampling data in
		Here a new TopLevel window is created.
		This window is blocking towards the main application:
		in this way you cannot modify other parameters if you don't 
		choose a file to save datas in as first.
	"""
	def definePath(self):

		self.pathTL = Toplevel()
		self.pathTL.title("Save in")
		self.pathTL.grab_set()

		#Set path
		self.mainPathFrame = Frame(self.pathTL)
		self.mainPathFrame.pack(expand=1,fill=BOTH)
		self.pathLabel = Label(self.mainPathFrame,text="Path: ")
		self.pathLabel.grid(column=0,row=0)
		self.pathEntry = Entry(self.mainPathFrame,textvariable=self._PATHVAR,width=40)
		self.pathEntry.grid(column=1,row=0)
		self.fileNameLabel = Label(self.mainPathFrame,text="Filename: ")
		self.fileNameLabel.grid(column=0,row=1)

		self._FILEVAR.set(self.createFilename())

		self.fileNameEntry = Entry(self.mainPathFrame,textvariable=self._FILEVAR,width=40)
		self.fileNameEntry.grid(column=1,row=1)

		#OK, Default and Cancel buttons
		self.OKButton = Button(self.mainPathFrame,text="OK")
		self.OKButton["command"] = self.confirmPath
		self.OKButton.grid(column=0,row=2,pady=20)
		self.defaultButton = Button(self.mainPathFrame,text="Default")
		self.defaultButton["command"] = self.defaultPath
		self.defaultButton.grid(column=1,row=2,pady=20)
		self.cancelButton = Button(self.mainPathFrame,text="Cancel")
		self.cancelButton["command"] = self.cancelPath
		self.cancelButton.grid(column=2,row=2,pady=20)



	"""
		Check if the path to save the sampled data in is valid
	"""
	def confirmPath(self):
		if self._FILEVAR.get() == "":
			showwarning(title="Error",message="Filename cannot be an empty string.")
			return
		if not os.path.exists(self._PATHVAR.get()):
			os.makedirs(self._PATHVAR.get())
		self._WORKVAR = str(self._PATHVAR.get())+str(self._FILEVAR.get())
		try:
			fp = file(self._WORKVAR,'r')
			fp.close()
			showwarning(title="Error",message="File already exists. Choice another filename.")
		except IOError:
			fp = file(self._WORKVAR,'w')
			fp.close()
			self.saveChkButton["state"] = ACTIVE
			self.pathTL.destroy()
		except:
			showwarning(title="Error",message="Invalid filename.")



	"""
		Restore default path
	"""
	def defaultPath(self):
		self._FILEVAR.set(self.createFilename())
		self._PATHVAR.set(_defaultPathVar)



	"""
		If you change your mind at last...
	"""
	def cancelPath(self):
		self.pathTL.destroy()



	"""
		Create a useful filename in the format yyyymmdd_hhmmss
	"""
	def createFilename(self):
		timeStruct = time.gmtime()
		name = ""
		tmp = ""
		for i in range(0,6):
			if i == 3:
				name = name + "_"
				tmp = str(timeStruct[i]+1)
			if len(str(timeStruct[i]))==1:
				tmp = "0"+str(timeStruct[i])
			else:
				tmp = str(timeStruct[i])
			name = name+str(tmp)
		return name



"""
	Serial Thread used to read datas from serial port and to plot
	a value on the screen in real-time
"""
class serialThread(Thread):
	def __init__(self,canva,statusvar,serial,fp,antinoise,antinoiseUltra,minVoltage,maxVoltage,maxvadc,ntraces,traceToPlot):
		Thread.__init__(self)
		self.traceToPlot = traceToPlot
		self.ntraces = ntraces
		self.canva = canva
		self.statusvar = statusvar
		self.serial = serial
		self.fp = fp
		self.antinoise = antinoise
		self.antinoiseUltra = antinoiseUltra
		self.minVoltage = minVoltage
		self.maxVoltage = maxVoltage
		self.maxVoltageADC = maxvadc

	def runMulti(self):
		global _RUN

		col = ["#00aa00","#aa0000","#0000aa","#aaaa00","#aa00aa","#00aaaa"]

		self.x = [40] * self.ntraces			#Initialize cursor x positions
		self.prvValues = [0] * self.ntraces		#Initialize previous values
		coeff = self.maxVoltageADC*500.0/(self.maxVoltage-self.minVoltage)/1024.0	#Pixel per unit
		while _RUN:

			if self.antinoiseUltra == 1:
				self.finalValues = [0.0] * self.ntraces
				for i in range(10):
					self.vals = self.getValues()
					for j in range(self.ntraces):
						self.finalValues[j] = self.finalValues[j] + self.vals[j]
				for j in range(self.ntraces):
					self.finalValues[j] = self.finalValues[j]/10
			elif self.antinoise == 1 and self.antinoiseUltra == 0:
				self.finalValues = [0.0] * self.ntraces
				for i in range(5):
					self.vals = self.getValues()
					for j in range(self.ntraces):
						self.finalValues[j] = self.finalValues[j] + self.vals[j]
				for j in range(self.ntraces):
					self.finalValues[j] = self.finalValues[j]/5
			else:
				self.finalValues = self.getValues()

			try:
				#Convert the absolute value (0-maxADC) into a coordinate of y
				for j in range(self.ntraces):
					self.finalValues[j] = (float(self.finalValues[j])*coeff)-(500.0/(self.maxVoltage-self.minVoltage))*float(self.minVoltage)	
				
				#Save in the file
				if self.fp != None:
					self.fp.write(str(self.finalValues)+"\n")

				#Plot the final values on the canva
				for i in range(self.ntraces):
					if self.x[i] > 840:
						self.canva.delete("lines")
						self.canva.update()
						self.x[i] = 40
					#Paint this if you select antinoiseUltra button. This condition is dominant
					if self.antinoiseUltra == 1:
						self.canva.create_line(self.x[i],510-self.prvValues[i],self.x[i]+2,510-int(self.finalValues[i]),tags="lines",fill=col[i],width=2.0)
						self.canva.update()
						self.x[i] += 2
					#Paint this if you didn't select anything
					elif self.antinoise == 0 and self.antinoiseUltra == 0:
						self.canva.create_line(self.x[i],510-self.prvValues[i],self.x[i]+3,510-int(self.finalValues[i]),tags="lines",fill=col[i],width=2.0)
						self.canva.update()
						self.x[i] += 3
					#Paint this if you select antinoise button
					elif self.antinoise == 1 and self.antinoiseUltra == 0:
						self.canva.create_line(self.x[i],510-self.prvValues[i],self.x[i]+2,510-int(self.finalValues[i]),tags="lines",fill=col[i],width=2.0)
						self.canva.update()
						self.x[i] += 2
					self.prvValues[i] = self.finalValues[i]
			except:
				pass

		else:
			return
			
	def runSingle(self):
		global _RUN

		col = "#aa0000"

		self.x = 40					#Initialize cursor x position
		self.prvValue = 0			#Initialize previous value
		coeff = 500.0/1024.0		#Pixel per unit
		while _RUN:
			if self.antinoiseUltra == 1:
				self.finalValue = 0.0
				for i in range(10):
					self.finalValue = self.finalValue + self.getValues()[self.traceToPlot]
				self.finalValue = self.finalValue/10
			elif self.antinoise == 1 and self.antinoiseUltra == 0:
				self.finalValue = 0.0
				for i in range(5):
					self.finalValue = self.finalValue + self.getValues()[self.traceToPlot]
				self.finalValue = self.finalValue/5
			else:
				self.finalValue = self.getValues()[self.traceToPlot]

			try:
				#Convert the absolute value (0-maxADC) into a coordinate of y
				self.finalValue = ((float(self.finalValue)*coeff-float(self.minVoltage)*100.0)/(float(self.maxVoltage)-float(self.minVoltage)))*5.0
				
				#Save in the file
				if self.fp != None:
					self.fp.write(str(self.finalValue)+"\n")

				#Plot the final value on the canva
				if self.x > 840:
					self.canva.delete("lines")
					self.canva.update()
					self.x = 40
				#Paint this if you select antinoiseUltra button. This condition is dominant
				if self.antinoiseUltra == 1:
					self.canva.create_line(self.x,510-self.prvValue,self.x+2,510-int(self.finalValue),tags="lines",fill=col,width=2.0)
					self.canva.update()
					self.x += 2
				#Paint this if you didn't select anything
				elif self.antinoise == 0 and self.antinoiseUltra == 0:
					self.canva.create_line(self.x,510-self.prvValue,self.x+3,510-int(self.finalValue),tags="lines",fill=col,width=2.0)
					self.canva.update()
					self.x += 3
				#Paint this if you select antinoise button
				elif self.antinoise == 1 and self.antinoiseUltra == 0:
					self.canva.create_line(self.x,510-self.prvValue,self.x+2,510-int(self.finalValue),tags="lines",fill=col,width=2.0)
					self.canva.update()
					self.x += 2
				self.prvValue = self.finalValue
			except:
				pass
			
		else:
			return


	def getValues(self):
		#Read from the serial and convert to integer
		buff = ""
		try:
			sym = self.serial.read()
			while sym != "\n" and len(buff) < 64:
				buff = buff + sym
				sym = self.serial.read()
			values = buff.split(" ")
			finalValues = []
			i = 0
			while i < len(values):
				finalValues.append(int(values[i]))
				i += 1
			if len(finalValues) != self.ntraces:
				self.statusvar.set("Problem: number of traces received different from the one given")
				raise Exception
			else:
				self.statusvar.set("Sampling")
		except:
			return [0] * self.ntraces
		
		return finalValues
			


""" 
	Create an instance of the class 
"""
Plotter()








