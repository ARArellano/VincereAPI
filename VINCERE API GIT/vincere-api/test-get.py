import argparse
import logging
import os
import sys

from core.logger import LOGGER_NAME, setup_logging
from vincere import VincereAPI
from vincere.candidate import CandidateAPI

logger = logging.getLogger(LOGGER_NAME)


if __name__ == '__main__':
    setup_logging(scrnlog=True)
    api_candidate = CandidateAPI()
    print (api_candidate.client.get(url="https://headhuntr.vincere.io/api/v2/candidate/1004286/industries"))
    print (api_candidate.client.get(url="https://headhuntr.vincere.io/api/v2/candidate/1004286/functionalexpertises"))
    print (api_candidate.client.get(url="https://headhuntr.vincere.io/api/v2/candidate/1004286"))
	
    print(api_candidate._get_candidate_details(candidate_id=1004286))