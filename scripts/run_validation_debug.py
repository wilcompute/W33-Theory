import json
from pathlib import Path


def main():
    logp = Path("logs/validate_debug.log")
    logp.parent.mkdir(exist_ok=True)
    with logp.open("w") as f:
        f.write("Starting validation\n")
        try:
            import jsonschema

            f.write("jsonschema " + jsonschema.__version__ + "\n")
        except Exception as e:
            f.write("ERROR import jsonschema: %r\n" % (e,))
            raise

        try:
            s = json.loads(Path("schemas/summary_results.schema.json").read_text())
            d = json.loads(Path("SUMMARY_RESULTS.json").read_text())
            jsonschema.validate(instance=d, schema=s)
            f.write("SUMMARY ok\n")
        except Exception as e:
            f.write("SUMMARY FAIL: %r\n" % (e,))

        try:
            s2 = json.loads(Path("schemas/numeric_comparisons.schema.json").read_text())
            d2 = json.loads(Path("NUMERIC_COMPARISONS.json").read_text())
            jsonschema.validate(instance=d2, schema=s2)
            f.write("NUMERIC ok\n")
        except Exception as e:
            f.write("NUMERIC FAIL: %r\n" % (e,))

        f.flush()
    print("WROTE", logp)


if __name__ == "__main__":
    main()
