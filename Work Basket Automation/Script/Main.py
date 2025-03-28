﻿import logging
import sys
from HealthEdgeManager import HealthEdgeManager
from Login import login
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f'workbasket_log_{timestamp}.txt'


# Configure logging
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def automate_workbasket_process():
    log_file_path = "D:\Test_Complete\Work Basket Automation\Log_files"
    
    try:
        # Start logging
        logger.info("Starting workbasket automation process.")
        
        # Login
        login("rthotakura", Project.Variables.Password1)
        
        # Initialize HealthEdge Manager
        health_edge_manager_alias = Aliases.HealthEdge_Manager
        manager = HealthEdgeManager(health_edge_manager_alias)
        
        # Navigate to Workbasket
        logger.info("Navigating to workbasket.")
        manager.navigate_to_workbasket()
        
        # Process Workbasket
        logger.info("Processing workbasket.")
        manager.process_workbasket()
        
        # Save the log to a file
        Log.SaveResultsAs(log_file_path, "txt")
        logger.info(f"Log saved to {log_file_path}")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)
    
    logger.info("Workbasket automation process completed successfully.")

if __name__ == "__main__":
    automate_workbasket_process()
