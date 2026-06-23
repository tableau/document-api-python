"""
Copyright (c) 2024 Nutanix Inc. All rights reserved.

Author: gdowding@nutanix.com

Description: Main module for running ward tests
"""
import contextlib
import os
import sys

import ward._run
from ward.models import ExitCode


# class StreamToLogger:
#     def __init__(self, level="INFO"):
#         self._level = level

#     def write(self, buffer):
#         for line in buffer.rstrip().splitlines():
#             logger.opt(depth=1).log(self._level, line.rstrip())

#     def flush(self):
#         pass


def main():
    # To pass test args using bazel, you must separate the arg name from the value using multiple --test_arg arguments.
    #
    # For example: --test_arg=--tags --test_arg="not system"
    # logger.remove()
    # logger.add(sys.__stdout__)
    # stream_to_logger = StreamToLogger()
    # for k, v in os.environ.items():
    #     if k.startswith("TEST_"):
    #         logger.debug("{k}: {v}", k=k, v=v)
    argv = sys.argv[1:]
    # Don't report no tests found as an error. This causes an error when run from
    # bazel, but it is possible for all tests from a file to be filtered out due to
    # selected tags.
    try:
        #with contextlib.redirect_stdout(stream_to_logger):
        ward._run.test(argv, standalone_mode=False)
    except SystemExit as e:
        if e.args[0] == ExitCode.NO_TESTS_FOUND.value:
            pass
        else:
            raise
    sys.exit(0)


if __name__ == "__main__":
    main()
