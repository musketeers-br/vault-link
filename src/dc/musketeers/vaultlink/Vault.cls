Class dc.musketeers.vaultlink.Vault Extends %RegisteredObject
{

ClassMethod CreateKVSecretEngine(pEngineName As %String)
{
    Set vault = ##class(%SYS.Python).Import("musketeers.vaultlink.vault")
    Do vault."create_kv_secret_engine"(pEngineName)
}

ClassMethod CreateSecret(pSecretEngineName As %String, pSecretName As %String, pSecret As %DynamicObject) As %DynamicObject
{
    Set json = ##class(%SYS.Python).Import("json")
    Set vault = ##class(%SYS.Python).Import("musketeers.vaultlink.vault")
    Set resp = vault."create_secret"(pSecretEngineName, pSecretName, pSecret)
    Return ##class(%DynamicObject).%FromJSON(json.dumps(resp))
}

ClassMethod GetSecret(pSecretEngineName As %String, pSecretName As %String) As %DynamicObject
{
    Set json = ##class(%SYS.Python).Import("json")
    Set vault = ##class(%SYS.Python).Import("musketeers.vaultlink.vault")
    Set resp = vault."get_secret"(pSecretEngineName, pSecretName)
    Return ##class(%DynamicObject).%FromJSON(json.dumps(resp))
}

}
