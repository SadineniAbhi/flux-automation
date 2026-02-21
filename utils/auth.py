from fastapi import Request
from typing import Any, cast, Awaitable, Callable
from fastapi_plugin.fast_api_client import Auth0FastAPI  # type: ignore

auth0 = Auth0FastAPI(
    domain="dev-xd0ga8sh216d7yr0.us.auth0.com",
    audience="https://startup-automation.com/"
)

Claims = dict[str, Any]
AuthDependency = Callable[[Request], Awaitable[Claims]]
auth_dependency = cast(AuthDependency, auth0.require_auth())