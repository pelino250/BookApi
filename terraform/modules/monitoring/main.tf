# Monitoring Module - main.tf
# This module creates Azure monitoring resources including Application Insights

# Create Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "workspace" {
  name                = var.log_analytics_workspace_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = var.log_analytics_workspace_sku
  retention_in_days   = var.log_retention_days

  tags = var.tags
}

# Create Application Insights
resource "azurerm_application_insights" "app_insights" {
  name                = var.application_insights_name
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.workspace.id
  retention_in_days   = var.log_retention_days

  tags = var.tags
}

# Create Action Group for alerts
resource "azurerm_monitor_action_group" "critical" {
  name                = "${var.environment}-critical-alerts"
  resource_group_name = var.resource_group_name
  short_name          = "critical"

  email_receiver {
    name                    = "DevOpsTeam"
    email_address           = var.alert_email
    use_common_alert_schema = true
  }

  tags = var.tags
}

# Create Alert for high CPU usage
resource "azurerm_monitor_metric_alert" "high_cpu" {
  name                = "${var.environment}-high-cpu-alert"
  resource_group_name = var.resource_group_name
  scopes              = var.app_service_ids
  description         = "Alert when CPU time is high"
  enabled             = true
  frequency           = "PT1M"
  window_size         = "PT5M"

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name      = "CpuTime"
    aggregation      = "Total"
    operator         = "GreaterThan"
    # This threshold represents 80% CPU utilization over 5 minutes for a single-core plan (like S1).
    # Calculation: 300 seconds (5 minutes) * 0.80 (80%) = 240.

    threshold        = 240
  }

  action {
    action_group_id = azurerm_monitor_action_group.critical.id
  }

  tags = var.tags
}

# Create Alert for high memory usage
resource "azurerm_monitor_metric_alert" "high_memory" {
  name                = "${var.environment}-high-memory-alert"
  resource_group_name = var.resource_group_name
  scopes              = var.app_service_ids
  description         = "Alert when memory usage exceeds 1.4 GB"
  enabled             = true
  frequency           = "PT1M"
  window_size         = "PT5M"

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name      = "MemoryWorkingSet"
    aggregation      = "Average"
    operator         = "GreaterThan"
    # This threshold represents roughly 80% of the 1.75 GB RAM available to an S1 App Service Plan.
    # The value is in bytes. 1.4 GB = 1,400,000,000 bytes.
    threshold        = 1400000000
  }

  action {
    action_group_id = azurerm_monitor_action_group.critical.id
  }

  tags = var.tags
}

# Create Alert for HTTP server errors
resource "azurerm_monitor_metric_alert" "http_server_errors" {
  name                = "${var.environment}-http-server-errors-alert"
  resource_group_name = var.resource_group_name
  scopes              = var.app_service_ids
  description         = "Alert when HTTP server errors (5xx) occur"

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name      = "Http5xx"
    aggregation      = "Total"
    operator         = "GreaterThan"
    threshold        = 5
  }

  window_size        = "PT5M"
  frequency          = "PT1M"
  severity           = 1

  action {
    action_group_id = azurerm_monitor_action_group.critical.id
  }

  tags = var.tags
}

# Create Key Vault for storing monitoring secrets
resource "azurerm_key_vault" "monitoring_kv" {
  name                        = var.key_vault_name
  location                    = var.location
  resource_group_name         = var.resource_group_name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

  access_policy {
    tenant_id = var.tenant_id
    object_id = var.admin_object_id

    key_permissions = [
      "Get", "List", "Create", "Delete", "Update",
    ]

    secret_permissions = [
      "Get", "List", "Set", "Delete",
    ]

    certificate_permissions = [
      "Get", "List", "Create", "Delete",
    ]
  }

  # Add access policy for App Service if provided
  dynamic "access_policy" {
    for_each = var.app_service_principal_id != "" ? [1] : []
    content {
      tenant_id = var.tenant_id
      object_id = var.app_service_principal_id

      secret_permissions = [
        "Get", "List",
      ]
    }
  }

  tags = var.tags
}
