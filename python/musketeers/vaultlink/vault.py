
import os
import requests
import json
import iris


class VaultSecretError(Exception):
    """Custom exception for errors related to Vault secrets."""
    pass


def create_kv_secret_engine(engine_name: str) -> str:
    """
    Create a KV secrets engine from HashiCorp Vault.

    Args:
        engine_name (str): The name of the KV secrets engine.

    Returns:
        str: The response from the vault.

    Raises:
        VaultSecretError: If there is an issue creating the KV secrets engine.
    """
    # Retrieve Vault token from environment variable
    vault_token = os.getenv("VAULT_LINK_HASHICORP_VAULT_TOKEN")
    if not vault_token:
        raise VaultSecretError("Vault token is not configured. Set the 'VAULT_LINK_HASHICORP_VAULT_TOKEN' environment variable.")

    # Headers
    headers = {
        "X-Vault-Token": vault_token,
        "Content-Type": "application/json"
    }

    # Base URL
    base_url = f'{os.getenv("VAULT_LINK_HASHICORP_VAULT_BASE_URL")}/v1/sys/mounts'
    if not base_url:
        raise VaultSecretError("Vault base URL is not configured. Set the 'VAULT_LINK_HASHICORP_VAULT_BASE_URL' environment variable.")

    # Payload to enable KV v2 secrets engine
    payload = {
        "type": "kv",
        "options": {
            "version": "2"
        }
    }

    # API Request
    try:
        response = requests.post(f"{base_url}/{engine_name}", headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
    except requests.RequestException as e:
        raise VaultSecretError(f"Error retrieving secret: {e}")


def create_secret(secret_engine: str, secret_name: str, secret: str) -> str:
    """
    Create a secret engine from HashiCorp Vault.

    Args:
        secret_engine (str): The name of the secret engine.
        secret_name (str): The name of the secret.
        secret (str): The value of the secret.

    Returns:
        str: The response from the vault.

    Raises:
        VaultSecretError: If there is an issue creating the KV secrets engine.
    """
    # Retrieve Vault token from environment variable
    vault_token = os.getenv("VAULT_LINK_HASHICORP_VAULT_TOKEN")
    if not vault_token:
        raise VaultSecretError("Vault token is not configured. Set the 'VAULT_LINK_HASHICORP_VAULT_TOKEN' environment variable.")

    # Headers
    headers = {
        "X-Vault-Token": vault_token,
        "Content-Type": "application/json"
    }

    # Base URL
    base_url = f'{os.getenv("VAULT_LINK_HASHICORP_VAULT_BASE_URL")}/v1'
    if not base_url:
        raise VaultSecretError("Vault base URL is not configured. Set the 'VAULT_LINK_HASHICORP_VAULT_BASE_URL' environment variable.")

    # Data to store in the secret
    payload = json.loads(secret.toJson())

    # API Request
    try:
        response = requests.post(f"{base_url}/{secret_engine}/data/{secret_name}", headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
    except requests.RequestException as e:
        raise VaultSecretError(f"Error retrieving secret: {e}")

    # Parse and return the response
    try:
        return response.json()
    except (KeyError, ValueError) as e:
        raise VaultSecretError(f"Failed to parse secret data: {e}")


def get_secret(secret_engine: str, secret_name: str) -> str:
    """
    Retrieve a secret from HashiCorp Vault.

    Args:
        secret_engine (str): The name of the secret engine.
        secret_name (str): The name of the secret.

    Returns:
        str: The value of the secret.

    Raises:
        VaultSecretError: If there is an issue retrieving the secret.
    """
    # Retrieve Vault token from environment variable
    vault_token = os.getenv("VAULT_LINK_HASHICORP_VAULT_TOKEN")
    if not vault_token:
        raise VaultSecretError("Vault token is not configured. Set the 'VAULT_LINK_HASHICORP_VAULT_TOKEN' environment variable.")

    # Headers
    headers = {
        "X-Vault-Token": vault_token,
        "Content-Type": "application/json"
    }

    # Base URL
    base_url = f'{os.getenv("VAULT_LINK_HASHICORP_VAULT_BASE_URL")}/v1'
    if not base_url:
        raise VaultSecretError("Vault base URL is not configured. Set the 'VAULT_LINK_HASHICORP_VAULT_BASE_URL' environment variable.")

    # API Request
    try:
        response = requests.get(f"{base_url}/{secret_engine}/data/{secret_name}", headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
    except requests.RequestException as e:
        raise VaultSecretError(f"Error retrieving secret: {e}")

    # Parse and return secret
    try:
        #secret_data = response.json()["data"]["data"]
        #return secret_data.get("password", None)  # Adjust the key as needed for your data structure
        return response.json()
    except (KeyError, ValueError) as e:
        raise VaultSecretError(f"Failed to parse secret data: {e}")