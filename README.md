# Pediatric APP Academy

Hub for the Academy's simulators: https://kayleighatodd-88.github.io/pediatric-app-academy/

- `index.html`: the hub page. It is generated, so don't edit it by hand.
- `tools/landing.py`: generates the hub and every lab's `index.html` landing page. To add a new lab, add it to `LABS` there.
- `tools/reskin.py`: adds the Academy theme to each lab (colours, Atkinson Hyperlegible Next, and a header lockup that links back here). Safe to re-run.
- `brand/`: the open-A mark, in light and reversed versions.

Run both from this folder, pointing at the folder that holds the lab repos:

    python3 tools/reskin.py ..
    python3 tools/landing.py ..

Then rebuild the labs that have a build step (`cicu-waveform-lab/build.sh`, `cicu-tpn-lab/build.py`) and commit each repo.
