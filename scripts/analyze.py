#!/usr/bin/env python3
"""
Simple CLI helper for the CloudOps AI Assistant project.

This script does not call any AI API yet. It only validates the input file and
shows which prompt and report path should be used for the selected analysis.
"""

import argparse
from pathlib import Path


def parse_args():
    """Read command-line arguments from the user."""
    parser = argparse.ArgumentParser(
        description="Prepare a Terraform, log, or AWS documentation analysis workflow."
    )

    parser.add_argument(
        "--type",
        choices=["terraform", "log", "aws-doc"],
        required=True,
        help="Type of analysis to run: terraform, log, or aws-doc.",
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to the Terraform, log, or AWS question file to analyze.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned analysis without creating or modifying files.",
    )

    return parser.parse_args()


def get_workflow_paths(analysis_type):
    """Return the prompt file and report folder for the selected analysis type."""
    if analysis_type == "terraform":
        return Path("prompts/terraform-review.md"), Path("reports/security/")

    if analysis_type == "log":
        return Path("prompts/log-analysis.md"), Path("reports/incidents/")

    return Path("prompts/aws-explainer.md"), Path("reports/reliability/")


def build_output_path(input_file, analysis_type, report_folder):
    """Create a report filename from the input filename."""
    if analysis_type == "terraform":
        report_name = f"{input_file.stem}-review.md"
    elif analysis_type == "log":
        report_name = f"{input_file.stem}-analysis.md"
    else:
        report_name = f"{input_file.stem}-guide.md"

    return report_folder / report_name


def main():
    """Validate the input and print the next steps for the user."""
    args = parse_args()
    input_file = Path(args.file)

    # Stop early if the requested input file does not exist.
    if not input_file.exists():
        print(f"Error: input file not found: {input_file}")
        return 1

    prompt_path, report_folder = get_workflow_paths(args.type)
    output_path = build_output_path(input_file, args.type, report_folder)

    print("CloudOps AI Assistant CLI")
    print("-------------------------")

    # Dry-run mode is useful for checking paths before doing any real work.
    # This script does not write files yet, but the message makes that explicit.
    if args.dry_run:
        print("Mode: dry run")
        print("No files will be created or modified.")
        print()

    print(f"Analysis type: {args.type}")
    print(f"Input file: {input_file}")
    print(f"Use prompt: {prompt_path}")
    print(f"Save report in: {report_folder}")
    print(f"Output report: {output_path}")
    print()
    print("Next step: use the prompt and input file with Codex to generate the report.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
