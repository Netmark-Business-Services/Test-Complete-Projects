# Defining global variables
address_values = []
DNU_CLAIM_ID = []
modified_claim_id = []
global process_count
#global reject_count
process_count = 0
#reject_count = 0
j = 0
Processed_claims = []
set_supplier_ids = []
global processed_count
processed_count = 0
global denied_count
denied_count = 0


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
def process_grid_rows():
    array1 = ['2024201003637', '2024184006639', '2024201003640', '2024184006673', '2024201004445', '2024193000871', 
     '2024201004464', '2024193000887', '2024201004474', '2024193001067', '2024201004577', '2024184006867', '2024201004579', 
     '2024184006944', '2024201004582', '2024193001620', '2024212000524', '2024193001663', '2024212000529', '2024193001782', 
     '2024201004668', '2024193001783', '2024201004671', '2024193001785', '2024201004682', '2024184007303', '2024201004763', 
     '2024184007316', '2024201004980', '2024193002238', '2024201004986']
    #'2024200006683', '2024184003128', '2024200006905', '2024192008873', '2024200007173', '2024192008988',
    #'2024186008616', '2024192009009', '2024209004125', '2024192009272', '2024209004527',
     #'2024164000332', '2024211000001',
     #'2024192009423', '2024178009406', '2024192009428', '2024201000780', '2024192009477', '2024178009460', '2024192009492', 
     #'2024211000560', '2024164000335', '2024211000563', '2024192009680', '2024211000567', '2024192010033', '2024211003285', 
     #'2024192010042', '2024211003297', '2024207000661', '2024211003301', '2024207000723', '2024211003306', '2024207001053', 
     #'2024211003314', '2024207001323', '2024211003317', '2024207001324', '2024211003322', '2024207001325', '2024211003324', 
     #'2024207001327', '2024211003332', '2024207001330', '2024211003353', '2024207001331', '2024211003357', '2024207001332', 
     #'2024211003372', '2024164000341', '2024201002731', '2024169000677', '2024201002824', '2024184004927', '2024201002836', 
     #'2024184005125', '2024201002896', '2024184005392', '2024220000628', '2024193000456', '2024220000634', '2024177000747', 
     #'2024220000645', '2024184006477', '2024220000655', '2024184006506', '2024201002902', '2024193000729', '2024201002906', 
     #'2024184006619', 
    
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    resultGridClaimReviewRepair = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
    #resultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Clear Inputs")
    textBoxMaskBox = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.autoEditClaimHccId.panelControlAutoEdit.TextEdit
    textBoxMaskBox.TextBoxMaskBox.Click(40, 4)
    
    # Iterate through array1 and process each claim
    for array in array1:
        if array not in DNU_CLAIM_ID:
            if len(Processed_claims) + len(DNU_CLAIM_ID) == len(array1):
                            Log.Message("All claims processed or denied, exiting the loop.")
                            break  # Exit the loop when all claims are processed or denied
            textBoxMaskBox.SetText(array)
            textBoxMaskBox.Keys("[Enter]")
            aqUtils.Delay(2000)
            gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
            WBrowCount = gridControl.wRowCount
            Log.Message(f"row count in this page is {WBrowCount}")
            if WBrowCount == 0:
              DNU_CLAIM_ID.append(rej_claim_id)
              continue
            claim_type = str(gridControl.wValue[0, 2])
            Log.Message(f"claim type: {claim_type}")  
            if claim_type == "Institutional":
                DNU_CLAIM_ID.append(rej_claim_id)
                continue
            rej_claim_id = str(gridControl.wValue[0, 1])
            Log.Message(f"Processing claim: {rej_claim_id}")
            review_reason = gridControl.wValue[0, 10]
            Log.Message(f"Reason in row is {review_reason}")

            # Call the edit_row function
            edit_row(0)
            combinedaddress, NPI = edit_claim_form()

            found = check_matching_supplier(NPI)
            if found:
                close_claim_editor()
            else:
                supp_to_copy = search_supplier(NPI, combinedaddress)
                if supp_to_copy:
                    #paste_supplier_name(supp_to_copy)
                    #Processed_claims.append(rej_claim_id)
                    #set_supplier_ids.append(supp_to_copy)
                    #Log.Message(f"Processed Claims: {Processed_claims}")
                    #Log.Message(f"Processed Supplier IDs: {set_supplier_ids}")
                        healthEdge_Manager = Aliases.HealthEdge_Manager
                        healthEdge_Manager.SearchDialog.Close()
                        claimEditor = healthEdge_Manager.ClaimEditor
                        claimEditor.Activate()
                        Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.HeaderGroupHyperLinkEdit.Click(71, 5)
                        aqUtils.Delay(2000)
                        healthEdge_Manager = Aliases.HealthEdge_Manager
                        headerGroupControl = healthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
                        #headerGroupControl.HeaderGroupHyperLinkEdit.Click(42, 9)
                        referenceMenuButton = headerGroupControl.supplierReference.autoSizingPanelSupplier.referenceMenuButtonSupplier
                        referenceMenuButton.Click(6, 8)
                        referenceMenuButton.PopupMenu.Click("Look up")
                        healthEdge_Manager.XtraMessageBoxForm3.SimpleButton.ClickButton()
                        resolveDialog = healthEdge_Manager.ResolveDialog
                        panelControl = resolveDialog.panelControlLeft
                        panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SimpleSupplierSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit.SetText(supp_to_copy)
                        panelControl.panelControlSearch.simpleButtonSearch.ClickButton()
                        resolveDialog.panelControlBottom.simpleButtonOK.ClickButton()
                        aqUtils.Delay(2000)
                        Log.Message("Pasted")
                        healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")           
                        promptForReasonCode = healthEdge_Manager.PromptForReasonCode
                        promptForReasonCode.panelReason.lookUpEditReasonCode.Click(238, 10)
                        healthEdge_Manager.PopupLookUpEditForm.Click(187, 24)
                        promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
                        aqUtils.Delay(5000)
                        
                        Processed_claims.append(rej_claim_id)
                        set_supplier_ids.append(supp_to_copy)
                                                
                        processed_count = len(Processed_claims)
                        denied_count = len(DNU_CLAIM_ID)
                                               
                        Log.Message(f"Processed Claims:  {Processed_claims}")
                        Log.Message(f"Processed Supplier IDs:  {set_supplier_ids}")
                        Log.Message(f"Processed Claims Count:  {processed_count}")
                        Log.Message(f"Denied Claims:  {DNU_CLAIM_ID}")
                        Log.Message(f"Denied Claims Count:  {denied_count}")
                        #j += 1
                        continue
                else:
                    
                        healthEdge_Manager = Aliases.HealthEdge_Manager
                        #healthEdge_Manager.SearchDialog.BarDockControl.DockedBarControl.ClickItem("Close")
                        #healthEdge_Manager.XtraMessageBoxForm2.SimpleButton.ClickButton()
                        claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
                        claimEditor.Activate()
                        claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
                        Aliases.HealthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
                        
                        
                        aqUtils.Delay(5000)
                        DNU_CLAIM_ID.append(rej_claim_id)
                        processed_count = len(Processed_claims)
                        denied_count = len(DNU_CLAIM_ID)
                        Log.Message(f"Processed Claims:  {Processed_claims}")
                        Log.Message(f"Processed Supplier IDs:  {set_supplier_ids}")
                        Log.Message(f"Processed Claims Count:  {processed_count}")
                        Log.Message(f"Denied Claims:  {DNU_CLAIM_ID}")
                        Log.Message(f"Denied Claims Count:  {denied_count}")
                        Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Refresh")
                        
                    #DNU_CLAIM_ID.append(rej_claim_id)
                    #Log.Message(f"Denied Claims: {DNU_CLAIM_ID}")
                resultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Refresh")
            # Check if all claims are processed or denied
            if len(Processed_claims) + len(DNU_CLAIM_ID) == len(array1):
                Log.Message("All claims processed or denied, exiting the loop.")
                break  # Exit the loop when all claims are processed or denied
        
    return True

    
    
    
    
