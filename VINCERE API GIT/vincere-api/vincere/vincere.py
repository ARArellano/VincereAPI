#!/usr/bin/python

import logging

from .client import VincereClient
from . import config
from core.logger import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


class VincereAPI(object):
    def __init__(self):
        server_url = config.server_url
        self.api_url = (server_url if server_url.endswith("/") else server_url + "/") + "api/v2/"
        logger.info("Creating instance of %s with url %s.", self.__class__.__name__, self.api_url)
        self.client = VincereClient()

    def generate_master_data(self, masters=[], sub_masters={}):
        for item in masters:
            record_url = "{0}{1}".format(self.api_url, item)
            data = self.client.get(url=record_url)
            sub_key = item in sub_masters.keys()

            with open(item + ".csv", 'w') as file_instance:
                if sub_key:
                    sub_master = sub_masters[item]
                    sub_file_instance = open(sub_master["sub_key"] + ".csv", 'w')
                    sub_file_instance.write("id,name,%s_id,%s_name\n" % (item, item))
                file_instance.write("id,name\n")
                for data_item in data:
                    file_instance.write("%s,%s\n"
                                        % (data_item.get('value'), data_item.get('description')))
                    if sub_key:
                        sub_record_url = "{0}{1}/{2}/{3}".format(self.api_url, sub_master['key'], data_item.get('value'),
                                                                 sub_master["sub_key"])
                        sub_data = self.client.get(url=sub_record_url)
                        for sub_data_item in sub_data:
                            sub_file_instance.write("%s,%s,%s,%s\n" % (
                                sub_data_item.get('value'), sub_data_item.get('description'),
                                data_item.get('value'), data_item.get('description')
                            ))
