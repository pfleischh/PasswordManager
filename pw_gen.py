#!/usr/bin/env pythonw

"""

Password Manager

Peter Fleischhacker
Aaron Pierson
Maren VanDenTop

May/June 2020 - CIS293 Project 1

"""

import sys
import os
import random
import sqlite3
import csv
import re
import wx
import wx.lib.mixins.inspection
import wx.lib.mixins.listctrl as listmix
import webbrowser

AppTitle = "Password Manager"
iPasswords = 0
filePath = "./AA_db.db"

"""
auto-generated password functions
"""
def shuffle(string):
    tempList = list(string)
    random.shuffle(tempList)
    return ''.join(tempList)

def randChar(length=2):
    characters = '@#$%&!'
    return ''.join((random.choice(characters)) for i in range(length))

def randUpper(length=1):
    uppers = chr(random.randint(65, 90))
    return ''.join((random.choice(uppers)) for i in range(length))

def randLower(length=1):
    lowers = chr(random.randint(97, 122))
    return ''.join((random.choice(lowers)) for i in range(length))

def randDigit(length=1):
    digits = chr(random.randint(48, 57))
    return ''.join((random.choice(digits)) for i in range(length))

def password(length=8):
    # generate random characters using above functions
    uppercaseLetter1 = randUpper()
    uppercaseLetter2 = randUpper()
    lowercaseLetter1 = randLower()
    lowercaseLetter2 = randLower()
    digit1 = randDigit()
    digit2 = randDigit()
    specialChars = randChar()

    # Generate password using all the characters, in random order
    password = uppercaseLetter1 + uppercaseLetter2 + lowercaseLetter1 + \
        lowercaseLetter2 + digit1 + digit2 + specialChars
    return shuffle(password)

#-------------------------------------------------------------------------------

