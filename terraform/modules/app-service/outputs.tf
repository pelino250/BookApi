# App Service Module - outputs.tf
# This file defines all outputs from the app-service module

output "app_service_name" {
  description = "The name of the App Service"
  value       = azurerm_linux_web_app.app.name
}

output "app_service_default_hostname" {
  description = "The default hostname of the App Service"
  value       = azurerm_linux_web_app.app.default_hostname
}

output "app_service_id" {
  description = "The ID of the App Service"
  value       = azurerm_linux_web_app.app.id
}

output "app_service_plan_id" {
  description = "The ID of the App Service Plan"
  value       = azurerm_service_plan.app_plan.id
}

output "app_service_principal_id" {
  description = "The Principal ID of the App Service's Managed Identity"
  value       = azurerm_linux_web_app.app.identity[0].principal_id
}

output "staging_slot_name" {
  description = "The name of the staging slot"
  value       = azurerm_linux_web_app_slot.staging_slot.name
}

output "staging_slot_hostname" {
  description = "The hostname of the staging slot"
  value       = azurerm_linux_web_app_slot.staging_slot.default_hostname
}

output "staging_slot_id" {
  description = "The ID of the staging slot"
  value       = azurerm_linux_web_app_slot.staging_slot.id
}

output "staging_slot_principal_id" {
  description = "The Principal ID of the staging slot's Managed Identity"
  value       = azurerm_linux_web_app_slot.staging_slot.identity[0].principal_id
}
