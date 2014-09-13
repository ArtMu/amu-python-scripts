
import stringParser
import sys
import collections
import wx
 
class StrFrequentCounter(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="Frequency of the strings:", pos=(20, 30))
        
        # Buttons
        self.SearchButton = wx.Button(self, label="Search", pos=(350, 325))
        self.Bind(wx.EVT_BUTTON, self.start_search, self.SearchButton)
        
        self.QuitButton = wx.Button(self, label='Quit', pos=(435, 325))
        self.Bind(wx.EVT_BUTTON, self.ExitApp, self.QuitButton)
        
        # Textboxes
        self.textBox = wx.TextCtrl(self, pos=(5, 50), size=(270, 450), style = wx.TE_MULTILINE)
        self.textBoxFrq = wx.TextCtrl(self, pos=(280, 50), size=(40, 450), style = wx.TE_MULTILINE)
        
        # Input textboxes where user can add values
        self.quote2 = wx.StaticText(self, label="File extension:", pos=(350, 40))
        self.textBoxFileType = wx.TextCtrl(self, pos=(350, 55), value = "log", size=(70, 25))
 
        self.quote3 = wx.StaticText(self, label="Min Length of the string:", pos=(350, 80))
        self.textBoxMinLen = wx.TextCtrl(self, pos=(350, 95), value = "4", size=(70, 25))

        self.quote4 = wx.StaticText(self, label="Max Length of the string:", pos=(350, 120))
        self.textBoxMaxLen = wx.TextCtrl(self, pos=(350, 135), value = "32", size=(70, 25))
                
        # Available directories Combobox Control
        self.quote5 = wx.StaticText(self, label="Founded Directories:", pos=(350, 165))
        self.sampleList = stringParser.parser().list_available_dirs()
        self.edithear = wx.ComboBox(self, pos=(350, 185), size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)

        # Radio Boxes
        #radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue', 'black', 'gray']
        #rb = wx.RadioBox(self, label="What color would you like ?", pos=(20, 210), choices=radioList,  majorDimension=3,
        #                    style=wx.RA_SPECIFY_COLS)
        #self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
   
    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        pass
        #self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
    
    def start_search(self, event):
        path = self.edithear.GetValue()
        suffix = self.textBoxFileType.GetValue()
        min_len = self.textBoxMinLen.GetValue()
        max_len = self.textBoxMaxLen.GetValue()
        
        print "## suffix: " + suffix
        arr = stringParser.parser().search_valid_files(suffix, path, min_len, max_len)
        self.write_results(arr)

    def ExitApp(self, event):
        sys.exit(0)
    
    def write_results(self, result_array):
        # Clear old results
        self.textBox.Clear()
        self.textBoxFrq.Clear()
        frq_counter = collections.Counter(result_array)
        for id in frq_counter:
            print "## id %s freq %s " %(id, frq_counter[id])
            self.textBox.WriteText(id + "\n")
            self.textBoxFrq.WriteText(str((frq_counter[id]))+"\n")
            
app = wx.App(False)
frame = wx.Frame(None)
panel = StrFrequentCounter(frame)
frame.Show()
app.MainLoop()