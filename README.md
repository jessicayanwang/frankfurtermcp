[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue?logo=python&logoColor=3776ab&labelColor=e4e4e4)](https://www.python.org/downloads/release/python-3120/)
[![Experimental status](https://img.shields.io/badge/Status-experimental-orange)](#)

[![Dependabot Updates](https://github.com/anirbanbasu/frankfurtermcp/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/anirbanbasu/frankfurtermcp/actions/workflows/dependabot/dependabot-updates) [![pytest](https://github.com/anirbanbasu/frankfurtermcp/actions/workflows/uv-pytest.yml/badge.svg)](https://github.com/anirbanbasu/frankfurtermcp/actions/workflows/uv-pytest.yml)
# Frankfurter MCP

[Frankfurter](https://frankfurter.dev/) is a useful API for latest currency exchange rates, historical data, or time series published by sources such as the European Central Bank. Should you need to access the Frankfurter API as tools for language model agents exposed over the Model Context Protocol (MCP), Frankfurter MCP is what you need.

## Project status

Following is a table of some updates regarding the project status. Note that these do not correspond to specific commits or milestones.

| Date     |  Status   |  Notes or observations   |
|----------|:-------------:|----------------------|
| June 8, 2025 |  active |  Added dynamic composition.<br/>**TODO**: Exception handling; outgoing proxy and self-signed certificate configuration; Dockerisation. |
| June 7, 2025 |  active |  Added tools to cover all the functionalities of the Frankfurter API. |
| June 7, 2025 |  active |  Project started.  |

## Installation

The directory where you clone this repository will be referred to as the _working directory_ or _WD_ hereinafter.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/). To install the project with its essential dependencies in a virtual environment, run the following in the _WD_. To install all non-essential dependencies (_which are required for developing and testing_), add the `--all-extras` flag to the following command.


```bash
uv sync
```

## Environment variables

Following is a list of environment variables that can be used to configure the application. A template of environment variables is provided in the file `.env.template`.

The following environment variables can be specified, prefixed with `FASTMCP_SERVER_`: `HOST`, `PORT`, `DEBUG` and `LOG_LEVEL`. See [key configuration options](https://gofastmcp.com/servers/fastmcp#key-configuration-options) for FastMCP. Note that `on_duplicate_` prefixed options specified as environment variables _will be ignored_.

| Variable |  [Default value] and description   |
|--------------|----------------|
| `MCP_SERVER_TRANSPORT` | [streamable-http] The acceptable options are `stdio`, `sse` or `streamable-http`. Given the use-case of running this MCP server as a remotely accessible endpoint, there is no real reason to choose `stdio`. |
| `FRANKFURTER_API_URL` | [https://api.frankfurter.dev/v1] If you are [self-hosting the Frankfurter API](https://hub.docker.com/r/lineofflight/frankfurter), you should change this to the API endpoint address of your deployment. |

## Usage (with `pip`)

Add this package from PyPI using `pip` in a virtual environment (possibly managed by `conda` or `pyenv`) and then start the server by running the following.

Add a `.env` file with the contents of the `.env.template` file if you wish to modify the default values of the aforementioned environment variables. Or, on your shell, you can export the environment variables that you wish to modify.

```bash
pip install frankfurtermcp
python -m frankfurtermcp.server
```

## Usage (self-hosted server using `uv`)

Copy the `.env.template` file to a `.env` file in the _WD_, to modify the aforementioned environment variables, if you want to use anything other than the default settings. Or, on your shell, you can export the environment variables that you wish to modify.

Run the following in the _WD_ to start the MCP server.

```bash
uv run frankfurtermcp
```

If you want to run it without `uv`, assuming that the appropriate virtual environment has been created in the `.venv` within the _WD_, you can start the server calling the following.

```bash
./.venv/bin/python -m frankfurtermcp.server
```

The MCP endpoint will be available over HTTP at [http://localhost:8000/sse](http://localhost:8000/sse) for the Server Sent Events (SSE) transport, or [http://localhost:8000/mcp](http://localhost:8000/mcp) for the streamable HTTP transport. To exit the server, use the Ctrl+C key combination.

## Usage (self-hosted server using Docker)

**TODO:** To be added, eventually.

## Usage (dynamic mounting with FastMCP)

To see how to use the MCP server by mounting it dynamically with [FastMCP](https://gofastmcp.com/), check the file `src/frankfurtermcp/composition.py`.

## Contributing

Install [`pre-commit`](https://pre-commit.com/) for Git and [`ruff`](https://docs.astral.sh/ruff/installation/). Then enable `pre-commit` by running the following in the _WD_.

```bash
pre-commit install
```
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Testing

To run the provided test cases, execute the following. Add the flag `--capture=tee-sys` to the command to display further console output.

_Note that for the tests to succeed, the environment variable `MCP_SERVER_TRANSPORT` must be set to either `sse` or `streamable-http`, or not set at all, in which case it will default to `streamable-http`_.

```bash
uv run --group test pytest -q tests/
```

## License

[MIT](https://choosealicense.com/licenses/mit/).
