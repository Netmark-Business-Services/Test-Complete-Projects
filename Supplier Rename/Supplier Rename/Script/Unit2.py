import logging
from datetime import datetime

class HealthEdgeManager:
    def __init__(self, healthEdge_Manager, username, password, target_reason):
        self.healthEdge_Manager = healthEdge_Manager
        self.username = username
        self.password = password
        self.target_reason = target_reason
        self.failed_rows = set()  # Track rows that failed to move out of the workbasket
        self.address_values = []

        # Set up logging to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f'workbasket_log_{timestamp}.txt'

        # Configure logging
        logging.basicConfig(filename=log_filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

    def login(self):
        self.logger.info("Starting the application and logging in.")
        TestedApps.HealthEdge_Manager.Run(1, True)
        loginForm = self.healthEdge_Manager.LoginForm
        loginForm.textEditUserName.TextBoxMaskBox.SetText(self.username)
        loginForm.textEditPassword.TextBoxMaskBox.SetText(self.password)
        loginForm.lookUpEditServers.Click(60, 9)
        self.healthEdge_Manager.PopupLookUpEditForm.Click(29, 73)
        loginForm.simpleButtonSubmit.ClickButton()
        aqUtils.Delay(30000)
        self.logger.info("Login complete.")

    def navigate_to_workbasket(self):
        self.logger.info("Navigating to Claim Review & Repair workbasket.")
        self.healthEdge_Manager.HomeForm.XtraMainMenu.Click("Workbasket|Claim Review & Repair")
        aqUtils.Delay(5000)
        self.logger.info("Navigation complete.")

    def set_filtering_criteria(self):
        self.logger.info("Setting filtering criteria in the workbasket.")
        resultGridClaimReviewRepair = self.healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
        panelControl = resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch
        referenceMenuButton = panelControl.codeEntryResolverButton
        referenceMenuButton.Click(12, 11)
        referenceMenuButton.PopupMenu.Click("Look up")
        resolveDialog = self.healthEdge_Manager.ResolveDialog
        resolveDialog.panelControlLeft.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.CodeEntrySearchCriteria.entityPanel.autoEditCodeEntry.panelControlAutoEdit.TextEdit.SetText("7")
        resolveDialog.panelControlLeft.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.CodeEntrySearchCriteria.entityPanel.autoEditShortName.panelControlAutoEdit.TextEdit.SetText("Supplier could not be identified")
        resolveDialog.panelControlLeft.panelControlSearch.simpleButtonSearch.ClickButton()
        resolveDialog.panelControlBottom.simpleButtonOK.ClickButton()
        panelControl.textEditReviewReasonCode.TextBoxMaskBox.Keys("[Enter]")
        self.logger.info("Filtering criteria set.")

    def process_workbasket(self):
        self.logger.info("Processing workbasket rows.")
        resultGridClaimReviewRepair = self.healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
        gridControl = resultGridClaimReviewRepair.gridControlResults
        WBrowCount = gridControl.wRowCount
        self.logger.info(f"Row count in this page is {WBrowCount}")
        
        for j in range(WBrowCount):
            review_reason = gridControl.wValue[j, 10]
            reasons = str(review_reason)
            self.logger.info(f"Reason in row {j} is {reasons}")

            if reasons == self.target_reason:
                gridControl.ClickCellXY(j, "Edit", 16, 14)
                self.logger.info(f"Editing row {j} with reason: {reasons}")
                self.edit_claim_form()
                break  # Assuming only one match is needed

    def edit_claim_form(self):
        self.logger.info("Editing claim form to retrieve address and NPI ID.")
        claimEditor = self.healthEdge_Manager.ClaimEditor
        claimEditor.Activate()
        headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.headerGroupControlSubmittedSupplierInformation
        headerGroupControl.HeaderGroupHyperLinkEdit.Click(8, 8)
        entityPanel = headerGroupControl.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo

        address = self.extract_address(entityPanel)
        NPI = self.extract_NPI(entityPanel)

        self.check_supplier_in_db(NPI, address)

    def extract_address(self, entityPanel):
        addressTextBox = entityPanel.autoEditSubmittedSupplierInfoAddress.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        address = str(addressTextBox.wText)
        address2TextBox = entityPanel.autoEditSubmittedSupplierInfoAddress2.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        address2 = str(address2TextBox.wText).strip()
        cityTextBox = entityPanel.autoEditSubmittedSupplierInfoCityName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        city = str(cityTextBox.wText)
        stateLookUpEdit = entityPanel.autoEditSubmittedSupplierInfoState.panelControlAutoEdit.LookUpEdit
        state = str(stateLookUpEdit.Text)
        zipTextBox = entityPanel.autoEditSubmittedSupplierInfoZipCode.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        zipCode = str(zipTextBox.Text)

        combined_address = f"{address}, {address2}, {city}, {state}, {zipCode}" if address2 else f"{address}, {city}, {state}, {zipCode}"
        self.logger.info(f"Extracted address: {combined_address}")
        return combined_address

    def extract_NPI(self, entityPanel):
        NPILookUpEdit = entityPanel.autoEditSubmittedSupplierInfoNPI.panelControlAutoEdit.TextEdit
        NPI = str(NPILookUpEdit.Text)
        self.logger.info(f"Extracted NPI: {NPI}")
        return NPI

    def check_supplier_in_db(self, NPI, address):
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

        if npi_int in rejected_list_npi:
            self.logger.info(f"NPI {NPI} exists in the rejected list.")
            print(f"NPI {NPI} exists in the rejected list.")
        else:
            self.logger.info(f"NPI {NPI} does not exist in the rejected list.")
            print(f"NPI {NPI} does not exist in the rejected list.")
            self.search_supplier(NPI, address)

    def search_supplier(self, NPI, address):
        self.logger.info("Searching for supplier in the database.")
        self.healthEdge_Manager.HomeForm.BarDockControl.DockedBarControl.ClickItem("Search")
        searchDialog = self.healthEdge_Manager.SearchDialog
        searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleSupplierSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit.SetText(NPI)
        searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleSupplierSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Keys("[Enter]")

        xtraMessageBoxForm = self.healthEdge_Manager.WaitAliasChild("XtraMessageBoxForm2", 1000)
        if xtraMessageBoxForm.Exists:
            self.logger.info("Data not Found.")
        else:
            self.logger.info("Supplier found, extracting details.")
            self.extract_supplier_details(searchDialog, address)

    def extract_supplier_details(self, searchDialog, address):
        gridControl = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults
        rowCount = gridControl.wRowCount

        for i in range(rowCount):
            address_value = gridControl.wValue[i, 3]
            address_str = str(address_value)
            self.address_values.append(address_str)

            if address_str == address:
                supplier_value = gridControl.wValue[i, 2]
                supplier_str = str(supplier_value)
                self.logger.info(f"Supplier to copy: {supplier_str}")
                self.paste_supplier_name(supplier_str)
                break
        else:
            self.logger.info("No matching supplier found.")

    def paste_supplier_name(self, supplier_name):
        self.logger.info("Pasting supplier name in the claim form.")
        claimEditor = self.healthEdge_Manager.ClaimEditor
        claimEditor.Activate()
        headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
        headerGroupControl.HeaderGroupHyperLinkEdit.Click(51, 7)
        supp_name = headerGroupControl.headerGroupControlSubmittedSupplierInformation.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo.autoEditSubmittedSupplierInfoFullName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
        supp_name.SetText(supplier_name)
        self.logger.info("Supplier name pasted successfully.")

# Usage example
healthEdge_Manager = Aliases.HealthEdge_Manager
manager = HealthEdgeManager(healthEdge_Manager, "skrishnan", Project.Variables.Password1, "Supplier could not be identified")
manager.login()
manager.navigate_to_workbasket()
manager.set_filtering_criteria()
manager.process_workbasket()