def edit_claim_form():
    aqUtils.Delay(6000)
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
    state1 = str(stateLookUpEdit.Text)
    Log.Message("The state is: " + state1)
    state = state_abbreviations.get(state1, "Unknown")
    Log.Message("The abbreviated state is: " + state)

    # Extract and log the zip code details
    zipTextBox = entityPanel.autoEditSubmittedSupplierInfoZipCode.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    zipTextBox.Click(56, 9)
    zipCode1 = str(zipTextBox.Text)
    Log.Message("The zip code is: " + zipCode1)
    zipCode = zipCode1[:5]
    Log.Message("The first 5 digits of the ZIP code are: " + zipCode)

    if address.startswith("STE"):
        combinedaddress = f"{address2}, {city}, {state}, {zipCode}"
        combinedaddress = combinedaddress.upper()
    elif address2:
        combinedaddress = f"{address}, {city}, {state}, {zipCode}"
        #, {address2}
        combinedaddress = combinedaddress.upper()
    else:
        combinedaddress = f"{address}, {city}, {state}, {zipCode}"
        combinedaddress = combinedaddress.upper()
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
        1609291996,  1639172372, 1710927231,
        1760047708, 1629167457,1780656421
    ] #1629167457,

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
    else:
        Log.Message("XtraMessageBoxForm2 not found, performing alternative actions")
        searchDialog = healthEdge_Manager.SearchDialog
        #searchDialog.BarDockControl.DockedBarControl.ClickItem("Search")
        dockedBarControl = searchDialog.BarDockControl2.DockedBarControl
        dockedBarControl.Drag(1400, 17, 166, 195)
        gridControl = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults
        rowCount = gridControl.wRowCount
        
        i=0
        while i < rowCount:
          searchDialog = healthEdge_Manager.SearchDialog
          address_value = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults.wValue[i, 3]
          address_str = str(address_value).upper()
          Log.Message(f"Given value  : {combinedaddress}")
          Log.Message(f"add to check  : {address_str}")
          if address_str == combinedaddress:
            address_values.append(address_str)
            supplier_value = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults.wValue[i, 0]
            supplier_str = str(supplier_value)
            supp_to_copy = supplier_str
            Log.Message("Compared")
            Log.Message(f"supplier id value to paste : {supp_to_copy}")
          
            return supp_to_copy
          else:
            Log.Message(f"Value at [{i}, 3]: {address_value}")
            Log.Message("No values found")
          i+=1
          
        Log.Message("No issues")
        Aliases.HealthEdge_Manager.SearchDialog.Close()
        
    return None

