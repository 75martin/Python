import tkinter as tk
from tkinter import Tk, Frame, StringVar, Button, Text
import sys, os, wmi, psutil


class MainWindow(tk.Tk):
	def __init__(self, *args):
		tk.Tk.__init__(self)

		global i

		i = StringVar()
		stickyVar = tk.N+tk.E+tk.S+tk.W

		self.frm_base = tk.Frame(bg="dimgrey")
		self.frm_input = tk.Frame(self.frm_base, bg="dimgrey")
		self.frm_output = tk.Frame(self.frm_base, bg="white", bd=1, relief="sunken")
		self.vscroll = tk.Scrollbar(self.frm_output, orient="vertical")		
		self.lbl = tk.Label(self.frm_input, text="Host / IP: ", bg="dimgrey", fg="white", font="arial 10 bold")
		self.ent = tk.Entry(self.frm_input, text="Host / IP", bg="white", insertbackground="dimgrey", relief="sunken", bd=3, insertwidth=2, width=40, textvariable=i)
		self.btn = tk.Button(self.frm_input, text="Go!", bg="white", command=lambda:[self.ldap_con(), self.del_func(), self.get_localinfo()])
		self.txt = tk.Text(self.frm_output, bg="white", bd=2, relief="sunken", yscrollcommand=self.vscroll.set)


		self.frm_base.grid(row=0, column=0, sticky=stickyVar)
		self.frm_input.grid(row=1, column=0, columnspan=2, sticky=stickyVar, padx=10, pady=10)
		self.frm_output.grid(row=10, column=0, columnspan=3, sticky=stickyVar, padx=10, pady=(0, 10))
		self.lbl.grid(row=1, column=0, sticky=tk.W)
		self.ent.grid(row=2, column=0, sticky=tk.E +tk.W, ipady=3, padx=(0, 10))
		self.ent.insert(tk.END, "localhost")
		self.btn.grid(row=2, column=3, sticky=tk.N + tk.E + tk.S)
		self.txt.grid(row=10, column=0, columnspan=2, sticky=stickyVar)
		self.vscroll.grid(row=10, column=0, sticky=tk.N+tk.S+tk.E)
		self.vscroll.config(command=self.txt.yview)

		sys.stdout = self
		sys.stderr = self
		
	def del_func(self):
		self.txt.delete(1.0, tk.END)

	def write(self, text_out):
		self.txt.insert(tk.END, str(text_out))

	def ldap_con(self):
		try:
			wi = wmi.WMI(moniker="winmgmts:{impersonationLevel=impersonate}!//" + i.get() + "\\root\\cimv2")
			return(wi)
		except(Exception):
			print("")
			print("===== Unable to connect to remote host =====")
			#return(wmi.WMI(moniker="winmgmts:{impersonationLevel=impersonate}!//" + "localhost" + "\\root\\cimv2"))


	def get_localinfo(self):

		try:
			w = self.ldap_con()
			cs = w.Win32_Computersystem
			for csitem in cs():
				
				print("")
				print("======= Computer =======")
				print("")
				print("Computername: ",csitem.Caption)
				print("Manufacturer: ",csitem.Manufacturer)
				print("Model: ",csitem.SystemFamily + " / " + csitem.Model)
				print("Domain: ",csitem.Domain)
				print("LoggedOnUser: ",csitem.username)

			wb = w.Win32_BIOS
			for wbitem in wb():
				print("BIOS: ",wbitem.Caption)
				print("BIOS Version: ",str(wbitem.SystemBiosMajorVersion) + "." + str(wbitem.SystemBiosMinorVersion))

			se = w.Win32_SystemEnclosure
			for seitem in se():
				print("SerialNumber: ", seitem.Serialnumber)
				print("AssetTag: ", seitem.SMBIOSAssetTag)

			nac = w.Win32_NetworkAdapterConfiguration
			for nacitem in nac():
				if nacitem.IPEnabled == True:
					print("")
					print("======= Network =======")
					print("")
					print("IPv4: ",nacitem.IPAddress[0])
					print("Subnet Mask: ",nacitem.IPSubnet[0])
					print("Default Gateway: ",nacitem.DefaultIPGateway[0])
					print("DHCPServer: ",nacitem.DHCPServer)
			
			if i.get() == "localhost" and psutil.Process().username() == os.environ["userdomain"] + "\\" + os.environ["username"]:
				o = "LogonServer: NA"
				ose = os.environ.get("logonserver", o)
				osen = ose.replace("\\","")
				print("LogonServer: ",osen)

			elif psutil.Process().username() != os.environ["userdomain"] + "\\" + os.environ["username"]:
				print("LogonServer: NA")

			else:
				print("LogonServer: NA")

		except(Exception):
			print("")

	def get_adinfo(self):
		pass
			
				
root = MainWindow()
root.title("ComputerInfo")
root.geometry("400x440")
root.iconbitmap("c:\Icons\Ampeross-Qetto-2-Info.ico")
root.rowconfigure(0, weight=1)
root.frm_input.columnconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.frm_base.columnconfigure(1, weight=1)
root.frm_base.rowconfigure(10, weight=1)
root.frm_input.rowconfigure(0, weight=1)
root.frm_input.columnconfigure(0, weight=1)
root.frm_output.rowconfigure(10, weight=1)
root.frm_output.columnconfigure(0, weight=1)
root.ent.rowconfigure(0, weight=1)
root.ent.columnconfigure(0, weight=1)
root.txt.columnconfigure(0, weight=1)
root.txt.rowconfigure(0, weight=1)
root.mainloop()