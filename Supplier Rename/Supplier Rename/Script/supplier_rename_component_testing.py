def Test1():
     i=0
     while i < 20:     
          combinedaddress = '2601 E MAIN ST STE 100, VENTURA, CA, 93003'
          address_values= []
          healthEdge_Manager = Aliases.HealthEdge_Manager
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
            
          i+=1
            
#supplier id value to paste : 1107045        

def Test2():
  healthEdge_Manager = Aliases.HealthEdge_Manager
  headerGroupControl = healthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
  headerGroupControl.HeaderGroupHyperLinkEdit.Click(42, 9)
  referenceMenuButton = headerGroupControl.supplierReference.autoSizingPanelSupplier.referenceMenuButtonSupplier
  referenceMenuButton.Click(6, 8)
  referenceMenuButton.PopupMenu.Click("Look up")
  healthEdge_Manager.XtraMessageBoxForm3.SimpleButton.ClickButton()
  resolveDialog = healthEdge_Manager.ResolveDialog
  panelControl = resolveDialog.panelControlLeft
  panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SimpleSupplierSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit.SetText("1107045")
  panelControl.panelControlSearch.simpleButtonSearch.ClickButton()
  resolveDialog.panelControlBottom.simpleButtonOK.ClickButton()

def Test3():
  healthEdge_Manager = Aliases.HealthEdge_Manager
  healthEdge_Manager.XtraMessageBoxForm2.SimpleButton.ClickButton()
  healthEdge_Manager.SearchDialog.BarDockControl.DockedBarControl.ClickItem("Close")
  
  
  
 # Processed Claims:  ['2024222001392']

def Test4():
  Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.BarDockControl.DockedBarControl.ClickItem("Refresh")
