global j  # To modify the global j variable
    #aqUtils.Delay(15000)
    j = start_index
    gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
    WBrowCount = gridControl.wRowCount
    
    Log.Message(f"row count in this page is {WBrowCount}")
    Log.Message(f"Processing row {j}")

#def process_each_row(j_index,WBrowCount):
    while j < WBrowCount:
        rej_claim_id = str(gridControl.wValue[j, 1])
        Log.Message(f"processing claim: " + rej_claim_id)
        
        # Check if rej_claim_id is not in DNU_CLAIM_ID
        if rej_claim_id not in DNU_CLAIM_ID:
            review_reason = gridControl.wValue[j, 10]
            reasons = str(review_reason)
            Log.Message(f"reason in row {j} is {reasons}")

            #if reasons == "Supplier could not be identified":
            edit_row(j)
            combinedaddress = edit_claim_form()
            #edit provider information
            #headerGroupControl = Aliases.HealthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
            #headerGroupControl.HeaderGroupHyperLinkEdit.Click(39, 7)
            #headerGroupControl.payToAddressControl.headerGroupControlPayToAddress.HeaderGroupHyperLinkEdit.Click(9, 7)
  
  
          #continuing process
            #healthEdge_Manager = Aliases.HealthEdge_Manager
            #referenceMenuButton = healthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider.supplierLocationPanel1.autoSizingPanelLocationName.referenceMenuButtonSupplierLocation
            healthEdge_Manager = Aliases.HealthEdge_Manager
            headerGroupControl = healthEdge_Manager.ClaimEditor.panelEditClaim.panelControlDetail.panelControlDetailView.Claim.tabControlClaim.tabPageHeader.claimHeader.entityPanel.subEntityPanelConsolidatedInput.panelControlSubscriber.headerGroupProvider
            claimSupplierReferenceControl = headerGroupControl.supplierReference
            supp_code = claimSupplierReferenceControl.autoSizingPanelSupplier.textEditSupplierID.TextBoxMaskBox
            supplier_id = str(supp_code.wText)
            Log.Message("The supplier_id is: " + supplier_id)
            
            referenceMenuButton = headerGroupControl.supplierLocationPanel1.autoSizingPanelLocationName.referenceMenuButtonSupplierLocation
            referenceMenuButton.Click(9, 8)
            referenceMenuButton.PopupMenu.Click("Look up")
            #panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit.TextBoxMaskBox.Click(57, 8)

            
            
            #referenceMenuButton.Click(9, 10)
            #referenceMenuButton.PopupMenu.Click("Look up")
            panelControl = healthEdge_Manager.ResolveDialog.panelControlLeft
            textBoxMaskBox = panelControl.panelControlSearchCriteria.xtraScrollableControlSearchCriteria.SupplierLocationSearchCriteria.entityPanelSupplierSearchInput.autoEditSupplierHccIdentifier.panelControlAutoEdit.TextEdit.TextBoxMaskBox
            textBoxMaskBox.SetText(supplier_id)
  
            panelControl.panelControlSearch.simpleButtonSearch.ClickButton()
            xtraMessageBoxForm = healthEdge_Manager.WaitAliasChild("XtraMessageBoxForm2", 1000)
            if xtraMessageBoxForm.Exists:
                Log.Message("Data not Found")
                healthEdge_Manager.XtraMessageBoxForm2.SimpleButton.ClickButton()
                #healthEdge_Manager.SearchDialog.BarDockControl.DockedBarControl.ClickItem("Close")
                Aliases.HealthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonCancel.ClickButton()
                close_claim_editor()
                #process_grid_rows(j + 1)
                return None
            #Build a for loop here
            else:
                gridControl = Aliases.HealthEdge_Manager.ResolveDialog.panelControlResults.BaseResultGrid.gridControlResults
                gcvalue = gridControl.wValue[0,0]
                Log.Message(f"{gcvalue}")
                gc_extracted = str(gcvalue).split(" - ")[1].strip()
                Log.Message(f"extracted string : {gc_extracted}")
                if gc_extracted == address:
                    Log.Message(f"extracted string {gc_extracted} matches with address in claim {address}")
                    healthEdge_Manager = Aliases.HealthEdge_Manager
                    simpleButton = healthEdge_Manager.ResolveDialog.panelControlBottom.simpleButtonOK
                    simpleButton.ClickButton()
                #####healthEdge_Manager.ClaimEditor.BarDockControl.DockedBarControl.ClickItem("Submit")
                else:
                    Log.Message("not matching")
    j += 1
        