# Getting Started
To work on this project, you should have the git client and an editor (VS Code is free and capable)

If this is your first time using git, you will need to tell it your name and email address. This can be done using the following two commands (making the obvious changes)

`git config --global user.name "Your Name"`

`git config --global user.email you@example.com`

# Introduction

This project mainly focussed on generating Azure Policy Compliance Report in Excel file stored in Azure Storage Account.

## Why choose Python over Powershell

1. Faster and efficient
2. A full fledged language
3. One of the most used programming language
4. Lesser amount of code
5. Dynamic when working with excels or Data frames
6. Human friendly language to work with

## Azure Governance Management Reporting

This process creates an excel file which contains information about Policy Compliance for a given Management Group scope. The excel file is then pushed to a storage container in Azure using the same Azure DevOps Pipeline which generates the excel file. The scope can be changed to Subscriptions if needed with little modification.

## The process in summary

This is the general idea how the process works within the Pipeline and Python. Start the pipeline selecting the Management group name which triggers the python scripts to do following:-

- Login to Azure using the Service Principle credentials to generate the API tokens.
- Query Azure API to get information about Policy and Compliance
- Format and inserts the data into Excel Sheet.
- Upload the excel file to Azure Storage Account Container.

![image](./images/Policy_Compliance_Workflow.png)

# Prerequisites

The bootstrap Resources include [Key Vault](#key-vault) and [Storage Account](#azure-storage-account). The Key Vault holds sensitive values which are required by Python to authenticate with Azure for Rest API Query. The Storage Account holds the Excel file which is generated from Python.

## Azure Storage Account

Please create an [Azure Storage Account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal#create-a-storage-account-1) and a [container](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container) named **policyreports** to store generated Excel Files. Please note the Service Principle should have access to the Storage Account. Note the [Access Key](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys) and Storage Account name from Azure Portal.

|Key Name|Value|
|:--|:--|
|ARM-ACCESS-KEY|Azure Storage Account Access Key|
|SA-NAME|Azure Storage Account Name|

## Service Connection

Azure DevOps Pipeline requires Service Connection to run tasks. The Service Principle should have access to Key Vault Secrets ([Get and List Permission](https://learn.microsoft.com/en-us/azure/devops/pipelines/release/azure-key-vault?view=azure-devops&tabs=yaml#set-up-azure-key-vault-access-policies)) to retrieve Key Vault Secret Values required during running the task. Please refer to this [official article](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml#create-a-service-connection) for creating the Service Connection from a Service Principle. Note the following values for a Service Principle from Azure Portal.

|Key Name|Value|
|:--|:--|
|ARM-CLIENT-ID|Application ID of the Service Principle|
|ARM-CLIENT-SECRET|Client Secret of the Service Principle|
|ARM-TENANT-ID|Azure Tenant ID|

## Key Vault

An Azure Key Vault is required to store Secrets which are used by the pipeline to authenticate against Azure and Azure DevOps to perform its desired operation. Please note the Service Principle mentioned [above](#service-connection) must have **GET** and **LIST** for the Key Vault Secrets. Please [create the secrets](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-portal#add-a-secret-to-key-vault) in Azure Key Vault. You may refer to the [Service Connection](#service-connection) section for values.

Secrets to be created in Azure Key Vault:

```
ARM-CLIENT-ID
ARM-CLIENT-SECRET
ARM-TENANT-ID
ARM-ACCESS-KEY
SA-NAME
```

## Variable Groups

The code needs an Azure DevOps Pipeline Variable Group linked to an existing Azure Key Vault containing the Secrets. Please refer to this [official article](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups?view=azure-devops&tabs=yaml#link-secrets-from-an-azure-key-vault) for more details.

## Excel File

Azure Storage Account Container is used to safe keep Excel files which are generated during the process. The reports are generated in a sub directory inside the Container with naming conventions as **Azure_Policy_Compliance-YYYY-MM-DD**.

# Pipeline

## Creating the Pipeline

Please follow this instruction to create the deploy pipeline

- Go to **Pipelines** in Azure DevOps
- Click on **New Pipeline** from right top corner
- Select **Azure Repos Git**
- Select your repository containing this code
- Select **Existing Azure Pipelines YAML file**
- Select the branch and select path as **/.pipelines/generate_report.yaml**
- Click on **Continue**
- Click on **Save** from **Run** drop down menu on top right corner
- You may rename the pipeline by choosing **Rename/move** from top right corner Kebab menu

### Running the Pipeline

Please follow the instruction to run the pipelines

- Go to **Pipelines** in Azure DevOps and select the [pipeline](#creating-the-pipeline)

- Click on **Run Pipeline** from top right corner

- Select Management Group ID and click on **Run** button

- Follow the Pipeline Status

### Recommendation

We will recommend to schedule the Pipeline to run everyday at spefic time for all Management Group instead of running it manually. This will ensure continuous availability of data without missing. We can do that.