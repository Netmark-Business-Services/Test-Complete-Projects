﻿# Defining global variables
address_values = []
DNU_CLAIM_ID = []
modified_claim_id = []
global process_count
#global reject_count
process_count = 0
#reject_count = 0
j = 0
# Mapping of state names to their abbreviations
state_abbreviations = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

# Part 1 - Starting the application and logging in
def start_application():
    TestedApps.HealthEdge_Manager.Run(1, True)
    healthEdge_Manager = Aliases.HealthEdge_Manager
    loginForm = healthEdge_Manager.LoginForm
    textBoxMaskBox = loginForm.textEditUserName.TextBoxMaskBox
    textBoxMaskBox.Click(23, 3)
    textBoxMaskBox.SetText("skrishnan")
    textBoxMaskBox.Keys("[Tab]")
    loginForm.textEditPassword.TextBoxMaskBox.SetText(Project.Variables.Password1)
    loginForm.lookUpEditServers.Click(60, 9)
    healthEdge_Manager.PopupLookUpEditForm.Click(29, 73)
    loginForm.simpleButtonSubmit.ClickButton()
    aqUtils.Delay(30000)

# Part 2 - Selecting work basket
def select_workbasket():
    healthEdge_Manager = Aliases.HealthEdge_Manager
    healthEdge_Manager.HomeForm.XtraMainMenu.Click("Workbasket|Claim Review & Repair")
    aqUtils.Delay(5000)

# Part 3 - Setting filtering criteria in work basket
def set_filtering_criteria():
    healthEdge_Manager = Aliases.HealthEdge_Manager
    referenceMenuButton = healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.codeEntryResolverButton
    referenceMenuButton.Click(0, 8)
    referenceMenuButton.PopupMenu.Click("Look up")
    resolveDialog = healthEdge_Manager.ResolveDialog
    panelControl = resolveDialog.panelControlLeft
    entityPanel = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.CodeEntrySearchCriteria.entityPanel
    #CLICK FOR CODE
    entityPanel.autoEditCodeEntry.panelControlAutoEdit.TextEdit.SetText("1146")
    #CLICK FOR SHORT DESCRIPTION
    entityPanel.autoEditShortName.panelControlAutoEdit.TextEdit.SetText("Supplier Location Required on Claim")
    panelControl.panelControlSearch.simpleButtonSearch.Click(33, 6)
    resolveDialog.panelControlBottom.simpleButtonOK.Click(45, 11)
    
    
    
    
    
 
    #textBoxMaskBox.Click(117, 5)
   # textBoxMaskBox.Keys("[Enter]")

