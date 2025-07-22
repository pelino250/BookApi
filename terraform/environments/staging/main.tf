terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.43.0"
    }
  }
  # cloud {
  #   organization = "BSE-DevOps"
  #   workspaces {
  #     name = "BookApi-cli"
  #   }
  # }
}

provider "azurerm" {
  features {}
  skip_provider_registration = false
}

# Import shared backend configuration
# Uncomment when ready to use a remote backend
# module "backend" {
#   source = "../../shared"
# }

# Create Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

# Create Container Registry
module "container_registry" {
  source = "../../modules/container-registry"

  resource_group_name     = azurerm_resource_group.rg.name
  location                = azurerm_resource_group.rg.location
  container_registry_name = var.container_registry_name
  container_registry_sku  = var.container_registry_sku
  admin_enabled           = true
  tags                    = var.tags
}

# Create Database
module "database" {
  source = "../../modules/database"

  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  postgresql_server_name     = var.postgresql_server_name
  postgresql_sku_name        = var.postgresql_sku_name
  postgresql_admin_username  = var.postgresql_admin_username
  postgresql_admin_password  = var.postgresql_admin_password
  postgresql_database_name   = var.postgresql_database_name
  postgresql_public_access   = true
  create_private_endpoint    = false
  postgresql_zone = "2"
  tags                       = var.tags
}

# Create Monitoring Resources
module "monitoring" {
  source = "../../modules/monitoring"

  resource_group_name         = azurerm_resource_group.rg.name
  location                    = azurerm_resource_group.rg.location
  environment                 = var.environment
  log_analytics_workspace_name = "${var.environment}-bookapi-workspace"
  application_insights_name   = var.application_insights_name
  key_vault_name              = var.key_vault_name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  admin_object_id             = data.azurerm_client_config.current.object_id
  tags                        = var.tags

  # These will be populated after the App Service is created
  app_service_ids             = [module.app_service.app_service_id]
  app_service_principal_id    = module.app_service.app_service_principal_id
}

# Create Storage Account
resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = var.storage_account_tier
  account_replication_type = var.storage_account_replication_type

  blob_properties {
    cors_rule {
      allowed_headers    = ["*"]
      allowed_methods    = ["GET", "HEAD", "POST", "PUT"]
      allowed_origins    = ["https://*.azurewebsites.net"]
      exposed_headers    = ["*"]
      max_age_in_seconds = 3600
    }
  }

  tags = var.tags
}

# Create Storage Container for Media
resource "azurerm_storage_container" "media" {
  name                  = "media"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "blob"
}

# Create Storage Container for Static Files
resource "azurerm_storage_container" "static" {
  name                  = "static"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "blob"
}

# Get current Azure client configuration
data "azurerm_client_config" "current" {}

# Create App Service
module "app_service" {
  source = "../../modules/app-service"

  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  app_service_plan_name    = var.app_service_plan_name
  app_service_name         = var.app_service_name
  app_service_sku_name     = var.app_service_sku_name

  container_registry_url      = module.container_registry.login_server
  container_registry_username = module.container_registry.admin_username
  container_registry_password = module.container_registry.admin_password
  docker_image_name           = "bookapi"
  docker_image_tag            = "latest"

  application_insights_connection_string = module.monitoring.connection_string
  database_connection_string             = module.database.connection_string
  storage_account_name                   = azurerm_storage_account.storage.name
  storage_account_key                    = azurerm_storage_account.storage.primary_access_key

  tags = var.tags
}
