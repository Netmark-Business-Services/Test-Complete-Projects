import os

def SaveScreenshot(file_path):
    """
    Captures the screenshot of the active window and saves it to the specified file path.
    """
    # Capture the entire screen
    aqUtils.Delay(1000)
    screenshot = Sys.Desktop.Picture()
    screenshot.SaveToFile(file_path)
    Log.Picture(screenshot, f"Screenshot saved to {file_path}")

def Login():
    """
    This function logs into the HealthEdge application.
    """
    Log.Message("Launching HealthEdge application.")
    TestedApps.HealthEdge.Run()
    
    healthEdge_Manager = Aliases.HealthEdge_Manager
    loginForm = healthEdge_Manager.LoginForm
    
    # Enter username
    Log.Message("Entering username.")
    textBoxMaskBox = loginForm.textEditUserName.TextBoxMaskBox
    textBoxMaskBox.Click()
    textBoxMaskBox.SetText("ndevineni")
    
    # Enter password
    Log.Message("Entering password.")
    textBoxMaskBox = loginForm.textEditPassword.TextBoxMaskBox
    textBoxMaskBox.Click()
    textBoxMaskBox.SetText(Project.Variables.Password1)
    
    # Select server from dropdown
    Log.Message("Selecting server.")
    loginForm.lookUpEditServers.Click()
    popupLookUpEditForm = healthEdge_Manager.PopupLookUpEditForm
    popupLookUpEditForm.Click(60, 109)
    
    # Submit login form
    Log.Message("Submitting login form.")
    loginForm.simpleButtonSubmit.ClickButton()
    
    # Wait for login to complete
    aqUtils.Delay(20000)  
