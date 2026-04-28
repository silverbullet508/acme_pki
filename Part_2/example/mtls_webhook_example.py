from updated_http_client import AcmeHTTPClient


def main() -> None:
    with AcmeHTTPClient(
        base_url="https://localhost:8443",
        timeout=10.0,
        ca_bundle_path="certs/ca.crt",          # trust the demo server CA
        client_cert_path="certs/client.crt",    # client cert presented to server
        client_key_path="certs/client.key",     # private key for mTLS
    ) as client:
        response = client.post(
            "/webhook",
            json={"event": "demo"},
            headers={"Content-Type": "application/json"},
        )

        print("status_code =", response.status_code)
        print("reason_phrase =", response.reason_phrase)
        print("response_text =", response.text)


if __name__ == "__main__":
    main()