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
    array1 = [  '2024226009257', '2024232000654', '2024246002738', '2024246002740', '2024194008368', '2024201002897', 
    '2024198008203', '2024201005001', '2024193006710', '2024201005002', '2024197004200', '2024201005003', '2024186003815', '2024201005005', '2024184007539', 
    '2024201005006', '2024208000017', '2024201005007', '2024195003380', '2024201005008', '2024218004797', '2024201005015', '2024199002110', '2024201005128', 
    '2024209003037', '2024201005187', '2024193003509', '2024201005227', '2024207010206', '2024201005238', '2024184008569', '2024201005343', '2024164000781', 
    '2024201005408', '2024177012993', '2024201005437', '2024197001146', '2024201005438', '2024198000468', '2024201005439', '2024186000229', '2024201005442', 
    '2024219001711', '2024201005444', '2024178008221', '2024201005445', '2024186006050', '2024201005446', '2024211003270', '2024178009487', '2024212002245', 
    '2024201005451', '2024193004060', '2024201005452', '2024214003685', '2024201005453', '2024164000347', '2024201005454', '2024184007600', '2024201005455', 
    '2024194003235', '2024201005457', '2024194004992', '2024201005458', '2024194006972', '2024201005460', '2024194008892', '2024178009492', '2024177013343', 
    '2024201005479', '2024195003874', '2024201005486', '2024185009692', '2024201005497', '2024197005210', '2024201005498', '2024218001124', '2024201005500', 
    '2024198004272', '2024201005502', '2024186000388', '2024201005504', '2024186000552', '2024201005506', '2024186000946', '2024201005507', '2024199002239', 
    '2024201005508', '2024186003556', '2024201005509', '2024200005222', '2024201005510', '2024200005959', '2024201005513', '2024209004136', '2024201005514', 
    '2024211003325', '2024201005515', '2024201003642', '2024201005516', '2024213005919', '2024201005517', '2024207005445', '2024201005518', '2024184007525', 
    '2024201005520', '2024207009098', '2024201005521', '2024207010180', '2024201005544', '2024207010266', '2024201005547', '2024193006467', '2024201005549', 
    '2024184007576', '2024201005550', '2024194001876', '2024201005551', '2024194002635', '2024201005552', '2024207019035', '2024201005553', '2024164000490', 
    '2024201005554', '2024194005837', '2024201005555', '2024185002548', '2024201005557', '2024194007558', '2024201005558', '2024163000315', '2024201005559', 
    '2024195000621', '2024201005560', '2024195001406', '2024201005562', '2024177013361', '2024201005563', '2024195003635', '2024201005565', '2024185008812', 
    '2024201005568', '2024197001651', '2024201005569', '2024185010169', '2024201005571', '2024197004904', '2024201005572', '2024197005231', '2024201005585', 
    '2024198002319', '2024201005588', '2024218004748', '2024201005592', '2024185010547', '2024201005596', '2024186000161', '2024201005598', '2024208005021', 
    '2024201005602', '2024208005757', '2024201005609', '2024198008845', '2024201005625', '2024208009723', '2024201005863', '2024199000524', '2024201005864', 
    '2024199001423', '2024201005865', '2024199002120', '2024201006240', '2024178008204', '2024201006246', '2024186003232', '2024201006373', '2024200003897', 
    '2024201006375', '2024186004877', '2024201006399', '2024200005308', '2024201006400', '2024178009335', '2024201006410', '2024219007770', '2024201006411', 
    '2024200006741', '2024201006432', '2024201000789', '2024187000595', '2024211003309', '2024178009536', '2024211003373', '2024179000150', '2024201002901', 
    '2024202000775', '2024201004578', '2024179000532', '2024178009483', '2024165000183', '2024193002726', '2024179000973', '2024207004828', '2024187000958', 
    '2024207005452', '2024202001497', '2024184007499', '2024202001554', '2024184007529', '2024202001616', '2024193004936', '2024202001718', '2024214002711', 
    '2024202001889', '2024207010105', '2024202001897', '2024207010190', '2024202001986', '2024207010248', '2024202002092', '2024193004998', '2024202002173', 
    '2024193005867', '2024202002266', '2024214008436', '2024202002267', '2024193006959', '2024202002439', '2024184007586', '2024202002444', '2024184007876', 
    '2024202002529', '2024184008555', '2024202002533', '2024194002550', '2024202002534', '2024184008588', '2024202002536', '2024184008600', '2024202002537', 
    '2024207019040', '2024202002539', '2024194003607', '2024202002540', '2024184009849', '2024202002541', '2024185000159', '2024202002542', '2024194006242', 
    '2024202002543', '2024194006509', '2024202002545', '2024215009197', '2024202002546', '2024194007201', '2024202002548', '2024194008096', '2024202002553', 
    '2024194008389', '2024202002584', '2024194008409', '2024202002609', '2024195000283', '2024202002650', '2024195000698', '2024202002739', '2024195001291', 
    '2024202002741', '2024195001486', '2024202002742', '2024177013348', '2024202002744', '2024195003242', '2024202002746', '2024195003514', '2024202002747', 
    '2024195003779', '2024179001140', '2024195004048', '2024202002755', '2024197000514', '2024179001406', '2024197001409', '2024202002773', '2024185009689', 
    '2024202002787', '2024197003419', '2024202002788', '2024197003894', '2024202002789', '2024197004502', '2024202002790', '2024197005008', '2024202002791', 
    '2024197005225', '2024202002792', '2024198000017', '2024202002793', '2024185010443', '2024202002794', '2024198002673', '2024202002799', '2024218001140', 
    '2024202002804', '2024218004768', '2024202002836', '2024218004812', '2024202002858', '2024198003655', '2024202002862', '2024186000114', '2024202002865', 
    '2024186000175', '2024202002866', '2024208005013', '2024202002868', '2024198007072', '2024202002871', '2024186000439', '2024202002928', '2024208006682', 
    '2024179001438', '2024198008694', '2024179001445', '2024186000519', '2024165000188', '2024208009718', '2024187001428', '2024198010886', '2024179001751', 
    '2024219001717', '2024187001654', '2024186000644', '2024204000727', '2024199001127', '2024204000729', '2024199001991', '2024204000730', '2024199002114', 
    '2024204000732', '2024199002179', '2024204000733', '2024199002743', '2024204000734', '2024186002682', '2024204000735', '2024199006913', '2024204000737', 
    '2024199009432', '2024171000142', '2024200003892', '2024171000772', '2024200003905', '2024187001783', '2024186004479', '2024187001794', '2024186005108', 
    '2024165000194', '2024178009164', '2024165000231', '2024186005729', '2024171000796', '2024178009180', '2024171000840', '2024186007384', '2024171000842', 
    '2024186008479', '2024179009940', '2024200006115', '2024179010001', '2024200006529', '2024187002106', '2024201000175', '2024179010089', '2024211000002', 
    '2024187002173', '2024211000562', '2024205000334', '2024211003300', '2024205000671', '2024211003319', '2024205000673', '2024211003356', '2024179010133', 
    '2024201002825', '2024179010941', '2024220000639', '2024179011819', '2024201003635', '2024205001815', '2024201004466', '2024179011821', '2024212000516', 
    '2024187002410', '2024201004672', '2024205002539', '2024201004987', '2024205003288', '2024213005924', '2024205003889', '2024193002830', '2024205004332', 
    '2024207004825', '2024205004333', '2024207005443', '2024205004334', '2024207005447', '2024205004335', '2024193003609', '2024205004336', '2024184007485', 
    '2024205004337', '2024184007515', '2024205004338', '2024193004573', '2024205004343', '2024193004766', '2024205004493', '2024193004874', '2024205004498', 
    '2024193004988', '2024205004500', '2024207009801', '2024205004514', '2024214002713', '2024205004515', '2024214003688', '2024205005370', '2024207010158', 
    '2024205005371', '2024207010187', '2024205005372', '2024207010202', '2024205005373', '2024207010211', '2024205006530', '2024207010251', '2024205007019', 
    '2024207010347', '2024205007202', '2024177002244', '2024179011824', '2024193005775', '2024179012555', '2024193006435', '2024187002629', '2024193006676', 
    '2024187002664', '2024193006690', '2024179012672', '2024214008459', '2024187002783', '2024193006987', '2024179012743', '2024193007964', '2024187002947', 
    '2024193008220', '2024179012752', '2024184007610', '2024179012754', '2024184008047', '2024179012756', '2024194002093', '2024179012762', '2024194002332', 
    '2024179012774', '2024184008583', '2024179012956', '2024194002578', '2024187003134', '2024194002825', '2024179013186', '2024194003157', '2024187003164', 
    '2024194003353', '2024179013187', '2024207018763', '2024179013188', '2024207019038', '2024179013189'
 ]
   #'2024241002781', '2024247002742', '2024241002783', '2024247003890', '2024226009248', '2024247003892', '2024226009249', '2024239000595', 
   # '2024226009250', '2024239000600', '2024226009251', '2024239002970', '2024226009252', '2024239002980', '2024226009253', '2024239002985', '2024226009255', 
   # '2024239002990', '2024226009256', '2024240002064',
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    resultGridClaimReviewRepair = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
    #resultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Clear Inputs")
    textBoxMaskBox = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.autoEditClaimHccId.panelControlAutoEdit.TextEdit
    textBoxMaskBox.TextBoxMaskBox.Click(40, 4)
    
    # Iterate through array1 and process each claim
    for array in array1:
        aqUtils.Delay(2000)
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
                DNU_CLAIM_ID.append(rej_claim_id)
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
    #aqUtils.Delay(6000)
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