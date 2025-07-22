# Container Registry Module - outputs.tf
# This file defines all outputs from the container-registry module

output "id" {
  description = "The ID of the Container Registry"
  value       = azurerm_container_registry.acr.id
}

output "name" {
  description = "The name of the Container Registry"
  value       = azurerm_container_registry.acr.name
}

output "login_server" {
  description = "The login server URL for the Container Registry"
  value       = azurerm_container_registry.acr.login_server
}

output "admin_username" {
  description = "The admin username for the Container Registry"
  value       = var.admin_enabled ? azurerm_container_registry.acr.admin_username : null
}

output "admin_password" {
  description = "The admin password for the Container Registry"
  value       = var.admin_enabled ? azurerm_container_registry.acr.admin_password : null
  sensitive   = true
}

output "identity_principal_id" {
  description = "The Principal ID of the Container Registry's system-assigned identity"
  value       = azurerm_container_registry.acr.identity.0.principal_id
}
