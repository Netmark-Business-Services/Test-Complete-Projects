﻿def login_to_application():
    # Part 1 - Starting the application
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

def select_work_basket():
    # Part 2 - Select work basket
    healthEdge_Manager = Aliases.HealthEdge_Manager
    healthEdge_Manager.HomeForm.XtraMainMenu.Click("Workbasket|Claim Review & Repair")
    resultGridClaimReviewRepair = healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
    panelControl = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch
    aqUtils.Delay(5000)

def set_filtering_criteria():
    # Part 3 - Set filtering criteria in work basket
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

def check_and_edit_claim(j, gridControl, resultGridClaimReviewRepair):
    # Part 4 - Check if reason matches with what we are looking for and edit
    review_reason = gridControl.wValue[j, 10]
    reasons = str(review_reason)
    Log.Message(f"Reason in row {j} is {reasons}")
    if reasons == "Supplier could not be identified":
        gridControl.ClickCellXY(j, "Edit", 16, 14)
        aqUtils.Delay(18000)
        return True
    return False

def retrieve_address_and_npi():
    # Part 5 - Edit claim form to retrieve address and NPI ID
    claimEditor = Aliases.HealthEdge_Manager.ClaimEditor
    claimEditor.Activate()
    headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.headerGroupControlSubmittedSupplierInformation
    headerGroupControl.HeaderGroupHyperLinkEdit.Click(8, 8)
    entityPanel = headerGroupControl.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo

    addressTextBox = entityPanel.autoEditSubmittedSupplierInfoAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    addressTextBox.Click(123, 9)
    address = str(addressTextBox.wText)
    Log.Message("The address is: " + address)

    address2TextBox = entityPanel.autoEditSubmittedSupplierInfoAddress2.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    address2TextBox.Click(115, 9)
    address2 = str(address2TextBox.wText).strip()
    Log.Message("The address 2 is: " + address2)

    cityTextBox = entityPanel.autoEditSubmittedSupplierInfoCityName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    cityTextBox.Click(114, 11)
    city = cityTextBox.wText
    Log.Message("The city is: " + city)

    stateLookUpEdit = entityPanel.autoEditSubmittedSupplierInfoState.panelControlAutoEdit.LookUpEdit
    stateLookUpEdit.Click(115, 9)
    state = str(stateLookUpEdit.Text)
    Log.Message("The state is: " + state)

    zipTextBox = entityPanel.autoEditSubmittedSupplierInfoZipCode.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    zipTextBox.Click(56, 9)
    zipCode = str(zipTextBox.Text)
    Log.Message("The zip code is: " + zipCode)

    if address2:
        combinedaddress = f"{address}, {address2}, {city}, {state}, {zipCode}"
    else:
        combinedaddress = f"{address}, {city}, {state}, {zipCode}"
    Log.Message("Combined details: " + combinedaddress)

    NPILookUpEdit = entityPanel.autoEditSubmittedSupplierInfoNPI.panelControlAutoEdit.TextEdit
    NPILookUpEdit.Click(128, 8)
    NPI = str(NPILookUpEdit.Text)
    Log.Message("The NPI is: " + NPI)

    return combinedaddress, NPI

def check_supplier_in_db(NPI, combinedaddress):
    # Part 6 - Check for matching supplier in DB
    npi_int = int(NPI)
    rejected_list_npi = [
        1104877810,
        1215903018,
        1235866138,
        1528488756,
        1609291996,
        1629167457,
        1639172372,
        1710927231,
        1760047708,
        1780656421
    ]

    found = False
    for npi in rejected_list_npi:
        if npi == npi_int:
            found = True
            Log.Message("NPI in rejected list")
            break

    if found:
        print(f"NPI {NPI} exists in the rejected list.")
        claimEditor = healthEdge_Manager.ClaimEditor
        claimEditor.Activate()
        claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
        healthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
    else:
        print(f"NPI {NPI} does not exist in the rejected list.")

    healthEdge_Manager = Aliases.HealthEdge_Manager
    healthEdge_Manager.HomeForm.BarDockControl.DockedBarControl.ClickItem("Search")
    textEdit = healthEdge_Manager.SearchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleSupplierSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit
    textEdit.SetText(NPI)
    textEdit.TextBoxMaskBox.Keys("[Enter]")

    xtraMessageBoxForm = healthEdge_Manager.WaitAliasChild("XtraMessageBoxForm2", 1000)
    if xtraMessageBoxForm.Exists:
        Log.Message("Data not Found")
        healthEdge_Manager = Aliases.HealthEdge_Manager
        healthEdge_Manager.XtraMessageBoxForm2.SimpleButton.ClickButton()
        healthEdge_Manager.SearchDialog.BarDockControl.DockedBarControl.ClickItem("Close")
        claimEditor = healthEdge_Manager.ClaimEditor
        claimEditor.Activate()
        claimEditor.BarDockControl.DockedBarControl.ClickItem("Close")
        healthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
        return None
    else:
        Log.Message("XtraMessageBoxForm2 not found, performing alternative actions")
        searchDialog = healthEdge_Manager.SearchDialog
        dockedBarControl = searchDialog.BarDockControl2.DockedBarControl
        dockedBarControl.Drag(1400, 17, 166, 195)
        gridControl = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults
        rowCount = gridControl.wRowCount

        for i in range(rowCount):
            address_value = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults.wValue[i, 3]
            address_str = str(address_value)
            if address_str == combinedaddress:
                supplier_value = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults.wValue[i, 2]
                supplier_str = str(supplier_value)
                Log.Message(f"Value to paste: {supplier_str}")
                Log.Message("Compared")
                return supplier_str

        Log.Message("No matching address found")
        return None

def paste_supplier_name(supp_to_copy):
    # Part 7 - Paste the Supplier name in edit_claim form
    healthEdge_Manager = Aliases.HealthEdge_Manager
    healthEdge_Manager.SearchDialog.Close()
    claimEditor = healthEdge_Manager.ClaimEditor
    claimEditor.Activate()
    headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
    headerGroupControl.HeaderGroupHyperLinkEdit.Click(51, 7)
    supp_name = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.headerGroupControlSubmittedSupplierInformation.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo.autoEditSubmittedSupplierInfoFullName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    supp_name.SetText(supp_to_copy)
    Log.Message("Pasted")

def main():
    #login_to_application()
    #select_work_basket()
    #set_filtering_criteria()

    healthEdge_Manager = Aliases.HealthEdge_Manager
    resultGridClaimReviewRepair = healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
    gridControl = resultGridClaimReviewRepair.gridControlResults
    WBrowCount = gridControl.wRowCount
    Log.Message(f"Row count in this page is {WBrowCount}")

    for j in range(WBrowCount):
        if check_and_edit_claim(j, gridControl, resultGridClaimReviewRepair):
            combinedaddress, NPI = retrieve_address_and_npi()
            supp_to_copy = check_supplier_in_db(NPI, combinedaddress)
            if supp_to_copy:
                paste_supplier_name(supp_to_copy)

# Execute the main function
main()
