import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

address_values = []
DNU_CLAIM_ID = []
modified_claim_id = []
global process_count
process_count = 0
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
    try:
        logging.info("Starting application...")
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
        logging.info("Application started successfully.")
    except Exception as e:
        logging.error(f"Error starting application: {str(e)}")

# Part 2 - Selecting work basket
def select_workbasket():
    try:
        logging.info("Selecting work basket...")
        healthEdge_Manager = Aliases.HealthEdge_Manager
        healthEdge_Manager.HomeForm.XtraMainMenu.Click("Workbasket|Claim Review & Repair")
        aqUtils.Delay(5000)
        logging.info("Work basket selected successfully.")
    except Exception as e:
        logging.error(f"Error selecting work basket: {str(e)}")

# Part 3 - Setting filtering criteria in work basket
def set_filtering_criteria():
    try:
        logging.info("Setting filtering criteria...")
        healthEdge_Manager = Aliases.HealthEdge_Manager
        referenceMenuButton = healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.codeEntryResolverButton
        referenceMenuButton.Click(0, 8)
        referenceMenuButton.PopupMenu.Click("Look up")
        resolveDialog = healthEdge_Manager.ResolveDialog
        panelControl = resolveDialog.panelControlLeft
        entityPanel = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.CodeEntrySearchCriteria.entityPanel
        # CLICK FOR CODE
        entityPanel.autoEditCodeEntry.panelControlAutoEdit.TextEdit.SetText("1146")
        # CLICK FOR SHORT DESCRIPTION
        entityPanel.autoEditShortName.panelControlAutoEdit.TextEdit.SetText("Supplier Location Required on Claim")
        panelControl.panelControlSearch.simpleButtonSearch.Click(33, 6)
        resolveDialog.panelControlBottom.simpleButtonOK.Click(45, 11)
        logging.info("Filtering criteria set successfully.")
    except Exception as e:
        logging.error(f"Error setting filtering criteria: {str(e)}")

# Part 4 - process Grid rows
def process_grid_rows(start_index):
    global j  
    global process_count 
    j = start_index
    try:
        gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
        WBrowCount = gridControl.wRowCount
        
        logging.info(f"Row count in this page is {WBrowCount}")
        logging.info(f"Processing row {j}")
        
        while j < WBrowCount:
            try:
                gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
                rej_claim_id = str(gridControl.wValue[j, 1])
                logging.info(f"Processing claim: " + rej_claim_id)
                
                # Check if rej_claim_id is not in DNU_CLAIM_ID
                if rej_claim_id not in DNU_CLAIM_ID and rej_claim_id not in modified_claim_id:
                    review_reason = gridControl.wValue[j, 10]
                    reasons = str(review_reason)
                    logging.info(f"Reason in row {j} is {reasons}")
    
                    edit_row(j)
                    combinedaddress = edit_claim_form()
                    headerGroupControl2 = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.payToAddressControl.headerGroupControlPayToAddress
                    # headerGroupControl2.HeaderGroupHyperLinkEdit.Click(7, 10)
  
                    subEntityPanel = headerGroupControl2.address.subEntityPanelPostalAddress
                    # Extracting address
                    addressTextBox = subEntityPanel.autoEditAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
                    address = str(addressTextBox.wText)
    
                    healthEdge_Manager = Aliases.HealthEdge_Manager
                    headerGroupControl = healthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
                    claimSupplierReferenceControl = headerGroupControl.supplierReference
                    supp_code = claimSupplierReferenceControl.autoSizingPanelSupplier.textEditSupplierID.TextBoxMaskBox
                    supplier_id = str(supp_code.wText)
                    logging.info("The supplier_id is: " + supplier_id)
                    # combinedaddress = edit_claim_form()
                    referenceMenuButton = headerGroupControl.supplierLocationPanel1.autoSizingPanelLocationName.referenceMenuButtonSupplierLocation
                    referenceMenuButton.Click(9, 8)
                    referenceMenuButton.PopupMenu.Click("Look up")
    
                    panelControl = healthEdge_Manager.ResolveDialog.panelControlLeft
                    textBoxMaskBox = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit.TextBoxMaskBox
                    textBoxMaskBox.SetText(supplier_id)
                    set_address_text = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditLocationAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
                    set_address_text.SetText(address)
                    # textBoxMaskBox = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditLocationAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
                    # textBoxMaskBox.SetText(address)
      
                    panelControl.panelControlSearch.simpleButtonSearch.ClickButton()
                    xtraMessageBoxForm = healthEdge_Manager.WaitAliasChild("XtraMessageBoxForm2", 1000)
                    
                    if xtraMessageBoxForm.Exists:
                        logging.info("Data not Found")
                        healthEdge_Manager.XtraMessageBoxForm2.SimpleButton.ClickButton()
                        Aliases.HealthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonCancel.ClickButton()
                        DNU_CLAIM_ID.append(rej_claim_id)
                        j += 1
                        # reject_count += 1
                        # Log.Message(f"rejected claim count = " + reject_count)
                        close_claim_editor()
                        # process_grid_rows(j + 1)
                        continue  # Go to the next row
                
                    gridControl = Aliases.HealthEdge_Manager.ResolveDialog.panelControlResults.BaseResultGrid.gridControlResults
                    gcvalue = gridControl.wValue[0, 0]
                    logging.info(f"Found value: {gcvalue}")
                    modified_claim_id.append(rej_claim_id)
                    # gc_extracted = str(gcvalue).split(" - ")[1].strip()
                    # Log.Message(f"extracted string : {gc_extracted}")
                    healthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonOK.ClickButton()
                    # process_count += 1
                    # Log.Message(f"processed claim count = " + process_count)
                    healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
                    logging.info(f"Submitted claim {rej_claim_id} with supplier id {supplier_id} with address {combinedaddress} ")
                    promptForReasonCode = healthEdge_Manager.PromptForReasonCode
                    promptForReasonCode.panelReason.lookUpEditReasonCode.Click(238, 10)
                    healthEdge_Manager.PopupLookUpEditForm.Click(187, 24)
                    promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
                    aqUtils.Delay(8000)
                    # Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Refresh")
                    aqUtils.Delay(3000)
                    # if gc_extracted == address:
                    #     Log.Message(f"extracted string {gc_extracted} matches with address in claim {address}")
                    #     simpleButton = healthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonOK
                    #     simpleButton.ClickButton()
                        # process_grid_rows(j + 1)
                    # else:
                    #     Log.Message("not matching")
                        # process_grid_rows(j + 1)
                else:
                    continue                    
            except Exception as e:
                logging.error(f"Error processing row {j}: {str(e)}")
            
            #aqUtils.Delay(1000)
    except Exception as e:
        logging.error(f"Error in processing grid rows: {str(e)}")