# Part 8 - Pasting the Supplier name in edit_claim form
def paste_supplier_name(supp_to_copy):
    healthEdge_Manager = Aliases.HealthEdge_Manager
    healthEdge_Manager.SearchDialog.Close()
    claimEditor = healthEdge_Manager.ClaimEditor
    claimEditor.Activate()
    Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.HeaderGroupHyperLinkEdit.Click(71, 5)
    aqUtils.Delay(2000)
    headerGroupControl = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.headerGroupControlSubmittedSupplierInformation
    headerGroupHyperLinkEdit = headerGroupControl.HeaderGroupHyperLinkEdit
    headerGroupHyperLinkEdit.Click(6, 3)
    headerGroupHyperLinkEdit.Click(6, 3)
    supp_name = headerGroupControl.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo.autoEditSubmittedSupplierInfoFullName.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Click(141, 9)
    supp_name = headerGroupControl.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo.autoEditSubmittedSupplierInfoFullName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    supp_name.SetText(supp_to_copy)
    Log.Message("Pasted")
    healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
    Log.Message(f"submitted claim {rej_claim_id} with supplier id {supplier_id} with address {combinedaddress} " )
    promptForReasonCode = healthEdge_Manager.PromptForReasonCode
    promptForReasonCode.panelReason.lookUpEditReasonCode.Click(238, 10)
    healthEdge_Manager.PopupLookUpEditForm.Click(187, 24)
    promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
    aqUtils.Delay(8000)
    
    return True
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
    
def test_procecss():
  array1 = ['1', '2', '3']  # Corrected the last element from 3' to '3'
  
  
  
  gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
  WBrowCount = gridControl.wRowCount
  resultGridClaimReviewRepair = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
  resultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Clear Inputs")
  textBoxMaskBox = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.autoEditClaimHccId.panelControlAutoEdit.TextEdit
  textBoxMaskBox.TextBoxMaskBox.Click(40, 4)
  
  # Iterate through array1 and set the text one by one
  for array in array1:
      textBoxMaskBox.SetText(array)
      # You can add any additional functionality here that needs to run after setting the text.
      
          
# Main Test Function
def Test1():
    #start_application()
    #select_workbasket()
    #set_filtering_criteria()
    process_grid_rows()
    #combinedaddress = edit_claim_form()
    #test_procecss()

Test1()