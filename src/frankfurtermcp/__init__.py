from dotenv import load_dotenv

from importlib.metadata import metadata
from frankfurtermcp.common import AppMetadata, EnvironmentVariables, ic
from frankfurtermcp.utils import parse_env

package_metadata = metadata(AppMetadata.PACKAGE_NAME)

frankfurter_api_url = parse_env(
    EnvironmentVariables.FRANKFURTER_API_URL,
    default_value=EnvironmentVariables.DEFAULT__FRANKFURTER_API_URL,
)

ic(load_dotenv())
