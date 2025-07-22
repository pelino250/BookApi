variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "Canada Central"
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "book-api-staging-rg"
}

variable "environment" {
  description = "Environment name (staging)"
  type        = string
  default     = "staging"
}

variable "app_service_plan_name" {
  description = "Name of the App Service Plan"
  type        = string
  default     = "book-api-staging-asp"
}

variable "app_service_name" {
  description = "Name of the App Service"
  type        = string
  default     = "book-api-staging-app"
}

variable "app_service_sku_name" {
  description = "Tier of the App Service Plan"
  type        = string
  default     = "S1"  # Standard tier for supports deployment slots
}

variable "container_registry_name" {
  description = "Name of the Azure Container Registry"
  type        = string
  default     = "bookapistagingreg"
}

variable "container_registry_sku" {
  description = "SKU of the Azure Container Registry"
  type        = string
  default     = "Basic"  # Lower tier for staging
}

variable "postgresql_server_name" {
  description = "Name of the PostgreSQL server"
  type        = string
  default     = "book-api-staging-db"
}

variable "postgresql_sku_name" {
  description = "SKU name for the PostgreSQL server"
  type        = string
  default     = "B_Gen5_1"  # Smaller size for staging
}

variable "postgresql_admin_username" {
  description = "Admin username for PostgreSQL server"
  type        = string
  default     = "psqladmin"
}

variable "postgresql_admin_password" {
  description = "Admin password for PostgreSQL server"
  type        = string
  sensitive   = true
}

variable "postgresql_database_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "bookapi"
}

variable "storage_account_name" {
  description = "Name of the Storage Account"
  type        = string
  default     = "bookapistaging"
}

variable "storage_account_tier" {
  description = "Tier of the Storage Account"
  type        = string
  default     = "Standard"
}

variable "storage_account_replication_type" {
  description = "Replication type of the Storage Account"
  type        = string
  default     = "LRS"  # Locally redundant storage for staging
}

variable "key_vault_name" {
  description = "Name of the Key Vault"
  type        = string
  default     = "book-api-staging-kv"
}

variable "application_insights_name" {
  description = "Name of the Application Insights"
  type        = string
  default     = "book-api-staging-ai"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "Staging"
    Project     = "BookAPI"
    ManagedBy   = "Terraform"
  }
}
