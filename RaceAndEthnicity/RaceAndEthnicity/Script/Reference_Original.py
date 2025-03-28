def Test1():
  healthEdge_Manager = Aliases.HealthEdge_Manager
  homeForm = healthEdge_Manager.HomeForm
  panelControl = homeForm.panelControlDetail
  panelControl.homeTab1.WidgetsHost.WidgetContainer2.ProviderWidgetControl.xtraScrollableControlProviders.TaskRow.panelControlTop.panelControlTaskLinks.SimpleButtonSearch.ClickButton()
  searchDialog = healthEdge_Manager.SearchDialog
  textEdit = searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimplePractitionerSearchCriteria.entityPanelSearchInput.autoEditHccIdentifier.panelControlAutoEdit.TextEdit
  textBoxMaskBox = textEdit.TextBoxMaskBox
  textBoxMaskBox.Click(52, 2)
  textEdit.SetText("1100741")
  textBoxMaskBox.Keys("[Enter]")
  
  searchDialog.panelControl1.standaloneBarDockControlTasks.DockedBarControl.ClickItem("Edit")
  asOfDate = healthEdge_Manager.AsOfDate
  asOfDate.panelControlTop.radioGroupReprocessClaims.ClickItem("Do Not Reprocess Claims")
  asOfDate.codeEntryEditReasonCodes.LookUpEdit.Click(225, 9)
  popupLookUpEditForm = healthEdge_Manager.PopupLookUpEditForm
  popupLookUpEditForm.Click(111, 55)
  asOfDate.panelControlBottom.simpleButtonOK.ClickButton()
  entityEditForm = healthEdge_Manager.EntityEditForm
  practitionerEditControl = entityEditForm.panelBottom.xtraTabControlEdit.xtraTabPageEdit.PractitionerEditControl
  lookUpEdit = practitionerEditControl.entityPanelSummary.codeEntryEditRaceOrEithnicity.LookUpEdit
  lookUpEdit.Click(164, 12)
  lookUpEdit.Keys("wh")
  popupLookUpEditForm.Click(29, 9)
  
  xtraTabControl = practitionerEditControl.xtraTabControlPractitioner
  xtraTabControl.ClickTab("UDT")
  lookUpEdit = xtraTabControl.xtraTabPageUDT.entityPanelUDT.repeaterPanelUDT.RepeatableUDTList.headerGroupTitle.repeaterPanelUdtListValueSet.RepeatableUdtListValueSet.udtValueEdit.panelControlAutoEdit.LookUpEdit
  lookUpEdit.Click(626, 9)
  lookUpEdit.Keys("No")
  popupLookUpEditForm.Click(224, 4)
  entityEditForm.BarDockControl.DockedBarControl.ClickItem("Save")
  panelControl.PractitionerView.xtraTabControlPractitioner.ClickTab("UDT")
  homeForm.BarDockControl.DockedBarControl.ClickItem("Home")
