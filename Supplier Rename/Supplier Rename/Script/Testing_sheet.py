def Test1():
            gridControl = Aliases.HealthEdge_Manager.WorkbasketForm.panelControlRight.panelControlBaseResults.panelControlResults.ResultGridClaimReviewRepair.gridControlResults
            WBrowCount = gridControl.wRowCount
            Log.Message(f"row count in this page is {WBrowCount}")
            claim_type = str(gridControl.wValue[0, 2])
            Log.Message(f"claim type: {claim_type}")