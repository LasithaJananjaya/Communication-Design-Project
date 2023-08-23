#!/usr/bin/env python

from gnuradio import gr
from gnuradio import audio
from array    import array     # Array
import wx
import os                   # Operating System dependent call
import socket               # Socket
import sys                  # System call
import TypeConverterModule  # Type converter
import DBPSKDemod           # DBPSK Demodulation
import GMSKDemod	          # GMSK Demodulation


# Define dialog component
ID_START_LISTEN = 100
ID_DBPSK_DEMODULATE = 101
ID_GMSK_DEMODULATE = 106
ID_STORE_DBPSK = 102
#ID_STORE_GMSK = 103
ID_EXIT  = 105

# ---------------------------------------
# Class: Main window
# ---------------------------------------
class MainWindow(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size = (320, 240))
        self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A statusbar in the bottom of the window
        #Setting up the menu
        filemenu=wx.Menu()
        filemenu.Append(ID_START_LISTEN, "&Start Listen", "Start Listen")
        filemenu.Append(ID_DBPSK_DEMODULATE, "&DBPSK_Demodulate", "DBPSK_Demodulate")
        filemenu.Append(ID_GMSK_DEMODULATE, "&GMSK_Demodulate", "GMSK_Demodulate")
        filemenu.Append(ID_STORE_DBPSK, "&Store DBPSK/DQPSK demod file", "remove the first byte")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT, "&Exit", "Terminate the program")
        # Creating the menubar
        menuBar=wx.MenuBar()
        menuBar.Append(filemenu, "&File",) #Adding the filemenu to the MenuBar
        self.SetMenuBar(menuBar) #Adding the MenuBar to the Frame content
        wx.EVT_MENU(self, ID_START_LISTEN, self.OnStartListen)
        wx.EVT_MENU(self, ID_DBPSK_DEMODULATE, self.OnDBPSK_Demodulate)
        wx.EVT_MENU(self, ID_GMSK_DEMODULATE, self.OnGMSK_Demodulate)
        wx.EVT_MENU(self, ID_STORE_DBPSK, self.OnStoreDBPSK)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)   #attach the menu-event ID_EXIT to method self.OnExit
        self.Show(True) # Note the capital on 'True'
        
    def OnStartListen(self, e):
        HOST = ''                 # Symbolic name meaning the local host
        PORT = 5000              # Arbitrary non-privileged port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(2)                 # 2 = max client number
        print 'Waiting to accept'
        conn, addr = s.accept()
        print 'New connection is established'
        print 'socket_ID is',conn
        print 'socket for listen is', s.getsockname()
        print 'server port of accept is',conn.getsockname()
        print 'Connected by', addr
        
        # Receive File
        arrTmpData = []             # string
        #arrImg = array('B')    # unsigned char
        arrImg = []
        while (1):
            data=conn.recv(1000)
            #arrTmpData = repr(data) # Convert binary to string
            #print 'arrTmpData=:', arrTmpData
            #print data
            
            i = 0
            while i < len(data):
                objTypeConv = TypeConverterModule.TypeConverter()
                lData  = objTypeConv.char2int(data[i])  # Convert char to int
                arrImg.append(lData)
                i += 1
            #print 'arrImg from receiver= ', arrImg
            if not data:
                break
        conn.close()
        print 'receive total = ', len(arrImg), 'bytes'
        
        # Construct graph
        fg = gr.flow_graph()
        bytes_src = gr.vector_source_b(arrImg, False)
        fg.connect(bytes_src, gr.file_sink(gr.sizeof_char, "SocketRecv.char"))
        fg.start()
        fg.stop()
	self.control.SetValue('[Receive file] - finish!')
    
    def OnDBPSK_Demodulate(self, e):
        # -------------------------------------------------------------
        # DBPSK Demodulation
        # -------------------------------------------------------------
        fg = gr.flow_graph()
    	objDemod = DBPSKDemod.dbpsk_demod(fg)
        fg.connect(gr.file_source(gr.sizeof_gr_complex, "SocketRecv.char"), objDemod)
        self.control.SetValue('[DBPSK Demodulation] - Start DBPSK Demodulation')
        fg.start()
        #raw_input('Enter to exit: ')
        fg.stop()  
    
        self.control.SetValue('[DBPSK Demodulation] - Finish DBPSK Demodulation')
  
    def OnGMSK_Demodulate(self, e):
        # -------------------------------------------------------------
        # GMSK Demodulation
        # -------------------------------------------------------------
        fg = gr.flow_graph()
    	objDemod = GMSKDemod.gmsk_demod(fg)
        fg.connect(gr.file_source(gr.sizeof_gr_complex, "SocketRecv.char"), objDemod)
        self.control.SetValue('[GMSK Demodulation] - Start GMSK Demodulation')
        fg.start()
        #raw_input('Enter to exit: ')
        fg.stop()
        self.control.SetValue('[GMSK Demodulation] - Finish GMSK Demodulation')


    #actually this function should be integrate into DBPSK, since it is not common for other mudulation to remove first byte! But the fg should be close to generate the files, so, we need to put this processing(remove one byte) by another event!

    def OnStoreDBPSK(self, e):
        fpR = open('DBPSKDemod.dat', 'r')
        fpW = open('Output.dat', 'w')
        
        # Read the data and convert to unsigned short
        #arrImg = ReadFile(fpR)
        
        # Store to Jpeg file
        index = 0
        while True:
            data = fpR.read(1)  # Read data, 1 byte each time
            if len(data) == 0:  # If reach EOF, finish the loop
                break
            
            if index == 0:      # We don't need the first element
                index += 1
            else:
                fpW.write(data)
        fpR.close()
        fpW.close()
    """
        objTypeConv = TypeConverterModule.TypeConverter()
        for i in len(arrImg):
            if(i>0):
                ch = objTypeConv.int2char(arrImg[i])  # Convert int to char
                fpW.write(ch)
        self.control.SetValue('[Write File] - Finish!')
    """
    
    def OnExit(self, e):
        self.Close(True) #Close the frame, note capitalization of 'T' in 'True'

# ---------------------------------------
# Main
# ---------------------------------------
app = wx.PySimpleApp()
frame = MainWindow(None, -1, "Receiver")
app.MainLoop()
