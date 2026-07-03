import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Convert a messy bug report into structured triage JSON."
    )
    parser.add_argument(
        "report",
        nargs="?",
        help="Bug report text written directly in the command.",
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--file", help="Path to a text file containing a bug report.")
    input_group.add_argument("--text", help="Bug report text written directly in the command.")
    parser.add_argument(
        "--output",
        help="Optional path to save the structured JSON. Prints to the terminal if omitted.",
    )

    args = parser.parse_args()
    if args.report and (args.file or args.text):
        parser.error("Use either quoted bug report text or --file/--text, not both.")

    from bug_triage_assistant.triage import triage_bug_report

    try:
        report_text = read_report_text(args)
        if not report_text or not report_text.strip():
            parser.error(
                'No bug report provided. Try: python main.py "App crashes when I click login"'
            )

        result = triage_bug_report(report_text)
    except FileNotFoundError:
        print(f"Error: Could not find the file: {args.file}", file=sys.stderr)
        return 1
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

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
    if args.text:
        return args.text
    return args.report


if __name__ == "__main__":
    raise SystemExit(main())
