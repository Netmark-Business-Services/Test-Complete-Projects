﻿# Separate login function
def login_to_health_edge(username, password):
    TestedApps.HealthEdge_Manager.Run(1, True)
    healthEdge_Manager = Aliases.HealthEdge_Manager
    loginForm = healthEdge_Manager.LoginForm
    
    loginForm.textEditUserName.TextBoxMaskBox.Click(130, 11)
    loginForm.textEditUserName.TextBoxMaskBox.SetText(username)
    
    loginForm.textEditPassword.TextBoxMaskBox.Click(139, 5)
    loginForm.textEditPassword.TextBoxMaskBox.SetText(password)
    
    loginForm.lookUpEditServers.Click(166, 8)
    popupLookUpEditForm = healthEdge_Manager.PopupLookUpEditForm
    popupLookUpEditForm.Click(41, 71)
    
    loginForm.simpleButtonSubmit.ClickButton()


  


