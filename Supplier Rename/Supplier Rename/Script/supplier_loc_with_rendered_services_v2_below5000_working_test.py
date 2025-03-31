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
  #88 claims 
  array1 = ['2024190005315', '2024206001047', '2024207000063', '2024213000069', '2024213000044'
  
]
  #array1 = ['2024220001648','2024220001700','2024220001682','2024220001726','2024220001823','2024220001804','2024220002188','2024216005947','2024216005998','2024216006592','2024216006649','2024216006746','2024216006929','2024220002227','2024205000535','2024209002994','2024207001019','2024212004997','2024221003634','2024221003675','2024221003927','2024221004231','2024221004338','2024221004339','2024221004331','2024221004358','2024221004412','2024221003617','2024221004490','2024221004555','2024221004570','2024221004696','2024221004399','2024206001676','2024222003223','2024222003607','2024222003509','2024222003697','2024222003792','2024222003858','2024222003878','2024205000604','2024207001689','2024206000900','2024222004047','2024222003475','2024222004260','2024222004332','2024222004539','2024222004721','2024222004768','2024221003551','2024221003628','2024220000485','2024220000556','2024220000677','2024220000909','2024220000951','2024220000952','2024220001283','2024220001506','2024220001531','2024220001534','2024220001692','2024219001866','2024220001854','2024220001809','2024220002260','2024215004343','2024215004414','2024214009457','2024214009810','2024214009976','2024214010003','2024219001908','2024219002151','2024219002195','2024219002196','2024219002241','2024219002771','2024219002913','2024219002908','2024219003162','2024219003319','2024219003395','2024219003443','2024206001666','2024214008955']
  
  
  gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
  #WBrowCount = gridControl.wRowCount
  resultGridClaimReviewRepair = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
  resultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Clear Inputs")
  textBoxMaskBox = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.autoEditClaimHccId.panelControlAutoEdit.TextEdit
  textBoxMaskBox.TextBoxMaskBox.Click(40, 4)
  
  # Iterate through array1 and set the text one by one
  for array in array1:
      
      if array in modified_claim_id or array in DNU_CLAIM_ID:
                  Log.Message(f"Claim {array} has already been processed. Skipping.")
                  continue
      if len(modified_claim_id) + len(DNU_CLAIM_ID) == len(array1):
                                  Log.Message("All claims processed or denied, exiting the loop.")
                                  break
      textBoxMaskBox = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.autoEditClaimHccId.panelControlAutoEdit.TextEdit
      textBoxMaskBox.TextBoxMaskBox.Click(40, 4)
      textBoxMaskBox.SetText(array)
      textBoxMaskBox.Keys("[Enter]")
      aqUtils.delay(2000)
      gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
      rej_claim_id = str(gridControl.wValue[j, 1])
      Log.Message(f"processing claim: " + rej_claim_id)
      review_reason = gridControl.wValue[j, 10]
      reasons = str(review_reason)
      Log.Message(f"reason in row {j} is {reasons}")
      
      # call edit_row function    
      edit_row(j)
      claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
      claimEditor.Activate()
      subEntityPanel = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput
      subEntityPanel.panelControlSubscriber.headerGroupProvider.HeaderGroupHyperLinkEdit.Click(27, 2)
      aqUtils.Delay(2000)
      #drop down rendering services address
      headerGroupControl = subEntityPanel.renderedServicesAddressControl.headerGroupControlRenderedAddress
      headerGroupControl.HeaderGroupHyperLinkEdit.Click(10, 8)
      
      
      # Extracting address
      addressTextBox = headerGroupControl.address.subEntityPanelPostalAddress.autoEditAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
      addressTextBox.Click(123, 11)
      address = str(addressTextBox.wText)
      if address:
                    #DNU_CLAIM_ID.append(rej_claim_id)
          Log.Message("The address is: " + address)
          combinedaddress = ' '.join(address.split()[:2])
          Log.Message("The first two words of the address is: " + combinedaddress)
      else:
          DNU_CLAIM_ID.append(rej_claim_id)
          processed_count = len(modified_claim_id)
          denied_count = len(DNU_CLAIM_ID)
          Log.Message(f"modified claim ids are: {modified_claim_id}")
          Log.Message(f"Processed Claims Count:  {processed_count}")
          Log.Message(f"denied claim ids are: {DNU_CLAIM_ID}")
          Log.Message(f"Denied Claims Count:  {denied_count}")
          close_claim_editor()
          continue  # Go to the next row
                
                
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
         processed_count = len(modified_claim_id)
         denied_count = len(DNU_CLAIM_ID)
         Log.Message(f"modified claim ids are: {modified_claim_id}")
         Log.Message(f"Processed Claims Count:  {processed_count}")
         Log.Message(f"denied claim ids are: {DNU_CLAIM_ID}")
         Log.Message(f"Denied Claims Count:  {denied_count}")
         close_claim_editor()
         continue  # Go to the next row
                
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
      
      processed_count = len(modified_claim_id)
      denied_count = len(DNU_CLAIM_ID)
      Log.Message(f"modified claim ids are: {modified_claim_id}")
      Log.Message(f"Processed Claims Count:  {processed_count}")
      Log.Message(f"denied claim ids are: {DNU_CLAIM_ID}")
      Log.Message(f"Denied Claims Count:  {denied_count}")
      promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
      aqUtils.Delay(8000)
      
      Log.Message(f"denied claim ids are: {DNU_CLAIM_ID}")
      Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Refresh")
      aqUtils.Delay(3000)
      #aqUtils.Delay(1000)
    
    
    
    
    
    
    

# Function to edit a row
def edit_row(row_index):
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    gridControl.ClickCellXY(row_index, "Edit", 16, 14)
    aqUtils.Delay(9000)
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