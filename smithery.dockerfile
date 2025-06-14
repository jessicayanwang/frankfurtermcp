# Smithery does not work with base images such as ghcr.io/astral-sh/uv:python3.12-bookworm-slim
FROM python:3.12.5-slim-bookworm

# Install the latest version as available on PyPI
RUN pip install --no-cache-dir frankfurtermcp

ENTRYPOINT ["sh", "-c"]
CMD ["PORT=${PORT} FASTMCP_PORT=${PORT} python -m frankfurtermcp.server"]