# Part 4 - process Grid rows
def process_grid_rows(start_index):
    
  
      claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
      claimEditor.Activate()
      subEntityPanel = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput
      Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanelConsolidatedClaim.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.HeaderGroupHyperLinkEdit.Click(65, 11)
      #subEntityPanel.panelControlSubscriber.headerGroupProvider.HeaderGroupHyperLinkEdit.Click(62, 4)
      #Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanelConsolidatedClaim.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.WinFormsObject("HeaderGroupHyperLinkEdit", "", 2)
      aqUtils.Delay(2000)
      #drop down rendering services address
      headerGroupControl = subEntityPanel.renderedServicesAddressControl.headerGroupControlRenderedAddress
      headerGroupControl.HeaderGroupHyperLinkEdit.Click(12, 5)
      
      #headerGroupControl = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanelConsolidatedClaim.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.renderedServicesAddressControl.headerGroupControlRenderedAddress
      #headerGroupControl.HeaderGroupHyperLinkEdit.Click(12, 5)
      #textEdit = headerGroupControl.address.subEntityPanelPostalAddress.autoEditAddress.panelControlAutoEdit.TextEdit
  
      #textEdit.TextBoxMaskBox.Click(113, 4)

      # Extracting address
      addressTextBox = headerGroupControl.address.subEntityPanelPostalAddress.autoEditAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
      addressTextBox.Click(113, 4)
      address = str(addressTextBox.wText)
      if address:
                    #DNU_CLAIM_ID.append(rej_claim_id)
          Log.Message("The address is: " + address)
          combinedaddress = ' '.join(address.split()[:2])
          Log.Message("The first two words of the address is: " + combinedaddress)
      else:
          DNU_CLAIM_ID.append(rej_claim_id)
          close_claim_editor()
          #continue  # Go to the next row
                
                
      headerGroupControl2 = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.payToAddressControl.headerGroupControlPayToAddress
      #headerGroupControl2.HeaderGroupHyperLinkEdit.Click(7, 10)
  
                    
      healthEdge_Manager = Aliases.HealthEdge_Manager
      headerGroupControl = healthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
      claimSupplierReferenceControl = headerGroupControl.supplierReference
      supp_code = claimSupplierReferenceControl.autoSizingPanelSupplier.textEditSupplierID.TextBoxMaskBox
      supplier_id = str(supp_code.wText)
      Log.Message("The supplier_id is: " + supplier_id)
      #combinedaddress = edit_claim_form()
      referenceMenuButton = headerGroupControl.supplierLocationPanel1.autoSizingPanelLocationName.referenceMenuButtonSupplierLocation
      referenceMenuButton.Click(9, 8)
      referenceMenuButton.PopupMenu.Click("Look up")
    
      panelControl = healthEdge_Manager.ResolveDialog.panelControlLeft
      textBoxMaskBox = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit.TextBoxMaskBox
      textBoxMaskBox.SetText(supplier_id)
      set_address_text = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditLocationAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
      set_address_text.SetText(combinedaddress)
      panelControl.panelControlSearch.simpleButtonSearch.ClickButton()
      xtraMessageBoxForm = healthEdge_Manager.WaitAliasChild("XtraMessageBoxForm2", 1000)
                
      if xtraMessageBoxForm.Exists:
         Log.Message("Data not Found")
         healthEdge_Manager.XtraMessageBoxForm2.SimpleButton.ClickButton()
         Aliases.HealthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonCancel.ClickButton()
         DNU_CLAIM_ID.append(rej_claim_id)
         close_claim_editor()
         #continue  # Go to the next row
                
      gridControl = Aliases.HealthEdge_Manager.ResolveDialog.panelControlResults.BaseResultGrid.gridControlResults
      gcvalue = gridControl.wValue[0, 0]
      Log.Message(f"{gcvalue}")
      modified_claim_id.append(rej_claim_id)
      healthEdge_Manager = Aliases.HealthEdge_Manager
      healthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonOK.ClickButton()
      healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
      Log.Message(f"submitted claim {rej_claim_id} with supplier id {supplier_id} with address {combinedaddress} " )
      promptForReasonCode = healthEdge_Manager.PromptForReasonCode
      promptForReasonCode.panelReason.lookUpEditReasonCode.Click(238, 10)
      healthEdge_Manager.PopupLookUpEditForm.Click(187, 24)
      promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
      aqUtils.Delay(8000)
      Log.Message(f"modified claim ids are: {modified_claim_id}")
      Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Refresh")
      aqUtils.Delay(3000)
      #aqUtils.Delay(1000)
    
    
    
    
    
    
    

# Function to edit a row
def edit_row(row_index):
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    gridControl.ClickCellXY(row_index, "Edit", 16, 14)
    aqUtils.Delay(18000)
# Close claim editor
def close_claim_editor():
    claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
    claimEditor.Activate()
    claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
    Aliases.HealthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
    aqUtils.Delay(5000)
    

          
# Main Test Function
def Test1():
    #start_application()
    #select_workbasket()
    #set_filtering_criteria()
    process_grid_rows(0)
    #combinedaddress = edit_claim_form()
    #test_procecss()

Test1()



def Test2():
  Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanelConsolidatedClaim.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.HeaderGroupHyperLinkEdit.Click(62, 4)

def Test3():
  Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanelConsolidatedClaim.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.HeaderGroupHyperLinkEdit.Click(65, 11)

def Test4():
  headerGroupControl = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanelConsolidatedClaim.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.renderedServicesAddressControl.headerGroupControlRenderedAddress
  headerGroupControl.HeaderGroupHyperLinkEdit.Click(12, 5)
  textEdit = headerGroupControl.address.subEntityPanelPostalAddress.autoEditAddress.panelControlAutoEdit.TextEdit
  
  textEdit.TextBoxMaskBox.Click(113, 4)
