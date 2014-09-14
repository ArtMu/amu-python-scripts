#!/usr/bin/env python

# 13.09.2014 Arto M
# Currently tool search string pairs: [port/addre/mac/etc..] 1 space [Hexadecimal string]
# Last one's length is specified by user.
# User can specify also the first string, suffix of the file. Tool will report findings 
#    as a content of found strings and the number of occurene of this specific string. 
# With small modifications to the script search can be done more flexible way, user can choose the pattern for second string 
#     or search only for 1 string etc ..
  
import stringParser
import sys
import collections
import wx
 
class StrFrequentCounter(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.quote0 = wx.StaticText(self, label="Tool which search the frequency of string pairs inside given dir - structure", style=3, pos=(50, 5))
        self.quote1 = wx.StaticText(self, label="Founded Strings:        Frequency of the strings:", pos=(5, 30))

        # Buttons
        self.SearchButton = wx.Button(self, label="Search", pos=(350, 325))
        self.Bind(wx.EVT_BUTTON, self.start_search, self.SearchButton)
        
        self.QuitButton = wx.Button(self, label='Quit', pos=(435, 325))
        self.Bind(wx.EVT_BUTTON, self.ExitApp, self.QuitButton)
        
        # Textboxes
        self.textBox = wx.TextCtrl(self, pos=(5, 50), size=(270, 450), style = wx.TE_MULTILINE)
        self.textBoxFrq = wx.TextCtrl(self, pos=(280, 50), size=(40, 450), style = wx.TE_MULTILINE)
        
        # Input text-boxes where user can add values
        self.quoteFileType = wx.StaticText(self, label="File extension:", pos=(350, 40))
        self.textBoxFileType = wx.TextCtrl(self, pos=(350, 55), value = "log", size=(70, 25))
 
        self.quoteFirstStr = wx.StaticText(self, label="First string [port/addr/item..]:", pos=(350, 80))
        self.textBoxFirstStr = wx.TextCtrl(self, pos=(350, 95), value = "port", size=(70, 25))
 
        self.quote3 = wx.StaticText(self, label="Min Length of the string:", pos=(350, 120))
        self.textBoxMinLen = wx.TextCtrl(self, pos=(350, 135), value = "4", size=(70, 25))

        self.quote4 = wx.StaticText(self, label="Max Length of the string:", pos=(350, 160))
        self.textBoxMaxLen = wx.TextCtrl(self, pos=(350, 175), value = "32", size=(70, 25))
                
        # Available directories Combo-box Control
        self.quote5 = wx.StaticText(self, label="Founded Directories:", pos=(350, 200))
        self.sampleList = stringParser.parser().list_available_dirs()
        self.edithear = wx.ComboBox(self, pos=(350, 220), size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        #self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
   
        # These 2 are mandatory, can't draw the frame without
        Sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizerAndFit(Sizer)
    
    def start_search(self, event):
        path = self.edithear.GetValue()
        suffix = self.textBoxFileType.GetValue()
        first_str = self.textBoxFirstStr.GetValue()
        min_len = self.textBoxMinLen.GetValue()
        max_len = self.textBoxMaxLen.GetValue()
        
        print "## first_str: " + first_str
        arr = stringParser.parser().search_valid_files(suffix, first_str, path, min_len, max_len)
        self.write_results(arr)

    def ExitApp(self, event):
        sys.exit(0)
    
    def write_results(self, result_array):
        # Clear old results
        self.textBox.Clear()
        self.textBoxFrq.Clear()
        count = 0 # for coloring odd and even lines different colors
        frq_counter = collections.Counter(result_array)
        for id in frq_counter:
            self.print_colors(count)
            self.textBox.WriteText(id + "\n")
            self.textBoxFrq.WriteText(str((frq_counter[id]))+"\n")
            count += 1
            
    def print_colors(self, count):
        if (count % 2) == 1:
            self.textBox.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textBoxFrq.SetDefaultStyle(wx.TextAttr(wx.RED))
        else:
            self.textBox.SetDefaultStyle(wx.TextAttr(wx.GREEN))
            self.textBoxFrq.SetDefaultStyle(wx.TextAttr(wx.GREEN))

class DemoFrame(wx.Frame):
        """Main Frame holding the Panel."""
        def __init__(self, *args, **kwargs):
            """Create the DemoFrame."""
            wx.Frame.__init__(self, *args, **kwargs)

            # Add the Widget Panel
            self.Panel = StrFrequentCounter(self)
   
   
        def OnQuit(self, event=None):
            """Exit application."""
            self.Close()
        
if __name__ == '__main__':
    app = wx.App()
    frame = DemoFrame(None, title="Multi Parser", size=(600, 540), pos=(60, 60))
    frame.Show()
    app.MainLoop()