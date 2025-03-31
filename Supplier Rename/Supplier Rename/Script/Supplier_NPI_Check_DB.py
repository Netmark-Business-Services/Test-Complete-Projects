def Test1():
    #23861 McBean Pkwy Ste, Valencia, CA, 91355
    #1205218641
    #1215903018
    #1629553730
    NPI = "1386937977"   
    add_to_check = "2601 E MAIN ST STE 100, VENTURA, CA, 93003"
    supp_to_copy = ""
    # Convert NPI to integer
    address_values = []
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
    

    # Initialize a variable to control the while loop
    found = False
    # Use while loop to check if NPI exists in the rejected_list_npi
    index = 0
    while index < len(rejected_list_npi):
      if rejected_list_npi[index] == npi_int:
        found = True
        Log.Message("npi in rejected list")
        break
      index += 1
    if found:
      print(f"NPI {NPI} exists in the rejected list.")
    else:
      print(f"NPI {NPI} does not exist in the rejected list.")
      
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
          address_value = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults.wValue[i, 3]
          address_str = str(address_value).upper()
          Log.Message(f"Given value  : {add_to_check}")
          Log.Message(f"add to check  : {address_str}")
          if address_str == add_to_check:
            address_values.append(address_str)
            supplier_value = searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults.wValue[i, 2]
            supplier_str = str(supplier_value).upper()
            supp_to_copy = supplier_str
            Log.Message("Compared")
            Log.Message(f"value to paste : {supp_to_copy}")
            healthEdge_Manager.SearchDialog.Close()
            #claimEditor = healthEdge_Manager.ClaimEditor
            #claimEditor.Activate()
          else:
            Log.Message(f"Value at [{i}, 3]: {address_value}")
            Log.Message("No values found")
          i+=1
          
          Log.Message("No issues")
        Aliases.HealthEdge_Manager.SearchDialog.Close()
        
    # Log the entire list of address values
    
    
    claimEditor = healthEdge_Manager.ClaimEditor
    claimEditor.Activate()
    headerGroupControl = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
    headerGroupControl.HeaderGroupHyperLinkEdit.Click(51, 7)
    supp_name = claimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.headerGroupControlSubmittedSupplierInformation.autoSizingPanelSubmittedSupplier.headerGroupControlSubmittedSupplierInfo.SubmittedSupplierInfo.entityPanelSubmittedSupplierInfo.autoEditSubmittedSupplierInfoFullName.panelControlAutoEdit.TextEdit.TextBoxMaskBox
    supp_name.SetText(supp_to_copy)
    Log.Message("Pasted")
  

