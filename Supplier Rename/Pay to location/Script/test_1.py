﻿def Test1():
  address = "221e Ventura Blvd, Ste 126"
  
  #edit provider information
  headerGroupControl = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
  headerGroupControl.HeaderGroupHyperLinkEdit.Click(39, 7)
  headerGroupControl.payToAddressControl.headerGroupControlPayToAddress.HeaderGroupHyperLinkEdit.Click(9, 7)
  
  
  #continuing process
  healthEdge_Manager = Aliases.HealthEdge_Manager
  referenceMenuButton = healthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.supplierLocationPanel1.autoSizingPanelLocationName.referenceMenuButtonSupplierLocation
  referenceMenuButton.Click(9, 10)
  referenceMenuButton.PopupMenu.Click("Look up")
  panelControl = healthEdge_Manager.ResolveDialog.panelControlLeft
  textBoxMaskBox = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditLocationAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
  textBoxMaskBox.SetText(address)
  
  panelControl.panelControlSearch.simpleButtonSearch.ClickButton()
  
  gridControl = Aliases.HealthEdge_Manager.ResolveDialog.panelControlResults.BaseResultGrid.gridControlResults
  gcvalue = gridControl.wValue[0,0]
  Log.Message(f"{gcvalue}")
  gc_extracted = str(gcvalue).split(" - ")[1].strip()
  Log.Message(f"extracted string : {gc_extracted}")
  if gc_extracted == address:
       Log.Message(f"extracted string {gc_extracted} matches with address in claim {address}")
       healthEdge_Manager = Aliases.HealthEdge_Manager
       simpleButton = healthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonOK
       simpleButton.ClickButton()
       #####healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
  else:
      Log.Message("not matching")
  
  
  
def Test2():
  gridControl = Aliases.HealthEdge_Manager.ResolveDialog.panelControlResults.BaseResultGrid.gridControlResults
  gcvalue = gridControl.wValue[0,0]
  Log.Message(f"{gcvalue}")
  gc_extracted = str(gcvalue).split(" - ")[1].strip()
  #re.search(r' - (.*)', gcvalue).group(1).strip()
  #gcvalue.split(" - ")[1].strip()
  Log.Message(f"extracted string : {gc_extracted}")
#  ClickCellRXY(0, "Location Name", 157, 4)
  if gc_extracted == address:
     Log.Message(f"extracted string {gc_extracted} matches with address in claim {address}")
     
     
   
     

def Test3():
  healthEdge_Manager = Aliases.HealthEdge_Manager
  healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
  promptForReasonCode = healthEdge_Manager.PromptForReasonCode
  panel = promptForReasonCode.panelReason
  panel.Click(273, 27)
  panel.lookUpEditReasonCode.Click(146, 14)
  healthEdge_Manager.PopupLookUpEditForm.Click(13, 23)
  promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
  homeForm = healthEdge_Manager.HomeForm
  homeForm.Activate()
  homeForm.BarDockControl.DockedBarControl.ClickItem("Home")

def Test4():
  headerGroupControl = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
  headerGroupControl.payToAddressControl.headerGroupControlPayToAddress.HeaderGroupHyperLinkEdit.Click(6, 11)
  headerGroupControl.headerGroupControlSubmittedSupplierInformation.HeaderGroupHyperLinkEdit.Click(8, 12)
  headerGroupControl.headerGroupControlSubmittedSupplierInformation.HeaderGroupHyperLinkEdit.Click(8, 12)
  


def Test5():
  headerGroupControl = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
  headerGroupControl.HeaderGroupHyperLinkEdit.Click(39, 7)
  headerGroupControl.payToAddressControl.headerGroupControlPayToAddress.HeaderGroupHyperLinkEdit.Click(9, 7)
#221e Ventura Blvd, Ste 126


def Test6():
  healthEdge_Manager = Aliases.HealthEdge_Manager
  referenceMenuButton = healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.codeEntryResolverButton
  referenceMenuButton.Click(0, 8)
  referenceMenuButton.PopupMenu.Click("Look up")
  resolveDialog = healthEdge_Manager.ResolveDialog
  panelControl = resolveDialog.panelControlLeft
  entityPanel = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.CodeEntrySearchCriteria.entityPanel
  entityPanel.autoEditCodeEntry.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Click(70, 8)
  entityPanel.autoEditShortName.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Click(57, 5)
  panelControl.panelControlSearch.simpleButtonSearch.Click(33, 6)
  resolveDialog.panelControlBottom.simpleButtonOK.Click(45, 11)

  
  
  
  
  
  
  
def dnu():
    healthEdge_Manager = Aliases.HealthEdge_Manager
    resultGridClaimReviewRepair = healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
    panelControl = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch

    referenceMenuButton = panelControl.codeEntryResolverButton
    referenceMenuButton.Click(12, 11)
    referenceMenuButton.PopupMenu.Click("Look up")
    resolveDialog = healthEdge_Manager.ResolveDialog
    panelControl2 = resolveDialog.panelControlLeft
    entityPanel = panelControl2.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.CodeEntrySearchCriteria.entityPanel
    entityPanel.autoEditCodeEntry.panelControlAutoEdit.TextEdit.SetText("1146")
    textEdit = entityPanel.autoEditShortName.panelControlAutoEdit.TextEdit
    textBoxMaskBox = textEdit.TextBoxMaskBox
    textBoxMaskBox.Click(31, 8)
    textBoxMaskBox.Keys("![ReleaseLast]")
    textEdit.SetText("Supplier Location Required on Claim")
    panelControl2.panelControlSearch.simpleButtonSearch.ClickButton()
    resolveDialog.panelControlBottom.simpleButtonOK.ClickButton()
    textBoxMaskBox = panelControl.textEditReviewReasonCode.TextBoxMaskBox    
    
    
    
    

def Test7():
  claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
  claimEditor.Click(1477, 25)
  headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanelConsolidatedClaim.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
  headerGroupControl.HeaderGroupHyperLinkEdit.Click(23, 12)
  headerGroupControl2 = headerGroupControl.payToAddressControl.headerGroupControlPayToAddress
  headerGroupControl2.HeaderGroupHyperLinkEdit.Click(7, 7)
  subEntityPanel = headerGroupControl2.address.subEntityPanelPostalAddress
  subEntityPanel.autoEditAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Click(86, 8)
  subEntityPanel.autoEditAddress2.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Click(81, 7)
  subEntityPanel.autoEditCityName.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Click(77, 7)
  subEntityPanel.autoEditState.panelControlAutoEdit.LookUpEdit.Click(55, 12)
  subEntityPanel.autoEditZipCode.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Click(31, 6)
