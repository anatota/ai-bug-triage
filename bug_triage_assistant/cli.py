import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Convert a messy bug report into structured triage JSON."
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", help="Path to a text file containing a bug report.")
    input_group.add_argument("--text", help="Bug report text written directly in the command.")
    parser.add_argument(
        "--output",
        help="Optional path to save the structured JSON. Prints to the terminal if omitted.",
    )

    args = parser.parse_args()

    from bug_triage_assistant.triage import triage_bug_report

    report_text = read_report_text(args)
    result = triage_bug_report(report_text)
    formatted_json = json.dumps(result, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(formatted_json + "\n", encoding="utf-8")
        print(f"Saved triage JSON to {output_path}")
    else:
        print(formatted_json)


def read_report_text(args):
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    return args.text


if __name__ == "__main__":
    main()
