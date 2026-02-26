#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
from typing import List, Tuple


DEFAULT_INPUT = "contractresults-GAZPF-25022025-25022026.csv"
DEFAULT_OUTPUT = "gazpf_funding_yield.html"
DEFAULT_PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.35.2.min.js"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read GAZPF contract results CSV and plot annualized funding yield."
        )
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help=f"Path to input CSV (default: {DEFAULT_INPUT}).",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Path to output HTML chart (default: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--plotly-cdn",
        default=DEFAULT_PLOTLY_CDN,
        help="Plotly JS URL used by generated HTML.",
    )
    return parser.parse_args()


def parse_decimal(value: str) -> float:
    return float(value.replace(" ", "").replace(",", "."))


def find_header(path: Path) -> Tuple[List[str], int]:
    with path.open("r", encoding="utf-8", newline="") as f:
        for idx, line in enumerate(f):
            stripped = line.strip()
            if not stripped:
                continue
            parts = [p.strip() for p in stripped.split(";")]
            if "TRADEDATE" in parts and "CLOSE" in parts and "SWAPRATE" in parts:
                return parts, idx
    raise ValueError("Header row with TRADEDATE/CLOSE/SWAPRATE not found")


def read_yield_series(path: Path) -> Tuple[List[datetime], List[float]]:
    header, header_idx = find_header(path)
    dates: List[datetime] = []
    yields: List[float] = []

    with path.open("r", encoding="utf-8", newline="") as f:
        for _ in range(header_idx + 1):
            next(f, None)
        reader = csv.DictReader(f, fieldnames=header, delimiter=";")
        for row in reader:
            date_raw = (row.get("TRADEDATE") or "").strip()
            close_raw = (row.get("CLOSE") or "").strip()
            swap_raw = (row.get("SWAPRATE") or "").strip()

            if not date_raw or not close_raw:
                continue

            try:
                trade_date = datetime.strptime(date_raw, "%d.%m.%Y")
            except ValueError:
                continue

            if trade_date.weekday() >= 5:
                annualized = 0.0
            else:
                if not swap_raw:
                    continue
                try:
                    close = parse_decimal(close_raw)
                    swaprate = parse_decimal(swap_raw)
                except ValueError:
                    continue
                if close == 0:
                    continue
                annualized = (swaprate / close) * 365.0 * 100.0

            dates.append(trade_date)
            yields.append(annualized)

    return dates, yields


def build_chart(dates: List[datetime], yields: List[float], output: Path, plotly_cdn: str) -> None:
    x_vals = [dt.date().isoformat() for dt in dates]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GAZPF Funding Yield</title>
  <script src="{plotly_cdn}"></script>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f8f9fa; }}
    .wrap {{ padding: 12px; }}
    #chart {{ width: 100%; height: 86vh; border: 1px solid #dee2e6; background: #fff; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div id="chart"></div>
  </div>
  <script>
    const trace = {{
      x: {json.dumps(x_vals)},
      y: {json.dumps(yields)},
      type: "scattergl",
      mode: "lines",
      name: "Funding yield",
      line: {{ color: "#1c7ed6", width: 1.6 }}
    }};
    const layout = {{
      title: "GAZPF Annualized Funding Yield",
      xaxis: {{ title: "Date", rangeslider: {{ visible: true }} }},
      yaxis: {{ title: "Annualized funding yield, %" }},
      hovermode: "x unified",
      legend: {{ orientation: "h", yanchor: "bottom", y: 1.02, x: 0 }}
    }};
    const config = {{
      responsive: true,
      displaylogo: false,
      modeBarButtonsToRemove: ["select2d", "lasso2d"]
    }};
    Plotly.newPlot("chart", [trace], layout, config);
  </script>
</body>
</html>
"""
    output.write_text(html, encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    dates, yields = read_yield_series(input_path)
    if not dates:
        raise SystemExit("No valid rows were found in the input file.")

    build_chart(dates, yields, output_path, args.plotly_cdn)

    print(f"Rows plotted: {len(dates)}")
    print(f"Saved chart: {output_path}")


if __name__ == "__main__":
    main()
