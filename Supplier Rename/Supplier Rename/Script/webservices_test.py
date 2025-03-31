import os
import requests
import logging
import pandas as pd
from requests.auth import HTTPBasicAuth
from lxml import etree

# Setup logging
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)  # Ensure 'logs' directory exists
logging.basicConfig(
    filename=os.path.join(log_dir, 'claim_status_lookup.log'), 
    level=logging.INFO,  
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Input and Output Files
input_file = './data/SupplierLocationNotFound-9-22-2024-5 PM EST.xlsx'  # Ensure correct file path
output_file = './data/supplier_rendering_info_output.csv'

# Check if input file exists
if not os.path.exists(input_file):
    logging.error(f"Input file {input_file} does not exist.")
    raise FileNotFoundError(f"Input file {input_file} not found.")

# Load Excel file
df_claims = pd.read_excel(input_file)

# Define how many records to process (control this number)
num_records_to_process = 2  # Example: only process the first 5 records

# Slice the dataframe to limit the number of records
df_claims = df_claims.head(num_records_to_process)

# Credentials and Environment Setup
url = "https://gchp-lb-pr01.gchp.local:5559/connector/services/v4/ClaimStatusLookup"
username = "connector"
password = "Connector123"

def generate_soap_request(claim_hcc_id):
    soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:stat="http://www.healthedge.com/connector/schema/claim/status">
       <soapenv:Header/>
       <soapenv:Body>
          <stat:originalEDI837AttachmentReferenceLookupCriteria>
             <hccClaimNumber>{claim_hcc_id}</hccClaimNumber>
          </stat:originalEDI837AttachmentReferenceLookupCriteria>
       </soapenv:Body>
    </soapenv:Envelope>
    """
    return soap_body.strip().encode('utf-8')

# Send SOAP request and get the response
def send_soap_request(claim_hcc_id):
    try:
        headers = {'Content-Type': 'text/xml; charset=utf-8'}
        soap_body = generate_soap_request(claim_hcc_id)
        
        # Log the SOAP request for debugging
        logging.info(f"Sending SOAP request for Claim HCC ID {claim_hcc_id}: {soap_body}")
        
        response = requests.post(url, data=soap_body, headers=headers, auth=HTTPBasicAuth(username, password), verify=False)
        
        if response.status_code == 200:
            # Write the SOAP response to a file
            response_log_file = os.path.join(log_dir, f"claim_{claim_hcc_id}_response.xml")
            with open(response_log_file, 'w') as file:
                file.write(response.text)
            
            return response.content
        else:
            logging.error(f"Failed to get response for Claim HCC ID {claim_hcc_id}. HTTP Status: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Exception occurred while processing Claim HCC ID {claim_hcc_id}: {str(e)}")
        return None

def extract_supplier_and_rendering_info(soap_response):
    try:
        # Parse the SOAP response first
        tree = etree.fromstring(soap_response)

        # Extract the CDATA content
        cdata_content = tree.xpath('//document/text()')[0]

        # Parse the CDATA content as a new XML document
        cdata_tree = etree.fromstring(cdata_content)

        # Extract Supplier Information with safety checks
        supplier_info = {}
        supplier_info['supplierBillingName'] = cdata_tree.xpath('//supplierInformation/supplierBillingName/text()')[0] if cdata_tree.xpath('//supplierInformation/supplierBillingName/text()') else "Not Available"
        supplier_info['taxIdentificationNumber'] = cdata_tree.xpath('//supplierInformation/taxIdentificationNumber/text()')[0] if cdata_tree.xpath('//supplierInformation/taxIdentificationNumber/text()') else "Not Available"
        supplier_info['streetAddress'] = cdata_tree.xpath('//supplierInformation/streetAddress/text()')[0] if cdata_tree.xpath('//supplierInformation/streetAddress/text()') else "Not Available"
        supplier_info['cityName'] = cdata_tree.xpath('//supplierInformation/cityName/text()')[0] if cdata_tree.xpath('//supplierInformation/cityName/text()') else "Not Available"
        supplier_info['stateCode'] = cdata_tree.xpath('//supplierInformation/stateCode/text()')[0] if cdata_tree.xpath('//supplierInformation/stateCode/text()') else "Not Available"
        supplier_info['postalCode'] = cdata_tree.xpath('//supplierInformation/postalCode/text()')[0] if cdata_tree.xpath('//supplierInformation/postalCode/text()') else "Not Available"
        supplier_info['npi'] = cdata_tree.xpath('//supplierInformation/npi/text()')[0] if cdata_tree.xpath('//supplierInformation/npi/text()') else "Not Available"

        # Combine supplier address
        supplier_info['combinedAddress'] = f"{supplier_info['streetAddress']} {supplier_info['cityName']} {supplier_info['stateCode']} {supplier_info['postalCode']}"

        # Extract Rendering Facility Information with safety checks
        rendering_info = {}
        rendering_info['facilityName'] = cdata_tree.xpath('//renderingFacility/facilityName/text()')[0] if cdata_tree.xpath('//renderingFacility/facilityName/text()') else "Not Available"
        rendering_info['streetAddress'] = cdata_tree.xpath('//renderingFacility/streetAddress/text()')[0] if cdata_tree.xpath('//renderingFacility/streetAddress/text()') else "Not Available"
        rendering_info['cityName'] = cdata_tree.xpath('//renderingFacility/cityName/text()')[0] if cdata_tree.xpath('//renderingFacility/cityName/text()') else "Not Available"
        rendering_info['stateCode'] = cdata_tree.xpath('//renderingFacility/stateCode/text()')[0] if cdata_tree.xpath('//renderingFacility/stateCode/text()') else "Not Available"
        rendering_info['postalCode'] = cdata_tree.xpath('//renderingFacility/postalCode/text()')[0] if cdata_tree.xpath('//renderingFacility/postalCode/text()') else "Not Available"

        # Combine rendering facility address
        rendering_info['combinedAddress'] = f"{rendering_info['streetAddress']} {rendering_info['cityName']} {rendering_info['stateCode']} {rendering_info['postalCode']}"

        return supplier_info, rendering_info
    except Exception as e:
        logging.error(f"Exception occurred while extracting info: {str(e)}")
        return None, None

# Processing each claim and writing to the output
os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output directory exists
with open(output_file, 'w') as output:
    output.write("CLAIM_HCC_ID,supplierBillingName,taxIdentificationNumber,supplierNPI,supplierAddress,renderingFacility,renderingAddress\n")
    
    for index, row in df_claims.iterrows():
        claim_hcc_id = row['CLAIM_HCC_ID']
        
        # Send SOAP request and get response
        soap_response = send_soap_request(claim_hcc_id)
        
        if soap_response:
            # Extract supplier and rendering facility information
            supplier_info, rendering_info = extract_supplier_and_rendering_info(soap_response)
            
            if supplier_info and rendering_info:
                # Write to output file with combined addresses
                output.write(f"{claim_hcc_id},{supplier_info['supplierBillingName']},{supplier_info['taxIdentificationNumber']},{supplier_info['npi']},{supplier_info['combinedAddress']},{rendering_info['facilityName']},{rendering_info['combinedAddress']}\n")
                
                logging.info(f"Processed Claim HCC ID {claim_hcc_id} successfully.")
            else:
                logging.error(f"Failed to extract data for Claim HCC ID {claim_hcc_id}.")
        else:
            logging.error(f"No response received for Claim HCC ID {claim_hcc_id}.")

logging.info(f"Process completed. Output written to {output_file}.")
