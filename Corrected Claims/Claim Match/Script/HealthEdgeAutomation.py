import logging
from datetime import datetime
from login import login_to_health_edge

class HealthEdgeAutomation:
    def __init__(self, username, password):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Configure logging
        logging.basicConfig(
            filename=f'D:/Robotic Process Automation/Supplier Invoice/healthEdgeAutomation-MatchingClaims-3_prod_{timestamp}.log',
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
        
        rowCount = resultGrid.RowCount
        # Repeatedly process claims until the workbasket is cleared
        while True:
            # Check the row count
            if rowCount > 0:
                logging.info(f"Found {rowCount} claim(s) for Claim ID: {claim_id}")
                for rowIndex in range(rowCount):
                    logging.info(f"Processing claim #{rowIndex + 1} out of {rowCount}")
                    self.match_claim(claim_id)
                    rowCount -= 1  # Decrement row count after processing each claim
            else:
                logging.info(f"No more claims found for Claim ID: {claim_id}")
                break  # Exit the loop when no more claims are found

        # Call close_workbasket here
        self.close_workbasket()

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
    # Log the matching process start
        Log.Message("Complete Matching now")

        wizardControl = self.healthEdge_Manager.MatchSupplierInvoiceWizard.xtraTabControlWizard.xtraTabPageWizard.wizardControl
        wizardControl.WizardButton.ClickButton()

        matchSupplierInvoiceAuditLog = wizardControl.wizardPageAuditLog.WizardPageAuditLogPage
        matchSupplierInvoiceAuditLog.lookUpEditDenialReasonCodes.Click(818, 9)
        
        textBoxMaskBox = wizardControl.wizardPageAuditLog.WizardPageAuditLogPage.lookUpEditDenialReasonCodes.TextBoxMaskBox
        textBoxMaskBox.Click(398, 9)
        
        textBoxMaskBox.SetText("Claim was replaced")
        popupLookUpEditForm = self.healthEdge_Manager.PopupLookUpEditForm
        #popupLookUpEditForm.Click(98, 28)

        matchSupplierInvoiceAuditLog.lookUpEditAssignReason.Click(823, 8)
        popupLookUpEditForm.Click(754, 27)

    # Increase delays to ensure the UI responds correctly
        aqUtils.Delay(3000)

        wizardControl.wizardButton.ClickButton()
        aqUtils.Delay(3000)

    # Complete the matching process
        wizardControl.WizardButton2.ClickButton()

    # Additional delay before logging completion
        aqUtils.Delay(5000)

        #logging.info(f"Completed the matching process for Claim ID: {claim_id}")
        Log.Message("Completed the Matching")

    # Return True indicating success and to continue with the next steps
        return True


    def close_workbasket(self):
        workbasketForm = self.healthEdge_Manager.WorkbasketForm
        dockedBarControl = workbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridSupplierInvoiceRepair.BarDockControl.DockedBarControl

        # Proceed to clear inputs and close workbasket
        dockedBarControl.ClickItem("Clear Inputs")
        aqUtils.Delay(2000)
        dockedBarControl.ClickItem("Refresh")
        aqUtils.Delay(5000)
        workbasketForm.BarDockControl.DockedBarControl.ClickItem("Close")
        self.healthEdge_Manager.HomeForm.BarDockControl.DockedBarControl.ClickItem("Home")
        #self.healthEdge_Manager.WorkbasketForm.BarDockControl.DockedBarControl.ClickItem("Close")
        logging.info("Closed the workbasket successfully.")





  
