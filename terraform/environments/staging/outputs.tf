output "resource_group_name" {
  description = "The name of the resource group"
  value       = azurerm_resource_group.rg.name
}

output "resource_group_location" {
  description = "The location of the resource group"
  value       = azurerm_resource_group.rg.location
}

output "app_service_name" {
  description = "The name of the App Service"
  value       = module.app_service.app_service_name
}

output "app_service_default_hostname" {
  description = "The default hostname of the App Service"
  value       = module.app_service.app_service_default_hostname
}

output "container_registry_login_server" {
  description = "The login server URL for the Container Registry"
  value       = module.container_registry.login_server
}

output "postgresql_server_fqdn" {
  description = "The fully qualified domain name of the PostgreSQL server"
  value       = module.database.server_fqdn
}

output "postgresql_connection_string" {
  description = "The connection string for the PostgreSQL database"
  value       = module.database.connection_string
  sensitive   = true
}

output "application_insights_instrumentation_key" {
  description = "The instrumentation key for Application Insights"
  value       = module.monitoring.instrumentation_key
  sensitive   = true
}

output "application_insights_app_id" {
  description = "The App ID for Application Insights"
  value       = module.monitoring.app_id
}
