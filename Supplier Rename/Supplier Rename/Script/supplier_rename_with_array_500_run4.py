﻿# Defining global variables
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
    array1 = [
   #'2024198008020', '2024181006906', '2024208005354', '2024181006934', 
    #'2024208005912', '2024191007729', '2024208006678', '2024191007753', '2024198008173', 
    '2024191007961']
    
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
              DNU_CLAIM_ID.append(array)
              processed_count = len(Processed_claims)
              denied_count = len(DNU_CLAIM_ID)
              Log.Message(f"Processed Claims:  {Processed_claims}")
              Log.Message(f"Processed Supplier IDs:  {set_supplier_ids}")
              Log.Message(f"Processed Claims Count:  {processed_count}")
              Log.Message(f"Denied Claims:  {DNU_CLAIM_ID}")
              Log.Message(f"Denied Claims Count:  {denied_count}")
              continue
            claim_type = str(gridControl.wValue[0, 2])
            Log.Message(f"claim type: {claim_type}")  
            if claim_type == "Institutional":
                DNU_CLAIM_ID.append(array)
                processed_count = len(Processed_claims)
                denied_count = len(DNU_CLAIM_ID)
                Log.Message(f"Processed Claims:  {Processed_claims}")
                Log.Message(f"Processed Supplier IDs:  {set_supplier_ids}")
                Log.Message(f"Processed Claims Count:  {processed_count}")
                Log.Message(f"Denied Claims:  {DNU_CLAIM_ID}")
                Log.Message(f"Denied Claims Count:  {denied_count}")
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
    aqUtils.Delay(600)
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

