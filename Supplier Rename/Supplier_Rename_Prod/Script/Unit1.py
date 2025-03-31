﻿# Defining global variables
address_values = []
DNU_CLAIM_ID = []
Finished_claims = []
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
    resultGridClaimReviewRepair = healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
    panelControl = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch

    referenceMenuButton = panelControl.codeEntryResolverButton
    referenceMenuButton.Click(12, 11)
    referenceMenuButton.PopupMenu.Click("Look up")
    resolveDialog = healthEdge_Manager.ResolveDialog
    panelControl2 = resolveDialog.panelControlLeft
    entityPanel = panelControl2.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.CodeEntrySearchCriteria.entityPanel
    entityPanel.autoEditCodeEntry.panelControlAutoEdit.TextEdit.SetText("7")
    textEdit = entityPanel.autoEditShortName.panelControlAutoEdit.TextEdit
    textBoxMaskBox = textEdit.TextBoxMaskBox
    textBoxMaskBox.Click(31, 8)
    textBoxMaskBox.Keys("![ReleaseLast]")
    textEdit.SetText("Supplier could not be identified")
    panelControl2.panelControlSearch.simpleButtonSearch.ClickButton()
    resolveDialog.panelControlBottom.simpleButtonOK.ClickButton()
    textBoxMaskBox = panelControl.textEditReviewReasonCode.TextBoxMaskBox
    textBoxMaskBox.Click(117, 5)
    textBoxMaskBox.Keys("[Enter]")

# Part 4 - Checking if reason matches and editing
def process_grid_rows(start_index):
    global j  # To modify the global j variable
    j = start_index
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    WBrowCount = gridControl.wRowCount
    Log.Message(f"row count in this page is {WBrowCount}")
    Log.Message(f"Processing row {j}")

    while j < WBrowCount:
        rej_claim_id = str(gridControl.wValue[j, 1])
        Log.Message(f"processing claim: " + rej_claim_id)
        
        # Check if rej_claim_id is not in DNU_CLAIM_ID
        if rej_claim_id not in DNU_CLAIM_ID or rej_claim_id not in Finished_claims:
            review_reason = gridControl.wValue[j, 10]
            reasons = str(review_reason)
            Log.Message(f"reason in row {j} is {reasons}")

            if reasons == "Supplier could not be identified":
                edit_row(j)
                combinedaddress, NPI = edit_claim_form()
                found = check_matching_supplier(NPI)
                if found:
                  claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
                  claimEditor.Activate()
                  claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
                  Aliases.HealthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
                  aqUtils.Delay(7000)
                  DNU_CLAIM_ID.append(rej_claim_id)
                  process_grid_rows(j + 1)  # Start processing from the next row
                else:
                  supp_to_copy = search_supplier(NPI, combinedaddress)
                  if supp_to_copy:
                      Finished_claims.append(rej_claim_id)
                      paste_supplier_name(supp_to_copy)
                  else:
                      DNU_CLAIM_ID.append(rej_claim_id)
                      process_grid_rows(j + 1)
                #edit_claim_form()
                
                return True # Exit the function to handle the specific case
            else:
                # Store the claim ID in DNU_CLAIM_ID
                claim_id = str(gridControl.wValue[j, 1])
                DNU_CLAIM_ID.append(claim_id)
        else:
            # Add the rej_claim_id to DNU_CLAIM_ID
            DNU_CLAIM_ID.append(rej_claim_id)
        
        # Increment j to process the next row
        j += 1

# Function to edit a row
def edit_row(row_index):
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    gridControl.ClickCellXY(row_index, "Edit", 16, 14)

# Part 5 - Editing claim form to retrieve address and NPI ID
def edit_claim_form():
    aqUtils.Delay(15000)
    claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
    claimEditor.Activate()
    headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.headerGroupControlSubmittedSupplierInformation
    headerGroupControl.HeaderGroupHyperLinkEdit.Click(8, 8)
    entityPanel = headerGroupControl.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo

    # Extracting address
    addressTextBox = entityPanel.autoEditSubmittedSupplierInfoAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    addressTextBox.Click(123, 9)
    address = str(addressTextBox.wText)
    Log.Message("The address is: " + address)

    address2TextBox = entityPanel.autoEditSubmittedSupplierInfoAddress2.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    address2TextBox.Click(115, 9)
    address2 = str(address2TextBox.wText).strip()
    Log.Message("The address 2 is: " + address2)

    # Extract and log the city details
    cityTextBox = entityPanel.autoEditSubmittedSupplierInfoCityName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    cityTextBox.Click(114, 11)
    city = str(cityTextBox.wText)
    Log.Message("The city is: " + city)

    # Extract and log the state details
    stateLookUpEdit = entityPanel.autoEditSubmittedSupplierInfoState.panelControlAutoEdit.LookUpEdit
    stateLookUpEdit.Click(115, 9)
    state = str(stateLookUpEdit.Text)
    Log.Message("The state is: " + state)
    
    # Get the abbreviated state name
    state1 = state_abbreviations.get(state, "Unknown")
    Log.Message("The abbreviated state is: " + state1)

    # Extract and log the zip code details
    zipTextBox = entityPanel.autoEditSubmittedSupplierInfoZipCode.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    zipTextBox.Click(56, 9)
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

    # Extract and log the NPI id details
    NPILookUpEdit = entityPanel.autoEditSubmittedSupplierInfoNPI.panelControlAutoEdit.TextEdit
    NPILookUpEdit.Click(128, 8)
    NPI = str(NPILookUpEdit.Text)
    Log.Message("The NPI is: " + NPI)
    return combinedaddress, NPI

