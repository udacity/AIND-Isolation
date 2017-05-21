import os

from udacity_pa import udacity

from glob import glob

SETTINGS = {
    "isolation": {
        "required": {
            "game_agent": {"ext": ["py"], "size": 0.2},
        },
        "optional": {
            "heuristic_analysis": {"ext": ["pdf"], "size": 6.0},
            "research_review": {"ext": ["pdf"], "size": 6.0},
        }
    },
    "isolation-pvp": {
        "required": {
            "competition_agent": {"ext": ["py"], "size": 0.2},
        },
        "optional": {
            "data": {"ext": ["json"], "size": 4}
        }
    }
}
nanodegree = "nd889"
projects = list(SETTINGS.keys())


RESUBMIT_MSG = """
NOTICE:

  You are about to submit your agent.  If you have previously submitted
  your agent, continuing will replace that submission.

"""


def require_confirmation(text):
    print(text)
    ans = input("Please type 'yes' to confirm submission>")
    print()
    if ans.lower() != "yes":
        print(
            "  Submission aborted -- you must confirm submission to proceed.\n"
        )
        exit()


def validate_file_info(pattern, lo=1, hi=1, size=6, ext=[]):

    filenames = [x for x in glob(pattern + ".*")
                 if not ext or str.lower(os.path.splitext(x)[-1])[1:] in ext]

    if not (lo <= len(filenames) <= hi):
        raise RuntimeError(
            ("Submission Failed - a required file was missing.  At least " +
             "{!s} file(s) and no more than {!s} file(s) that match the " +
             "pattern '{!s}.<EXT>' with one of the extensions: {!s} must " +
             "be found in the current working directory.")
            .format(lo, hi, pattern, ext))

    large_files = [x for x in filenames if os.stat(x).st_size > size * 2**20]
    if large_files:
        raise RuntimeError(
            ("Submission Failed: One or more files is too large. Please " +
             "make sure that the following files are under {!s}MB and try " +
             "again: {!s}").format(size, large_files))

    return filenames


def submit(options):

    if len(options.args) == 0 or options.args[0] not in projects:
        raise RuntimeError("You must specifiy 'isolation' or 'isolation-pvp' after 'udacity submit'.")

    project_name = options.args[0]
    if project_name == 'isolation-pvp':
        require_confirmation(RESUBMIT_MSG)
    patterns = SETTINGS.get(project_name, {})
    if not patterns:
        raise RuntimeError("")

    required_files = [validate_file_info(ptn, **kwargs)
                      for ptn, kwargs in patterns.get("required", {}).items()]
    optional_files = [validate_file_info(ptn, lo=0, **kwargs)
                      for ptn, kwargs in patterns.get("optional", {}).items()]
    filenames = sum(required_files + optional_files, [])
    file_info = (list(patterns.get("required", {}).values()) +
                 list(patterns.get("optional", {}).values()))
    max_size = sum([dict(info).get("size", 0) for info in file_info]) * 2**20

    udacity.submit(nanodegree,
                   project_name,
                   filenames, 
                   environment = options.environment,
                   max_zip_size=max_size)
