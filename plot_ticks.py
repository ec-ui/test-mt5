#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
import sys
import time
from typing import List, Sequence, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read MT5 tick CSV/TSV and build interactive ASK/BID chart."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input tick file (MT5 export format).",
    )
    parser.add_argument(
        "--output",
        default="ticks_chart.html",
        help="Path to output HTML chart (default: ticks_chart.html).",
    )
    parser.add_argument(
        "--max-points",
        type=int,
        default=0,
        help="Optional max points per series (0 = no downsampling).",
    )
    parser.add_argument(
        "--plotly-cdn",
        default="https://cdn.plot.ly/plotly-2.35.2.min.js",
        help="Plotly JS URL used by generated HTML.",
    )
    return parser.parse_args()


def detect_delimiter(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as f:
        first_line = f.readline()
    return "\t" if "\t" in first_line else ","


def parse_timestamp(date_str: str, time_str: str) -> datetime:
    value = f"{date_str} {time_str}"
    try:
        return datetime.strptime(value, "%Y.%m.%d %H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(value, "%Y.%m.%d %H:%M:%S")


def parse_ticks(
    path: Path,
) -> Tuple[List[datetime], List[float], List[datetime], List[float], int]:
    delimiter = detect_delimiter(path)
    total_bytes = max(path.stat().st_size, 1)

    bid_ts: List[datetime] = []
    bid_vals: List[float] = []
    ask_ts: List[datetime] = []
    ask_vals: List[float] = []
    rows = 0
    last_percent = -1
    last_update = 0.0

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            rows += 1
            if rows % 5000 == 0:
                progress = min(f.buffer.tell() / total_bytes, 1.0)
                percent = int(progress * 100)
                now = time.monotonic()
                if percent != last_percent and (now - last_update >= 0.25):
                    print(f"\rParsing ticks: {percent:3d}% ({rows:,} rows)", end="")
                    sys.stdout.flush()
                    last_percent = percent
                    last_update = now

            date_value = (row.get("<DATE>") or "").strip()
            time_value = (row.get("<TIME>") or "").strip()
            if not date_value or not time_value:
                continue

            ts = parse_timestamp(date_value, time_value)

            bid_raw = (row.get("<BID>") or "").strip()
            if bid_raw:
                bid_ts.append(ts)
                bid_vals.append(float(bid_raw))

            ask_raw = (row.get("<ASK>") or "").strip()
            if ask_raw:
                ask_ts.append(ts)
                ask_vals.append(float(ask_raw))

    print(f"\rParsing ticks: 100% ({rows:,} rows)")

    return bid_ts, bid_vals, ask_ts, ask_vals, rows


def downsample(
    ts: Sequence[datetime], vals: Sequence[float], max_points: int
) -> Tuple[List[datetime], List[float]]:
    if max_points <= 0 or len(ts) <= max_points:
        return list(ts), list(vals)

    step = max(1, len(ts) // max_points)
    sampled_ts = list(ts[::step])
    sampled_vals = list(vals[::step])

    if sampled_ts and sampled_ts[-1] != ts[-1]:
        sampled_ts.append(ts[-1])
        sampled_vals.append(vals[-1])

    return sampled_ts, sampled_vals


def build_chart(
    bid_ts: Sequence[datetime],
    bid_vals: Sequence[float],
    ask_ts: Sequence[datetime],
    ask_vals: Sequence[float],
    output: Path,
    plotly_cdn: str,
) -> None:
    bid_x = [dt.isoformat(sep=" ") for dt in bid_ts]
    ask_x = [dt.isoformat(sep=" ") for dt in ask_ts]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Tick Prices (BID / ASK)</title>
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
    const bidTrace = {{
      x: {json.dumps(bid_x)},
      y: {json.dumps(list(bid_vals))},
      type: "scattergl",
      mode: "lines",
      name: "BID",
      line: {{ color: "#0b7285", width: 1.2 }}
    }};
    const askTrace = {{
      x: {json.dumps(ask_x)},
      y: {json.dumps(list(ask_vals))},
      type: "scattergl",
      mode: "lines",
      name: "ASK",
      line: {{ color: "#d9480f", width: 1.2 }}
    }};
    const layout = {{
      title: "Tick Prices (BID / ASK)",
      xaxis: {{ title: "Time", rangeslider: {{ visible: true }} }},
      yaxis: {{ title: "Price" }},
      hovermode: "x unified",
      legend: {{ orientation: "h", yanchor: "bottom", y: 1.02, x: 0 }}
    }};
    const config = {{
      responsive: true,
      displaylogo: false,
      modeBarButtonsToRemove: ["select2d", "lasso2d"]
    }};
    Plotly.newPlot("chart", [bidTrace, askTrace], layout, config);
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

    bid_ts, bid_vals, ask_ts, ask_vals, row_count = parse_ticks(input_path)

    bid_ts, bid_vals = downsample(bid_ts, bid_vals, args.max_points)
    ask_ts, ask_vals = downsample(ask_ts, ask_vals, args.max_points)

    if not bid_ts and not ask_ts:
        raise SystemExit("No BID/ASK values were found in the input file.")

    build_chart(
        bid_ts=bid_ts,
        bid_vals=bid_vals,
        ask_ts=ask_ts,
        ask_vals=ask_vals,
        output=output_path,
        plotly_cdn=args.plotly_cdn,
    )

    print(f"Parsed rows: {row_count}")
    print(f"BID points: {len(bid_ts)}")
    print(f"ASK points: {len(ask_ts)}")
    print(f"Saved chart: {output_path}")


if __name__ == "__main__":
    main()