# Function to edit a row
def edit_row(row_index):
    try:
        logging.info(f"Editing row {row_index}...")
        gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
        gridControl.ClickCellXY(row_index, "Edit", 16, 14)
        aqUtils.Delay(32000)
        logging.info(f"Row {row_index} edited successfully.")
    except Exception as e:
        logging.error(f"Error editing row {row_index}: {str(e)}")

# Part 5 - Editing claim form to retrieve address and NPI ID
def edit_claim_form():
    try:
        logging.info("Editing claim form...")
        claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
        claimEditor.Activate()
        headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
        
        # Wait until the headerGroupControl element is ready
        if not headerGroupControl.WaitProperty("Exists", True, 10000):
            logging.error("headerGroupControl not found.")
            return ""

        headerGroupControl.HeaderGroupHyperLinkEdit.Click(57, 7)
        aqUtils.Delay(2000)
        headerGroupControl2 = headerGroupControl.WaitChild('payToAddressControl', 10000)
        
        if not headerGroupControl2.Exists:
            logging.error("headerGroupControl2 not found.")
            return ""
        
        headerGroupControl2.HeaderGroupHyperLinkEdit.Click(7, 10)

        subEntityPanel = headerGroupControl2.address.subEntityPanelPostalAddress
        
        # Wait until the addressTextBox element is ready
        addressTextBox = subEntityPanel.autoEditAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        if not addressTextBox.WaitProperty("Exists", True, 10000):
            logging.error("addressTextBox not found.")
            return ""
        
        address = str(addressTextBox.wText)
        logging.info("The address is: " + address)

        address2TextBox = subEntityPanel.autoEditAddress2.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        address2 = str(address2TextBox.wText).strip()
        logging.info("The address 2 is: " + address2)

        cityTextBox = subEntityPanel.autoEditCityName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        city = str(cityTextBox.wText)
        logging.info("The city is: " + city)

        stateLookUpEdit = subEntityPanel.autoEditState.panelControlAutoEdit.LookUpEdit
        state = str(stateLookUpEdit.Text)
        logging.info("The state is: " + state)
   
        state1 = state_abbreviations.get(state, "Unknown")
        logging.info("The abbreviated state is: " + state1)

        zipTextBox = subEntityPanel.autoEditZipCode.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        zipCode = str(zipTextBox.Text)
        logging.info("The zip code is: " + zipCode)
   
        zip1 = zipCode[:5]
        logging.info("The first 5 digits of the ZIP code are: " + zip1)

        if address2:
            combinedaddress = f"{address}, {city}, {state1}, {zip1}"
        else:
            combinedaddress = f"{address}, {city}, {state1}, {zip1}"
     
        logging.info("Combined details: " + combinedaddress)
        return combinedaddress
    except Exception as e:
        logging.error(f"Error editing claim form: {str(e)}")
        return ""

# Close claim editor
def close_claim_editor():
    try:
        logging.info("Closing claim editor...")
        claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
        claimEditor.Activate()
        claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
        Aliases.HealthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
        aqUtils.Delay(5000)
        logging.info("Claim editor closed successfully.")
    except Exception as e:
        logging.error(f"Error closing claim editor: {str(e)}")

# Main Test Function
def Test1():
    try:
        logging.info("Starting Test1...")
        # start_application()
        # select_workbasket()
        # set_filtering_criteria()
        process_grid_rows(0)
        #combinedaddress = edit_claim_form()
        logging.info("Test1 completed successfully.")
    except Exception as e:
        logging.error(f"Error in Test1: {str(e)}")

Test1()