class DbConnection(object):
  
    def __init__(self):
        #database info
        self.database_dir = wx.GetApp().GetDatabaseDir()
        dbFile = os.path.join(self.database_dir, filePath)
        
       #connect to database
        self.con = sqlite3.connect(dbFile, isolation_level=None,
                                   detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.con.cursor()

        try:
            # create/execute userPasswords table. 
            self.cur.execute("""CREATE TABLE IF NOT EXISTS userPasswords (
                                    pwID             INTEGER       PRIMARY KEY,
                                    Website          VARCHAR (140),
                                    URL              VARCHAR (140),
                                    Login            VARCHAR (40),
                                    Question         VARCHAR (100),
                                    Answer           VARCHAR (100),
                                    Password         VARCHAR (15));
                             """)
        
        except sqlite3.OperationalError:
            wx.LogMessage("already exists")
            return
            
        #commit
        self.con.commit()

    def OnQuery(self, sSQL):
        # Execute query 
        self.cur.execute(sSQL)
        rsRecordSet = self.cur.fetchall()
        
        return rsRecordSet

    def OnQueryParameter(self, sSQL, sParameter):
        # Query Parameters
        Parameter =(sParameter, )
        self.cur.execute(sSQL, Parameter)
        rsRecordSet = self.cur.fetchall()
            
        return rsRecordSet


    def OnQueryUpdate(self, sSQL, sParameter):   
        # update query
        self.cur.execute(sSQL, sParameter)
        rsRecordSet = self.cur.fetchall()
            
        return rsRecordSet

    def OnCloseDb(self):
        # Disconnect from server.
        self.cur.close()
        self.con.close()

#-------------------------------------------------------------------------------

class InsertDlg(wx.Dialog):
    """
    pop up for inserting new record
    """
    def __init__(self, caller_dlgInsert, title=""):
        wx.Dialog.__init__(self,
                            parent=caller_dlgInsert,
                            id=-1,
                            title="")

        self.caller = caller_dlgInsert
        
        # simplified function calls
        self.ConnectDb()
        self.CreateCtrls()
        self.BindEvents()
        self.DoLayout()
    
    #---------------------------------------------------------------------------
    
    def ConnectDb(self):
        # connect to db      
        self.con = DbConnection()
 
    def CreateCtrls(self):
        """
        labels, textboxes, and buttons for the dialog
        """
    
        # font settings
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
            
        # panel
        self.panel = wx.Panel(self)

        #-- pwID
        
        self.strPasswordID = wx.StaticText(self.panel, -1, "Password ID:")
        self.strPasswordID.SetForegroundColour("gray")
        self.strPasswordID.SetFont(font)
    
        self.text_pwID = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
    
        #-- website
        
        self.strWebsite = wx.StaticText(self.panel, -1, "Website:")
        self.strWebsite.SetForegroundColour("gray")
        self.strWebsite.SetFont(font)
    
        self.txtWebsite = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
    
        #-- url
        
        self.strURL = wx.StaticText(self.panel, -1, "URL:")
        self.strURL.SetForegroundColour("gray")
        self.strURL.SetFont(font)
    
        self.txtURL = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
    
        #-- login
    
        self.strLogin = wx.StaticText(self.panel, -1, "Login:")
        self.strLogin.SetForegroundColour("gray")
        self.strLogin.SetFont(font)
    
        self.txtLogin = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
        
        #-- question
    
        self.strSecQ = wx.StaticText(self.panel, -1, "Security Question:")
        self.strSecQ.SetForegroundColour("gray")
        self.strSecQ.SetFont(font)
    
        self.txtSecQ = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
        
        #-- answer
    
        self.strSecA = wx.StaticText(self.panel, -1, "Security Answer:")
        self.strSecA.SetForegroundColour("gray")
        self.strSecA.SetFont(font)
    
        self.txtSecA = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
        
        #-- password
    
        self.strPassword = wx.StaticText(self.panel, -1, "Password:")
        self.strPassword.SetForegroundColour("gray")
        self.strPassword.SetFont(font)
    
        self.txtPassword = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
        
        #-- box sizer
    
        self.StaticSizer = wx.StaticBox(self.panel, -1, "")
    
        #-- buttons
        
        self.btnSave = wx.Button(self.panel, -1, "&Save")
        self.btnSave.SetToolTip("Save")
    
        self.btnClose = wx.Button(self.panel, -1, "&Close")
        self.btnClose.SetToolTip("Close")

        self.btnGenerate = wx.Button(self.panel, -1, "&Generate")
        self.btnGenerate.SetToolTip("Generate Random Password")
    
    def BindEvents(self):
        """
        consolidated bind function for all controls in the insert dialog frame
        """

        self.Bind(wx.EVT_BUTTON, self.OnSave, self.btnSave)
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.btnClose)
        self.Bind(wx.EVT_BUTTON, self.OnGenerate, self.btnGenerate)
    
        self.Bind(wx.EVT_CLOSE, self.OnExit)
    
    def DoLayout(self):
        """
        create and set sizers for the layout
        """
    
        # Sizers.
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        textSizer.AddGrowableCol(1)
        
        buttonSizer = wx.StaticBoxSizer(self.StaticSizer, wx.VERTICAL)
        
        # Assign widgets to sizers.
    
        # textSizer.
        textSizer.Add(self.strPasswordID, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.text_pwID, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strWebsite, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.txtWebsite, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        textSizer.Add(self.strURL, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.txtURL, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strLogin, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.txtLogin, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strSecQ, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.txtSecQ, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strSecA, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.txtSecA, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strPassword, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.txtPassword, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
            
        # buttonSizer.
        buttonSizer.Add(self.btnSave)
        buttonSizer.Add((5, 5), -1)
        buttonSizer.Add(self.btnClose)
        buttonSizer.Add((5, 5), -1)
        buttonSizer.Add(self.btnGenerate)
        
        # Assign to mainSizer the other sizers. 
        mainSizer.Add(textSizer, 0, wx.ALL, 10)
        mainSizer.Add(buttonSizer, 0, wx.ALL, 10)
        
        # Assign to panel the mainSizer.
        self.panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)
    
    def Validators(self):
        
        if len(self.text_pwID.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "Password ID" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.text_pwID.SetFocus()
                
                return 0
        
        elif len(self.txtWebsite.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "Website" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.txtWebsite.SetFocus()
                
                return 0
        
        elif len(self.txtURL.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "URL" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.txtURL.SetFocus()
                
                return 0
        
        elif len(self.txtLogin.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "Login" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.txtLogin.SetFocus()
                
                return 0

        elif len(self.txtPassword.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "Password" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.txtPassword.SetFocus()
                
                return 0
        
        try:
            pwIDint = int(self.text_pwID.GetValue())

        except ValueError:
            wx.MessageBox('ATTENTION !\nInvalid "Password ID" field\nPlease enter an integer',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
            return 0

    def OnSave(self, event):

        if self.Validators() == 0:
            
            return
        
        else:
            sMessage = "Save new password?"
            dlgAsk = wx.MessageDialog(None,
                                        sMessage,
                                        AppTitle,
                                        wx.YES_NO | wx.ICON_QUESTION)
            
            answer = dlgAsk.ShowModal()
            
            if (answer == wx.ID_YES):               
                sPasswordID = str(self.text_pwID.GetValue())
                sWebsite = str(self.txtWebsite.GetValue())
                sURL = str(self.txtURL.GetValue())             
                sLogin = str(self.txtLogin.GetValue()) 
                sSecQ = str(self.txtSecQ.GetValue())  
                sSecA = str(self.txtSecA.GetValue())  
                sPassword = str(self.txtPassword.GetValue())    
                
                InsertParameters = (sPasswordID,
                                    sWebsite,
                                    sURL,
                                    sLogin,
                                    sSecQ,
                                    sSecA,
                                    sPassword)

                sSQL = "INSERT INTO userPasswords (pwID, \
                                                Website, \
                                                URL, \
                                                Login, \
                                                Question, \
                                                Answer, \
                                                Password) \
                                        VALUES (?, ?, ?, ?, ?, ?, ?)"

                # try to insert new password in the database.
                # if pwID primary key already used, throws error
                
                try: 
                    self.con.OnQueryUpdate(sSQL, InsertParameters)
                    self.caller.OnUpdateList()

                    dlgAsk.Destroy()
                    self.OnExit(self)
                
                except sqlite3.IntegrityError:
                    wx.MessageBox("This Password ID has already been used",
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                    self.text_pwID.SetFocus()
                    self.text_pwID.SelectAll()

            elif (answer == wx.ID_NO):
                wx.MessageBox("Insert operation aborted !",
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                dlgAsk.Destroy()
                self.OnExit(self)

    def OnGenerate(self, event):
        self.txtPassword.SetValue(password())
        self.txtPassword.SetFocus()
        self.txtPassword.SelectAll()
       
    def OnExit(self, event):
        """
        close insert dialog
        """
        self.Destroy()

#-------------------------------------------------------------------------------
       
class UpdateDlg(wx.Dialog):
    """
    class for updating existing records
    """
    def __init__(self, caller_dlgUpdate, title=""):
        wx.Dialog.__init__(self,
                           parent=caller_dlgUpdate,
                           id=-1,
                           title=title,
                           size=(400, 200))
        
        self.caller = caller_dlgUpdate

        # simple call functions
        self.ConnectDb()
        self.CreateCtrls()
        self.BindEvents()
        self.DoLayout()

    #------ update functions:

    def ConnectDb(self):
        # connect to db
        self.con = DbConnection()

    def CreateCtrls(self):
        """
        labels, textboxes, and buttons for the dialog
        """

        # font settings
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)

        #panel
        self.panel = wx.Panel(self)

        #-- pwid
        
        self.strPasswordID = wx.StaticText(self.panel, -1, "Password ID:")
        self.strPasswordID.SetForegroundColour("gray")
        self.strPasswordID.SetFont(font)

        self.textUp_pwID = wx.TextCtrl(self.panel, -1, "", size=(230, -1),
                                        style=wx.TE_READONLY | wx.TE_CENTRE)
        self.textUp_pwID.SetForegroundColour("white")
        self.textUp_pwID.SetBackgroundColour("gray")
        self.textUp_pwID.SetFont(font)

        #-- web
        
        self.strWebsite = wx.StaticText(self.panel, -1, "Website :")
        self.strWebsite.SetForegroundColour("gray")
        self.strWebsite.SetFont(font)

        self.textUp_web = wx.TextCtrl(self.panel, -1, "", size=(230, -1))

        #-- url
        
        self.strURL = wx.StaticText(self.panel, -1, "URL:")
        self.strURL.SetForegroundColour("gray")
        self.strURL.SetFont(font)
    
        self.textUp_url = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
    
        #-- login
    
        self.strLogin = wx.StaticText(self.panel, -1, "Login:")
        self.strLogin.SetForegroundColour("gray")
        self.strLogin.SetFont(font)
    
        self.textUp_login = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
        
        #-- question
    
        self.strSecQ = wx.StaticText(self.panel, -1, "Security Question:")
        self.strSecQ.SetForegroundColour("gray")
        self.strSecQ.SetFont(font)
    
        self.textUp_secq = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
        
        #-- answer
    
        self.strSecA = wx.StaticText(self.panel, -1, "Security Answer:")
        self.strSecA.SetForegroundColour("gray")
        self.strSecA.SetFont(font)
    
        self.textUp_seca = wx.TextCtrl(self.panel, -1, "", size=(230, -1))
        
        #-- password
    
        self.strPassword = wx.StaticText(self.panel, -1, "Password:")
        self.strPassword.SetForegroundColour("gray")
        self.strPassword.SetFont(font)
    
        self.textUp_pw = wx.TextCtrl(self.panel, -1, "", size=(230, -1))

        #--
        
        self.StaticSizer = wx.StaticBox(self.panel, -1,"")

        #--
        
        self.bntSave = wx.Button(self.panel, -1, "&Save")
        self.bntSave.SetToolTip("Save !")

        self.bntClose = wx.Button(self.panel, -1, "&Close")
        self.bntClose.SetToolTip("Close !")

        self.btnGenerate = wx.Button(self.panel, -1, "&Generate")
        self.btnGenerate.SetToolTip("Generate A New Password")

        self.sep1 = wx.StaticText(self.panel, -1, '      ')

        self.btnVisit = wx.Button(self.panel, -1, "&Visit")
        self.btnVisit.SetToolTip("Visit Website")

    def BindEvents(self):
        """
        consolidated bind function for all controls in the insert dialog frame
        """

        self.Bind(wx.EVT_BUTTON, self.OnSave, self.bntSave)
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.bntClose)
        self.Bind(wx.EVT_BUTTON, self.OnGenerate, self.btnGenerate)
        self.Bind(wx.EVT_BUTTON, self.OnVisit, self.btnVisit)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def DoLayout(self):
        """
        create and set sizers for the layout
        """

        # Sizers.
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        textSizer.AddGrowableCol(1)
        
        buttonSizer = wx.StaticBoxSizer(self.StaticSizer, wx.VERTICAL)
        
        # Assign widgets to sizers.

        # textSizer.
        textSizer.Add(self.strPasswordID, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.textUp_pwID, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        textSizer.Add(self.strWebsite, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.textUp_web, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        textSizer.Add(self.strURL, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.textUp_url, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strLogin, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.textUp_login, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strSecQ, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.textUp_secq, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strSecA, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.textUp_seca, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        textSizer.Add(self.strPassword, 0, wx.ALIGN_CENTER_VERTICAL)
        textSizer.Add(self.textUp_pw, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        # buttonSizer.
        buttonSizer.Add(self.bntSave)
        buttonSizer.Add((5, 5), -1)
        buttonSizer.Add(self.bntClose)
        buttonSizer.Add((5, 5), -1)
        buttonSizer.Add(self.btnGenerate)
        buttonSizer.Add(self.sep1)
        buttonSizer.Add((5, 5), -1)
        buttonSizer.Add(self.btnVisit)
       
        # Assign to mainSizer the other sizers.  
        mainSizer.Add(textSizer, 0, wx.ALL, 10)
        mainSizer.Add(buttonSizer, 0, wx.ALL, 10)
        
        # Assign to panel the mainSizer.
        self.panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)

    def Validators(self):

        if len(self.textUp_pwID.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "Password ID" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.textUp_pwID.SetFocus()
                
                return 0
        
        elif len(self.textUp_web.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "Website" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.textUp_web.SetFocus()
                
                return 0
        
        elif len(self.textUp_url.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "URL" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.textUp_url.SetFocus()
                
                return 0
        
        elif len(self.textUp_login.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "Login" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.textUp_login.SetFocus()
                
                return 0

        elif len(self.textUp_pw.GetValue()) == 0:
                wx.MessageBox('ATTENTION !\nThe "Password" field is empty',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
                
                self.textUp_pw.SetFocus()
                
                return 0
        
        try:
            pwIDint = int(self.textUp_pwID.GetValue())

        except ValueError:
            wx.MessageBox('ATTENTION !\nInvalid "Password ID" field\nnPlease enter an integer',
                                AppTitle,
                                wx.OK | wx.ICON_INFORMATION)
            return 0
            
    def OnSave(self, event):

        if self.Validators()==0:
            
            return
        
        else:
            sMessage = "Save update data?"
            dlgAsk = wx.MessageDialog(None,
                                      sMessage,
                                      AppTitle,
                                      wx.YES_NO | wx.ICON_QUESTION)
            
            answer = dlgAsk.ShowModal()
            
            if (answer == wx.ID_YES):

                sPasswordID = str(self.textUp_pwID.GetValue())
                sWebsite = str(self.textUp_web.GetValue())
                sURL = str(self.textUp_url.GetValue())             
                sLogin = str(self.textUp_login.GetValue()) 
                sSecQ = str(self.textUp_secq.GetValue())  
                sSecA = str(self.textUp_seca.GetValue())  
                sPassword = str(self.textUp_pw.GetValue())    
                
                UpdateParameters = (sWebsite,
                                    sURL,
                                    sLogin,
                                    sSecQ,
                                    sSecA,
                                    sPassword,
                                    sPasswordID)

                sSQL = "UPDATE userPasswords SET Website = ?, \
                                                URL = ?, \
                                                Login = ?, \
                                                Question = ?, \
                                                Answer = ?, \
                                                Password = ? \
                                       WHERE pwID = ?"

                # Update the database.
                self.con.OnQueryUpdate(sSQL, UpdateParameters)
                self.caller.OnUpdateList()
           
                wx.MessageBox("This record has been updated",
                              AppTitle,
                              wx.OK | wx.ICON_INFORMATION)
        
            elif (answer == wx.ID_NO):
                wx.MessageBox("no information has been updated",
                              AppTitle,
                              wx.OK | wx.ICON_INFORMATION)
     
            dlgAsk.Destroy()
            self.OnExit(self)

    def OnGenerate(self, event):
        self.textUp_pw.SetValue(password())
        self.textUp_pw.SetFocus()
        self.textUp_pw.SelectAll()        

    def OnVisit(self, event):
        self.textUp_pw.SelectAll()
        self.textUp_pw.Copy()
        website = self.textUp_url.GetValue()
        webbrowser.open_new(website)

    def OnExit(self, event):
        """
        close update dialog
        """
        self.Destroy()

#-------------------------------------------------------------------------------
           
class ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        super(ListCtrl, self).__init__(parent, id, pos, size, style)
        
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        # call list control functions
        self.CreateColumns()
        self.SetProperties()

    def CreateColumns(self):
        # Add columns
        self.InsertColumn(col=0,  heading="ID", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=1,  heading="Website", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=2,  heading="URL", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=3,  heading="Login", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=4,  heading="Security Question", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=5,  heading="Security Answer", format=wx.LIST_FORMAT_LEFT)
        self.InsertColumn(col=6,  heading="Password", format=wx.LIST_FORMAT_LEFT)

        # set column widths
        self.SetColumnWidth(col=0,  width=50) 
        self.SetColumnWidth(col=1,  width=140) 
        self.SetColumnWidth(col=2,  width=140)
        self.SetColumnWidth(col=3,  width=200)
        self.SetColumnWidth(col=4,  width=200)
        self.SetColumnWidth(col=5,  width=200)
        self.SetColumnWidth(col=6,  width=200)

    def SetProperties(self):

        # Font size and style
        fontSize = self.GetFont().GetPointSize()

        boldFont = wx.Font(fontSize,
                            wx.DEFAULT,
                            wx.NORMAL,
                            wx.BOLD,
                            False, "")
        self.SetForegroundColour("#black")
        self.SetBackgroundColour("#ffffff")

        self.SetFont(boldFont)

#-------------------------------------------------------------------------------

class Frame(wx.Frame):
    
    def __init__(self, parent, id, title, 
                 style=wx.DEFAULT_FRAME_STYLE |
                       wx.NO_FULL_REPAINT_ON_RESIZE |
                       wx.CLIP_CHILDREN):
        super(Frame, self).__init__(parent=None,
                                          id=-1,
                                          title=title,
                                          style=style)
        
        # get app name
        self.app_name = wx.GetApp().GetAppName() 

        # methods
        self.ConnectDb()
        self.SetProperties()
        self.MakeMenuBar()
        self.MakeStatusBar()
        self.CreateCtrls()
        self.BindEvents()
        self.DoLayout()

    def ConnectDb(self):
        # connect to db       
        self.con = DbConnection()

    def SetProperties(self):
        # set frame properties
        self.SetTitle(("%s") % (self.app_name))
        
    def MakeMenuBar(self):
        # menu.
        mnuFile = wx.Menu()
        mnuInfo = wx.Menu()
        
        mnuExport = wx.MenuItem(mnuFile, wx.ID_FILE, "E&xport Passwords\tCtrl+E", "Exports passwords to CSV")
        mnuFile.Append(mnuExport)
        mnuQuit = wx.MenuItem(mnuFile, wx.ID_EXIT, "&Quit\tCtrl+Q", "Close Program")
        mnuFile.Append(mnuQuit)
        mnuAbout = wx.MenuItem(mnuInfo, wx.ID_ABOUT, "A&bout\tCtrl+A", "About the developers")
        mnuInfo.Append(mnuAbout)
        
        self.Bind(wx.EVT_MENU, self.OnAbout, mnuAbout)
        self.Bind(wx.EVT_MENU, self.OnExport, mnuExport)
        self.Bind(wx.EVT_MENU, self.OnExit, mnuQuit)

        # create menu bar
        menubar = wx.MenuBar()

        # Add menu titles
        menubar.Append(mnuFile, "&File")
        menubar.Append(mnuInfo, "I&nfo")
        
        self.SetMenuBar(menubar)

    def MakeStatusBar(self):  
        # Status bar
        self.statusBar = self.CreateStatusBar(1)
        self.statusBar.SetFieldsCount(2)
        self.statusBar.SetStatusWidths([-8, -4])
        self.statusBar.SetStatusText("", 0)
        self.statusBar.SetStatusText("CIS293 - Summer 2020", 1)

    def CreateCtrls(self):
        """
        Creates controls for the frame
        """

        # Font style for wx.StaticText.
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
        
        # Widgets.
        self.panel = wx.Panel(self)

        self.strPasswords = wx.StaticText(self.panel, -1, "Passwords list:")
        self.strPasswords.SetFont(font)

        #listCtrl
        self.listCtrl = ListCtrl(self.panel,
                                   -1,
                                   style=wx.LC_REPORT |
                                         wx.LC_SINGLE_SEL |
                                         wx.LC_VRULES | 
                                         wx.BORDER_SUNKEN)

        # load database
        self.passwordData = self.OnLoadData()

        # Populate the ListCtrl
        for i in self.passwordData:
            record = self.listCtrl.InsertItem(self.listCtrl.GetItemCount(),
                                             ((str(i[0]))))
            self.listCtrl.SetItem(record, 1, i[1])
            self.listCtrl.SetItem(record, 2, i[2])
            self.listCtrl.SetItem(record, 3, i[3])
            self.listCtrl.SetItem(record, 4, i[4])
            self.listCtrl.SetItem(record, 5, i[5])
            self.listCtrl.SetItem(record, 6, i[6])
             
            # Alternate the row colors of a ListCtrl.
            if record % 2:
                self.listCtrl.SetItemBackgroundColour(record, "#b2afcc")
            else:
                self.listCtrl.SetItemBackgroundColour(record, "#ffffff")
          
        self.strSearch = wx.StaticText(self.panel, -1, 'Search "Website" :')
        self.txtSearch = wx.TextCtrl(self.panel, -1, "", size=(100, -1))
        self.txtSearch.SetToolTip("Search passwords")
        
        self.StaticSizer = wx.StaticBox(self.panel, -1, "")
        self.StaticSizer.SetFont(font)
        
        self.btnSearch = wx.Button(self.panel, -1, "&Search")
        self.btnSearch.SetToolTip("Search passwords")

        self.btnClear = wx.Button(self.panel, -1, "&Clear")
        self.btnClear.SetToolTip("Clear the search text")

        self.btnShowAll = wx.Button(self.panel, -1, "&All")
        self.btnShowAll.SetToolTip("Show all")

        self.btnNew = wx.Button(self.panel, -1, "&Insert")
        self.btnNew.SetToolTip("Insert a new password")
        
        self.btnEdit = wx.Button(self.panel, -1, "&Update")
        self.btnEdit.SetToolTip("Update selected password")

        self.btnDelete = wx.Button(self.panel, -1, "&Delete")
        self.btnDelete.SetToolTip("Delete selected password")

        self.btnClose = wx.Button(self.panel, -1, "&Quit")
        self.btnClose.SetToolTip("Close")   

        self.sep1 = wx.StaticText(self.panel, -1, '        ')
        self.sep2 = wx.StaticText(self.panel, -1, '        ')

    def BindEvents(self):
        """
        Bind all the events related to my frame.
        """

        # bind ListCtrl actions
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.listCtrl)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.listCtrl)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.listCtrl)
        #bind buttons
        self.Bind(wx.EVT_BUTTON, self.OnSearch, self.btnSearch)
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.btnClear)        
        self.Bind(wx.EVT_BUTTON, self.OnShowAll, self.btnShowAll)
        self.Bind(wx.EVT_BUTTON, self.OnNew, self.btnNew)        
        self.Bind(wx.EVT_BUTTON, self.OnEdit, self.btnEdit)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.btnDelete)
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.btnClose)

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def DoLayout(self):
        # parent sizers
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.StaticBoxSizer(self.StaticSizer, wx.VERTICAL)
        btmSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # text sizers (title)
        textSizer.Add(self.strPasswords, 0, wx.BOTTOM, 5)

        textSizer.Add(self.listCtrl, 1, wx.EXPAND)

        # button sizers (on right side of list control)
        btnSizer.Add(self.strSearch)
        btnSizer.Add(self.txtSearch)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.btnSearch, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.btnClear, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.btnShowAll, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.sep1)
        btnSizer.Add(self.btnNew, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.btnEdit, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.btnDelete, 0, wx.ALL, 5)
        btnSizer.Add((5, 5), -1)
        btnSizer.Add(self.sep2)
        btnSizer.Add(self.btnClose, 0, wx.ALL, 5)

        # main sizers
        
        mainSizer.Add(textSizer, 1, wx.ALL | wx.EXPAND, 10)  
        mainSizer.Add(btnSizer, 0, wx.ALL, 10)
        
        # assign to panel
        self.panel.SetSizer(mainSizer)             
        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)

    def OnLoadData(self):
        """
        Retrieves data from the database
        """
    
        # Retrieve passwords data from database
        strSQL = "SELECT * FROM userPasswords"
        
        # The recordset retrieved
        rsRecordset = self.con.OnQuery(strSQL)
        
        return rsRecordset       

    def OnItemActivated(self, event):
        """
        what happens when a record is clicked in the list control
        """
        item = event.GetItem()        
        iPasswords = item.GetText()
        
        # Show what was selected in the frame status bar.
        self.statusBar.SetStatusText("Selected password = %s " %(iPasswords), 1)
        
        frame = self.GetTopLevelParent()         
        frame.OnEdit(event)
         
    def OnDelete(self, event):
        """
        when delete button is clicked
        """
        global iPasswords
        
        # throw error if no password selected
        if iPasswords ==0:
             wx.MessageBox("ATTENTION!\nSelect a password",
                           AppTitle,
                           wx.OK | wx.ICON_INFORMATION)
             
             return

        else:
            # confirm delete
            sMessage = "Delete selected password? %s " %(iPasswords)
            dlgAsk = wx.MessageDialog(None,
                                      sMessage,
                                      AppTitle,
                                      wx.YES_NO | wx.ICON_QUESTION)
            
            answer = dlgAsk.ShowModal()
            
            if (answer == wx.ID_YES):
                
                sSQL = "DELETE FROM userPasswords WHERE pwID = ?"
                self.con.OnQueryParameter(sSQL, iPasswords)

                self.OnShowAll(self)
                
                wx.MessageBox("SUCCESS!\nThis record has been deleted",
                              AppTitle,
                              wx.OK | wx.ICON_INFORMATION)
            
            dlgAsk.Destroy()
    
    def OnUpdateList(self):

        self.OnShowAll(self)
        
    def OnShowAll(self, event):
        
        sSQL = "SELECT * FROM userPasswords WHERE pwID LIKE ? "
        sSearch = "%"
        
        self.OnRetrieveData(sSQL, sSearch)

        self.OnClear(self)        

    def OnClear(self, event):
        # clears search
        global iPasswords
        
        sSQL = "SELECT * FROM userPasswords WHERE pwID LIKE ? "
        sSearch = "%"
        
        self.OnRetrieveData(sSQL, sSearch)
    
        self.txtSearch.Clear()
        self.txtSearch.SetFocus()

        iPasswords = 0

    def OnSearch(self, event):

        # gets search box value
        sSearch = str(self.txtSearch.GetValue())
        
        # Adds wildcard symbol
        sSearch = sSearch+"%"
        
        # throw error if search box is empty
        if sSearch == "%" :
                wx.MessageBox("ATTENTION!\nThe search text is empty",
                              AppTitle,
                              wx.OK | wx.ICON_INFORMATION)
                
                self.txtSearch.SetFocus()
                
                return
        # displays all db records that match search
        else:
            sSQL = "SELECT * FROM userPasswords WHERE Website LIKE ? "
            self.OnRetrieveData(sSQL, sSearch)

    def OnRetrieveData(self, sSQL, IDParameter):

        global iPasswords         
        
        # Delete the item from listctrl.
        self.listCtrl.SetFocus()
        self.listCtrl.DeleteAllItems()
            
        # Retrieve the recordset
        self.passwordData = self.con.OnQueryParameter(sSQL, IDParameter)

        # populate the listctrl
        if self.passwordData:
            for i in self.passwordData:
                record = self.listCtrl.InsertItem(self.listCtrl.GetItemCount(),
                                                 ((str(i[0]))))                
                self.listCtrl.SetItem(record, 1, i[1])
                self.listCtrl.SetItem(record, 2, i[2])
                self.listCtrl.SetItem(record, 3, i[3])
                self.listCtrl.SetItem(record, 4, i[4])
                self.listCtrl.SetItem(record, 5, i[5])
                self.listCtrl.SetItem(record, 6, i[6])
                
                # Alternate the row colors of a ListCtrl.
                if record % 2:
                    self.listCtrl.SetItemBackgroundColour(record, "#b2afcc")
                else:
                    self.listCtrl.SetItemBackgroundColour(record, "#ffffff")
        
        else:
             wx.MessageBox("ATTENTION!\nNo results for your search criteria\nPlease try a different search",
                           AppTitle,
                           wx.OK | wx.ICON_INFORMATION)
       
    def OnEdit(self, event):
        # edit records
        global iPasswords
        
        # throw error if no password is selected
        if iPasswords ==0:
             wx.MessageBox("ATTENTION!\nSelect a password to edit",
                           AppTitle,
                           wx.OK | wx.ICON_INFORMATION)
             return

        else:  
            sSQL = "SELECT * FROM userPasswords WHERE pwID = ?"
            self.OnOpenEdit(sSQL, iPasswords)

    def OnNew(self, event):
        
        # Create an instance of the Child_Frame.
        self.dlgInsert = self.dlgInsert = InsertDlg(caller_dlgInsert=self)
            
        sTitle = "Insert new password"
        self.dlgInsert.SetTitle(sTitle)
        self.dlgInsert.CenterOnParent(wx.BOTH)
        self.dlgInsert.ShowModal()
            
    def OnOpenEdit(self, sSQL, sParameter):

        # Retrieve data for the selected product.
        rsPasswords = self.con.OnQueryParameter(sSQL, sParameter)
            
        # Create an instance of the Child_Frame.
        self.dlgEdit = self.dlgEdit = UpdateDlg(caller_dlgUpdate=self)
            
        # Populate the fields of the frame with the recordset.
        for i in rsPasswords:
            self.dlgEdit.textUp_pwID.SetValue(str(i[0]))
            self.dlgEdit.textUp_web.SetValue(str(i[1]))
            self.dlgEdit.textUp_url.SetValue(str(i[2]))
            self.dlgEdit.textUp_login.SetValue(str(i[3]))             
            self.dlgEdit.textUp_secq.SetValue(str(i[4]))
            self.dlgEdit.textUp_seca.SetValue(str(i[5]))
            self.dlgEdit.textUp_pw.SetValue(str(i[6]))
                
            # We use this for the title of the frame.
            sWebsite =(str(i[1]))              

        sTitle = "Selected password: %s" %(sWebsite)
        self.dlgEdit.SetTitle(sTitle)
        self.dlgEdit.CenterOnParent(wx.BOTH)
        self.dlgEdit.ShowModal()
        self.dlgEdit.Destroy()

    def OnItemSelected(self, event):
        """
        what happens when you single-click a password
        """
        
        global iPasswords
        
        item = event.GetItem()        
        iPasswords = item.GetText()

        # update status bar
        self.statusBar.SetStatusText("Selected password = %s " %(iPasswords), 1)

    def OnColBeginDrag(self, event):
        """
        what happens when you drag columns
        """
        
        if event.GetColumn() == 0:
            event.Veto()

    def OnAbout(self, event):
           
        message = """Made by:\nPeter Fleischhacker\nAaron Pierson\nMaren VanDenTop\n\n
                     Class: CIS293 - Summer 2020"""

        wx.MessageBox(message,
                      AppTitle,
                      wx.OK)

    def OnExport(self, event):
        
        """
        file dialog settings:
        passwords = default name file
        CSV files = sets export extension and file type
        """
        
        with wx.FileDialog(self, "Export Location", "", "passwords", "CSV files (*.csv)|*.csv",
                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            # sets pathname to the location chosen by the user
            pathname = fileDialog.GetPath()
            
            #write all database lines to csv file
            try:
                with open(pathname, 'w') as file:
                    Records = self.OnLoadData()
                    wr = csv.writer(file, dialect='excel')
                    wr.writerow([i[0] for i in Records])
                    wr.writerows(Records)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def OnClose(self):
        """
        close Frame
        """
            
        ret = wx.MessageBox("Do you want exit?",
                            AppTitle,
                            wx.YES_NO |wx.ICON_QUESTION|
                            wx.CENTRE |wx.NO_DEFAULT)
        
        return ret
                
    def OnExit(self, event):
        """
        exit Frame
        """
        
        # Ask for exit.
        intChoice = self.OnClose()
        
        if intChoice == 2:
            # Disconnect from server.
            self.con.OnCloseDb()
            self.Destroy()

#-------------------------------------------------------------------------------

class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):

    def OnInit(self):
        #basic app info
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.SetAppName("Password Manager")
        self.installDir = os.path.split(os.path.abspath(sys.argv[0]))[0]
        
        self.InitInspection()      
        
        frame = Frame(None, -1, title="")
        frame.SetSize(1350, 527)
        self.SetTopWindow(frame)
        frame.Center()
        frame.Show(True)

        return True

    def GetDatabaseDir(self):
        #returns database directory

        if not os.path.exists("data"):
            # Create the data folder, it still doesn't exist.
            os.makedirs("data")
            
        database_dir = os.path.join(self.installDir, "data")
        return database_dir

#-------------------------------------------------------------------------------

def main():
    app = MyApp(redirect=False)
    app.MainLoop()

if __name__ == '__main__':
    main()
