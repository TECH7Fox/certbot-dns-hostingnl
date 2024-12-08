"""DNS Authenticator for Hostingnl."""
import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
import requests

from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://mijn.hosting.nl/index.php?m=APIKeyGenerator'


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Hostingnl

    This Authenticator uses the Hostingnl API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are using Hostingnl for '
                   'DNS).')
    ttl = 120

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None],
                             default_propagation_seconds: int = 10) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add('credentials', help='Hostingnl credentials INI file.')

    def more_info(self) -> str:
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Hostingnl API.'

    def _validate_credentials(self, credentials: CredentialsConfiguration) -> None:
        key = credentials.conf('api-key')
        if not key:
            raise errors.PluginError('{}: dns_hostingnl_api_key is required when using a '
                                     'Global API Key. (see {})'
                                     .format(credentials.confobj.filename, ACCOUNT_URL))

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            'credentials',
            'Hosting.nl credentials INI file',
            None,
            self._validate_credentials
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_hostingnl_client().add_txt_record(domain, validation_name, validation, self.ttl)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_hostingnl_client().del_txt_record(domain, validation_name, validation)

    def _get_hostingnl_client(self) -> "_HostingnlClient":
        if not self.credentials:  # pragma: no cover
            raise errors.Error("Plugin has not been prepared.")
        return _HostingnlClient(api_key = self.credentials.conf('api-key'))


class _HostingnlClient:
    """
    Encapsulates all communication with the Hosting.nl API.
    """

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.api_url = "https://api.hosting.nl"
        self.record_id = None

    def add_txt_record(self, domain: str, record_name: str, record_content: str,
                       record_ttl: int) -> None:
        """
        Add a TXT record using the supplied information.

        :param str domain: The domain to use to look up the Hosting.nl zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the Hosting.nl API
        """

        data = [
            {
                'type': 'TXT',
                'name': record_name,
                'content': '"' + record_content + '"',
                'ttl': "3600",
                'prio': "0",
            }
        ]

        print(data)

        try:
            logger.debug(f"Attempting to add record to domain {domain}")
            # Send request
            url = f"{self.api_url}/domains/{domain}/dns"
            response = requests.post(
                url,
                headers={"API-TOKEN": self.api_key},
                json=data,
            )
            print(response.text)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Error communicating with the Hosting.nl API: {e}")
            raise errors.PluginError("Error communicating with the Hosting.nl API: {e}")

        self.record_id = response.json()["data"][0]["id"]
        print(self.record_id)
        logger.debug('Successfully added TXT record with record_id: %s', self.record_id)

    def del_txt_record(self, domain: str, record_name: str, record_content: str) -> None:
        """
        Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        :param str domain: The domain to use to look up the Hostingnl zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """

        if self.record_id is None:
            logger.debug('No record_id found to delete')
            print('No record_id found to delete')
            return

        data = [
            {
                "id": self.record_id,
            }
        ]

        try:
            url = f"{self.api_url}/domains/{domain}/dns"
            response = requests.get(
                url,
                headers={"API-TOKEN": self.api_key},
                json=data,
            )
            print(response.text)
            print(response.status_code)
            response.raise_for_status()
        except Exception as e:
            logger.debug('Encountered error finding zone_id during deletion: %s', e)
            return
    
        self.record_id = None
