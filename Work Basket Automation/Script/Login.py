import logging

def login(username, password):
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting the HealthEdge Manager application.")
        Log.Message("Starting the HealthEdge Manager application.")
        TestedApps.HealthEdge_Manager.Run(1, True)

        healthEdge_Manager = Aliases.HealthEdge_Manager
        login_form = healthEdge_Manager.LoginForm

        # Set username
        logger.info("Entering username.")
        login_form.textEditUserName.TextBoxMaskBox.SetText(username)

        # Set password
        logger.info("Entering password.")
        password_box = login_form.textEditPassword.TextBoxMaskBox
        password_box.Click(182, 5)
        password_box.SetText(password)

        # Select server
        logger.info("Selecting server.")
        login_form.lookUpEditServers.Click(191, 6)
        healthEdge_Manager.PopupLookUpEditForm.Click(94, 79)

        # Submit login form
        logger.info("Submitting login form.")
        login_form.simpleButtonSubmit.ClickButton()

        logger.info("Logged in to HealthEdge Manager successfully.")
        Log.Message("Logged in to HealthEdge Manager.")

    except Exception as e:
        logger.error(f"An error occurred during login: {e}", exc_info=True)
        Log.Error(f"Login failed: {e}")
        