def dnu():
  used =['2024201004574', '2024212009349', '2024201004581', '2024212009615', '2024212000528', '2024212009819', '2024201004670', '2024212009820', '2024201004761', '2024212009821', 
    '2024201004982', '2024212009822', '2024201004993', '2024212009823', '2024213005920', '2024212009824', '2024213006360', '2024212009825', '2024184007475', '2024212009826', '2024193002985', 
    '2024212009827', '2024193003560', '2024212009828', '2024207004827', '2024212009829', '2024207005442', '2024213000167', '2024207005444', '2024180008461', '2024207005446', '2024180008463', 
    '2024207005448', '2024180008470', '2024193003562', '2024180008897', '2024193003674', '2024180009139', '2024184007480', '2024213000348', '2024184007495', '2024180009140', '2024184007509', 
    '2024180009146', '2024184007519', '2024180009352', '2024193004552', '2024180009375', '2024193004633', '2024180009393', '2024193004737', '2024180009394', '2024184007535', '2024180009395', 
    '2024184007545', '2024180009396', '2024193004899', '2024180009429', '2024213009592', '2024180009431', '2024207009096', '2024180009433', '2024207009789', '2024180009442', '2024207010101', 
    '2024180009478', '2024214002712', '2024166000951', '2024214003684', '2024172000804', '2024214003687', '2024172000894', '2024214003690', '2024172000910', '2024207010109', '2024172000911', 
    '2024207010176', '2024172000912', '2024207010184', '2024166000991', '2024207010189', '2024163001150', '2024207010201', '2024163001154', '2024207010205', '2024162000177', '2024207010209', 
    '2024162000779', '2024207010226', '2024163000218', '2024214008187', '2024181004787', '2024207010264', '2024181004841', '2024207010276', '2024213002833', '2024207010706', '2024206000658', 
    '2024184007549', '2024206000791', '2024193005377', '2024206000829', '2024193005675', '2024206000832', '2024193005830', '2024206000833', '2024193006175', '2024206001007', '2024193006466', 
    '2024206001008', '2024193006663', '2024206001010', '2024193006688', '2024206001054', '2024214008441', '2024206001188', '2024193006705', '2024206001189', '2024214008457', '2024206001190', 
    '2024214008460', '2024206001193', '2024193006960', '2024206001200', '2024184007569', '2024190001405', '2024193007863', '2024181004842', '2024193007973', '2024181004844', '2024184007589', 
    '2024181005036', '2024177003408', '2024181005269', '2024184007606', '2024181005676', '2024164000460', '2024190002983', '2024184007879', '2024190003155', '2024184008541', '2024181006011', 
    '2024184008553', '2024181006442', '2024184008554', '2024181006445', '2024184008557', '2024181006448', '2024184008568', '2024181006457', '2024184008575', '2024213002930', '2024194002547', 
    '2024181006459', '2024194002575', '2024190004163', '2024194002634', '2024190004230', '2024194002642', '2024213002935', '2024184008585', '2024181006460', '2024184008599', '2024181006461', 
    '2024194003204', '2024181006462', '2024194003336', '2024190005086', '2024194003355', '2024181006466', '2024184008603', '2024190005321', '2024207019033', '2024181006467', '2024207019037', 
    '2024181006510', '2024207019039', '2024190006174', '2024207019041', '2024191000284', '2024207019043', '2024191000328', '2024208000018', '2024191000665', '2024194003525', '2024191000697', 
    '2024208001466', '2024191000703', '2024215002861', '2024213002960', '2024184009319', '2024213002961', '2024184009324', '2024191000734', '2024184010259', '2024191000768', '2024184010346', 
    '2024181006515', '2024194005054', '2024191000944', '2024184010762', '2024191000967', '2024185000173', '2024181006666', '2024185000268', '2024213002971', '2024194005860', '2024181006670', 
    '2024185000426', '2024181006844', '2024194006275', '2024181006845', '2024185000491', '2024191001622', '2024185000802', '2024191001729', '2024185000961', '2024181006846', '2024164000799', 
    '2024191001807', '2024163000238', '2024181006847', '2024185002995', '2024191001866', '2024215009194', '2024181006848', '2024215009207', '2024191001946', '2024215009243', '2024191002253', 
    '2024185003417', '2024191002267', '2024163000312', '2024181006849', '2024164000867', '2024181006850', '2024185004739', '2024181006851', '2024170000600', '2024191002583', '2024194007857', 
    '2024191002795', '2024194008358', '2024191002887', '2024194008366', '2024206001424', '2024194008373', '2024181006852', '2024164000876', '2024206002231', '2024194008390', '2024206002233', 
    '2024194008393', '2024206002235', '2024194008396', '2024206002236', '2024194008402', '2024206002238', '2024194008561', '2024191003110', '2024194008596', '2024191003158', '2024177011770', 
    '2024191003192', '2024195000250', '2024181006853', '2024177011910', '2024206003081', '2024195000617', '2024206003082', '2024195000649', '2024206003975', '2024195000678', '2024206003982', 
    '2024195000714', '2024206003984', '2024177012992', '2024206004002', '2024177012997', '2024206004219', '2024177013002', '2024206004220', '2024195001292', '2024206004221', '2024195001375', 
    '2024206004222', '2024195001413', '2024206004229', '2024195001467', '2024206004270', '2024177013167', '2024206004272', '2024177013169', '2024206004273', '2024177013345', '2024206004274', 
    '2024177013347', '2024206004275', '2024177013350', '2024206004276', '2024177013352', '2024206004277', '2024177013384', '2024206004279', '2024177013386', '2024206004281', '2024195003266', 
    '2024206004282', '2024195003354', '2024206004283', '2024195003405', '2024206004286', '2024195003503', '2024206004287', '2024195003559', '2024206004288', '2024195003581', '2024206004289', 
    '2024177013391', '2024206004291', '2024195003769', '2024206004293', '2024185008650', '2024206004407', '2024195003852', '2024206004409', '2024195003893', '2024206004411', '2024195003974', 
    '2024206004413', '2024177013393', '2024206004416', '2024197000284', '2024206004418', '2024185008816', '2024206004419', '2024197000418', '2024206004420', '2024197000642', '2024206004421', 
    '2024197001035', '2024206004434', '2024197001212', '2024206005189', '2024197001400', '2024191003331', '2024185008858', '2024191003348', '2024170001025', '2024191003391', '2024197001823', 
    '2024191003403', '2024197003006', '2024191003405', '2024197003287', '2024181006854', '2024197003299', '2024191003469', '2024185009697', '2024181006887', '2024197003404', '2024191003612', 
    '2024197003450', '2024191003635', '2024197003509', '2024181006890', '2024185010174', '2024191003819', '2024197003819', '2024191003840', '2024197004015', '2024191003849', '2024185010183', 
    '2024191003877', '2024197004236', '2024191003882', '2024197004341', '2024191003922', '2024197004531', '2024181006892', '2024197004779', '2024191004028', '2024197004948', '2024206009169', 
    '2024197005007', '2024206009308', '2024197005056', '2024206009309', '2024197005209', '2024206009311', '2024197005211', '2024206009312', '2024197005213', '2024206009313', '2024197005227', 
    '2024206009314', '2024197005230', '2024206009315', '2024197005232', '2024206009316', '2024197005238', '2024206009318', '2024198000187', '2024206009319', '2024198000359', '2024206009320', 
    '2024185010429', '2024206009321', '2024185010433', '2024206009322', '2024198002047', '2024206009323', '2024185010466', '2024206009324', '2024185010490', '2024206009325', '2024198002503', '2024206010162', '2024198002786', '2024207000048', '2024185010503', '2024207000049', '2024218001134', '2024207000050', '2024218001139', '2024207000051', '2024218001149', '2024207000052', 
    '2024218004689', '2024191004097', '2024218004760', '2024181006893', '2024218004765', '2024191004173', '2024218004771', '2024191004326', '2024218004793', '2024191004334', '2024218004799', 
    '2024191004369', '2024218004805', '2024191004424', '2024218004831', '2024181006895', '2024185010534', '2024181006897', '2024186000004', '2024191004761', '2024198003618', '2024181006898', 
    '2024198003700', '2024181006899', '2024198004264', '2024181006902', '2024198004466', '2024191005812', '2024186000100', '2024191005863', '2024186000145', '2024191006504', '2024186000157', 
    '2024191006530', '2024198006272', '2024181006903', '2024186000166', '2024191006647', '2024186000181', '2024181006904', '2024198006492', '2024191006788', '2024186000303', '2024191006997', 
    '2024208005004', '2024191007020', '2024208005014', '2024191007077', '2024208005017', '2024191007079', '2024198006682', '2024191007135', '2024198006952', '2024191007304', '2024186000364', 
    '2024191007509', '2024186000379', '2024191007540', '2024198007668', '2024191007550', '2024198007784', '2024181006905',  ]