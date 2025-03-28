import os
import csv

def SaveScreenshot(file_path):
    """
    Captures the screenshot of the active window and saves it to the specified file path.
    """
    aqUtils.Delay(1000)
    screenshot = Sys.Desktop.Picture()
    screenshot.SaveToFile(file_path)
    Log.Picture(screenshot, f"Screenshot saved to {file_path}")

def save_missing_ids_to_csv(missing_practitioners, file_path):
    """
    Save the missing practitioner IDs to a CSV file.
    """
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if not file_exists:
            csvwriter.writerow(["Practitioner ID"])  # Write headers if file doesn't exist
        for practitioner_id in missing_practitioners:
            csvwriter.writerow([practitioner_id])
    Log.Message(f"Missing practitioner IDs have been saved to {file_path}")

def focus_and_clear_field(textEdit):
    """
    Focus on the Practitioner ID field and clear any existing text.
    """
    Log.Message("Focusing and clearing the Practitioner ID field.")
    textEdit.Click()  # Ensure field is focused
    textEdit.Keys("^a")  # Select all text
    textEdit.Keys("[BS]")  # Backspace to clear the text
    aqUtils.Delay(500)  # Short delay to ensure text is cleared

def RaceAndEthnicityUpdate():
    """
    This function performs automated testing for the HealthEdge application.
    It reads data from an Excel file and updates Practitioner Race and Ethnicity details.
    """
    # Start of the script
    Log.Message("Starting the RaceAndEthnicityUpdate script.")
 
    # Define directories for screenshots and logs
    project_dir = Project.Path
    screenshots_dir = os.path.join(project_dir, "Screenshots")
    logs_dir = os.path.join(project_dir, "Logs")
    missing_ids_csv_file = os.path.join(logs_dir, "MissingPractitioners.csv")
 
    # Create directories if they do not exist
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
 
    try:
        # Load data from the Excel file for data-driven testing
        Log.Message("Opening Excel file for data-driven testing.")
        excel_file_path = "C:\\Users\\nishw\\OneDrive\\Documents\\TestComplete 15 Projects\\RaceAndEthnicity\\DesktopCleanedData2.xlsx"
        DDT.ExcelDriver(excel_file_path, "Sheet1", True)
        
        missing_practitioners = []  # List to store missing practitioner IDs

        while not DDT.CurrentDriver.EOF():
            Log.Message("Reading data from Excel file.")
            
            practitioner_id_npi = DDT.CurrentDriver.Value["Practitioner ID"]
            race = DDT.CurrentDriver.Value["Race"]
            ethnicity_name = DDT.CurrentDriver.Value["EthnicityName"]
        
            Log.Message(f"Processing practitioner ID: {practitioner_id_npi}")
            
            # Navigate to the search tab and search for the practitioner
            healthEdge_Manager = Aliases.HealthEdge_Manager
            homeForm = healthEdge_Manager.HomeForm
            panelControl = homeForm.panelControlDetail

            panelControl.homeTab1.WidgetsHost.WidgetContainer.ProviderWidgetControl.xtraScrollableControlProviders.TaskRow.panelControlTop.panelControlTaskLinks.SimpleButtonSearch.ClickButton()
            
            Log.Message("Entering search criteria.")
            searchDialog = healthEdge_Manager.SearchDialog
            textEdit = searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimplePractitionerSearchCriteria.entityPanelSearchInput.autoEditHccIdentifier.panelControlAutoEdit.TextEdit
            
            if textEdit.Exists:
                Log.Message("TextEdit object found, preparing to enter new ID.")
                
                # Explicitly click and clear the field before setting new text
                textEdit.Click()
                textEdit.Keys("^a[BS]")  # Clear any existing text
                aqUtils.Delay(500)  # Ensure the field is clear

                # Set the new Practitioner ID
                textEdit.SetText(practitioner_id_npi)
                aqUtils.Delay(500)  # Ensure the text is entered

                # Hit Enter to initiate the search
                textBoxMaskBox = searchDialog.panelTop.panelSearchCriteria.tabControlSearchCriteria.tabPageGeneral.SimplePractitionerSearchCriteria.entityPanelSearchInput.autoEditHccIdentifier.panelControlAutoEdit.TextEdit.TextBoxMaskBox
                textBoxMaskBox.Keys("[Enter]")
                aqUtils.Delay(2000)  # Ensure the search operation completes
                
                # Check for "No input found" scenario
                if healthEdge_Manager.XtraMessageBoxForm.Exists:
                    Log.Message("No input found for the practitioner ID. Handling the error.")
                    healthEdge_Manager.XtraMessageBoxForm.SimpleButton.ClickButton()  # Click OK on the dialog
                    Log.Message(f"Practitioner ID {practitioner_id_npi} not found, logging and moving to next.")
                    
                    # Log the missing Practitioner ID
                    missing_practitioners.append(practitioner_id_npi)
                    save_missing_ids_to_csv(missing_practitioners, missing_ids_csv_file)  # Immediately save to CSV

                    # Clear the text box again to ensure the next ID is entered correctly
                    textEdit.Click()
                    textEdit.Keys("^a[BS]")  # Ensure the field is clear
                    aqUtils.Delay(500)

                    # Close the search dialog and prepare for new search
                    searchDialog.BarDockControl.DockedBarControl.ClickItem("Close")
                    aqUtils.Delay(1000)  # Ensure dialog closes

                    # Start a new search to reset state
                    homeForm.panelControlDetail.homeTab1.WidgetsHost.WidgetContainer2.ProviderWidgetControl.xtraScrollableControlProviders.TaskRow.panelControlTop.panelControlTaskLinks.SimpleButtonSearch.ClickButton()
                    Log.Message("Closed current search and started a new search session.")
                    

                    # Move to the next record in the Excel file
                    DDT.CurrentDriver.Next()
                    aqUtils.Delay(2000)  # Add delay to ensure the next record loads and is entered correctly

                    continue  # Skip to the next iteration to load the next Practitioner ID

                else:
                    Log.Message("Practitioner ID found, checking if results are displayed.")
                    # Check if search results are displayed by looking for a known grid or result element
                    if searchDialog.panelControl1.panelResults.Exists:
                        Log.Message("Search results loaded, proceeding to click 'Edit'.")
                        searchDialog.panelControl1.standaloneBarDockControlTasks.DockedBarControl.ClickItem("Edit")

                        # Now proceed with editing the practitioner details
                        asOfDate = healthEdge_Manager.AsOfDate
                        asOfDate.panelControlTop.radioGroupReprocessClaims.ClickItem("Do Not Reprocess Claims")
                        asOfDate.codeEntryEditReasonCodes.LookUpEdit.Click(225, 9)
                        popupLookUpEditForm = healthEdge_Manager.PopupLookUpEditForm
                        popupLookUpEditForm.Click(111, 55)
                        asOfDate.panelControlBottom.simpleButtonOK.ClickButton()
                        entityEditForm = healthEdge_Manager.EntityEditForm
                        practitionerEditControl = entityEditForm.panelBottom.xtraTabControlEdit.xtraTabPageEdit.PractitionerEditControl
                        lookUpEdit = practitionerEditControl.entityPanelSummary.codeEntryEditRaceOrEithnicity.LookUpEdit

                        # Update Race in General section
                        lookUpEdit.Keys(race)
                        lookUpEdit.Keys("[Down][Enter]")

                        # Update Ethnicity Name in UDT section
                        xtraTabControl = practitionerEditControl.xtraTabControlPractitioner
                        xtraTabControl.ClickTab("UDT")
                        lookUpEdit = xtraTabControl.xtraTabPageUDT.entityPanelUDT.repeaterPanelUDT.RepeatableUDTList.headerGroupTitle.repeaterPanelUdtListValueSet.RepeatableUdtListValueSet.udtValueEdit.panelControlAutoEdit.LookUpEdit
                        lookUpEdit.Keys(ethnicity_name)
                        lookUpEdit.Keys("[Down][Enter]")

                        # Save the updated information
                        Log.Message("Saving the updated information.")
                        entityEditForm.BarDockControl.DockedBarControl.ClickItem("Save")

                        panelControl.PractitionerView.xtraTabControlPractitioner.ClickTab("UDT")

                        screenshot_path = os.path.join(screenshots_dir, f"AfterSave_{practitioner_id_npi}.png")
                        Log.Message("Taking screenshot after saving.")
                        SaveScreenshot(screenshot_path)

                        aqUtils.Delay(1000)
                        homeForm.BarDockControl.DockedBarControl.ClickItem("Home")
                    else:
                        Log.Warning("Search results not loaded as expected. Unable to find practitioner. Skipping this record.")
                        # Log the missing Practitioner ID
                        missing_practitioners.append(practitioner_id_npi)
                        save_missing_ids_to_csv(missing_practitioners, missing_ids_csv_file)

            else:
                Log.Error("TextEdit object is None or not found. Skipping to the next record.")
            
            # Move to the next record in the Excel file
            DDT.CurrentDriver.Next()
            aqUtils.Delay(1000)  # Ensure the next record is properly loaded

    finally:
        if DDT.CurrentDriver is not None:
            Log.Message("Closing the Excel driver.")
            DDT.CloseDriver(DDT.CurrentDriver.Name)
        else:
            Log.Message("No driver to close.")
        
        # Log missing practitioners
        if missing_practitioners:
            Log.Message("Saving missing practitioners to CSV file.")
            save_missing_ids_to_csv(missing_practitioners, missing_ids_csv_file)

    Log.Message("RaceAndEthnicityUpdate script completed.")