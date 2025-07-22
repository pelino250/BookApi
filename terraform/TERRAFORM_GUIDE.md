# Terraform Infrastructure Guide for BookAPI

This guide provides a comprehensive overview of the Terraform configuration used to deploy and manage the BookAPI infrastructure on Azure. It explains the project structure, modules, environments, and best practices.

## Table of Contents

1. [Introduction](#introduction)
2. [Terraform Fundamentals for Beginners](#terraform-fundamentals-for-beginners)
   - [What is a Module?](#what-is-a-module)
   - [Understanding main.tf Files](#understanding-maintf-files)
   - [Working with Variables](#working-with-variables)
   - [Using Outputs](#using-outputs)
   - [Other Key Concepts](#other-key-concepts)
3. [Project Structure](#project-structure)
4. [Modules](#modules)
   - [App Service](#app-service-module)
   - [Container Registry](#container-registry-module)
   - [Database](#database-module)
   - [Monitoring](#monitoring-module)
5. [Environments](#environments)
   - [Staging](#staging-environment)
6. [State Management](#state-management)
7. [Deployment Workflow](#deployment-workflow)
8. [Best Practices](#best-practices)

## Introduction

The BookAPI infrastructure is managed using Terraform, an Infrastructure as Code (IaC) tool that allows us to define, provision, and manage cloud infrastructure in a declarative configuration language. This approach provides several benefits:

- **Version Control**: Infrastructure changes are tracked in Git alongside application code
- **Reproducibility**: Environments can be consistently recreated
- **Automation**: Deployments can be automated through CI/CD pipelines
- **Documentation**: The code itself serves as documentation of the infrastructure

The infrastructure is deployed on Microsoft Azure and includes resources for hosting the application, storing data, managing container images, and monitoring the system.

## Terraform Fundamentals for Beginners

If you're new to Terraform, this section will help you understand the basic concepts and components that make up a Terraform project. These fundamentals will make it easier to understand the rest of this guide.

### What is a Module?

In Terraform, a **module** is a container for multiple resources that are used together. Think of a module as a reusable blueprint or template for a specific piece of infrastructure. Modules help you:

- **Organize code**: Group related resources together
- **Reuse code**: Define a component once and use it multiple times
- **Encapsulate complexity**: Hide the details of how a component is implemented

A module typically consists of several files:
- `main.tf`: Contains the primary resource definitions
- `variables.tf`: Defines input variables that can be customized
- `outputs.tf`: Specifies values that will be accessible to the parent module

In our project, we have modules for App Service, Container Registry, Database, and Monitoring. Each module encapsulates all the resources needed for that specific component of our infrastructure.

Example of using a module:
```hcl
module "database" {
  source = "../../modules/database"

  resource_group_name = "my-resource-group"
  location            = "eastus"
  database_name       = "my-database"
}
```

### Understanding main.tf Files

The `main.tf` file is the primary configuration file in a Terraform project or module. It contains:

- **Provider configurations**: Specify which cloud providers (AWS, Azure, GCP, etc.) to use
- **Resource definitions**: Declare the infrastructure components to create
- **Module calls**: Reference and configure other modules

Think of `main.tf` as the "main script" that defines what infrastructure will be created. It's usually the first file you'll look at to understand what a Terraform configuration does.

Example of a simple main.tf file:
```hcl
# Configure the Azure provider
provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}

# Create a virtual network within the resource group
resource "azurerm_virtual_network" "example" {
  name                = "example-network"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  address_space       = ["10.0.0.0/16"]
}
```

### Working with Variables

**Variables** in Terraform allow you to parameterize your configurations, making them more flexible and reusable. Variables are defined in a `variables.tf` file and can be:

- **Required**: Must be provided by the user
- **Optional with defaults**: Will use a default value if not specified
- **Sensitive**: Marked as sensitive to hide their values in logs and outputs

Variables can be set in several ways:
- In a `.tfvars` file (like `terraform.tfvars`)
- On the command line with `-var` flags
- Through environment variables (prefixed with `TF_VAR_`)

Example of variable definitions:
```hcl
# variables.tf
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region to deploy resources"
  type        = string
  default     = "East US"
}

variable "database_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}
```

Using variables in your configuration:
```hcl
resource "azurerm_resource_group" "example" {
  name     = var.resource_group_name
  location = var.location
}
```

### Using Outputs

**Outputs** in Terraform allow you to extract and expose specific values from your infrastructure. They are defined in an `outputs.tf` file and serve several purposes:

- **Share information** between modules
- **Return values** to the user after applying a configuration
- **Integrate** with other tools or scripts

Outputs are particularly useful when one piece of infrastructure needs information about another piece. For example, an App Service might need the connection string for a database.

Example of output definitions:
```hcl
# outputs.tf
output "resource_group_id" {
  description = "ID of the created resource group"
  value       = azurerm_resource_group.example.id
}

output "database_connection_string" {
  description = "Connection string for the database"
  value       = azurerm_postgresql_server.example.connection_string
  sensitive   = true
}
```

Accessing outputs from a module:
```hcl
module "database" {
  source = "./modules/database"
  # ...
}

resource "azurerm_app_service" "example" {
  # ...
  app_settings = {
    "DATABASE_URL" = module.database.connection_string
  }
}
```

### Other Key Concepts

**Providers**: Plugins that allow Terraform to interact with cloud providers, SaaS providers, and other APIs. Each provider offers a set of resource types and data sources that Terraform can manage.

```hcl
provider "azurerm" {
  features {}
  subscription_id = "your-subscription-id"
}
```

**Resources**: The most important element in Terraform - they represent infrastructure objects like virtual networks, compute instances, or DNS records.

```hcl
resource "azurerm_virtual_machine" "example" {
  name                  = "example-vm"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  # ...
}
```

**Data Sources**: Allow Terraform to use information defined outside of Terraform, like existing infrastructure or values from other systems.

```hcl
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "example" {
  # ...
  tenant_id = data.azurerm_client_config.current.tenant_id
}
```

**State**: Terraform keeps track of the resources it manages in a state file. This state maps real-world resources to your configuration, tracks metadata, and improves performance.

**Plan**: Before making changes, Terraform creates an execution plan that shows what actions will be taken to reach the desired state defined in your configuration.

**Apply**: The process of executing the actions proposed in a plan to create, update, or destroy infrastructure.

## Project Structure

The Terraform configuration is organized as follows:

```
terraform/
├── environments/
│   └── staging/
│       ├── main.tf           # Main configuration for staging environment
│       ├── outputs.tf        # Output values for staging environment
│       ├── terraform.tfvars  # Variable values for staging environment
│       └── variables.tf      # Variable definitions for staging environment
├── modules/
│   ├── app-service/          # Module for Azure App Service
│   ├── container-registry/   # Module for Azure Container Registry
│   ├── database/             # Module for Azure Database for PostgreSQL
│   └── monitoring/           # Module for Azure monitoring resources
└── shared/
    └── backend.tf            # Shared backend configuration
```

This structure follows the Terraform best practice of separating reusable modules from environment-specific configurations. The `modules` directory contains reusable infrastructure components, while the `environments` directory contains environment-specific configurations that use these modules.

## Modules

### App Service Module

**Purpose**: Hosts the Django web application in a containerized environment.

**Key Resources**:
- `azurerm_service_plan`: Defines the compute resources for the App Service
- `azurerm_linux_web_app`: The main web application that runs the Docker container
- `azurerm_linux_web_app_slot`: A staging slot for blue-green deployments

**Configuration Highlights**:
- Configured to run a Docker container from Azure Container Registry
- Health check path for monitoring application health
- Environment variables for application configuration
- System-assigned identity for secure access to other Azure resources
- Staging slot for zero-downtime deployments

**Inputs**:
- Resource group and location
- App Service plan and name
- Container registry details
- Application configuration (database connection, storage, etc.)

**Outputs**:
- App Service ID
- App Service principal ID (for identity)
- Default hostname

### Container Registry Module

**Purpose**: Stores and manages Docker images for the application.

**Key Resources**:
- `azurerm_container_registry`: Azure Container Registry for storing Docker images

**Configuration Highlights**:
- Support for different SKUs (Basic, Standard, Premium)
- Premium SKU features (when enabled):
  - Geo-replication for global distribution
  - Encryption for enhanced security
  - Network rules for access control
  - Zone redundancy for high availability
  - Retention policies for image lifecycle management
- Security features:
  - Content trust for image verification
  - Quarantine policy for image scanning
  - System-assigned identity

**Inputs**:
- Resource group and location
- Container registry name and SKU
- Admin access configuration
- Advanced features configuration (for Premium SKU)

**Outputs**:
- Login server URL
- Admin username and password (if admin enabled)

### Database Module

**Purpose**: Provides a managed PostgreSQL database for the application.

**Key Resources**:
- `azurerm_postgresql_flexible_server`: Azure Database for PostgreSQL Flexible Server
- `azurerm_postgresql_flexible_server_database`: PostgreSQL database within the server

**Configuration Highlights**:
- Flexible server with configurable SKU and compute resources
- Storage configuration with backup retention and geo-redundancy
- Zone placement for high availability
- Administrator credentials for access

**Inputs**:
- Resource group and location
- PostgreSQL server name and SKU
- Administrator credentials
- Database name and configuration
- Backup and redundancy settings

**Outputs**:
- Server ID and name
- Database ID and name
- Connection string for application use

### Monitoring Module

**Purpose**: Provides monitoring, alerting, and secret management for the application.

**Key Resources**:
- `azurerm_log_analytics_workspace`: Centralized logging solution
- `azurerm_application_insights`: Application performance monitoring
- `azurerm_monitor_action_group`: Alert notification configuration
- `azurerm_monitor_metric_alert`: Alert rules for critical conditions
- `azurerm_key_vault`: Secure storage for sensitive information

**Configuration Highlights**:
- Log Analytics Workspace for centralized logging
- Application Insights for application performance monitoring
- Alerts for critical conditions:
  - High CPU usage
  - High memory usage
  - HTTP server errors (5xx)
- Key Vault for secret management:
  - Access policies for administrators and App Service
  - Disk encryption
  - Soft delete and retention policies

**Inputs**:
- Resource group and location
- Workspace and Application Insights names
- Alert email address
- App Service IDs for monitoring
- Key Vault name and access configuration

**Outputs**:
- Application Insights instrumentation key and connection string
- Key Vault ID and URI

## Environments

### Staging Environment

The staging environment is a pre-production environment that closely resembles the production environment but with lower-tier resources for cost efficiency.

**Configuration Highlights**:
- Located in Canada Central region
- Resource naming follows a consistent pattern with "staging" included
- Lower-tier SKUs for cost efficiency:
  - App Service: S1 (supports deployment slots)
  - Container Registry: Basic
  - PostgreSQL: B_Standard_B1ms
  - Storage: Standard LRS (Locally Redundant Storage)
- Consistent tagging for resource organization

**Resource Relationships**:
- App Service uses the Container Registry for Docker images
- App Service connects to the PostgreSQL database
- App Service uses Storage Account for media and static files
- App Service is monitored by Application Insights
- Key Vault stores sensitive configuration

## State Management

Terraform state is managed using a backend configuration defined in `shared/backend.tf`. The configuration is currently commented out and needs to be configured with actual values before use.

**Options for State Management**:
1. **Azure Storage Account**: Store state in Azure Blob Storage
2. **Terraform Cloud**: Use HashiCorp's managed service
3. **Other options**: Consul, Amazon S3, Google Cloud Storage

For production use, it's recommended to use a remote backend to:
- Store the state file securely
- Enable collaboration among team members
- Support state locking to prevent concurrent modifications
- Maintain state history

## Deployment Workflow

The typical workflow for deploying infrastructure changes is:

1. **Development**:
   - Make changes to Terraform configuration
   - Run `terraform fmt` to format the code
   - Run `terraform validate` to check for syntax errors

2. **Planning**:
   - Run `terraform plan` to preview changes
   - Review the plan to ensure it matches expectations

3. **Approval**:
   - Submit changes for review (pull request)
   - Get approval from team members

4. **Application**:
   - Run `terraform apply` to apply changes
   - Verify resources are created/updated correctly

5. **Verification**:
   - Test the application in the updated environment
   - Monitor for any issues

This workflow can be automated using CI/CD pipelines, as configured in `.github/workflows/terraform.yml`.

## Best Practices

The Terraform configuration follows several best practices:

1. **Modularity**:
   - Reusable modules for common infrastructure components
   - Environment-specific configurations that use these modules

2. **Variable Management**:
   - Clear variable definitions with descriptions
   - Default values where appropriate
   - Sensitive values marked as sensitive

3. **State Management**:
   - Shared backend configuration for consistent state management
   - Remote backend recommended for production use

4. **Security**:
   - Sensitive values not hardcoded (use environment variables or Key Vault)
   - System-assigned identities for secure access
   - Key Vault for secret management

5. **Naming Conventions**:
   - Consistent naming pattern for resources
   - Environment included in resource names

6. **Tagging**:
   - Consistent tagging for resource organization
   - Environment, Project, and ManagedBy tags

7. **Documentation**:
   - Comments explaining resource configurations
   - This guide providing comprehensive documentation

By following these practices, the infrastructure is maintainable, secure, and scalable.
