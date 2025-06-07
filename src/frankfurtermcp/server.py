import signal
import sys
import httpx

from dotenv import load_dotenv
from fastmcp import FastMCP

from rich import print as print
from frankfurtermcp.common import AppMetadata, EnvironmentVariables, ic
from frankfurtermcp.utils import parse_env

from importlib.metadata import metadata


package_metadata = metadata(AppMetadata.PACKAGE_NAME)

ic(load_dotenv())

frankfurter_api_url = parse_env(
    EnvironmentVariables.FRANKFURTER_API_URL,
    default_value=EnvironmentVariables.DEFAULT__FRANKFURTER_API_URL,
)

app = FastMCP(
    name=package_metadata["Name"],
    description=package_metadata["Description"],
    tags=["frankfurtermcp", "mcp", "currency-rates"],
    on_duplicate_prompts="error",
    on_duplicate_resources="error",
    on_duplicate_tools="error",
)


@app.tool(
    description="Get supported currencies",
    tags=["currency-rates", "supported-currencies"],
)
def get_supported_currencies() -> list[str]:
    """
    Returns a list of supported currencies.
    """
    return httpx.get(f"{frankfurter_api_url}/currencies").json()


@app.tool(
    description="Get latest exchange rates in specific currencies for a given base currency",
    tags=["currency-rates", "exchange-rates"],
)
def get_latest_exchange_rates(
    base_currency: str = None, symbols: list[str] = None
) -> dict:
    """
    Returns the latest exchange rates for a specific currency.
    If no base currency is provided, it defaults to EUR. The
    symbols parameter can be used to filter the results
    to specific currencies. If symbols is not provided, all
    available currencies will be returned.
    """
    params = {}
    if base_currency:
        params["base"] = base_currency
    if symbols:
        params["symbols"] = ",".join(symbols)
    return httpx.get(
        f"{frankfurter_api_url}/latest",
        params=params,
    ).json()


@app.tool(
    description="Get historical exchange rates for a specific date or date range in specific currencies for a given base currency",
    tags=["currency-rates", "historical-exchange-rates"],
)
def get_historical_exchange_rates(
    specific_date: str = None,
    start_date: str = None,
    end_date: str = None,
    base_currency: str = None,
    symbols: list[str] = None,
) -> dict:
    """
    Returns historical exchange rates for a specific date or date range.
    If no specific date is provided, it defaults to the latest available date.
    The symbols parameter can be used to filter the results to specific currencies.
    If symbols is not provided, all available currencies will be returned.
    """
    params = {}
    if base_currency:
        params["base"] = base_currency
    if symbols:
        params["symbols"] = ",".join(symbols)

    frankfurter_url = frankfurter_api_url
    if start_date and end_date:
        frankfurter_url += f"/{start_date}..{end_date}"
    elif start_date:
        # If only start_date is provided, we assume the end date is the latest available date
        frankfurter_url += f"/{start_date}.."
    elif specific_date:
        # If only specific_date is provided, we assume it is the date for which we want the rates
        frankfurter_url += f"/{specific_date}"
    else:
        raise ValueError(
            "You must provide either a specific date, a start date, or a date range."
        )

    return httpx.get(
        frankfurter_url,
        params=params,
    ).json()


def main():
    def sigint_handler(signal, frame):
        """
        Signal handler to shut down the server gracefully.
        """
        print("[green]Attempting graceful shutdown[/green], please wait...")
        # This is absolutely necessary to exit the program
        sys.exit(0)

    # TODO: Should we also catch SIGTERM, SIGKILL, etc.? What about Windows?
    signal.signal(signal.SIGINT, sigint_handler)

    print(
        f"[green]Initiating startup[/green] of [bold]{package_metadata['Name']} {package_metadata['Version']}[/bold], [red]press CTRL+C to exit...[/red]"
    )
    # TODO: Should this be forked as a separate process, to which we can send the SIGINT signal?
    app.run(
        transport=parse_env(
            EnvironmentVariables.MCP_SERVER_TRANSPORT,
            default_value=EnvironmentVariables.DEFAULT__MCP_SERVER_TRANSPORT,
            allowed_values=EnvironmentVariables.ALLOWED__MCP_SERVER_TRANSPORT,
        )
    )


if __name__ == "__main__":
    main()
