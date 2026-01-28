import sys
from pathlib import Path

import pytest


def main():
    log = Path("logs/artifact_pytest_run.log")
    log.parent.mkdir(exist_ok=True)
    with log.open("w") as f:
        f.write("Running artifact tests\n")
        rc = pytest.main(
            [
                "-q",
                "tests/test_summary.py::test_summary_and_numeric_comparisons",
                "tests/test_summary_schema.py::test_summary_matches_schema",
                "tests/test_summary_schema.py::test_numeric_comparisons_matches_schema",
                "-q",
                "-r",
                "a",
            ]
        )
        f.write("RC: %s\n" % rc)
    print("WROTE", log)


if __name__ == "__main__":
    main()
