terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.43.0"
    }
  }
  cloud {
    organization = "BSE-DevOps"
    workspaces {
      name = "BookApi-cli"
    }
  }
}

provider "azurerm" {
  features {}
  skip_provider_registration = true

}

resource "azurerm_resource_group" "rg" {
  location = "Canada Central"
  name     = "book-api_group"
}

resource "azurerm_storage_account" "storage" {
  name                     = "bookapistorage"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
}