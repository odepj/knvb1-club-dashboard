import logging
from hashlib import md5

import requests

from client.util.mapper import instantiateClassFromList
from client.models.models import KnvbResponse


class KnvbDatacentreRequestHandler:
    def __init__(self, base_url, auth_path, api_key, status_codes):
        self.base_url = base_url
        self.auth_path = auth_path
        self.api_key = api_key
        self.status_codes = status_codes

    def handle(self, url_path, params=None, data_classtype=dict):
        to_be_authorized = '/' + url_path.split('/')[1]

        auth_params = self._get_authorization_request_params(to_be_authorized)
        if not params:
            params = dict()
        params.update(auth_params)

        result = self._send_request(url_path, params)
        return instantiateClassFromList(data_classtype, result.List)

    def _send_request(self, url_path, params):
        try:
            response = requests.get(self.base_url + url_path, params)
            response.raise_for_status()
            knvb_response = KnvbResponse(response.json())
            self._check_request_code(knvb_response)
            return knvb_response
        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logging.error("Something went wrong:", err)

    def _get_authorization_request_params(self, auth_path):
        session_id = self._get_session_id()
        hash_code = self._generate_hash(auth_path, session_id)
        return {'PHPSESSID': session_id, 'hash': hash_code}

    #  pathname: Unieke pathname voor de club zoals vastgelegd in het admin interface.
    #  apiversion: Is optioneel; in sommige gevallen kan er een bepaald versie nummer van de API mee afgedwongen worden.
    def _get_session_id(self):
        # BASEURL/api/initialisatie/<super_secret_personal_path>[&apiversion=1.0]
        url = self.base_url + '/initialisatie' + self.auth_path
        auth_resp = requests.get(url=url).json()
        response = KnvbResponse(auth_resp)
        if not response.List:
            msg = f'An error occurred while fetching a session_id, code: {response.errorcode} message: {response.message}'
            logging.error(msg)
        return response.List[0]['PHPSESSID']

    def _generate_hash(self, url_path, session_id):
        return md5(f'{self.api_key}#{url_path}#{session_id}'.encode('utf-8')).hexdigest()

    def _check_request_code(self, response: KnvbResponse):
        if response.errorcode != 1000:
            key = str(response.errorcode)
            msg = f'Client responded with an error, statuscode: {response.errorcode},' \
                  f' http response message: {response.message} \nerror message according to API doc: '
            status_code_info = self.status_codes[key] if key in self.status_codes.keys() else 'not available'
            msg = msg + status_code_info
            logging.error(msg)
