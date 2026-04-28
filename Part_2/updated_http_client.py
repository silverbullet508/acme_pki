import ssl
from typing import Optional, Dict, Any

import httpx


class AcmeHTTPClient:
    """
    A synchronous base client for making HTTP requests using httpx.

    - this client only supports mTLS - verifies the remote server cert & client cert 
    """

    USER_AGENT = "AcmeHTTPClient/1.0"

    def __init__(
        self,
        ca_bundle_path: str,
        client_cert_path: str,
        client_key_path: str,
        client_key_password: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = 10.0,
        headers: Optional[Dict[str, str]] = None,
        follow_redirects: bool = False,
    ):

        default_headers = {"User-Agent": self.USER_AGENT}
        if headers:
            default_headers.update(headers)

        ssl_context = self._build_ssl_context(
                ca_bundle_path=ca_bundle_path,
                client_cert_path=client_cert_path,
                client_key_path=client_key_path,
                client_key_password=client_key_password,
            )

        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers=default_headers,
            follow_redirects=follow_redirects,
            verify=ssl_context,
        )

    @staticmethod
    def _build_ssl_context(
        *,
        ca_bundle_path: str,
        client_cert_path: str,
        client_key_path: str,
        client_key_password: Optional[str] = None,
    ) -> ssl.SSLContext:
        ctx = ssl.create_default_context(cafile=ca_bundle_path)
        ctx.load_cert_chain(
            certfile=client_cert_path,
            keyfile=client_key_path,
            password=client_key_password,
        )
        return ctx

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
        return False 

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        return self._client.get(url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> httpx.Response:
        return self._client.post(url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> httpx.Response:
        return self._client.put(url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> httpx.Response:
        return self._client.patch(url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> httpx.Response:
        return self._client.delete(url, **kwargs)