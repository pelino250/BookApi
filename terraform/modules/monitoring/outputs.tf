# Monitoring Module - outputs.tf
# This file defines all outputs from the monitoring module

output "app_insights_id" {
  description = "The ID of the Application Insights resource"
  value       = azurerm_application_insights.app_insights.id
}

output "app_id" {
  description = "The App ID of the Application Insights resource"
  value       = azurerm_application_insights.app_insights.app_id
}

output "instrumentation_key" {
  description = "The Instrumentation Key of the Application Insights resource"
  value       = azurerm_application_insights.app_insights.instrumentation_key
  sensitive   = true
}

output "connection_string" {
  description = "The Connection String of the Application Insights resource"
  value       = azurerm_application_insights.app_insights.connection_string
  sensitive   = true
}

output "workspace_id" {
  description = "The ID of the Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.workspace.id
}

output "workspace_primary_shared_key" {
  description = "The Primary Shared Key of the Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.workspace.primary_shared_key
  sensitive   = true
}

output "action_group_id" {
  description = "The ID of the Action Group"
  value       = azurerm_monitor_action_group.critical.id
}

output "key_vault_id" {
  description = "The ID of the Key Vault"
  value       = azurerm_key_vault.monitoring_kv.id
}

output "key_vault_uri" {
  description = "The URI of the Key Vault"
  value       = azurerm_key_vault.monitoring_kv.vault_uri
}
