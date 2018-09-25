#!/usr/bin/python

import json
import logging

import requests

from . import config
from core.rest_client import RestClient

from core.logger import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


class VincereClient(RestClient):
    def __init__(self):
        self.id_token = ""
        self.load_token()
        self.validate_token()

    def validate_token(self):
        url = "https://id.vincere.io/oauth2/user"
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        headers.update(self.get_auth_header())

        response = requests.get(url=url, headers=headers)
        logger.info("Method:GET, Response Code: %s, URL: %s" %
                    (response.status_code, url))

        if response.status_code == 401:
            self.get_new_token()
        elif response.status_code != 200:
            logger.error("Failed to validate token expiry. Error Code: %s" % response.status_code)
            raise Exception("Failed to validate token expiry. Error Code: %s" % response.status_code)

    def get_auth_header(self):
        return {
            "x-api-key": config.API_KEY,
            "id-token": self.id_token,
        }

    def load_token(self):
        with open('token.json') as json_data:
            try:
                token_data = json.load(json_data)
                self.id_token = token_data.get('id_token')
            except json.decoder.JSONDecodeError as ex:
                logger.exception(ex)
            if not self.id_token:
                self.get_new_token()

    def save_token(self):
        with open('token.json', 'w') as token_file:
            json_data = {"id_token": self.id_token}
            token_file.write(json.dumps(json_data))

    def get_new_token(self):
        url = "https://id.vincere.io/oauth2/token"
        data = {
            "refresh_token": config.REFRESH_TOKEN,
            "grant_type": "refresh_token",
            "client_id": config.CLIENT_ID
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        response = requests.post(url=url, data=data, headers=headers)
        logger.info("Method:POST, Response Code: %s, URL: %s" %
                    (response.status_code, url))

        if response.status_code != 200:
            logger.error("Failed to get new token. Error Code: %s" % response.status_code)
            raise Exception("Failed to get new token. Error Code: %s" % response.status_code)

        response_data = response.json()
        self.id_token = response_data['id_token']
        self.save_token()

    def get(self, url, headers={}, response_code=200):
        headers = headers if headers else {}
        headers.update({"Accept": "application/json"})
        headers.update(self.get_auth_header())
        return super().get(url, headers=headers, response_code=response_code)

    def post(self, url, data, response_code=200, headers={}):
        headers = headers if headers else {}
        headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        headers.update(self.get_auth_header())
        return super().post(url, data=json.dumps(data), headers=headers, response_code=response_code)

    def put(self, url, data, headers={}, response_code=200):
        headers = headers if headers else {}
        headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        headers.update(self.get_auth_header())
        return super().put(url, data=json.dumps(data), headers=headers, response_code=response_code)

    def delete(self, url, data, headers={}, response_code=200):
        headers = headers if headers else {}
        headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        headers.update(self.get_auth_header())
        return super().delete(url, data=json.dumps(data), headers=headers, response_code=response_code)