#!/usr/bin/env python3
import os
import sys
import time
import json
import logging
import requests
from dotenv import load_dotenv
from logger import CustomFormatter

# create logger with 'lightning_app'
logger = logging.getLogger("dex_lightning")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)

load_dotenv()
MM2_USERPASS = os.getenv("MM2_USERPASS")
if not MM2_USERPASS:
    logger.warning("MM2_USERPASS not set! Set it in a .env file in this folder. For more information, refer to https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/")
    MM2_USERPASS = input("Enter your userpass: ")

class LightningNode:
    def __init__(self, coin, dex_url="http://127.0.0.1:7783", name="dragonhound-lightning", port=9735, color="000000", payment_retries=5):
        '''
        Coin should be the base ticker: e.g. tBTC
        We must activate the segwit variant of the coin before we can create
        a lightning node for it.        
        '''
        self.dex_url = dex_url
        self.name = name
        self.port = port
        self.color = color
        self.payment_retries = payment_retries
        self.coin = f"{coin.split('-')[0]}-lightning"
        self.activate_coin(coin)
        self.get_pubkey()
        self.initialize_lightning()

    def dexAPI(self, params):
        params.update({"userpass": MM2_USERPASS})
        logger.debug(f"PARAMS: {params}")
        resp = requests.post(self.dex_url, json.dumps(params)).json()
        if "error" in resp:
            logger.warning(f"ERROR: {resp}")
        else:
            logger.info(f"RESP: {resp}")
        return resp

    def activate_coin(self, coin):
        activation_params = requests.get(f"https://stats.kmd.io/api/atomicdex/activation_commands/?coin={coin}").json()
        if "coin" in activation_params:
            activation_params.update({"coin": f"{coin}-segwit"})
        else:
            logger.critical(f"Coin {coin} not found in UTXO activation params! Exiting...")
            sys.exit(1)
        return self.dexAPI(activation_params)

    def get_pubkey(self):
        params = {
            "mmrpc": "2.0",
            "method": "get_public_key",
            "params": {},
            "id": 762
        }
        return self.dexAPI(params)

    def initialize_lightning(self):
        '''Creates a lightning node for the coin'''
        params = {
            "method": "task::enable_lightning::init",
            "mmrpc": "2.0",
            "params": {
                "ticker": self.coin,
                "activation_params": {
                    "name": self.name,
                    "listening_port": int(self.port),
                    "color": self.color,
                    "payment_retries": self.payment_retries
                }
            },
            "id": 762
        }
        resp = self.dexAPI(params)
        if "error" in resp:
            if resp["error"].find("already activated") == -1:
                print(resp["error"])
                logger.warning(f"Error intializing {self.coin}!")
                exit(1)
            return
        else:
            if "result" not in resp:
                logger.warning(f"No result for {self.coin} !")
                exit(1)
            if "task_id" not in resp["result"]:
                logger.warning(f"No task_id for {self.coin} !")
                exit(1)
        task_id = resp["result"]["task_id"]
        i = 0
        '''Loop status until it's either Ok or Error'''
        while True:
            i += 1
            resp = self.init_lightning_status(task_id)
            if i == 30:
                resp = self.init_lightning_cancel(task_id)
                break
            if "error" in resp:
                break
            if resp["result"]["status"] in ["Ok", "Error"]:
                break
            time.sleep(2)

    def init_lightning_status(self, task_id):
        params = {
            "mmrpc": "2.0",
            "method": "task::enable_lightning::status",
            "params": {
                "task_id": task_id,
                "forget_if_finished": False
            },
            "id": 762
        }
        response = self.dexAPI(params)
        return response

    def init_lightning_cancel(self, task_id):
        params = {
            "mmrpc": "2.0",
            "method": "task::enable_lightning::cancel",
            "params": {
                "task_id": task_id
            },
            "id": 762
        }
        return self.dexAPI(params)

    def connect_to_node(self, node_address):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::nodes::connect_to_node",
            "params": {
                "coin": self.coin,
                "node_address": node_address
            },
            "id": 762
        }
        return self.dexAPI(params)

    def list_trusted_nodes(self):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::nodes::list_trusted_nodes",
            "params": {
                "coin": self.coin
            },
            "id": 762
        }
        return self.dexAPI(params)

    def remove_trusted_node(self, node_id="038863cf8ab91046230f561cd5b386cbff8309fa02e3f0c3ed161a3aeb64a643b9"):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::nodes::remove_trusted_node",
            "params": {
                "coin": self.coin,
                "node_id": node_id
            },
            "id": 762
        }
        return self.dexAPI(params)

    def add_trusted_node(self, node_id="038863cf8ab91046230f561cd5b386cbff8309fa02e3f0c3ed161a3aeb64a643b9"):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::nodes::add_trusted_node",
            "params": {
                "coin": self.coin,
                "node_id": node_id
            },
            "id": 762
        }
        return self.dexAPI(params)

    def open_channel(self, node_address):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::channels::open_channel",
            "params": {
                "coin": self.coin,
                "node_address": node_address,
                "amount": {
                    "type": "Exact",
                    "value": 0.0004
                }
            },
            "id": 762
        }
        return self.dexAPI(params)

    def update_channel(self, uuid, proportional_fee_in_millionths_sats,
                       base_fee_msat, cltv_expiry_delta, max_dust_htlc_exposure_msat,
                       force_close_avoidance_max_fee_sats):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::channels::update_channel",
            "params": {
                "coin": self.coin,
                "uuid": uuid,
                "channel_options": {
                    "proportional_fee_in_millionths_sats": proportional_fee_in_millionths_sats,
                    "base_fee_msat": base_fee_msat,
                    "cltv_expiry_delta": cltv_expiry_delta,
                    "max_dust_htlc_exposure_msat": max_dust_htlc_exposure_msat,
                    "force_close_avoidance_max_fee_sats": force_close_avoidance_max_fee_sats
                }
            },
            "id": 762
        }
        return self.dexAPI(params)

    def list_open_channels(self):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::channels::list_open_channels_by_filter",
            "params": {
                "coin": self.coin
            },
            "id": 762
        }
        return self.dexAPI(params)

    def list_closed_channels(self):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::channels::list_closed_channels_by_filter",
            "params": {
                "coin": self.coin
            },
            "id": 762
        }
        return self.dexAPI(params)

    def generate_invoice(self, description, amount_in_msat=10000, expiry=600):
        params = {
            "method": "lightning::payments::generate_invoice",
            "mmrpc": "2.0",
            "params": {
                "coin": self.coin,
                "description": description,
                "amount_in_msat": amount_in_msat,
                "expiry": expiry
            },
            "id": 762
        }
        return self.dexAPI(params)

    def send_payment(self, invoice=False, amount_in_msat=False, pubkey=False, expiry=24):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::payments::send_payment",
            "params": {
                "coin": self.coin,
            },
            "id": 762
        }
        if invoice is not None:
            params["params"].update({
                "payment": {
                    "type": "invoice",
                    "invoice": invoice
                }             
            })
        elif amount_in_msat and pubkey:
            params["params"].update({
                "payment": {
                    "type": "keysend",
                    "destination": pubkey,
                    "amount_in_msat": amount_in_msat,
                    "expiry": expiry
                }
            })
        return self.dexAPI(params)

    def get_payment_details(self, payment_hash):
        params = {
            "method": "lightning::payments::get_payment_details",
            "mmrpc": "2.0",
            "params": {
                "coin": self.coin,
                "payment_hash": payment_hash
            },
            "id": 762
        }
        return self.dexAPI(params)

    def list_payments(self, page=1, limit=10):
        params = {
            "method": "lightning::payments::list_payments_by_filter",
            "mmrpc": "2.0",
            "params": {
                "coin": self.coin,
                "limit": limit,
                "paging_options": {
                    "PageNumber": page
                }
            },
            "id": 762
        }
        return self.dexAPI(params)

    def list_inbound_payments(self, page=1, limit=10):
        params = {
            "method": "lightning::payments::list_payments_by_filter",
            "mmrpc": "2.0",
            "params": {
                "coin": self.coin,
                "filter": {
                    "payment_type": {
                        "type": "Inbound Payment"
                    },
                },
                "limit": limit,
                "paging_options": {
                    "PageNumber": page
                }
            },
            "id": 762
        }
        return self.dexAPI(params)
    
    def list_outbound_payments(self, page=1, limit=10):
        params = {
            "method": "lightning::payments::list_payments_by_filter",
            "mmrpc": "2.0",
            "params": {
                "coin": self.coin,
                "filter": {
                    "payment_type": {
                        "type": "Outbound Payment"
                    },
                },
                "limit": limit,
                "paging_options": {
                    "PageNumber": page
                }
            },
            "id": 762
        }
        return self.dexAPI(params)

    def get_claimable_balances(self, include_open_channels_balances=True):
        params = {
            "mmrpc": "2.0",
            "method": "lightning::channels::get_claimable_balances",
            "params": {
                "coin": self.coin,
                "include_open_channels_balances": include_open_channels_balances
            },
            "id": 762
        }
        return self.dexAPI(params)

if __name__ == "__main__":
    node = LightningNode("tBTC")