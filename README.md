# FR4 from woven glass cloth

A trail for making a glass and epoxy circuit board by hand, and a small
model that predicts what a test panel should measure.

**Nothing here has been made or measured.** The trail collects what
published sources say. The model gives predictions to test.

## Read it

The documentation is a small site with a collapsible sidebar:

```bash
pip install -r requirements-docs.txt
mkdocs serve          # then open http://127.0.0.1:8000
```

Or read the pages as plain markdown in [`docs/`](docs/index.md).

| Group | Start at |
|---|---|
| The trail: cloth, resin, coating, copper, press, measurement | [`docs/trail/decisions.md`](docs/trail/decisions.md) |
| The model, explained one piece at a time | [`docs/model/overview.md`](docs/model/overview.md) |
| Words and reading list | [`docs/reference/glossary.md`](docs/reference/glossary.md) |

## Run the model

```bash
pip install numpy
python -m fr4sim      # prints every prediction
python -m pytest      # 22 checks
```

## The code, in reading order

| File | What it answers |
|---|---|
| [`fr4sim/materials.py`](fr4sim/materials.py) | What numbers does the model assume? |
| [`fr4sim/laminate.py`](fr4sim/laminate.py) | Resin content → thickness and dielectric constant |
| [`fr4sim/microstrip.py`](fr4sim/microstrip.py) | A trace on the board → impedance, delay, ring resonance |
| [`fr4sim/weave.py`](fr4sim/weave.py) | The cloth pattern → skew between two traces |
| [`fr4sim/coupons.py`](fr4sim/coupons.py) | The two test patterns |
| [`fr4sim/press.py`](fr4sim/press.py) | How hard the press must push |
| [`fr4sim/report.py`](fr4sim/report.py) | Prints the predictions |

## What the model found

1. The weave hardly shows on a thick board with a wide trace. It matters on
   one thin ply under a narrow trace.
2. On a hand-coated panel, resin content is the bigger risk. Thickness
   tells you resin content, and resin content sets the dielectric constant.

The model reads about 12% low on the dielectric constant against one
maker's figure. Use it for differences, not absolute values.

## Who wrote it

Claude wrote the site and the model on 16 Nov 2026, at Aldrin's request.
