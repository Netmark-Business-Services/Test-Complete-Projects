﻿import os

def Test1():
    """
    This function performs automated testing for the HealthEdge application.
    It reads data from an Excel file and updates Practitioner Race and Ethnicity details.
    """
    # Start of the script
    Log.Message("Starting the ProviderAddressUpdate script.")
 
    # Define directories for screenshots and logs
    project_dir = Project.Path
    screenshots_dir = os.path.join(project_dir, "Screenshots")
    logs_dir = os.path.join(project_dir, "Logs")
 
    # Create directories if they do not exist
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
 
    # Call the Login function
    # Login()  # Uncomment this if you have a Login function to call

    try:
        # Load data from the Excel file for data-driven testing
        Log.Message("Opening Excel file for data-driven testing.")
        DDT.ExcelDriver("C:\\Users\\nishw\\OneDrive\\Documents\\TestComplete 15 Projects\\RaceAndEthnicity\\Practitioner_Demographics_20240412.xlsx", "Sheet2", True)
        record_count = 0

        while not DDT.CurrentDriver.EOF():
            record_count += 1
            Log.Message("Reading data from Excel file.")
            Practitioner_HccId = DDT.CurrentDriver.Value["Practitioner HccId"]
            Race = DDT.CurrentDriver.Value["Race"]
            Ethnicity = DDT.CurrentDriver.Value["EthnicityName"]
            
            
            Log.Message(f"Processing Practitioner_HccId: {Practitioner_HccId}")
            
            # Navigate to the search tab and search for the practitioner
            healthEdge_Manager = Aliases.HealthEdge_Manager
            homeForm = healthEdge_Manager.HomeForm
            panelControl = homeForm.panelControlDetail
            
            Log.Message("Navigating to search tab.")
            healthEdge_Manager.panelControl.homeTab1.WidgetsHost.WidgetContainer.ProviderWidgetControl.xtraScrollableControlProviders.TaskRow.panelControlTop.panelControlTaskLinks.SimpleButtonSearch.ClickButton()
            
            Log.Message("Entering Practitioner HccId in search.")
            searchDialog = healthEdge_Manager.SearchDialog
            textEdit = searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimplePractitionerSearchCriteria.entityPanelSearchInput.autoEditHccIdentifier.panelControlAutoEdit.TextEdit
            textEdit.SetText(Practitioner_HccId)
            textEdit.TextBoxMaskBox.Keys("[Enter]")
            Log.Message("Opening Practitioner details.")
            searchDialog.panelControl1.panelResults.BaseResultGrid.gridControlResults.DblClickCellXY(0, "NPI", 60, 8)
            dockedBarControl = homeForm.BarDockControl.DockedBarControl
            Log.Message("Clicking to open edit form for the practitioner.")
            dockedBarControl.ClickItem("Open for Edit")

            # Edit Ethnicity and Race
            entityEditForm = healthEdge_Manager.EntityEditForm
            practitionerEditControl = entityEditForm.panelBottom.xtraTabControlEdit.xtraTabPageEdit.PractitionerEditControl
            
            Log.Message("Updating Ethnicity.")
            lookUpEdit = practitionerEditControl.entityPanelSummary.codeEntryEditRaceOrEithnicity.LookUpEdit
            lookUpEdit.Click()
            lookUpEdit.SetText(Ethnicity)
            popupLookUpEditForm.Click(17, 10)

            Log.Message("Updating Race.")
            lookUpEdit = practitionerEditControl.entityPanelSummary.codeEntryEditRaceOrEithnicity.LookUpEdit
            lookUpEdit.Click()
            lookUpEdit.SetText(Race)
            popupLookUpEditForm.Click(17, 10)

            # Take a screenshot before saving
            screenshot_path = os.path.join(screenshots_dir, f"BeforeSave_{Practitioner_HccId}.png")
            Log.Message("Taking screenshot before saving.")
            SaveScreenshot(screenshot_path)

            # Save the updated information
            Log.Message("Saving the updated information.")
            entityEditForm.BarDockControl.DockedBarControl.ClickItem("Save")
            
            aqUtils.Delay(1000)
            Log.Message(f"Finished processing Practitioner_HccId: {Practitioner_HccId}")
            DDT.CurrentDriver.Next()

    finally:
        if DDT.CurrentDriver is not None:
            Log.Message("Closing the Excel driver.")
            DDT.CloseDriver(DDT.CurrentDriver.Name)
        else:
            Log.Message("No driver to close.")

    # End of the script
    Log.Message("Test1 script completed.")