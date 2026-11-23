# The World in One Day — Monday 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/iAm-182/news-image-20261123-entry/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/iAm-182/news-image-20261123-entry/reward.svg)](https://make.fun/bounty/news-image-20261123)

Entry for the [news-image-20261123](https://make.fun/bounty/news-image-20261123)
competition on [make.fun](https://make.fun): one 1024×1024 front page that sums
up the world's news of Monday 23 November 2026.

The page carries 68 stories — 7 features and 61 briefs — every one of them
an event that happened, or was first reported, on Monday 23 November 2026.
The lead is the sixth tanker struck in the Strait of Hormuz that morning;
the page also covers the COP31 collapse, Nvidia reinstating Jensen Huang
and Wall Street's sharp rebound (S&P +5%, Nasdaq +6.9%), the Russian
warship Merkury sunk off Benghazi, the Dymer strike near Kyiv (toll 11),
the Wellington Test draw, the full NFL Week 11 results, Liverpool's 4–0
win over Manchester United, and the day's markets (gold ~$3,666/oz,
Bitcoin ~$63,400). A DATE CHECK bar states the date rule the whole page
is built to.

## How it works

- `draw.py` renders `entry.png` with Pillow (local build step only).
  It is deterministic: no timestamps, no randomness, no network — two
  renders produce byte-identical output.
- `main.py` is the graded program. It uses only the Python standard
  library and copies the pre-rendered `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). It never
  re-renders, because the grading sandbox has no Pillow and no fonts.

## Verify locally

```sh
python3 draw.py            # renders entry.png (1024x1024, under 1 MiB)
python3 draw.py            # render again; sha256 must match the first run
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

## Licence

MIT — see [LICENSE](LICENSE).
