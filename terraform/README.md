# BookAPI Terraform Infrastructure

This directory contains the Terraform configuration for the BookAPI project. The infrastructure is defined as code using Terraform, which allows for consistent, repeatable deployments across environments.

## Directory Structure

```
terraform/
├── environments/
│   ├── staging/
│   │   ├── main.tf         # Main configuration for staging environment
│   │   ├── variables.tf    # Variable definitions for staging
│   │   ├── outputs.tf      # Output definitions for staging
│   │   └── terraform.tfvars # Variable values for staging
├── modules/
│   ├── app-service/        # App Service module for hosting the Django application
│   ├── database/           # Database module for PostgreSQL
│   ├── container-registry/ # Container Registry module for Docker images
│   └── monitoring/         # Monitoring module for Application Insights
└── shared/
    └── backend.tf          # Shared backend configuration
```

## Modules

### App Service Module

The App Service module creates an Azure App Service Plan and App Service for hosting the Django application. It includes:

- Linux-based App Service Plan
- App Service configured for Docker container deployment
- Deployment slot for staging (blue-green deployment)
- System-assigned managed identity for secure access to other Azure resources

### Database Module

The Database module creates an Azure Database for PostgreSQL. It includes:

- PostgreSQL server with appropriate SKU
- PostgreSQL database
- Firewall rules for Azure Services and App Service
- Optional private endpoint for secure connectivity

### Container Registry Module

The Container Registry module creates an Azure Container Registry for storing Docker images. It includes:

- Container Registry with appropriate SKU
- Admin access for easier integration with App Service
- System-assigned managed identity
- Various security and policy settings

### Monitoring Module

The Monitoring module creates Azure monitoring resources. It includes:

- Log Analytics Workspace for centralized logging
- Application Insights for application monitoring
- Action Group and alerts for critical issues
- Key Vault for storing monitoring secrets

## Environments

### Staging Environment

The staging environment is configured for development and testing purposes. It includes:

- Lower-tier SKUs for cost optimization
- Public access for easier development
- Simplified security settings
- Monitoring and alerting for critical issues

## Usage

### Prerequisites

- Azure CLI installed and configured
- Terraform CLI installed
- Access to an Azure subscription

### Deploying to Staging

1. Navigate to the staging environment directory:

```bash
cd terraform/environments/staging
```

2. Initialize Terraform:

```bash
terraform init
```

3. Plan the deployment:

```bash
terraform plan -out=tfplan
```

4. Apply the deployment:

```bash
terraform apply tfplan
```

### Managing Secrets

Sensitive values like database passwords should not be stored in the repository. Instead, they can be provided in several ways:

1. Environment variables:

```bash
export TF_VAR_postgresql_admin_password="your-secure-password"
```

2. Command-line arguments:

```bash
terraform apply -var="postgresql_admin_password=your-secure-password"
```

3. Azure Key Vault (for CI/CD pipelines)

## Best Practices

1. Always run `terraform plan` before applying changes
2. Use modules for reusable components
3. Keep sensitive data out of version control
4. Use remote state storage for team collaboration
5. Tag all resources for better organization and cost tracking
