import logging
from datetime import datetime
from login import login_to_health_edge

class HealthEdgeAutomation:
    def __init__(self, username, password):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Configure logging
        logging.basicConfig(
            filename=f'D:/Robotic Process Automation/Supplier Invoice/healthEdgeAutomation-version-2_uat_sample_{timestamp}.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.username = username
        self.password = password
        self.healthEdge_Manager = Aliases.HealthEdge_Manager

    def login(self):
        # Login using a separate function
        login_to_health_edge(self.username, self.password)

    def navigate_to_workbasket(self):
        homeForm = self.healthEdge_Manager.HomeForm
        homeForm.BarDockControl2.DockedBarControl.ClickItem("Workbasket|Supplier Invoice Repair")

    def search_claim_in_workbasket(self, claim_id):
        resultGrid = self.healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridSupplierInvoiceRepair
        textEdit = resultGrid.panelControlCustomPanel.SupplierInvoiceRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.autoEditClaimHccId.panelControlAutoEdit.TextEdit

        # Set the claim ID and search
        textEdit.TextBoxMaskBox.Click(60, 8)
        textEdit.SetText(claim_id)
        textEdit.TextBoxMaskBox.Keys("[Enter]")

        # Check the row count
        rowCount = resultGrid.RowCount
        if rowCount > 0:
            logging.info(f"Found {rowCount} claim(s) for Claim ID: {claim_id}")
            for rowIndex in range(rowCount):
                Log.Message("Click on Match Claim")
                rowCount=rowCount - 1
                Log.Message(rowCount)
                self.match_claim(claim_id)
                
        else:
            logging.info(f"No claims found for Claim ID: {claim_id}")

        # Call close_workbasket here and pass the rowCount
        self.close_workbasket(rowCount)

    def match_claim(self, claim_id):
        # Match and process the claim
        self.healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridSupplierInvoiceRepair.BarDockControl.DockedBarControl.ClickItem("Match Claim")
        panelControl = self.healthEdge_Manager.MatchSupplierInvoiceWizard.xtraTabControlWizard.xtraTabPageWizard.wizardControl.wizardClaimCriteriaPage.WizardClaimCriteria.panelControl
        claimSearchInput = panelControl.xtraScrollableControlSearch.MatchSupplierInvoiceClaimSearch.xtraTabControl.xtraTabPageClaim.SimpleClaimSearchCriteria.entityPanelSearchInput.autoEditClaimId.panelControlAutoEdit.TextEdit

        claimSearchInput.TextBoxMaskBox.Click(75, 13)
        claimSearchInput.SetText(claim_id)
        panelControl.standaloneBarDockControlClaimSearch.DockedBarControl.ClickItem("Search")
        self.sort_claims_by_last_changed()
        logging.info(f"Claim {claim_id} matched successfully.")

    def sort_claims_by_last_changed(self):
        # Sort claims by "Last Changed On"
        logging.info("Starting to sort claims by 'Last Changed On'")
        Log.Message("Sort the claim now")
        aqUtils.Delay(5000)

        # Ensure you are in the correct context
        matchSupplierInvoiceClaimSelection = self.healthEdge_Manager.MatchSupplierInvoiceWizard.xtraTabControlWizard.xtraTabPageWizard.wizardControl.wizardClaimCriteriaPage.WizardClaimCriteria
        gridControl = matchSupplierInvoiceClaimSelection.panelControl.panelResults.claimSearchResultGrid.gridControlResults
        gridControl.ClickColumnHeaderRXY("Last Changed On", 92, 12)
        matchSupplierInvoiceClaimSelection.XtraPopupMenu.Check("Sort Descending", True)
        aqUtils.Delay(2000)
        gridControl.ClickCellXY(0, "Last Changed On", 90, 9)
        logging.info("Sorting completed, proceeding to complete matching process")
        self.complete_matching_process()

    def complete_matching_process(self):
        # Complete the matching process
        Log.Message("Complete Matching now")

        wizardControl = self.healthEdge_Manager.MatchSupplierInvoiceWizard.xtraTabControlWizard.xtraTabPageWizard.wizardControl
        wizardControl.WizardButton.ClickButton()
        matchSupplierInvoiceAuditLog = wizardControl.wizardPageAuditLog.WizardPageAuditLogPage
        matchSupplierInvoiceAuditLog.lookUpEditDenialReasonCodes.Click(818, 9)
        popupLookUpEditForm = self.healthEdge_Manager.PopupLookUpEditForm
        popupLookUpEditForm.Click(790, 40)
        matchSupplierInvoiceAuditLog.lookUpEditAssignReason.Click(823, 8)
        popupLookUpEditForm.Click(754, 27)
        aqUtils.Delay(2000)
        wizardControl.wizardButton.ClickButton()
        aqUtils.Delay(2000)
        wizardControl.WizardButton2.ClickButton()
        aqUtils.Delay(5000)
        logging.info(f"Completed the matching process for Claim ID: {claim_id}")
        Log.Message("Completed the Matching")
        return True
        

    def close_workbasket(self, rowCount):
        workbasketForm = self.healthEdge_Manager.WorkbasketForm
        dockedBarControl = workbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridSupplierInvoiceRepair.BarDockControl.DockedBarControl
        
        if rowCount > 1:
            logging.info(f"Not closing the workbasket because there are {rowCount} claims.")
            return  # Exit the method without closing the workbasket

        # Proceed to clear inputs and close workbasket if rowCount is 1 or less
        dockedBarControl.ClickItem("Clear Inputs")
        dockedBarControl.ClickItem("Refresh")
        workbasketForm.BarDockControl.DockedBarControl.ClickItem("Close")
        self.healthEdge_Manager.HomeForm.BarDockControl.DockedBarControl.ClickItem("Home")
        self.healthEdge_Manager.WorkbasketForm.BarDockControl.DockedBarControl.ClickItem("Close")
        logging.info(f"Closed the workbasket for Claim ID: {self.claim_id}")

