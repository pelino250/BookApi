# Database Module - main.tf
# This module creates an Azure Database for PostgreSQL

# Create PostgreSQL Server
resource "azurerm_postgresql_flexible_server" "postgres" {
  name                = var.postgresql_server_name
  location            = var.location
  resource_group_name = var.resource_group_name
  zone = var.postgresql_zone

  sku_name = var.postgresql_sku_name

  storage_mb                   = var.postgresql_storage_mb
  backup_retention_days        = var.postgresql_backup_retention_days
  geo_redundant_backup_enabled = var.postgresql_geo_redundant_backup

  administrator_login          = var.postgresql_admin_username
  administrator_password = var.postgresql_admin_password
  version                      = var.postgresql_version




  # public_network_access_enabled is automatically determined by the provider
  # and cannot be directly configured


  tags = var.tags
}

# Create PostgreSQL Database
resource "azurerm_postgresql_flexible_server_database" "database" {
  name                = var.postgresql_database_name
  server_id           = azurerm_postgresql_flexible_server.postgres.id
  charset             = "UTF8"
  collation           = "en_US.UTF8"
}
