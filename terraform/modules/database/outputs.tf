# Database Module - outputs.tf
# This file defines all outputs from the database module

output "server_name" {
  description = "The name of the PostgreSQL server"
  value       = azurerm_postgresql_server.postgres.name
}

output "server_id" {
  description = "The ID of the PostgreSQL server"
  value       = azurerm_postgresql_server.postgres.id
}

output "server_fqdn" {
  description = "The fully qualified domain name of the PostgreSQL server"
  value       = azurerm_postgresql_server.postgres.fqdn
}

output "database_name" {
  description = "The name of the PostgreSQL database"
  value       = azurerm_postgresql_database.database.name
}

output "connection_string" {
  description = "The connection string for the PostgreSQL database"
  value       = "postgresql://${var.postgresql_admin_username}:${var.postgresql_admin_password}@${azurerm_postgresql_server.postgres.fqdn}:5432/${azurerm_postgresql_database.database.name}"
  sensitive   = true
}

output "admin_username" {
  description = "The administrator username for the PostgreSQL server"
  value       = var.postgresql_admin_username
}

output "private_endpoint_ip" {
  description = "The private IP address of the PostgreSQL server private endpoint"
  value       = var.create_private_endpoint ? azurerm_private_endpoint.postgres_endpoint[0].private_service_connection[0].private_ip_address : null
}
