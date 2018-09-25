#!/usr/bin/python

import logging

from .vincere import VincereAPI
from vincere import config
from core.logger import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


class CandidateAPI(VincereAPI):
    def __init__(self):
        super().__init__()
        server_url = config.server_url
        self.api_url = (server_url if server_url.endswith("/") else server_url + "/") + "api/v2/candidate/"
        logger.info("Creating instance of %s with url %s.", self.__class__.__name__, self.api_url)

    def _get_candidate_url(self, candidate_id):
        return "{0}{1}".format(self.api_url, candidate_id)

    def _get_candidate_details(self, candidate_id):
        candidate_url = self._get_candidate_url(candidate_id)
        return self.client.get(url=candidate_url)

    def get_note_on(self, candidate_id):
        data = self._get_candidate_details(candidate_id=candidate_id)
        return data.get("note_on")

    def set_company_count(self, candidate_id, company_counts=0):
        data = self._get_candidate_details(candidate_id=candidate_id)
        data.update({"company_count": company_counts})
        logger.info("Sending request to set company counts for Candidate {candidate_id:%s, company_counts=%s",
                    candidate_id, company_counts)

        return self.client.put(url=self._get_candidate_url(candidate_id=candidate_id), data=data)

    def set_industries(self, candidate_id, industries=[]):
        industries_url = "{0}{1}/industries".format(self.api_url, candidate_id)
        logger.info("Sending request to set Industries for Candidate {candidate_id:%s, url: %s, industries=%s",
                    candidate_id, industries_url, industries)

        return self.client.put(url=industries_url, data=industries)

    def set_functional_expertise(self, candidate_id, expertises=[]):
        expertise_url = "{0}{1}/functionalexpertises".format(self.api_url, candidate_id)
        logger.info(
            "Sending request to set functional expertise for Candidate {candidate_id:%s, url: %s, expertises=%s",
            candidate_id, expertise_url, expertises)

        return self.client.put(url=expertise_url, data=expertises)

    def set_sub_functional_expertise(self, candidate_id, functional_expertise_id, expertises=[]):
        expertise_url = "{0}{1}/functionalexpertise/{2}/subfunctionalexpertises".format(self.api_url, candidate_id,
                                                                                        functional_expertise_id)
        logger.info(
            "Sending request to set sub functional expertise for Candidate {candidate_id:%s, url: %s, expertises=%s",
            candidate_id, expertise_url, expertises)

        return self.client.put(url=expertise_url, data=expertises)

    def delete_candidate(self, candidate_id, reason):
        candidate_url = self._get_candidate_url(candidate_id)
        data = {
            "reason": reason
        }
        logger.info(
            "Sending request to Delete Candidate {candidate_id:%s, reason=%s",
            candidate_id, reason)
        response = self.client.delete(url=candidate_url, data=data)
        if "SUCCEEDED" != response.get('status'):
            logger.error("Failed to delete candidate %s %s", candidate_id, str(response))
            return False
        return True

    def bulk_delete_candidates(self, candidate_ids, reason):
        result = {
            "Failed": [],
            "Success": []
        }
        for candidate_id in candidate_ids:
            candidate_url = self._get_candidate_url(candidate_id)

            if self.delete_candidate(candidate_id=candidate_id, reason=reason):
                result['Success'].append(candidate_id)
            else:
                result['Failed'].append(candidate_id)

        return result
