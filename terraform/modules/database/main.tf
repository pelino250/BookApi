# Database Module - main.tf
# This module creates an Azure Database for PostgreSQL

# Create PostgreSQL Server
resource "azurerm_postgresql_server" "postgres" {
  name                = var.postgresql_server_name
  location            = var.location
  resource_group_name = var.resource_group_name

  sku_name = var.postgresql_sku_name

  storage_mb                   = var.postgresql_storage_mb
  backup_retention_days        = var.postgresql_backup_retention_days
  geo_redundant_backup_enabled = var.postgresql_geo_redundant_backup
  auto_grow_enabled            = true

  administrator_login          = var.postgresql_admin_username
  administrator_login_password = var.postgresql_admin_password
  version                      = var.postgresql_version
  ssl_enforcement_enabled      = true

  public_network_access_enabled    = var.postgresql_public_access
  ssl_minimal_tls_version_enforced = "TLS1_2"

  tags = var.tags
}

# Create PostgreSQL Database
resource "azurerm_postgresql_database" "database" {
  name                = var.postgresql_database_name
  resource_group_name = var.resource_group_name
  server_name         = azurerm_postgresql_server.postgres.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}

# Create PostgreSQL Firewall Rule for Azure Services
resource "azurerm_postgresql_firewall_rule" "azure_services" {
  name                = "AllowAzureServices"
  resource_group_name = var.resource_group_name
  server_name         = azurerm_postgresql_server.postgres.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

# Create PostgreSQL Firewall Rule for App Service
resource "azurerm_postgresql_firewall_rule" "app_service" {
  count               = length(var.app_service_outbound_ips) > 0 ? length(var.app_service_outbound_ips) : 0
  name                = "AppService-${count.index}"
  resource_group_name = var.resource_group_name
  server_name         = azurerm_postgresql_server.postgres.name
  start_ip_address    = var.app_service_outbound_ips[count.index]
  end_ip_address      = var.app_service_outbound_ips[count.index]
}

# Optional: Create Private Endpoint for PostgreSQL Server
resource "azurerm_private_endpoint" "postgres_endpoint" {
  count               = var.create_private_endpoint ? 1 : 0
  name                = "${var.postgresql_server_name}-endpoint"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.private_endpoint_subnet_id

  private_service_connection {
    name                           = "${var.postgresql_server_name}-privateserviceconnection"
    private_connection_resource_id = azurerm_postgresql_server.postgres.id
    subresource_names              = ["postgresqlServer"]
    is_manual_connection           = false
  }

  tags = var.tags
}
