# App Service Module - variables.tf
# This file defines all variables used by the app-service module

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
}

variable "app_service_plan_name" {
  description = "The name of the App Service Plan"
  type        = string
}

variable "app_service_name" {
  description = "The name of the App Service"
  type        = string
}

variable "app_service_sku_tier" {
  description = "The pricing tier of the App Service Plan"
  type        = string
  default     = "Basic"
}

variable "app_service_sku_size" {
  description = "The instance size of the App Service Plan"
  type        = string
  default     = "B1"
}

variable "container_registry_url" {
  description = "The URL of the container registry"
  type        = string
}

variable "container_registry_username" {
  description = "The username for the container registry"
  type        = string
  default     = ""
}

variable "container_registry_password" {
  description = "The password for the container registry"
  type        = string
  sensitive   = true
  default     = ""
}

variable "docker_image_name" {
  description = "The name of the Docker image"
  type        = string
  default     = "bookapi"
}

variable "docker_image_tag" {
  description = "The tag of the Docker image"
  type        = string
  default     = "latest"
}

variable "application_insights_connection_string" {
  description = "The connection string for Application Insights"
  type        = string
  default     = ""
}

variable "database_connection_string" {
  description = "The connection string for the database"
  type        = string
  sensitive   = true
  default     = ""
}

variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
  default     = ""
}

variable "storage_account_key" {
  description = "The access key for the storage account"
  type        = string
  sensitive   = true
  default     = ""
}

variable "subnet_id" {
  description = "The ID of the subnet to connect the App Service to"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "app_service_sku_name" {
  description = "The SKU name for the App Service plan (e.g., S1, B1, P1v2)."
  type        = string
}
