import requests
import json
import sys
import csv
import os

def policyStatus(mg, header):
  assessment_excel_header = ["Scope", "Policy Assignment Name", "Policy Definition Name", "Effect", "Resource Type", "Resource Location", "Subscription Name", "Resource Group Name", "Resource Name", "Compliance"]
  with open('reports.csv', mode = 'w', newline='') as pa_excel_file_header:
    csvwriter = csv.writer(pa_excel_file_header, delimiter=',')
    csvwriter.writerow(assessment_excel_header)
                
  print("Getting Policy States for Management Group - ", mg)
  get_assignment_status = requests.post(url = "https://management.azure.com/providers/Microsoft.Management/managementGroups/"+mg+"/providers/Microsoft.PolicyInsights/policyStates/latest/queryResults?api-version=2019-10-01", headers = header)
  get_assignment_status_to_json = get_assignment_status.json()
  if get_assignment_status.status_code == 200 or get_assignment_status.status_code == 204:
    if "value" in get_assignment_status_to_json:
      for state in get_assignment_status_to_json["value"]:
        assignment_scope = state["policyAssignmentScope"]
        assignment_id = state["policyAssignmentId"]
        definition_id = state["policyDefinitionId"]
        definition_effect = state["policyDefinitionAction"]
        subscription_id = state["subscriptionId"]
        resource_type = state["resourceType"]
        resource_location = state["resourceLocation"]
        resource_group_name = state["resourceGroup"]
        resource_name = state["resourceId"].split("/")[-1]
        resource_compliance = state["complianceState"]

        # Get Assignment Display Name
        get_assignment_name = requests.get(url = "https://management.azure.com/"+assignment_id+"?api-version=2023-04-01", headers = header)
        get_assignment_name_to_json = get_assignment_name.json()
        if get_assignment_name.status_code == 200 or get_assignment_name.status_code == 204:
          if "properties" in get_assignment_name_to_json:
            assignment_name = get_assignment_name_to_json["properties"]["displayName"]
          else:
            assignment_name = "Not Returned from API"
        else:
            assignment_name = "Not Returned from API"
        
        # Get Definition Display Name
        get_definition_name = requests.get(url = "https://management.azure.com/"+definition_id+"?api-version=2023-04-01", headers = header)
        get_definition_name_to_json = get_definition_name.json()
        if get_definition_name.status_code == 200 or get_definition_name.status_code == 204:
          if "properties" in get_definition_name_to_json:
            definition_name = get_definition_name_to_json["properties"]["displayName"]
          else:
            definition_name = "Not Returned from API"
        else:
          definition_name = "Not Returned from API"
        
        # Get Subscription Display name
        get_subscription_name = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"?api-version=2022-12-01", headers = header)
        get_subscription_name_to_json = get_subscription_name.json()
        if get_subscription_name.status_code == 200 or get_subscription_name.status_code == 204:
          subscription_name = get_subscription_name_to_json["displayName"]
        else:
          subscription_name = "Not Returned from API"
      
        # Write CSV data
        policy_status_csv_data = [assignment_scope, assignment_name, definition_name, definition_effect, resource_type, resource_location, subscription_name, resource_group_name, resource_name, resource_compliance]
        with open('reports.csv', mode = 'a', newline='') as pa_excel_file_data:
          csvwriter = csv.writer(pa_excel_file_data, delimiter=',')
          csvwriter.writerow(policy_status_csv_data)
    else:
      pass
  else:
    pass
