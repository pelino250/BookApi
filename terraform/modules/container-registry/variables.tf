# Container Registry Module - variables.tf
# This file defines all variables used by the container-registry module

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
}

variable "container_registry_name" {
  description = "The name of the container registry"
  type        = string
}

variable "container_registry_sku" {
  description = "The SKU of the container registry (Basic, Standard, Premium)"
  type        = string
  default     = "Basic"  # Lower tier for staging
}

variable "admin_enabled" {
  description = "Enable admin user for the container registry"
  type        = bool
  default     = true
}

variable "georeplication_locations" {
  description = "List of Azure locations where the container registry should be geo-replicated"
  type        = list(string)
  default     = []  # No geo-replication for staging
}

variable "encryption_key_vault_key_id" {
  description = "The ID of the Key Vault key to use for encryption"
  type        = string
  default     = ""  # No encryption for staging
}

variable "encryption_identity_id" {
  description = "The ID of the user assigned identity to use for encryption"
  type        = string
  default     = ""  # No encryption for staging
}

variable "enable_network_rules" {
  description = "Enable network rules for the container registry"
  type        = bool
  default     = false  # No network rules for staging
}

variable "allowed_ip_range" {
  description = "The IP range that is allowed to access the container registry"
  type        = string
  default     = "0.0.0.0/0"  # Allow all IPs for staging
}

variable "allowed_subnet_id" {
  description = "The ID of the subnet that is allowed to access the container registry"
  type        = string
  default     = ""  # No subnet restriction for staging
}

variable "anonymous_pull_enabled" {
  description = "Enable anonymous pull for the container registry"
  type        = bool
  default     = false
}

variable "quarantine_policy_enabled" {
  description = "Enable quarantine policy for the container registry"
  type        = bool
  default     = false
}

variable "trust_policy_enabled" {
  description = "Enable trust policy for the container registry"
  type        = bool
  default     = false
}

variable "retention_policy_enabled" {
  description = "Enable retention policy for the container registry"
  type        = bool
  default     = true
}

variable "retention_days" {
  description = "The number of days to retain images"
  type        = number
  default     = 7  # 7 days for staging
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
