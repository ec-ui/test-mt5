# test-mt5

Python utility for plotting MT5 tick data (`<DATE> <TIME> <BID> <ASK> ...`) as an interactive ASK/BID chart.

## Requirements

- Python 3.9+

## Usage

```bash
python plot_ticks.py --input EURUSD_202601020000_202601291513.csv --output eurusd_ticks.html
```

Optional arguments:

- `--max-points 200000` to downsample very large files.
- `--plotly-cdn https://cdn.plot.ly/plotly-2.35.2.min.js` to override Plotly JS source.

After generation, open the HTML file in a browser:

- Zoom in/out with mouse wheel and toolbar.
- Pan using the pan tool.
- Toggle ASK/BID visibility by clicking legend items.

Note: generated HTML uses Plotly from CDN, so internet access is needed when opening the chart unless you point `--plotly-cdn` to a local Plotly file.
