import logging
from datetime import datetime

# Generate timestamp for log filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Configure logging with timestamp in the filename
log_filename = rf"C:\Users\rthotakura\Documents\Supplemental Claims\Prod_approval_claim_{timestamp}.log"

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)

logging.info("Logging initialized with timestamped filename.")

class HealthEdgeAutomation:
    def __init__(self):
        try:
            TestedApps.HealthEdge_Manager.Run(1, True)
            self.healthEdge_Manager = Aliases.HealthEdge_Manager
            self.loginForm = self.healthEdge_Manager.LoginForm
            self.dockedBarControl = self.healthEdge_Manager.HomeForm.BarDockControl.DockedBarControl
            logging.info("HealthEdgeAutomation initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing HealthEdgeAutomation: {str(e)}")
            raise

    def login(self, username, password):
        try:
            logging.info(f"Attempting to log in as {username}.")
            
            self.loginForm.textEditUserName.TextBoxMaskBox.Click(30, 4)
            self.loginForm.textEditUserName.TextBoxMaskBox.SetText(username)

            self.loginForm.textEditPassword.TextBoxMaskBox.Click(51, 10)
            self.loginForm.textEditPassword.TextBoxMaskBox.SetText(password)

            self.loginForm.lookUpEditServers.Click(88, 8)
            #Prod
            self.healthEdge_Manager.PopupLookUpEditForm.Click(46, 74)
            #UAT
            #self.healthEdge_Manager.PopupLookUpEditForm.Click(40, 103)
           

            self.loginForm.simpleButtonSubmit.ClickButton()
            aqUtils.Delay(5000)
            logging.info("Login successful.")
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            Log.Warning(f"Login failed: {str(e)}")

    def search_claim(self, claim_id):
        try:
            aqUtils.Delay(10000)
            logging.info(f"Searching for Claim ID: {claim_id}.")
            
            self.dockedBarControl.ClickItem("Search")
            searchDialog = self.healthEdge_Manager.SearchDialog

            textEdit = searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleClaimSearchCriteria.entityPanelSearchInput.autoEditClaimId.panelControlAutoEdit.TextEdit

            textEdit.TextBoxMaskBox.Click(86, 8)
            textEdit.SetText(claim_id)

            searchDialog.BarDockControl.DockedBarControl.ClickItem("Search")
            searchDialog.panelControl1.standaloneBarDockControlTasks.DockedBarControl.ClickItem("View")

            logging.info(f"Claim {claim_id} searched successfully.")
        except Exception as e:
            logging.error(f"Error searching claim {claim_id}: {str(e)}")
            Log.Warning(f"Error searching claim {claim_id}: {str(e)}")

    def approve_claim(self, claim_id):
        try:
            aqUtils.Delay(8000)
            logging.info(f"Attempting to approve Claim ID: {claim_id}.")
            
            self.dockedBarControl.ClickItem("Open for Edit")
            aqUtils.Delay(8000)
            self.healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Approve")

            promptForReasonCode = self.healthEdge_Manager.PromptForReasonCode
            promptForReasonCode.panelReason.lookUpEditReasonCode.Click(241, 6)
            self.healthEdge_Manager.PopupLookUpEditForm2.Click(193, 26)
            promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()

            #selectReviewCodes = self.healthEdge_Manager.SelectReviewCodes
            #selectReviewCodes.panelControlMessage.gridControlCodes.ClickCellXY(0, "Approve", 35, 6)
            #selectReviewCodes.flowLayoutPanel1.simpleButtonOK.ClickButton()

            logging.info(f"Claim {claim_id} approved successfully.")
        except Exception as e:
            logging.error(f"Error approving claim {claim_id}: {str(e)}")
            Log.Warning(f"Error approving claim {claim_id}: {str(e)}")

    def process_claim(self, claim_id):
        try:
            logging.info(f"Processing Claim ID: {claim_id}.")
            
            self.search_claim(claim_id)
            self.approve_claim(claim_id)
            aqUtils.Delay(15000)
            self.dockedBarControl.ClickItem("Home")
            logging.info(f"Processed Claim ID: {claim_id} successfully.")
        except Exception as e:
            logging.error(f"Failed to process Claim ID: {claim_id}. Error: {str(e)}")
            Log.Warning(f"Failed to process Claim ID: {claim_id}. Error: {str(e)}")

# Move the ExcelReader class here so it's defined before it's used
class ExcelReader:
    def __init__(self, file_path, sheet_name):
        self.driver = DDT.ExcelDriver(file_path, sheet_name)

    def get_claim_ids(self):
        claim_ids = []
        while not self.driver.EOF():
            claim_id = self.driver.Value[0]  # Assuming Claim ID is in column 1
            if claim_id:
                claim_ids.append(str(claim_id))  # Convert to string for safety
            self.driver.Next()
        
        DDT.CloseDriver(self.driver.Name)
        return claim_ids

def main():
    logging.info("Starting claim processing script.")

    app = HealthEdgeAutomation()
    username = "rthotakura"
    password = Project.Variables.Password1

    app.login(username, password)

    # Correctly instantiate ExcelReader
    excel_file = r"C:\Users\rthotakura\Documents\Supplemental Claims\ClaimReviewRepair Results_latest_prod_2.xlsx"
    sheet_name = "Sheet"
    
    reader = ExcelReader(excel_file, sheet_name)

    processed_claim_ids = set()

    # Fetch claim IDs from Excel
    claim_ids = reader.get_claim_ids()

    if not claim_ids:
        logging.warning("No Claim IDs found in Excel file.")
        Log.Message("No Claim IDs found in Excel file.")
        return

    for claim_id in claim_ids:
        if claim_id in processed_claim_ids:
            logging.info(f"Skipping already processed Claim ID: {claim_id}")
            Log.Message(f"Skipping already processed Claim ID: {claim_id}")
        else:
            app.process_claim(claim_id)
            processed_claim_ids.add(claim_id)

    logging.info("All claims have been processed successfully.")
    Log.Message("All claims have been processed successfully.")

if __name__ == "__main__":
    main()

    
    
    
            

  
