﻿def Test1():
    TestedApps.HealthEdge.Run()
    healthEdge_Manager = Aliases.HealthEdge_Manager
    loginForm = healthEdge_Manager.LoginForm
    textBoxMaskBox = loginForm.textEditUserName.TextBoxMaskBox
    textBoxMaskBox.Click()
    textBoxMaskBox.SetText("vpatibandla")
  
    textBoxMaskBox = loginForm.textEditPassword.TextBoxMaskBox
    textBoxMaskBox.Click()
    textBoxMaskBox.SetText(Project.Variables.Password1)
    loginForm.lookUpEditServers.Click(60, 10)
    healthEdge_Manager.PopupLookUpEditForm.Click(57, 100)
    loginForm.simpleButtonSubmit.ClickButton()
  
    homeForm = healthEdge_Manager.HomeForm
    homeForm.panelControlDetail.homeTab1.WidgetsHost.WidgetContainer.ProviderWidgetControl.xtraScrollableControlProviders.TaskRow.panelControlTop.panelControlTaskLinks.SimpleButtonSearch.ClickButton()
    searchDialog = healthEdge_Manager.SearchDialog
    textEdit = searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleSupplierSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit
    textEdit.SetText("15840")
    textEdit.TextBoxMaskBox.Keys("[Enter]")
  
    gridControl = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults
    gridControl.DblClickCellXY(0, "Supplier Name", 77, 6)
  
    homeForm.BarDockControl.DockedBarControl.ClickItem("Open for Edit")
    asOfDate = healthEdge_Manager.AsOfDate
  
    asOfDate.panelControlTop.radioGroupReprocessClaims.ClickItem("Do Not Reprocess Claims")
    asOfDate.panelControlBottom.simpleButtonOK.ClickButton()
  
    xtraTabControl = healthEdge_Manager.EntityEditForm.panelBottom.xtraTabControlEdit.xtraTabPageEdit.SupplierEditControl.supplierDetails.xtraTabControlSupplier
    xtraTabControl.ClickTab("Contact")
  
    headerGroupControl = xtraTabControl.xtraTabPageSupplierContact.supplierDetailsContact.entityPanelSupplier.repeaterPanelOtherAddress.RepeatableSupplierCorrespondenceInformation.headerGroupControlOtherCorrespondence
    headerGroupControl.HeaderGroupHyperLinkEdit.Click()
  
    subEntityPanel = headerGroupControl.CorrespondenceInformationPanel.entityPanelCorrespondenceInformation.headerGroupControlCorrespondenceInformation.subEntityPanelAddressInformation.address1.subEntityPanelPostalAddress
  
    referenceMenuButton = subEntityPanel.referenceMenuButtonCounty
    referenceMenuButton.Click()
    referenceMenuButton.PopupMenu.Click("Look up")
    resolveDialog = healthEdge_Manager.ResolveDialog
    textEdit = resolveDialog.panelControlLeft.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.CountySearchCriteria.entityPanelSearchInput.autoEditCountyCode.panelControlAutoEdit.TextEdit
    textBoxMaskBox = textEdit.TextBoxMaskBox
    textBoxMaskBox.Click()
    textEdit.SetText("53077")
    textBoxMaskBox.Keys("[Enter]")
    resolveDialog.panelControlBottom.simpleButtonOK.ClickButton()
    textBoxMaskBox = subEntityPanel.textEditCounty.TextBoxMaskBox
    textBoxMaskBox.Click()
    textBoxMaskBox.Keys("^a^c")
  
    #excel7 = Aliases.EXCEL.wndXLMAIN.XLDESK.EXCEL7
    #excel7.Click(320, 74)
    #excel7.Click(320, 74)
    #excel7.Keys("^v")

    # Open the Excel file
    excel = Sys.OleObject("Excel.Application")
    excel.Visible = True
    workbook = excel.Workbooks.Open(r"C:\Test complete\Netmark\Projects\County longitude and latitude\county.xlsx")  # Open the existing workbook
    sheet = workbook.Sheets(2)  # Select the second sheet

    # Find the first empty row
    row = 1
    while sheet.Cells(row, 1).Value != "":
        row += 1

    # Paste the copied data into the first empty row
    copied_data = Sys.Clipboard
    sheet.Cells(row, 1).Value = copied_data

    # Save and close the workbook
    workbook.Save()
    workbook.Close(False)
    excel.Quit()

Test1()
