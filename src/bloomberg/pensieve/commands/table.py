import argparse
import sys
from pathlib import Path

from bloomberg.pensieve import Tracker
from bloomberg.pensieve.reporters.table import TableReporter


class TableCommand:
    """Generate an HTML table with all records in the peak memory usage."""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-o",
            "--output",
            help="Output file name",
            default="pensieve-table.html",
        )
        parser.add_argument("results", help="Results of the tracker run")

    def run(self, args: argparse.Namespace) -> int:
        if not Path(args.results).exists():
            print(f"No such file: {args.results}", file=sys.stderr)
            return 1
        tracker = Tracker(args.results)

        snapshot = tracker.get_high_watermark_allocation_records()
        reporter = TableReporter.from_snapshot(snapshot)

        with open(args.output, "w") as f:
            reporter.render(f)

        print(f"Wrote {args.output}")
        return 0