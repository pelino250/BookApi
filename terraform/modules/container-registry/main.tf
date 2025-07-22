# Container Registry Module - main.tf
# This module creates an Azure Container Registry for storing Docker images

# Create Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = var.container_registry_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.container_registry_sku
  admin_enabled       = var.admin_enabled

  # Enable features based on SKU
  dynamic "georeplications" {
    for_each = var.container_registry_sku == "Premium" && length(var.georeplication_locations) > 0 ? var.georeplication_locations : []
    content {
      location                = georeplications.value
      zone_redundancy_enabled = true
      tags                    = var.tags
    }
  }

  # Enable encryption if using Premium SKU
  dynamic "encryption" {
    for_each = var.container_registry_sku == "Premium" && var.encryption_key_vault_key_id != "" ? [1] : []
    content {
      enabled            = true
      key_vault_key_id   = var.encryption_key_vault_key_id
      identity_client_id = var.encryption_identity_id
    }
  }

  # Enable network rules if specified
  dynamic "network_rule_set" {
    for_each = var.container_registry_sku == "Premium" && var.enable_network_rules ? [1] : []
    content {
      default_action = "Deny"

      ip_rule {
        action   = "Allow"
        ip_range = var.allowed_ip_range
      }

      virtual_network {
        action    = "Allow"
        subnet_id = var.allowed_subnet_id
      }
    }
  }

  # Enable zone redundancy for Premium SKU
  zone_redundancy_enabled = var.container_registry_sku == "Premium" ? true : false

  # Enable data endpoint for Premium SKU
  data_endpoint_enabled = var.container_registry_sku == "Premium" ? true : false

  # Enable anonymous pull for public repositories
  anonymous_pull_enabled = var.anonymous_pull_enabled

  # Enable quarantine policy for images
  quarantine_policy_enabled = var.quarantine_policy_enabled

  # Enable content trust for images
  trust_policy {
    enabled = var.trust_policy_enabled
  }

  # Enable retention policy for images (only for Premium SKU)
  dynamic "retention_policy" {
    for_each = var.container_registry_sku == "Premium" ? [1] : []
    content {
      days    = var.retention_days
      enabled = var.retention_policy_enabled
    }
  }

  # Empty retention policy block for non-Premium SKUs
  dynamic "retention_policy" {
    for_each = var.container_registry_sku != "Premium" ? [1] : []
    content {
      days    = 7
      enabled = false
    }
  }

  # Enable system-assigned identity for the Container Registry
  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}
