1. This prototype displays a mTLS handshake between one receiver/sender that share the same root CA. It is one directional, and listens on a localhost loopback. 

2. If this was going to be deployed to production, I would include more test functions, and would expect the service to be protected by both a proxy and WAF. From a business prospective, I would ensure there was alignment on root and intermediate CA validity dates, sufficient incident respone logging, and an integration with both a CRL and OCSP. After generation, the keys and cert should be stored in an encrypted vault to protect the confidentiality of the payloads and integrity of the service. 

3. The design of this prototype is verifying a simple handshake, however, I would expect other engineers to protect the root ca.key value in a secure storage solution (KMS/HSM). The program currently doesn't have automatic cert rotation enabled, so the client/webhook certs will need to be regenerated every 90 days and the root cert every year. Similar to the above question, logging and revocation controls will need to be enabled and maintained. 

4. The ACME webhook uses a server HTTPS connection. You can verify mTLS by running the instructions listed in the README.md. If mTLS is successful, you will see `204 No Content` with logs that display the webhook's cert identity. Below are the steps for mTLS: 
    a. Certificate Authority creates cryptographically-signed server and client certs for the ACME webhook and client-server. 
    b. When the ACME webhook is prompted to send a webhook to the client-server it validates the client-server's certificate (HTTPS) 
    c. Then the TLS handshake ensues: the server validates ACME's cert against the root CA"s cert. Once mutual authentication is confirmed, the payload is sent over an encrypted connection

5. The client could use HMAC, every webhook payload would include a signature that verfiies the sender's identity and payload integrity. This implementation requires a shared secret to validate the signature, if the secret is leaked there is an assumed compromise. IP whitelisting could also be used but this is difficult for larger or cloud environments with large IP blocks, it also doesn't enforce encryption or payload protection. mTLS is scalable, enables mutual trust, and confirms both sender authentication and payload confidentiality.  
