try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa


class EnvironmentVariables:
    """
    List of environment variables used in this project.
    """

    MCP_SERVER_TRANSPORT = "MCP_SERVER_TRANSPORT"
    DEFAULT__MCP_SERVER_TRANSPORT = "streamable-http"
    ALLOWED__MCP_SERVER_TRANSPORT = ["stdio", "sse", "streamable-http"]

    FRANKFURTER_API_URL = "FRANKFURTER_API_URL"
    DEFAULT__FRANKFURTER_API_URL = "https://api.frankfurter.dev/v1"


class AppMetadata:
    """
    Metadata for the application.
    """

    PACKAGE_NAME = "frankfurtermcp"
