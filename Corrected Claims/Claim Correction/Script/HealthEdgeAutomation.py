import logging
from datetime import datetime

class HealthEdgeAutomation:
    def __init__(self):
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Configure logging
        logging.basicConfig(
    filename=f'D:/Robotic Process Automation/Supplier Invoice/logs/healthEdgeAutomation_Renew-prod-3_{timestamp}.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
        
        self.healthEdge_Manager = Aliases.HealthEdge_Manager
        self.loginForm = self.healthEdge_Manager.LoginForm
        self.homeForm = self.healthEdge_Manager.HomeForm
        self.searchDialog = self.healthEdge_Manager.SearchDialog
        logging.info('HealthEdgeAutomation instance created.')

    def login(self, username, password):
        """Logs into the HealthEdge Manager"""
        try:
            TestedApps.HealthEdge_Manager.Run(1, True)
            textBoxMaskBox = self.loginForm.textEditUserName.TextBoxMaskBox
            textBoxMaskBox.Click(99, 8)
            textBoxMaskBox.SetText(username)
            logging.info(f'Entered username: {username}')

            textBoxMaskBox = self.loginForm.textEditPassword.TextBoxMaskBox
            textBoxMaskBox.Click(110, 0)
            textBoxMaskBox.SetText(password)
            logging.info('Entered password.')

            #for PROD
            self.loginForm.lookUpEditServers.Click(137, 4)
            popupLookUpEditForm = self.healthEdge_Manager.PopupLookUpEditForm
            popupLookUpEditForm.Click(55, 73)
            
            #for UAT
            #self.loginForm.lookUpEditServers.Click(213, 17)
            #healthEdge_Manager.PopupLookUpEditForm.Click(62, 104)
            
            self.loginForm.simpleButtonSubmit.ClickButton()
            logging.info('Clicked Submit button and logged in successfully.')
            
            
            
        except Exception as e:
            logging.error(f'Login failed: {str(e)}')

    def search_claim(self, claim_id):
        """Searches for a claim based on claim ID"""
        try:
            dockedBarControl = self.homeForm.BarDockControl.DockedBarControl
            dockedBarControl.ClickItem("Search")
            dockedBarControl2 = self.searchDialog.BarDockControl.DockedBarControl
            dockedBarControl2.ClickItem("Search For|Claim")

            textEdit = self.searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimpleClaimSearchCriteria.entityPanelSearchInput.autoEditClaimId.panelControlAutoEdit.TextEdit
            textEdit.TextBoxMaskBox.Click(63, 9)
            textEdit.SetText(claim_id)
            logging.info(f'Entered claim ID: {claim_id}')

            dockedBarControl2.ClickItem("Search")
            logging.info('Performed search for claim.')
        except Exception as e:
            logging.error(f'Search failed: {str(e)}')
    
    """Renews a claim from the claim view screen."""
    def renew_claim(self, claim_id):
      try:
        logging.info(f'Starting claim renewal process for claim ID: {claim_id}')
        aqUtils.Delay(2000)
        # Click on the View item to open the claim
        dockedBarControl3 = self.searchDialog.panelControl1.standaloneBarDockControlTasks.DockedBarControl
        dockedBarControl3.ClickItem("View")
        logging.info(f'Clicked View for claim ID: {claim_id}')

        # Wait for the screen to update
        aqUtils.Delay(6000)
        logging.info('Waiting for the screen to update after clicking View.')
        
        # Check if LookUpEdit exists in the expected path
        lookUpEditPath = self.homeForm.panelControlSummary.ClaimSummary.entityPanelClaimSummary.panelTop.autoEditClaimState.panelControlAutoEdit.LookUpEdit
        lookUpEditFinalPath = self.homeForm.panelControlSummary.ConvertedClaimSummary.entityPanelClaimSummary.panelTop.autoEditClaimState.panelControlAutoEdit.LookUpEdit
        
        if lookUpEditFinalPath.Exists:
          lookUpEdit = lookUpEditFinalPath
          lookUpEdit.Click(131, 12)
                        
                        # Retrieve the docked bar control and check for items
          self.homeForm.panelControlSummary.ConvertedClaimSummary.BarDockControl.DockedBarControl.ClickItem("Renew Claim")
          aqUtils.Delay(4000)
        
          logging.info(f"Clicked Renew Claim for claim ID: {claim_id}")
        
          self.healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
          logging.info(f'Successfully renewed claim ID: {claim_id}')
        else:
          if lookUpEditPath.Exists:
            lookUpEdit = lookUpEditPath
            lookUpEdit.Click(122, 8)
            value = lookUpEdit.Text
            Log.Message(value)
            logging.info(f"The value retrieved from LookUpEdit is: '{value}'")
            self.homeForm.BarDockControl2.DockedBarControl.ClickItem("Home")
            return False
            
          

      except Exception as e:
        logging.error(f'Failed to renew claim ID: {claim_id}. Error: {str(e)}')
        return False

      return True



    def handle_reason_code(self):
        """Handles the reason code popup during claim renewal"""
        try:
            promptForReasonCode = self.healthEdge_Manager.PromptForReasonCode
            promptForReasonCode.panelReason.lookUpEditReasonCode.Click(241, 14)
            popupLookUpEditForm = self.healthEdge_Manager.PopupLookUpEditForm
            popupLookUpEditForm.Click(93, 78)
            
            textBoxMaskBox = promptForReasonCode.panelReason.memoEditComment.TextBoxMaskBox
            textBoxMaskBox.Click(107, 9)
            textBoxMaskBox.keys("Claim renewed, Corrected claim received")
            
            promptForReasonCode.panelControlBottom.simpleButtonOK.ClickButton()
            logging.info('Handled reason code popup and clicked OK.')
            
            aqUtils.Delay(6000)
            self.homeForm.BarDockControl2.DockedBarControl.ClickItem("Home")
        except Exception as e:
            logging.error(f'Handling reason code failed: {str(e)}')
    


  
  


def Test1():
  self.homeForm.panelControlSummary.ClaimSummary.entityPanelClaimSummary.panelTop.autoEditClaimState.panelControlAutoEdit.LookUpEdit
  lookUpEdit = self.homeForm.panelControlSummary.ConvertedClaimSummary.entityPanelClaimSummary.panelTop.autoEditClaimState.panelControlAutoEdit.LookUpEdit
  lookUpEdit.Click(131, 12)
  lookUpEdit.Click(131, 12)
  lookUpEdit.Click(131, 12)
