def Test1():
  healthEdge_Manager = Aliases.HealthEdge_Manager
  healthEdge_Manager.HomeForm.XtraMainMenu.Click("Workbasket|Claim Review & Repair")
  aqUtils.delay(5000)
  resultGridClaimReviewRepair = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair
  dockedBarControl = resultGridClaimReviewRepair.BarDockControl.DockedBarControl
  dockedBarControl.ClickItemXY("Rows per Page", 110, 11)
  textBoxMaskBox = dockedBarControl.SpinEdit3.TextBoxMaskBox
  textBoxMaskBox.Keys("^a")
  textBoxMaskBox.SetText("2,000")
  aqUtils.Delay(2000)
  textBoxMaskBox.Keys("[Enter]")
  aqUtils.Delay(2000)
  resultGridClaimReviewRepair.panelControlCustomPanel.ClaimReviewRepairWorkbasketSearchCriteria.entityPanelSearchInput.panelControlCommonSearch.autoEditClaimHccId.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Keys("[Enter]")

  