# Part 6 - Checking for matching supplier in DB
def check_matching_supplier(NPI):
    # Convert NPI to integer
    npi_int = int(NPI)
    rejected_list_npi = [
        1104877810, 1215903018, 1235866138, 1528488756,
        1609291996, 1629167457, 1639172372, 1710927231,
        1760047708, 1780656421
    ]

    # Initialize a variable to control the while loop
    found = False
    # Use while loop to check if NPI exists in the rejected_list_npi
    index = 0
    while index < len(rejected_list_npi):
        if rejected_list_npi[index] == npi_int:
            found = True
            Log.Message("NPI in rejected list")
            break
        index += 1
    return found

# Part 7 - Searching for supplier in the system
def search_supplier(NPI, combinedaddress):
    healthEdge_Manager = Aliases.HealthEdge_Manager
    healthEdge_Manager.HomeForm.BarDockControl.DockedBarControl.ClickItem("Search")
    textEdit = healthEdge_Manager.SearchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleSupplierSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit
    textEdit.SetText(NPI)
    textEdit.TextBoxMaskBox.Keys("[Enter]")

    # Wait for the XtraMessageBoxForm2 to appear
    xtraMessageBoxForm = healthEdge_Manager.WaitAliasChild("XtraMessageBoxForm2", 1000)
    if xtraMessageBoxForm.Exists:
        Log.Message("Data not Found")
        healthEdge_Manager.XtraMessageBoxForm2.SimpleButton.ClickButton()
        healthEdge_Manager.SearchDialog.BarDockControl.DockedBarControl.ClickItem("Close")
        close_claim_editor()
        return None
    else:
        Log.Message("XtraMessageBoxForm2 not found, performing alternative actions")
        searchDialog = healthEdge_Manager.SearchDialog
        dockedBarControl = searchDialog.BarDockControl2.DockedBarControl
        gridControl = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults
        rowCount = gridControl.wRowCount

        i = 0
        while i < rowCount:
            address_value = gridControl.wValue[i, 3]
            address_str = str(address_value)
            address_values.append(address_str)
            if address_str == combinedaddress:
                supplier_value = gridControl.wValue[i, 2]
                supplier_str = str(supplier_value)
                Log.Message(f"value to paste : {supplier_str}")
                Log.Message("Compared")
                return supplier_str
            else:
                Log.Message(f"Value in claim form: {combinedaddress}")
                Log.Message(f"No value to paste. \nValue at [{i}, 3]: {address_value}")
                healthEdge_Manager.SearchDialog.BarDockControl.DockedBarControl.ClickItem("Close")
                claimEditor = healthEdge_Manager.ClaimEditor
                claimEditor.Activate()
                claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
                healthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
                Log.Message(f"Closing all windows")
                aqUtils.Delay(6000)
            i += 1
        Log.Message("No issues")
        return None

# Part 8 - Pasting the Supplier name in edit_claim form
def paste_supplier_name(supp_to_copy):
    healthEdge_Manager = Aliases.HealthEdge_Manager
    healthEdge_Manager.SearchDialog.Close()
    claimEditor = healthEdge_Manager.ClaimEditor
    claimEditor.Activate()
    Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.HeaderGroupHyperLinkEdit.Click(65, 10)
    supp_name = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.headerGroupControlSubmittedSupplierInformation.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo.autoEditSubmittedSupplierInfoFullName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    supp_name.SetText(supp_to_copy)
    Log.Message("Pasted")
    healthEdge_Manager = Aliases.HealthEdge_Manager
    #healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
    promptForReasonCode = healthEdge_Manager.PromptForReasonCode
    promptForReasonCode.panelReason.lookUpEditReasonCode.Click(239, 7)
    healthEdge_Manager.PopupLookUpEditForm.Click(58, 19)
    promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
    aqUtils.delay(7000)

# Close claim editor
def close_claim_editor():
    claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
    claimEditor.Activate()
    claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
    Aliases.HealthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()

# Main Test Function
def Test1():
    #start_application()
    #select_workbasket()
    #set_filtering_criteria()
    process_grid_rows(0)
#    combinedaddress, NPI = edit_claim_form()
    
#    found = check_matching_supplier(NPI)
#    if found:
#        claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
#        claimEditor.Activate()
#        claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
#        Aliases.HealthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
#        process_grid_rows(j + 1)  # Start processing from the next row
#    else:
#        supp_to_copy = search_supplier(NPI, combinedaddress)
#        if supp_to_copy:
#            paste_supplier_name(supp_to_copy)
#        else:
#            process_grid_rows(j + 1)

# Run the test
Test1()