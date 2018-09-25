import argparse
import logging
import os
import sys

from core.logger import LOGGER_NAME, setup_logging
from vincere import VincereAPI
from vincere.candidate import CandidateAPI

logger = logging.getLogger(LOGGER_NAME)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

    def initialize(self):
        group = self.add_argument_group('Requests')
        group.add_argument('-m', '--master', action="store_true", help="Generate Master Records", default=False)
        group.add_argument('-c', '--candidate', action="store", help="Candidate ID", dest="candidate")
        group.add_argument('-d', '--delete', help="Space separated candidate list.", dest="delete",
                           nargs='+')
        group.add_argument('-r', '--reason', action="store", help="Reason to delete candidates.", dest="reason")
        group.add_argument('-i', '--industries', action="store", help="Space separated industries list.",
                           dest="industries", nargs='+')
        group.add_argument('-e', '--expertise', action="store", help="Space separated function expertise list.",
                           dest="expertise", nargs='+')
        group.add_argument('-s', '--sub', action="store", help="Space separated Sub function expertise list.",
                           dest="sub", nargs='+')
        group.add_argument('-f', '--functional', action="store", help="Functional Expertise ID.", dest="functional_id")
        group.add_argument('-l', '--company_count', action="store", help="Company count.", dest="company_count")
        self.add_argument('-n', '--note', action="store_true", default=False, help="Get Candidate note")
        self.add_argument('-v', '--verbose', action="store_true", default=False, help="Print verbose logging on screen")
        if len(sys.argv) == 1:
            self.print_help()
            sys.exit(1)

    def validate(self):
        result = self.parse_args()
        if result.master:
            return result
        if not result.delete and not result.candidate:
            self.error("Missing Candidate ID")
        if result.delete and not result.reason:
            self.error("Missing Reason")
        if result.sub and not result.functional_id:
            self.error("Missing Functional Expertise ID")
        return result


def main1():
    p = CandidateAPI()
    industries = ['28735', '28885', '28886']
    candidate_id = 79255
    # p.set_industries(candidate_id=candidate_id, industries=industries)
    # p.set_company_count(candidate_id=candidate_id, company_counts=3)
    expertises = ['2992', '2995', '2996']
    # p.set_functional_expertise(candidate_id=candidate_id, expertises=expertises)

    functional_expertise_id = 2992
    sub_expertises = ['200', '198']
    p.set_sub_functional_expertise(candidate_id=candidate_id, functional_expertise_id=functional_expertise_id,
                                   expertises=sub_expertises)
    # v = VincereAPI(server_url="https://headhuntr.vincere.io/")
    # masters = ['industries', 'functionalexpertises']
    # sub_masters = {
    #     'functionalexpertises': {
    #         'key': 'functionalexpertise',
    #         'sub_key': 'subfunctionalexpertises',
    #     }
    # }
    # v.generate_master_data(masters=masters, sub_masters=sub_masters)


def generate_master():
    logger.info("generating Master records")
    api_client = VincereAPI()
    masters = ['industries', 'functionalexpertises']
    sub_masters = {
        'functionalexpertises': {
            'key': 'functionalexpertise',
            'sub_key': 'subfunctionalexpertises',
        }
    }
    api_client.generate_master_data(masters=masters, sub_masters=sub_masters)
    return True


def delete_candidates(candidates=[], reason=''):
    if not candidates:
        raise Exception("no candidates specified to delete")
    logger.info("Deleting '%s' candidates", ",".join(candidates))
    api_candidate = CandidateAPI()
    api_candidate.bulk_delete_candidates(candidate_ids=candidates, reason=reason)


def main(result):
    if result.master:
        return generate_master()
    if result.delete:
        return delete_candidates(candidates=result.delete, reason=result.reason)
    if result.candidate:
        api_candidate = CandidateAPI()
        if result.note:
            return {
                "note": api_candidate.get_note_on(
                    candidate_id=result.candidate
                )
            }
        if result.company_count:
            return api_candidate.set_company_count(
                candidate_id=result.candidate,
                company_counts=result.company_count
            )
        if result.industries:
            return api_candidate.set_industries(
                candidate_id=result.candidate,
                industries=result.industries
            )
        if result.expertise:
            return api_candidate.set_functional_expertise(
                candidate_id=result.candidate,
                expertises=result.expertise
            )
        if result.sub:
            return api_candidate.set_sub_functional_expertise(
                candidate_id=result.candidate,
                functional_expertise_id=result.functional_id,
                expertises=result.sub
            )


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    parser = MyParser(add_help=True)
    parser.initialize()
    result = parser.validate()
    setup_logging(scrnlog=result.verbose)
    print(result)
    print(main(result=result))
