#!/usr/bin/env python

from gnuradio import gr
from gnuradio import audio
from array    import array     # Array
import wx
import os                   # Operating System dependent call
import socket               # Socket
import sys                  # System call
#import GenJpegModule        # JPEG CODEC
import TypeConverterModule  # Type converter
import DBPSKMod           # DBPSK Modulation
import GMSKMod	          # GMSK Modulation

# Define dialog component
ID_PLAYSOUND = 100
ID_JPEGENC = 101
ID_DBPSK_MODULATE = 102
ID_GMSK_MODULATE = 106
ID_TRANSMIT = 103
ID_EXIT  = 105

# ---------------------------------------
# Function: Dial the tone
# ---------------------------------------
def build_graph ():

    sampling_freq = 48000
    ampl = 0.1

    fg = gr.flow_graph ()
    src0 = gr.sig_source_f (sampling_freq, gr.GR_SIN_WAVE, 350, ampl)
    src1 = gr.sig_source_f (sampling_freq, gr.GR_SIN_WAVE, 440, ampl)
    dst = audio.sink (sampling_freq)
    fg.connect ((src0, 0), (dst, 0))
    fg.connect ((src1, 0), (dst, 1))

    return fg

# -----------------------------------------
# Function: Read file and return data array
# -----------------------------------------
def ReadFile (arrImg, fpR):

    while True:
        data = fpR.read(1)  # Read data, 1 byte each time
        if len(data) == 0:  # If reach EOF, finish the loop
            break
    
        objTypeConv = TypeConverterModule.TypeConverter()
        lData  = objTypeConv.char2int(data)  # Convert char to int
    
        arrImg.append(lData) # Store data(int) into array
        #print lData, ' ', 
    
    return arrImg
    

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
        filemenu.Append(ID_PLAYSOUND, "&PlaySound","Play the tone")
        filemenu.Append(ID_JPEGENC, "&JPEG Encoder", "Generate JPEG")
        filemenu.Append(ID_DBPSK_MODULATE, "&DBPSK_Modulate", "DBPSK_Modualtion")
        filemenu.Append(ID_GMSK_MODULATE, "&GMSK_Modulate", "GMSK_Modualtion")
        filemenu.Append(ID_TRANSMIT, "&Transmit JPEG", "Transmit JPEG")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT, "&Exit", "Terminate the program")
        # Creating the menubar
        menuBar=wx.MenuBar()
        menuBar.Append(filemenu, "&File",) #Adding the filemenu to the MenuBar
        self.SetMenuBar(menuBar) #Adding the MenuBar to the Frame content
        wx.EVT_MENU(self, ID_PLAYSOUND, self.OnPlaySound) #attach the menu-event ID_ABOUT to method self.OnAbout
        wx.EVT_MENU(self, ID_JPEGENC, self.OnJpegEnc)
        wx.EVT_MENU(self, ID_DBPSK_MODULATE, self.OnDBPSK_Modulate)
        wx.EVT_MENU(self, ID_GMSK_MODULATE, self.OnGMSK_Modulate)
        wx.EVT_MENU(self, ID_TRANSMIT, self.OnTransmit)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)   #attach the menu-event ID_EXIT to method self.OnExit
        self.Show(True) # Note the capital on 'True'
        
    def OnPlaySound(self, e):
        d=wx.MessageDialog(self, "Press 'OK' to stop the tone", "Demo - Play Sound", wx.OK) #Create a message dialog box
        fg = build_graph ()
        fg.start ()
        d.ShowModal() # Shows it
        fg.stop()
        d.Destroy() # finally destroy it when finished
        
    def OnJpegEnc(self, e):
        # Open a file
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            # Get the full path of input image
            self.filename = dlg.GetFilename()
            self.dirname  = dlg.GetDirectory()
            self.fullpath = os.path.join(self.dirname, self.filename)
            
            # Join the command and send it into shell to execute
            cmd = './JpegEncoder/cjpeg -quality 80 ' + self.fullpath + ' > ./JpegEncoder/Output.jpg'
            self.control.SetValue('[Jpeg Encoder] - Start encoder')
            os.system(cmd)
            self.control.SetValue('[Jpeg Encode] - Finish !')
        dlg.Destroy()
        
    def OnDBPSK_Modulate(self, e):
        fpR = open('./JpegEncoder/Output.jpg', 'r')

        # Read the data and print
	arrImg = array('B')
    	arrImg.append(0)        # you know, for the diff encoding stuff
        arrImg = ReadFile(arrImg, fpR)
        print ' '
        print 'Total = ', len(arrImg), 'bytes'
        self.control.SetValue('[Read File] - Finish!')
     
        # -------------------------------------------------------------
        # Start to send jpeg file
        # -------------------------------------------------------------
        # Construct graph
        fg = gr.flow_graph()
        arrImg[0] = 0  # you know, for the diff encoding stuff
        bytes_src = gr.vector_source_b(arrImg, False)

    	objMod = DBPSKMod.dbpsk_mod(fg)
        fg.connect(bytes_src, objMod)
        self.control.SetValue('[DBPSK Modulation] - Start DBPSK modulation')
        fg.start()
        #raw_input('Enter to exit: ')
        fg.stop()
        self.control.SetValue('[DBPSK Modulation] - Finish DBPSK modulation')
        
    def OnGMSK_Modulate(self, e):
        fpR = open('./JpegEncoder/Output.jpg', 'r')
        
        # Read the data and print
	arrImg = array('B')
        arrImg = ReadFile(arrImg, fpR)
    	arrImg.append(0)        # Add a byte since clock recovery processing will lose last 5 bits
        print ' '
        print 'Total = ', len(arrImg), 'bytes'
        self.control.SetValue('[Read File] - Finish!')
     
        # -------------------------------------------------------------
        # Start to send jpeg file
        # -------------------------------------------------------------
        # Construct graph
        fg = gr.flow_graph()
        #arrImg[0] = 0  # you know, for the diff encoding stuff
        bytes_src = gr.vector_source_b(arrImg, False)

    	objMod = GMSKMod.gmsk_mod(fg)
        fg.connect(bytes_src, objMod)
        self.control.SetValue('[GMSK Modulation] - Start GMSK modulation')
        fg.start()
        #raw_input('Enter to exit: ')
        fg.stop()
        self.control.SetValue('[GMSK Modulation] - Finish GMSK modulation')
        
    def OnTransmit(self, e):
        HOST = '127.0.0.1'    # The remote host
        PORT = 5000            # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        
        self.control.SetValue('[Socket] - Start transmission')
        ##print 'Connected to', s.getpeername()

        fpR = open('Modulated.dat', 'r')
        while True:
            data = fpR.read(1)  # Read data
            if len(data) == 0:  # If reach EOF, finish the loop
                break
            sent=s.send(data)   # Start Transmission
        
        self.control.SetValue('[Socket] - Transmission Finish !')
    
    def OnExit(self, e):
        self.Close(True) #Close the frame, note capitalization of 'T' in 'True'

# ---------------------------------------
# Main
# ---------------------------------------
app = wx.PySimpleApp()
frame = MainWindow(None, -1, "Sender")
app.MainLoop()
