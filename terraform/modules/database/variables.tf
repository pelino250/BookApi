# Database Module - variables.tf
# This file defines all variables used by the database module

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
}

variable "postgresql_server_name" {
  description = "The name of the PostgreSQL server"
  type        = string
}

variable "postgresql_sku_name" {
  description = "The SKU name for the PostgreSQL flexible server"
  type        = string
  default     = "B_Standard_B1ms"  # Valid SKU name for flexible server
}

variable "postgresql_storage_mb" {
  description = "The storage size for the PostgreSQL server in MB"
  type        = number
  default     = 32768  # 32GB - minimum allowed for flexible server
}

variable "postgresql_backup_retention_days" {
  description = "The number of days to retain backups"
  type        = number
  default     = 7
}

variable "postgresql_geo_redundant_backup" {
  description = "Enable geo-redundant backups"
  type        = bool
  default     = false  # Disabled for staging to reduce costs
}

variable "postgresql_admin_username" {
  description = "The administrator username for the PostgreSQL server"
  type        = string
}

variable "postgresql_admin_password" {
  description = "The administrator password for the PostgreSQL server"
  type        = string
  sensitive   = true
}

variable "postgresql_version" {
  description = "The version of PostgreSQL"
  type        = string
  default     = "11"
}

variable "postgresql_public_access" {
  description = "Allow public access to the PostgreSQL server"
  type        = bool
  default     = true  # For staging, can be disabled in production
}

variable "postgresql_database_name" {
  description = "The name of the PostgreSQL database"
  type        = string
}

variable "app_service_outbound_ips" {
  description = "List of outbound IPs from the App Service"
  type        = list(string)
  default     = []
}

variable "create_private_endpoint" {
  description = "Whether to create a private endpoint for the PostgreSQL server"
  type        = bool
  default     = false
}

variable "private_endpoint_subnet_id" {
  description = "The ID of the subnet for the private endpoint"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
variable "postgresql_zone" {
  description = "The zone for the PostgreSQL server"
  type        = string
  default     = null  # Default to zone 1
}
