FROM python:3.12.5-slim-bookworm

# Upgrade
RUN apt-get update && apt-get -y upgrade

# Create a non-root user.
RUN useradd -m -u 1000 app_user

# Switch to the non-root user
ENV HOME="/home/app_user"
USER app_user
# Set the working directory in the container
WORKDIR ${HOME}/app

RUN pip install --upgrade pip
RUN pip install frankfurtermcp

# Copy the default environment values
COPY ./.env.template ./.env

# Expose the port to conect
ENV PORT=8000
ENV FASTMCP_PORT=${PORT}
EXPOSE ${PORT}
# Run the application
ENTRYPOINT [ "python", "-m", "frankfurtermcp.server" ]
