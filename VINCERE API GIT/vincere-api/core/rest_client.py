#!/usr/bin/python

import logging
import requests
from core.logger import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


class RestClient(object):
    def __init__(self):
        pass

    def get_auth_token(self):
        return

    def get(self, url, response_code=200, headers={}):
        response = requests.get(url=url, headers=headers)
        logger.info("Method:GET, Response Code: %s, URL: %s" %
                    (response.status_code, url))
        if response.status_code != response_code:
            logger.error("Failed to get data. Error Code: %s" % response.status_code)
            raise Exception("Exception caught: Method:GET, Response Code: %s, URL: %s" %
                            (response.status_code, url))
        return response.json()

    def post(self, url, data, response_code=200, headers={}):
        response = requests.post(url=url, data=data, headers=headers)
        logger.info("Method:POST, Response Code: %s, URL: %s" %
                    (response.status_code, url))
        if response.status_code != response_code:
            logger.error("Failed to post data. Error Code: %s" % response.status_code)
            raise Exception("Exception caught: Method:POST, Response Code: %s, URL: %s" %
                            (response.status_code, url))
        return response.json()

    def put(self, url, data, response_code=200, headers={}):
        response = requests.put(url=url, data=data, headers=headers)
        logger.info("Method:PUT, Response Code: %s, URL: %s" %
                    (response.status_code, url))
        if response.status_code != response_code:
            logger.error("Failed to update data. Error Code: %s" % response.status_code)
            raise Exception("Exception caught: Method:PUT, Response Code: %s, URL: %s" %
                            (response.status_code, url))
        return response.json()

    def delete(self, url, data, response_code=200, headers={}):
        print(data)
        response = requests.delete(url=url, data=data, headers=headers)
        logger.info("Method:Delete, Response Code: %s, URL: %s" %
                    (response.status_code, url))
        if response.status_code != response_code:
            logger.error("Failed to delete data. Error Code: %s" % response.status_code)
            raise Exception("Exception caught: Method:DELETE, Response Code: %s, URL: %s" %
                            (response.status_code, url))
        return response.json()