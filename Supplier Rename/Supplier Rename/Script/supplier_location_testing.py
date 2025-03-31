# Defining global variables
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
    global j  # To modify the global j variable
    global process_count 
    j = start_index
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    WBrowCount = gridControl.wRowCount
    
    Log.Message(f"row count in this page is {WBrowCount}")
    Log.Message(f"Processing row {j}")
    
    while j < WBrowCount:
        try:
            gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
            rej_claim_id = str(gridControl.wValue[j, 1])
            Log.Message(f"processing claim: " + rej_claim_id)
            
            # Check if rej_claim_id is not in DNU_CLAIM_ID
            if rej_claim_id not in DNU_CLAIM_ID and rej_claim_id not in modified_claim_id:
                review_reason = gridControl.wValue[j, 10]
                reasons = str(review_reason)
                Log.Message(f"reason in row {j} is {reasons}")
    
                edit_row(j)
                combinedaddress = edit_claim_form()
                headerGroupControl2 = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.payToAddressControl.headerGroupControlPayToAddress
                #headerGroupControl2.HeaderGroupHyperLinkEdit.Click(7, 10)
  
                subEntityPanel = headerGroupControl2.address.subEntityPanelPostalAddress
      # Extracting address
                addressTextBox = subEntityPanel.autoEditAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
                addressTextBox.Click(135, 6)
                address = str(addressTextBox.wText)
    
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
                set_address_text.SetText(address)
                #textBoxMaskBox = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditLocationAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
                #textBoxMaskBox.SetText(address)
      
                panelControl.panelControlSearch.simpleButtonSearch.ClickButton()
                xtraMessageBoxForm = healthEdge_Manager.WaitAliasChild("XtraMessageBoxForm2", 1000)
                
                if xtraMessageBoxForm.Exists:
                    Log.Message("Data not Found")
                    healthEdge_Manager.XtraMessageBoxForm2.SimpleButton.ClickButton()
                    Aliases.HealthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonCancel.ClickButton()
                    DNU_CLAIM_ID.append(rej_claim_id)
                    j += 1
                    #reject_count += 1
                    #Log.Message(f"rejected claim count = " + reject_count)
                    close_claim_editor()
                    #process_grid_rows(j + 1)
                    continue  # Go to the next row
                
                gridControl = Aliases.HealthEdge_Manager.ResolveDialog.panelControlResults.BaseResultGrid.gridControlResults
                gcvalue = gridControl.wValue[0, 0]
                Log.Message(f"{gcvalue}")
                modified_claim_id.append(rej_claim_id)
                #gc_extracted = str(gcvalue).split(" - ")[1].strip()
                #Log.Message(f"extracted string : {gc_extracted}")
                healthEdge_Manager = Aliases.HealthEdge_Manager
                healthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonOK.ClickButton()
                #process_count += 1
               # Log.Message(f"processed claim count = " + process_count)
                healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
                Log.Message(f"submitted claim {rej_claim_id} with supplier id {supplier_id} with address {combinedaddress} " )
                promptForReasonCode = healthEdge_Manager.PromptForReasonCode
                promptForReasonCode.panelReason.lookUpEditReasonCode.Click(238, 10)
                healthEdge_Manager.PopupLookUpEditForm.Click(187, 24)
                promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
                aqUtils.Delay(8000)
                #Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Refresh")
                aqUtils.Delay(3000)
                #if gc_extracted == address:
                 #   Log.Message(f"extracted string {gc_extracted} matches with address in claim {address}")
                 #   simpleButton = healthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonOK
                 #   simpleButton.ClickButton()
                    #process_grid_rows(j + 1)
                #else:
                #    Log.Message("not matching")
                    #process_grid_rows(j + 1)
            else:
              continue                    
        except Exception as e:
            Log.Error(f"Error processing row {j}: {str(e)}")
        
        
        aqUtils.Delay(1000)
    

# Function to edit a row
def edit_row(row_index):
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    gridControl.ClickCellXY(row_index, "Edit", 16, 14)

# Part 5 - Editing claim form to retrieve address and NPI ID
def edit_claim_form():
      aqUtils.Delay(32000)
      claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
      claimEditor.Activate()
      headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
      headerGroupControl.HeaderGroupHyperLinkEdit.Click(57, 7)
      aqUtils.Delay(2000)
      #Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.payToAddressControl.headerGroupControlPayToAddress.HeaderGroupHyperLinkEdit.Click(7, 8)
      headerGroupControl2 = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.payToAddressControl.headerGroupControlPayToAddress
      headerGroupControl2.HeaderGroupHyperLinkEdit.Click(7, 10)
  
      subEntityPanel = headerGroupControl2.address.subEntityPanelPostalAddress
      # Extracting address
      addressTextBox = subEntityPanel.autoEditAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
      addressTextBox.Click(135, 6)
      address = str(addressTextBox.wText)
      Log.Message("The address is: " + address)
  
      address2TextBox = subEntityPanel.autoEditAddress2.panelControlAutoEdit.TextEdit.TextBoxMaskBox
      address2TextBox.Click(119, 9)
      address2 = str(address2TextBox.wText).strip()
      Log.Message("The address 2 is: " + address2)
  
      # Extract and log the city details
      cityTextBox = subEntityPanel.autoEditCityName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
      cityTextBox.Click(78, 6)
      city = str(cityTextBox.wText)
      Log.Message("The city is: " + city)
  
  # Extract and log the state details
      stateLookUpEdit = subEntityPanel.autoEditState.panelControlAutoEdit.LookUpEdit
      stateLookUpEdit.Click(69, 8)
      state = str(stateLookUpEdit.Text)
      Log.Message("The state is: " + state)
      
      # Get the abbreviated state name
      state1 = state_abbreviations.get(state, "Unknown")
      Log.Message("The abbreviated state is: " + state1)
  
  # Extract and log the zip code details
      zipTextBox = subEntityPanel.autoEditZipCode.panelControlAutoEdit.TextEdit.TextBoxMaskBox
      zipTextBox.Click(32, 4)
      zipCode = str(zipTextBox.Text)
      Log.Message("The zip code is: " + zipCode)
      
      # Extract only the first 5 digits of the ZIP code
      zip1 = zipCode[:5]
      Log.Message("The first 5 digits of the ZIP code are: " + zip1)
  
      if address2:
        combinedaddress = f"{address}, {city}, {state1}, {zip1}"
      else:
        combinedaddress = f"{address}, {city}, {state1}, {zip1}"
        Log.Message("Combined details: " + combinedaddress)

      return combinedaddress

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

Test1()