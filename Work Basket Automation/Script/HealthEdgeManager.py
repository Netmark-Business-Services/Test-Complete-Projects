import logging
from datetime import datetime

class HealthEdgeManager:
    def __init__(self, healthEdge_Manager):
        self.healthEdge_Manager = healthEdge_Manager
        self.processed_rows = set()  # Track processed rows across all pages
        self.failed_rows = set()  # Track rows that failed to move out of the workbasket
        
        # Set up logging to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f'workbasket_log_{timestamp}.txt'


        # Configure logging
        logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

    def navigate_to_workbasket(self):
        self.logger.info("Navigating to the Enrollment Review Repair Workbasket.")
        Log.Message("Navigating to the Enrollment Review Repair Workbasket.")
        self.healthEdge_Manager.HomeForm.BarDockControl.DockedBarControl.ClickItem("Workbasket|Enrollment Review  Repair")
        self.logger.info("Navigation complete.")
        Log.Message("Navigation complete.")

    def process_workbasket(self):
        currentPage = 1
        while True:
            self.navigate_to_page(currentPage)
            resultGridEnrollmentReviewRepair = self.healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridEnrollmentReviewRepair
            gridControl = resultGridEnrollmentReviewRepair.gridControlResults
            rowCount = gridControl.wRowCount
            self.logger.info(f"Processing page {currentPage}, Initial Row Count: {rowCount}")
            Log.Message(f"Processing page {currentPage}, Initial Row Count: {rowCount}")

            targetDescription = "Plan Selection Date Range UDT validation failed"
            reviewRepairReasonColumnIndex = 12

            i = 0
            while i < rowCount:
                subscriptionId = gridControl.wValue[i, 2]
                self.logger.info(f"Processing row: {i}")
                Log.Message(f"Processing row: {i}")
                rowKey = (currentPage, i)
                if rowKey in self.failed_rows:
                    self.logger.info(f"Skipping row {i} with {subscriptionId} on page {currentPage} as it previously failed to move out of workbasket.")
                    Log.Message(f"Skipping row {i} with {subscriptionId} on page {currentPage} as it previously failed to move out of workbasket.")
                    i += 1
                    continue

                reviewReason = gridControl.wValue[i, reviewRepairReasonColumnIndex]
                subscriptionId = gridControl.wValue[i, 2]
                #if reviewReason.contains(targetDescription) and gridControl.wValue[i,9] is None:
                if reviewReason.contains(targetDescription):
                    self.logger.info(f"Matched Row {i} on page {currentPage}: {reviewReason}, Subscription ID: {subscriptionId}")
                    Log.Message(f"Matched Row {i} on page {currentPage}: {reviewReason}, Subscription ID: {subscriptionId}")
                    self.edit_row(gridControl, i)
                    self.save_changes()
                    self.add_comment()
                    self.confirm_changes()
                    self.refresh_workbasket(resultGridEnrollmentReviewRepair)

                    # After refresh, reset to the first page and start over
                    self.failed_rows.add(rowKey)  # Mark the row as failed
                    currentPage = 1
                    i = 0
                    break

                else:
                    self.logger.info(f"No match found for row {i} on page {currentPage}, moving to the next row.")
                    Log.Message(f"No match found for row {i} on page {currentPage}, moving to the next row.")
                    i += 1
            else:
                # If we finish all rows in the current page without break, try next page
                if self.has_next_page(currentPage):
                    currentPage += 1
                    self.logger.info(f"Moving to page {currentPage}.")
                    Log.Message(f"Moving to page {currentPage}.")
                else:
                    break

        self.logger.info("Completed processing all pages.")
        Log.Message("Completed processing all pages.")

    def has_next_page(self, currentPage):
        try:
            dockedBarControl = self.healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridEnrollmentReviewRepair.BarDockControl.DockedBarControl
            dockedBarControl.ClickItem("[4]")
            return True
        except:
            return False

    def navigate_to_page(self, pageNumber):
        try:
            dockedBarControl = self.healthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridEnrollmentReviewRepair.BarDockControl.DockedBarControl
            for _ in range(pageNumber - 1):
                dockedBarControl.ClickItem("[4]")
                aqUtils.Delay(5000)  # Wait for the page to load
        except:
            Log.Message(f"Unable to navigate to page {pageNumber}")
            self.logger.warning(f"Unable to navigate to page {pageNumber}")

    def edit_row(self, gridControl, rowIndex):
        gridControl.ClickCellXY(rowIndex, "Edit", 22, 44)
        asOfDate = self.healthEdge_Manager.AsOfDate
        if asOfDate.Exists:
            Log.Message("Setting 'Do Not Reprocess Claims' option.")
            self.logger.info("Setting 'Do Not Reprocess Claims' option.")
            asOfDate.panelControlTop.radioGroupReprocessClaims.ClickItem("Do Not Reprocess Claims")
            asOfDate.panelControlBottom.simpleButtonOK.ClickButton()
        else:
            Log.Warning("asOfDate object does not exist.")
            self.logger.warning("asOfDate object does not exist.")

    def save_changes(self):
        dockedBarControl = self.healthEdge_Manager.EntityEditForm.BarDockControl.DockedBarControl
        dockedBarControl.ClickItem("Save")

    def add_comment(self):
        selectMemberReasonCodes = self.healthEdge_Manager.SelectMemberReasonCodes
        panelControl = selectMemberReasonCodes.panelControl1
        panelControl.lookUpReasonCodes.Click(112, 16)
        self.healthEdge_Manager.PopupLookUpEditForm.Click(109, 13)
        textBoxMaskBox = panelControl.memoEditMemberComment.TextBoxMaskBox
        textBoxMaskBox.Click(69, 19)
        textBoxMaskBox.Keys("WB_Automation")
        selectMemberReasonCodes.simpleButtonOK.ClickButton()

    def confirm_changes(self):
        #aqUtils.Delay(3000)
        if self.healthEdge_Manager.XtraMessageBoxForm.Exists:
            self.healthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()
        else:
            return

    def refresh_workbasket(self, resultGridEnrollmentReviewRepair):
        dockedBarControl = resultGridEnrollmentReviewRepair.BarDockControl.DockedBarControl
        #aqUtils.Delay(5000)
        dockedBarControl.ClickItem("Refresh")
        aqUtils.Delay(3000)
