#!/usr/bin/env python

# Purpose is to have fast way to see server log issues on the left textfield.
# By giving inputs as:
# - search word: e.g. "Fail" of "ERROR"
# - Server node: your IP or domain name for server
# - Amount of lines after match: how many trace of lines the left textfield will show after the matched search word
# - start time delay: how many minutes back in history from current moment
# - end time delay: This is not implemented yet

import searchEngine
import TimeWindow
import os
import sys
import wx

class UiCreator(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        VERTICAL_ALIGNMENT_ON_RIGHT_SIDE = 950;
        self.directory = None
        
        self.quote0 = wx.StaticText(self, label="Tool which search log - lines starting of the defined search word.", style=3, pos=(50, 5))
        self.quote1 = wx.StaticText(self, label="### Founded log traces ###", pos=(5, 30))

        ##### Time - frame text-boxes
        self.quoteTimeFrame = wx.StaticText(self, label="Parsed log - file on time frame:", pos=(460, 5))
        self.textBoxTimeFrameStart = wx.TextCtrl(self, pos=(460, 25), style=wx.TE_CENTRE, value = "hr:min:sec", size=(80, 25))
        self.textBoxTimeFrameEnd = wx.TextCtrl(self, pos=(550, 25), style=wx.TE_CENTRE, value = "hr:min:sec", size=(80, 25))

        ###### Buttons #######
        # Start SSH connection
        self.sshLoginButton = wx.Button(self, label='SSH', pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 285))
        self.Bind(wx.EVT_BUTTON, self.ssh_connection, self.sshLoginButton)

        self.SearchButton = wx.Button(self, label="Parse", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 310))
        self.Bind(wx.EVT_BUTTON, self.start_search, self.SearchButton)
        
        self.QuitButton = wx.Button(self, label='Quit', pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 335))
        self.Bind(wx.EVT_BUTTON, self.ExitApp, self.QuitButton)
        
        # File browser
        self.dialog = wx.DirDialog(self, message="Browse file", defaultPath=os.getcwd(),
                                   pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 200))
        
        ##### Parsed log - file Text-box #####
        self.textBox = wx.TextCtrl(self, pos=(5, 50), size=(900, 700), style = wx.TE_MULTILINE)
        
        # Input text-boxes where user can add values
        self.quoteUsername = wx.StaticText(self, label="Username:", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 40))
        self.textBoxUsername = wx.TextCtrl(self, pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 55),
                                           value = "your-username", size=(180, 25))
 
        self.quotePassword = wx.StaticText(self, label="Password", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 80))
        self.textBoxPassword = wx.TextCtrl(self, style=wx.TE_PASSWORD, pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 95),
                                           value = "your-password", size=(180, 25))
 
        self.quote3 = wx.StaticText(self, label="String to search", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 120))
        self.textBoxParseString = wx.TextCtrl(self, pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 135),
                                              value = "ERROR", size=(180, 25))

        self.quote4 = wx.StaticText(self, label="Server node:", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 160))
        self.textBoxNodeUrl = wx.TextCtrl(self, pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 175),
                                          value = "stb-sit-itas-adp01.nix.cydmodule.com", size=(180, 25))
                
        self.numberOfLines = wx.StaticText(self, label="Amount of lines after match:", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 200))
        self.textBoxAmountOfLines = wx.TextCtrl(self, pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 215),
                                                value = "10", size=(180, 25))
  
        self.startAndEndTimes = wx.StaticText(self, label="Start time delay.    End time delay: (minutes)", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 240))
        self.textBoxTimeStampS = wx.TextCtrl(self, pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 255),
                                             value = "0", size=(50, 25))
        self.textBoxTimeStampE = wx.TextCtrl(self, pos=(1050, 255), value = "0", size=(50, 25))
        
        #### ERROR statistics - list - table - first labels #####
        self.errorStatsLabel = wx.StaticText(self, label="Amount of Matches:", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 360))
        self.errorStatsLabel = wx.StaticText(self, label="FRQ in %:     List of Errors:", pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 380))
        
        self.errorAmountTextBox = wx.TextCtrl(self, pos=(1060, 355), value = "0", size=(50, 25))
        self.errorStatisticsTextBox = wx.TextCtrl(self, pos=(1012, 400), size=(270, 220), style = wx.TE_MULTILINE|wx.HSCROLL)
        #### ERROR statistics - frequency of ERROR type #####
        self.errorFrequencyTextBox = wx.TextCtrl(self, pos=(VERTICAL_ALIGNMENT_ON_RIGHT_SIDE, 400),
                                                 size=(60, 220), style = wx.TE_MULTILINE)
        
        # Available directories Combo-box Control
        #self.quote5 = wx.StaticText(self, label="Founded Directories:", pos=(350, 200))
        #self.sampleList = searchEngine.parser().list_available_dirs()
        #self.edithear = wx.ComboBox(self, pos=(350, 220), size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        #self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
   
        # These 2 are mandatory, can't draw the frame without
        Sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizerAndFit(Sizer)
    
        self.se = searchEngine.parser()
        self.timeWindow = None
    
    def writeTimeFrame(self, startTimeStamp, latestTimestamp):
        # Write time - frame values to UI
        self.textBoxTimeFrameStart.Clear()
        self.textBoxTimeFrameEnd.Clear()

        self.textBoxTimeFrameStart.WriteText(startTimeStamp)
        self.textBoxTimeFrameEnd.WriteText(latestTimestamp)
        
    # TODOs for all methods, error handling (event argument)
    def start_search(self, path):
        # First lets set the time frame for log 
        startTime = self.textBoxTimeStampS.GetValue()
        self.timeWindow = TimeWindow.TimeWindow(int(startTime), None, None)
        startTimeStamp = self.timeWindow.create_timeframe()
        
        # TODO: if latest is None or '0' we get latest on the server.log. Otherwise we pick it from textbox!!!
        latestTimestamp = self.se.latest_timestamp()
        self.writeTimeFrame(startTimeStamp, latestTimestamp)
        
        # Create time-frame log, TODO currently endTimestamp is None = latest trace on the log file
        self.se.create_log(startTimeStamp, None)
        print "### SEARCH .... "
        parseString = self.textBoxParseString.GetValue()
        lines = self.textBoxAmountOfLines.GetValue()
        result = self.se.parse_logfile(parseString, lines)
        self.write_results(result)
        
        # Error statistics table populating
        errorDict = self.se.calc_error_statistics(result)
        self.errorFrequencyTextBox.Clear()
        self.errorStatisticsTextBox.Clear()
        for key in errorDict:
            self.errorStatisticsTextBox.WriteText(key + "\n")
            self.errorFrequencyTextBox.WriteText(errorDict[key])
        
        # Error statistics - Amount of errors
        self.errorAmountTextBox.Clear()
        self.errorAmountTextBox.WriteText(self.se.get_error_count())
                
    def ssh_connection(self, event):
        username = self.textBoxUsername.GetValue()
        password = self.textBoxPassword.GetValue()
        node = self.textBoxNodeUrl.GetValue()
        response = self.se.log_to_node(node, username, password)
        #self.textBox.Clear()
        self.textBox.WriteText(response)
        
    def ExitApp(self, event):
        searchEngine.parser().close()
        sys.exit(0)
    
    def write_results(self, result):
        # Clear old results
        self.textBox.Clear()
        #self.print_colors(1)
        self.textBox.WriteText(result)

    def print_colors(self, count):
        if (count % 2) == 1:
            self.textBox.SetDefaultStyle(wx.TextAttr(wx.RED))
            #self.textBoxFrq.SetDefaultStyle(wx.TextAttr(wx.RED))
        else:
            self.textBox.SetDefaultStyle(wx.TextAttr(wx.GREEN))
            #self.textBoxFrq.SetDefaultStyle(wx.TextAttr(wx.GREEN))

class DemoFrame(wx.Frame):
        """Main Frame holding the Panel."""
        def __init__(self, *args, **kwargs):
            """Create the DemoFrame."""
            wx.Frame.__init__(self, *args, **kwargs)

            # Add the Widget Panel
            self.Panel = UiCreator(self)
   
   
        def OnQuit(self, event=None):
            """Exit application."""
            self.Close()
        
if __name__ == '__main__':
    app = wx.App()
    frame = DemoFrame(None, title="Multi Parser", size=(1600, 800), pos=(60, 60))
    frame.Show()
    app.MainLoop()