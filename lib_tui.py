#!/usr/bin/env python3
import sys
import logging
from logger import CustomFormatter
import dex_lightning as dex

# create logger with 'lightning_app'
logger = logging.getLogger("lib_tui")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)


def color_input(msg):
  return input(colorize(msg, "orange"))


def colorize(string, color):
    colors = {
        'black':'\033[30m',
        'error':'\033[31m',
        'red':'\033[31m',
        'green':'\033[32m',
        'orange':'\033[33m',
        'blue':'\033[34m',
        'purple':'\033[35m',
        'cyan':'\033[36m',
        'lightgrey':'\033[37m',
        'table':'\033[37m',
        'darkgrey':'\033[90m',
        'lightred':'\033[91m',
        'lightgreen':'\033[92m',
        'yellow':'\033[93m',
        'lightblue':'\033[94m',
        'status':'\033[94m',
        'pink':'\033[95m',
        'lightcyan':'\033[96m',
    }
    if color not in colors:
        return str(string)
    else:
        return colors[color] + str(string) + '\033[0m'


class LightningTUI():
    def __init__(self, coin: str=None, node: dex.LightningNode=None):
        self.menu_items = [
            {"Initialize Lightning": self.start_lightning},
            {"Connect to Lightning Node": self.connect_to_node},
            {"Add Trusted Node": self.add_trusted_node},
            {"Remove Trusted Node": self.remove_trusted_node},
            {"List Trusted Nodes": self.list_trusted_nodes},
            {"Open Channel": self.open_channel},
            {"Update Channel": self.update_channel},
            {"List Open Channels": self.list_open_channels},
            {"List Closed Channels": self.list_closed_channels},
            {"Generate Invoice": self.generate_invoice},
            {"Pay Invoice": self.pay_invoice},
            {"Pay Keysend": self.pay_keysend},
            {"List Payments": self.list_payments},
            {"View Payment Details": self.get_payment_details},
            {"Get Claimable Balances": self.get_claimable_balances},
            {"View Lightning Explorers": self.get_lightning_explorers},
            {"Grab a coffee from StarBlocks": self.get_coffee},
            {"Help!": self.get_help},
            {"Exit TUI": self.exit_tui}
        ]
        self.coin = coin
        self.port = None
        self.name = None
        self.color = None
        self.node = node
        self.status = self.get_status()

    def start_lightning(self):
        
        if self.status['lightning_status'] == "Initialized":
            return
        self.coin = color_input(" Select coin to initialize lightning [tBTC, BTC, LTC]: ") or "tBTC"
        while self.coin not in ["tBTC", "BTC", "LTC"]:
            logging.warning("Invalid coin selection. Please try again.")
            self.coin = color_input(" Select coin to initialize lightning [tBTC, BTC, LTC]: ") or "tBTC"
        self.port = color_input(" Select lightning port [9735]: ") or "9735"
        self.name = color_input(" Select lightning node name: ") or "dragonhound-lightning"
        self.color = color_input(" Select lightning node color (in hex): ") or "000000"
        self.node = dex.LightningNode(
            coin=self.coin,
            port=self.port,
            name=self.name,
            color=self.color
        )
        self.status = self.get_status()
        return self.node
    
    def get_coffee(self):
        print(colorize(f"{' '*6}Once you have:", "cyan"))
        print(colorize(f"{' '*8}- initialised your node", "cyan"))
        print(colorize(f"{' '*8}- connected to a well known node (check the lightning explorers)", "cyan"))
        print(colorize(f"{' '*8}- opened a channel from node", "cyan"))
        print(colorize(f"\n{' '*6}You can get an invoice for a coffee from https://starblocks.acinq.co!", "blue"))
        print(colorize(f"\n{' '*8}Then you can get pay the `Pay Invoice`, `View Payment Details` or `List Payments`", "cyan"))

    def get_help(self):
        print(colorize(f"{' '*6}Get more information about the AtomicDEX API Lightning features at:", "green"))
        print(colorize(f"{' '*6}https://github.com/KomodoPlatform/komodo-docs-mdx/pull/31/files", "green"))

    def get_lightning_explorers(self):
        print(colorize(f"{' '*6}=== Lightining Explorers ===", "cyan"))
        print(colorize(f"{' '*6}https://1ml.com/", "green"))
        print(colorize(f"{' '*6}https://mempool.space/lightning", "green"))
        print(colorize(f"{' '*6}https://explorer.acinq.co/", "green"))


    def get_coin_balance(self):
        return self.node.get_coin_balance()
    
    def get_lightning_balance(self):
        return self.node.get_lightning_balance()

    def get_pubkey(self):
        return self.node.get_pubkey()
    
    def get_status(self):
        if self.node is None:
            return {"lightning_status": "Not Initialized"}
        if self.node.coin_pubkey is None:
            self.get_pubkey()
        self.get_coin_balance()
        self.get_lightning_balance()

        self.status = {
            "coin": self.node.coin,
            "platform_coin": self.node.platform_coin,
            "coin_address": self.node.coin_address,
            "coin_balance": self.node.coin_balance,
            "coin_pubkey": self.node.coin_pubkey,
            "lightning_address": self.node.lightning_address,
            "lightning_balance": self.node.lightning_balance,
            "lightning_port": self.node.port,
            "lightning_name": self.node.name,
            "lightning_color": self.node.color,
            "lightning_status": "Initialized"
        }
        return self.status

    def connect_to_node(self):
        if self.node is None:
            logger.warning(" Lightning not initialized. Please initialize lightning first.")
            return
        node_address = color_input(" Enter lightning node address to connect to: ") or "038863cf8ab91046230f561cd5b386cbff8309fa02e3f0c3ed161a3aeb64a643b9@203.132.94.196:9735"
        self.node.connect_to_node(node_address)
        self.status = self.get_status()
    
    def open_channel(self):
        if self.node is None:
            logger.warning(" Lightning not initialized. Please initialize lightning first.")
            return
        node_address = color_input(" Enter lightning node address to connect to: ") or "038863cf8ab91046230f561cd5b386cbff8309fa02e3f0c3ed161a3aeb64a643b9@203.132.94.196:9735"
        self.node.open_channel(node_address)
        
    def update_channel(self):
        if self.node is None:
            logger.warning(" Lightning not initialized. Please initialize lightning first.")
            return
        uuid = color_input(" Enter channel uuid: ")
        proportional_fee_in_millionths_sats = color_input(" Enter proportional_fee_in_millionths_sats: ")
        base_fee_msat = color_input(" Enter base_fee_msat: ")
        cltv_expiry_delta = color_input(" Enter cltv_expiry_delta: ")
        max_dust_htlc_exposure_msat = color_input(" Enter max_dust_htlc_exposure_msat: ")
        force_close_avoidance_max_fee_sats = color_input(" Enter force_close_avoidance_max_fee_sats: ")
        self.node.update_channel(
            uuid=uuid,
            proportional_fee_in_millionths_sats=proportional_fee_in_millionths_sats,
            base_fee_msat=base_fee_msat,
            cltv_expiry_delta=cltv_expiry_delta,
            max_dust_htlc_exposure_msat=max_dust_htlc_exposure_msat,
            force_close_avoidance_max_fee_sats=force_close_avoidance_max_fee_sats
        )
    
    def generate_invoice(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        description = color_input(" Enter description: ")
        amount_in_msat = None
        while amount_in_msat is None:
            try:
                amount_in_msat = int(color_input(" Enter amount_in_msat: "))
            except:
                logger.warning("Invalid amount_in_msat (must be an integer). Please try again.")

        expiry = None
        while expiry is None:
            try:
                expiry = int(color_input(" Enter expiry: "))
            except:
                logger.warning("Invalid expiry (must be an integer). Please try again.")

        self.node.generate_invoice(
            description=description,
            amount_in_msat=amount_in_msat,
            expiry=expiry
        )
    
    def pay_invoice(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        invoice = color_input(" Enter invoice: ")
        self.node.send_payment(invoice=invoice)
    
    def pay_keysend(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        
        pubkey = color_input(" Enter pubkey: ")
        amount_in_msat = None
        while amount_in_msat is None:
            try:
                amount_in_msat = int(color_input(" Enter amount_in_msat: "))
            except:
                logger.warning("Invalid amount_in_msat (must be an integer). Please try again.")

        expiry = None
        while expiry is None:
            try:
                expiry = int(color_input(" Enter expiry: "))
            except:
                logger.warning("Invalid expiry (must be an integer). Please try again.")

        self.node.send_payment(
            amount_in_msat=amount_in_msat,
            pubkey=pubkey,
            expiry=expiry
        )
    
    def list_open_channels(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        self.node.list_open_channels()
    
    def list_closed_channels(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        self.node.list_closed_channels()

    def list_trusted_nodes(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        self.node.list_trusted_nodes()

    def add_trusted_node(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        node_id = color_input(" Enter Node ID: ")
        self.node.add_trusted_node(node_id)
    
    def remove_trusted_node(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        node_id = color_input(" Enter Node ID: ")
        self.node.remove_trusted_node(node_id)
    
    def get_payment_details(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        payment_hash = color_input(" Enter payment_hash: ") or "414f9b3524fc4e48c99f2723952732d8bc2eba1b35ce3bf2a70f5144b40f599e"
        self.node.get_payment_details(payment_hash)
    
    def list_payments(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        self.node.list_payments()
    
    def get_claimable_balances(self):
        if self.node is None:
            print(colorize(" Lightning not initialized. Please initialize lightning first.", "red"))
            return
        include_open_channels_balances  = color_input(" Enter include_open_channels_balances: ") or True
        self.node.get_claimable_balances(include_open_channels_balances)
    
    def exit_tui(self):
        print(colorize(" Exiting TUI", "red"))
        sys.exit()
    

        