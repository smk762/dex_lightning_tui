# dex_lightning_tui
A TUI for using the  Lightning Network with the AtomicDEX API


## Setup
- Run `pip3 install -r requirements.txt` to install python dependencies.
- Run `./configure.py` to setup the AtomicDEX API configuration files (MM2.json).
- Run `./update_API.py` to update the AtomicDEX API to a specific commit/branch. E.g. `./update_API.py -a c755e14  -b dev -c test-lightning` will update the AtomicDEX API to the commit `c755e14` on the `dev` branch using the `test-lightning` branch of the `coins` file.
- Run `./start_mm2.sh` to start the AtomicDEX API.
- Run `./lightning_tui.py` to start the TUI.

- Use `./stop_mm2.sh` to stop the AtomicDEX API.
- Use `tail -f mm2.log` to follow AtomicDEX API logs.

Refer to the docs for more information about the AtomicDEX API Lightning Methods: https://docs.atomicdex.io/atomicdex/atomicdex-api#lightning-methods

## Tips
Use the `View Lightning Explorers` option to find a node to connect or open a channel with.