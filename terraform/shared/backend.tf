# This file configures the Terraform backend for state storage
# It's shared across environments to ensure consistent state management

terraform {
  # The backend configuration is commented out because it needs to be configured
  # with actual values before use. Uncomment and fill in the values when ready.

  # backend "azurerm" {
  #   resource_group_name  = "terraform-state-rg"
  #   storage_account_name = "bookapitfstate"
  #   container_name       = "tfstate"
  #   key                  = "terraform.tfstate"
  # }

  # Alternatively, you can use Terraform Cloud as configured in the main.tf
  # cloud {
  #   organization = "your-organization"
  #   workspaces {
  #     name = "your-workspace"
  #   }
  # }
}

# Note: For production use, it's recommended to use a remote backend
# to store the Terraform state file securely and enable collaboration.
# Options include:
# 1. Azure Storage Account (as shown above)
# 2. Terraform Cloud
# 3. HashiCorp Consul
# 4. Amazon S3
# 5. Google Cloud Storage
