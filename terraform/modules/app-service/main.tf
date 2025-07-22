# App Service Module - main.tf
# This module creates an Azure App Service Plan and App Service for hosting the Django application

# Create the App Service Plan
resource "azurerm_service_plan" "app_plan" {
  name                = var.app_service_plan_name
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "${var.app_service_sku_size}"

  tags = var.tags
}

# Create the App Service
resource "azurerm_linux_web_app" "app" {
  name                = var.app_service_name
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.app_plan.id

  site_config {
    application_stack {
      docker_image     = "${var.container_registry_url}/${var.docker_image_name}"
      docker_image_tag = var.docker_image_tag
    }

    always_on                = true
    ftps_state               = "Disabled"
    minimum_tls_version      = "1.2"
    health_check_path        = "/health/"
    health_check_eviction_time_in_min = 2
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"          = "https://${var.container_registry_url}"
    "DOCKER_REGISTRY_SERVER_USERNAME"     = var.container_registry_username
    "DOCKER_REGISTRY_SERVER_PASSWORD"     = var.container_registry_password
    "DJANGO_SETTINGS_MODULE"              = "BookApi.settings.staging"
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = var.application_insights_connection_string
    "DATABASE_URL"                        = var.database_connection_string
    "AZURE_STORAGE_ACCOUNT_NAME"          = var.storage_account_name
    "AZURE_STORAGE_ACCOUNT_KEY"           = var.storage_account_key
    "WEBSITES_PORT"                       = "8000"
  }

  # Identity for accessing Key Vault
  identity {
    type = "SystemAssigned"
  }

  # Connection to virtual network if needed
  # virtual_network_subnet_id = var.subnet_id

  tags = var.tags

  # Lifecycle to prevent accidental destruction
  lifecycle {
    prevent_destroy = true
  }
}

# Create a slot for staging deployments (blue-green deployment)
resource "azurerm_linux_web_app_slot" "staging_slot" {
  name                = "staging"
  app_service_id      = azurerm_linux_web_app.app.id

  site_config {
    application_stack {
      docker_image     = "${var.container_registry_url}/${var.docker_image_name}"
      docker_image_tag = "latest"
    }

    always_on                = true
    ftps_state               = "Disabled"
    minimum_tls_version      = "1.2"
    health_check_path        = "/health/"
    health_check_eviction_time_in_min = 2
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"          = "https://${var.container_registry_url}"
    "DOCKER_REGISTRY_SERVER_USERNAME"     = var.container_registry_username
    "DOCKER_REGISTRY_SERVER_PASSWORD"     = var.container_registry_password
    "DJANGO_SETTINGS_MODULE"              = "BookApi.settings.staging"
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = var.application_insights_connection_string
    "DATABASE_URL"                        = var.database_connection_string
    "AZURE_STORAGE_ACCOUNT_NAME"          = var.storage_account_name
    "AZURE_STORAGE_ACCOUNT_KEY"           = var.storage_account_key
    "WEBSITES_PORT"                       = "8000"
    "SLOT_SETTING"                        = "true"
  }

  # Identity for accessing Key Vault
  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}
