import signal
import sys
import httpx

from fastmcp import FastMCP

from rich import print as print
from frankfurtermcp.common import EnvironmentVariables
from frankfurtermcp.utils import parse_env

from frankfurtermcp import package_metadata, frankfurter_api_url

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
    name="get_supported_currencies",
)
def get_supported_currencies() -> list[str]:
    """
    Returns a list of supported currencies.
    """
    return httpx.get(f"{frankfurter_api_url}/currencies").json()


def _get_latest_exchange_rates(
    base_currency: str = None, symbols: list[str] = None
) -> dict:
    """
    Internal function to get the latest exchange rates.
    This is a helper function for the main tool.
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
    description="Get latest exchange rates in specific currencies for a given base currency",
    tags=["currency-rates", "exchange-rates"],
    name="get_latest_exchange_rates",
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
    return _get_latest_exchange_rates(
        base_currency=base_currency,
        symbols=symbols,
    )


@app.tool(
    description="Convert an amount from one currency to another using the latest exchange rates",
    tags=["currency-rates", "currency-conversion"],
    name="convert_currency_latest",
)
def convert_currency_latest(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    """
    Converts an amount from one currency to another using the latest exchange rates.
    The from_currency and to_currency parameters should be 3-character currency codes.
    """
    latest_rates = _get_latest_exchange_rates(
        base_currency=from_currency,
        symbols=[to_currency],
    )
    if not latest_rates or "rates" not in latest_rates:
        raise ValueError(
            f"Could not retrieve exchange rates for {from_currency} to {to_currency}."
        )
    rate = latest_rates["rates"].get(to_currency)
    if rate is None:
        raise ValueError(
            f"Exchange rate for {from_currency} to {to_currency} not found."
        )
    converted_amount = amount * float(rate)
    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "converted_amount": converted_amount,
        "exchange_rate": rate,
    }


@app.tool(
    description="Get historical exchange rates for a specific date or date range in specific currencies for a given base currency",
    tags=["currency-rates", "historical-exchange-rates"],
    name="get_historical_exchange_rates",
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
    def sigterm_handler(signal, frame):
        """
        Signal handler to shut down the server gracefully.
        """
        print("[green]Attempting graceful shutdown[/green], please wait...")
        # This is absolutely necessary to exit the program
        sys.exit(0)

    # TODO: Should we also catch SIGTERM, SIGKILL, etc.? What about Windows?
    signal.signal(signal.SIGTERM, sigterm_handler)

    print(
        f"[green]Initiating startup[/green] of [bold]{package_metadata['Name']} {package_metadata['Version']}[/bold], [red]press CTRL+C to exit...[/red]"
    )
    # TODO: Should this be forked as a separate process, to which we can send the SIGTERM signal?
    app.run(
        transport=parse_env(
            EnvironmentVariables.MCP_SERVER_TRANSPORT,
            default_value=EnvironmentVariables.DEFAULT__MCP_SERVER_TRANSPORT,
            allowed_values=EnvironmentVariables.ALLOWED__MCP_SERVER_TRANSPORT,
        )
    )


if __name__ == "__main__":
    main()
