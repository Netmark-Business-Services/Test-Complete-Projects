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
    array1 = [  
    '2024227000105', '2024240009669', '2024227000109', '2024240009670', 
    '2024227000658', '2024241000102', '2024233004642', '2024242002624', '2024241009542', '2024242002626', '2024241009546', '2024242005024', '2024241009550', '2024241000103', 
    '2024241009554', '2024233000152', '2024241009558', '2024233000154', '2024233008201', '2024233000162', '2024233008206', '2024233000163', '2024233008210', '2024233000168', 
    '2024233008214', '2024233000169', '2024233008218', '2024233000173', '2024233008222', '2024233000176', '2024233008226', '2024241000113', '2024233008230', '2024241000117', 
    '2024233008234', '2024240000192', '2024233008238', '2024240000200', '2024233008690', '2024235001401', '2024233008695', '2024235001423', '2024234000048', '2024235001871', 
    '2024234000058', '2024235003982', '2024234000610', '2024235003986', '2024225005110', '2024235003987', '2024225005114', '2024233000384', '2024242001351', '2024235003989', 
    '2024242001355', '2024235003990', '2024242001359', '2024235003991', '2024242001364', '2024235003993', '2024242001369', '2024235003995', '2024242001373', '2024235003997', 
    '2024242001377', '2024222010746', '2024242001381', '2024222010749', '2024242001385', '2024222010750', '2024225005121', '2024222010754', '2024225005207', '2024222010756', 
    '2024234002283', '2024222010757', '2024247002334', '2024222010764', '2024229003888', '2024222010766', '2024226000055', '2024222010767', '2024234002287', '2024222010771', 
    '2024239000572', '2024222010772', '2024239000576', '2024222010773', '2024239000580', '2024235003998', '2024239000584', '2024235003999', '2024239000588', '2024235004002', 
    '2024222002493', '2024235004003', '2024239000593', '2024235004004', '2024247003891', '2024235004005', '2024239000596', '2024235004006', '2024239002972', '2024235004009', 
    '2024239002986', '2024221010455', '2024232000617', '2024235004014', '2024246002742', '2024236000837', '2024246002746', '2024236000867', '2024246002750', '2024236000874', 
    '2024246002754', '2024236000876', '2024246002758', '2024236000883', '2024246002762', '2024235004015', '2024246002766', '2024220006805', '2024246002770', '2024220006811', 
    '2024246002773', '2024220006819', '2024246002777', '2024240000288', '2024246002781', '2024240000293', '2024246002785', '2024220000953', '2024246002789', '2024240000297', 
    '2024246002793', '2024235004019', '2024246002797', '2024235004020', '2024246003024', '2024235004022', '2024246003028', '2024235004024', '2024246003032', '2024235004025', 
    '2024246003036', '2024235004029', '2024246003040', '2024235004031', '2024246003044', '2024235004034', '2024246003048', '2024235004036', '2024247000396', '2024235004041', 
    '2024247000399', '2024235004048', '2024247000403', '2024234002278', '2024247000406', '2024234002279', '2024241002784', '2024234002280', '2024241002786', '2024234002281', 
    '2024241002791', '2024226001738', '2024241002795', '2024226001739', '2024241002800', '2024226001744', '2024241002802', '2024227006956', '2024241002808', '2024227007560', 
    '2024241002812', '2024228000860', '2024241002815', '2024227007561', '2024241002818', '2024227007563', '2024241002826', '2024227007564', '2024228005638', '2024227007565', 
    '2024228005642', '2024227007566', '2024228005644', '2024227007567', '2024228005646', '2024227007570', '2024228005654', '2024227007571', '2024241005172', '2024235005609', 
    '2024241005182', '2024225004943', '2024234009969', '2024225005008', '2024229003877', '2024225005015', '2024229003881', '2024225005026', '2024229003883', '2024225005030', 
    '2024229003886', '2024225005031', '2024234009971', '2024225005033', '2024235009379', '2024225005034', '2024235009381', '2024225005041', '2024234009973', '2024225005051', 
    '2024228009636', '2024225005059', '2024228009638', '2024225005063', '2024228009640', '2024225005066', '2024226009259', '2024225005070', '2024233002161', '2024243003534', 
    '2024226009261', '2024243003535', '2024226009263', '2024243003536', '2024227000104', '2024243003538', '2024227000106', '2024243003539', '2024227000108', '2024243003540', 
    '2024227000113', '2024243003541', '2024227000657', '2024243003542', '2024227000659', '2024243003543', '2024228009642', '2024243003544', '2024241009538', '2024243003545', 
    '2024241009540', '2024243003546', '2024241009543', '2024243003547', '2024241009545', '2024243003548', '2024241009547', '2024243003549', '2024241009549', '2024243003550', 
    '2024241009551', '2024243003551', '2024241009553', '2024243003552', '2024241009555', '2024243003553', '2024241009557', '2024243003554', '2024241009559', '2024243003555', 
    '2024225005084', '2024243003556', '2024233008203', '2024243003557', '2024233008205', '2024243003558', '2024233008207', '2024243003559', '2024233008209'
 ]
  
