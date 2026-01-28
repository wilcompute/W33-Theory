import json
from pathlib import Path


def main():
    logp = Path("logs/validate_summaries.log")
    logp.parent.mkdir(exist_ok=True)
    with logp.open("w") as f:
        f.write("Validating summary and numeric comparison JSONs against schemas\n")
        try:
            import jsonschema

            f.write("jsonschema import OK\n")
        except Exception as e:
            f.write("ERROR: jsonschema not available: %s\n" % (e,))
            raise

        s = json.loads(Path("schemas/summary_results.schema.json").read_text())
        d = json.loads(Path("SUMMARY_RESULTS.json").read_text())
        jsonschema.validate(instance=d, schema=s)
        f.write("SUMMARY_RESULTS.json validates OK\n")

        s2 = json.loads(Path("schemas/numeric_comparisons.schema.json").read_text())
        d2 = json.loads(Path("NUMERIC_COMPARISONS.json").read_text())
        jsonschema.validate(instance=d2, schema=s2)
        f.write("NUMERIC_COMPARISONS.json validates OK\n")
        f.flush()
        print("WROTE", logp)


if __name__ == "__main__":
    main()
