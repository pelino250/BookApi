# Monitoring Module - variables.tf
# This file defines all variables used by the monitoring module

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
}

variable "environment" {
  description = "The environment name (e.g., staging, production)"
  type        = string
}

variable "log_analytics_workspace_name" {
  description = "The name of the Log Analytics Workspace"
  type        = string
}

variable "log_analytics_workspace_sku" {
  description = "The SKU of the Log Analytics Workspace"
  type        = string
  default     = "PerGB2018"  # Pay-as-you-go pricing
}

variable "log_retention_days" {
  description = "The number of days to retain logs"
  type        = number
  default     = 30
}

variable "application_insights_name" {
  description = "The name of the Application Insights resource"
  type        = string
}

variable "alert_email" {
  description = "The email address to send alerts to"
  type        = string
  default     = "devops@example.com"
}

variable "app_service_ids" {
  description = "List of App Service IDs to monitor"
  type        = list(string)
  default     = []
}

variable "app_service_principal_id" {
  description = "The Principal ID of the App Service's Managed Identity"
  type        = string
  default     = ""
}

variable "key_vault_name" {
  description = "The name of the Key Vault"
  type        = string
}

variable "tenant_id" {
  description = "The Azure AD tenant ID"
  type        = string
}

variable "admin_object_id" {
  description = "The Object ID of the admin user or group"
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