# '2024233008220', '2024247000401', '2024239000586', '2024232000658', '2024226009258', '2024232001223', '2024242001366', '2024232001225', '2024246002771', '2024232001226', 
#    '2024228005645', '2024232001235', '2024241009548', '2024229003891', '2024234000050', '2024229003892', '2024234002285', '2024229003893', '2024232000657', '2024229003894', 
#    '2024246003026', '2024229003896', '2024241002805', '2024229003897', '2024229003884', '2024230000063', '2024227000553', '2024230000075', '2024233008204', '2024239002995', 
#    '2024233008236', '2024239002999', '2024225005119', '2024239003003', '2024242001383', '2024239003005', '2024239000570', '2024239003007', '2024239000594', '2024239003009', 
#    '2024246002756', '2024239003010', '2024246002787', '2024239003238', '2024246003042', '2024234002289', '2024241002789', '2024234002290', '2024241002825', '2024234002291', 
#    '2024241005449', '2024234002292', '2024234009972', '2024234002293', '2024227000101', '2024228009644', '2024241009539', '2024228009645', '2024241009556', '2024242001746', 
#    '2024233008212', '2024228009646', '2024233008228', '2024229000053', '2024233008692', '2024229000066', '2024225005089', '2024229000480', '2024242001357', '2024229000484', 
#    '2024242001375', '2024229000485', '2024225005139', '2024229000492', '2024226000046', '2024229000499', '2024239000578', '2024234002294', '2024239000591', '2024234002295', 
#    '2024239002982', '2024234002296', '2024246002748', '2024240003933', '2024246002764', '2024240003934', '2024246002779', '2024240003935', '2024246002795', '2024240003937', 
#    '2024246003034', '2024240003938', '2024247000394', '2024240003939', '2024247000408', '2024240003940', '2024241002797', '2024240003941', '2024241002814', '2024240003942', '2024228005641', '2024240003943', '2024227004240', '2024240003944', '2024229003880', '2024240003945', '2024235009376', '2024240003946', '2024229003887', '2024240003947', 
#    '2024233002167', '2024240004671', '2024227000107', '2024240005409', '2024228009641', '2024237000259', '2024241009544', '2024232006775', '2024241009552', '2024232006777', 
#    '2024228009643', '2024232006779', '2024233008208', '2024232006781', '2024233008216', '2024232006784', '2024233008224', '2024232006786', '2024233008232', '2024232006787', 
#    '2024233008687', '2024232006789', '2024233008697', '2024232006790', '2024234000601', '2024232006793', '2024237001736', '2024232006795', '2024242001353', '2024232006797', 
#    '2024242001362', '2024232006802', '2024242001371', '2024232007286', '2024242001379', '2024232007287', '2024242001387', '2024232007288', '2024228000284', '2024232007289', 
#    '2024225005218', '2024232007292', '2024226000060', '2024232007293', '2024239000574', '2024232007294', '2024239000582', '2024232007296', '2024239000590', '2024234002297', 
#    '2024247002743', '2024234002298', '2024239002941', '2024242002440', '2024240002055', '2024242002441', '2024246002744', '2024234002301', '2024246002752', '2024234002306', 
#    '2024246002760', '2024234002274', '2024246002768', '2024239006084', '2024246002775', '2024239006089', '2024246002783', '2024239006090', '2024246002791', '2024239006091', 
#    '2024246003022', '2024239006092', '2024246003030', '2024239006093', '2024246003038', '2024239006094', '2024246003046', '2024239006095', '2024247000398', '2024239006096', 
#    '2024247000404', '2024239006097', '2024241002785', '2024239006098', '2024241002792', '2024239006099', '2024241002801', '2024239006100', '2024241002810', '2024239006101', 
#    '2024241002816', '2024234002275', '2024227004238', '2024234002276', '2024228005643', '2024234002277', '2024228005648', '2024240000180', '2024241005174', '2024240000182', 
#    '2024234009970', '2024240000189', '2024229003882', '2024240009661', '2024233001235', '2024240009663', '2024235009380', '2024240009664', '2024228009635', '2024240009665', 
#    '2024228009639', '2024240009666', '2024226009260', '2024240009667', '2024226009262', '2024240009668', 
 
 
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