#!/usr/bin/env python3
import sys
import json
import string
import random
import os.path
import mnemonic
from dotenv import load_dotenv
import logging
from logger import CustomFormatter

# create logger with 'lightning_app'
logger = logging.getLogger("configure")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)

load_dotenv()

class MM2Config():
    def __init__(self):
        self.MM2_RPC_PORT = 7783
        self.MM2_RPC_IP = "127.0.0.1"
        self.MM2_RPC_LOCAL_ONLY = True
        self.MM2_I_AM_SEED = False
        self.MM2_GUI = "dragonhound-lightning-tui"
        self.MM2_SEED = None
        self.MM2_SEEDNODES = ["80.82.76.214", "89.248.168.39", "89.248.173.231"]
        self.MM2_USERPASS = None
        self.MM2_NETID = 7777
        self.MM2_METRICS = 300
        self.conf = {}

    def generate_rpc_pass(self, length=16):
        special_chars = ["@", "~", "-", "_", "|", ":", "+"]
        rpc_pass = ""
        quart = int(length/4)
        while len(rpc_pass) < length:
            rpc_pass += ''.join(random.sample(string.ascii_lowercase, random.randint(1,quart)))
            rpc_pass += ''.join(random.sample(string.ascii_uppercase, random.randint(1,quart)))
            rpc_pass += ''.join(random.sample(string.digits, random.randint(1,quart)))
            rpc_pass += ''.join(random.sample(special_chars, random.randint(1,quart)))
        str_list = list(rpc_pass)
        random.shuffle(str_list)
        return ''.join(str_list)

    def generate_seed(self):
        return mnemonic.Mnemonic("english").generate(strength=256)

    def get_conf_from_env(self):
        if os.getenv('MM2_RPC_PORT'):
            self.MM2_RPC_PORT = int(os.getenv('MM2_RPC_PORT'))
        if os.getenv('MM2_RPC_IP'):
            self.MM2_RPC_IP = os.getenv('MM2_RPC_IP')
        if os.getenv('MM2_RPC_LOCAL_ONLY'):
            self.MM2_RPC_LOCAL_ONLY = os.getenv('MM2_RPC_LOCAL_ONLY')
        if os.getenv('MM2_I_AM_SEED'):
            self.MM2_I_AM_SEED = os.getenv('MM2_I_AM_SEED')
        if os.getenv('MM2_GUI'):
            self.MM2_GUI = os.getenv('MM2_GUI')
        if os.getenv('MM2_SEED'):
            self.MM2_SEED = os.getenv('MM2_SEED')
        if os.getenv('MM2_SEEDNODES'):
            self.MM2_SEEDNODES = os.getenv('MM2_SEEDNODES').split(" ")
        if os.getenv('MM2_USERPASS'):
            self.MM2_USERPASS = os.getenv('MM2_USERPASS')
        if os.getenv('MM2_NETID'):  
            self.MM2_NETID = int(os.getenv('MM2_NETID'))
        if os.getenv('MM2_METRICS'):  
            self.MM2_METRICS = int(os.getenv('MM2_METRICS'))

        conf = {
            "gui": self.MM2_GUI,
            "netid": self.MM2_NETID,
            "i_am_seed": self.MM2_I_AM_SEED,
            "rpc_local_only": self.MM2_RPC_LOCAL_ONLY,
            "rpcport": self.MM2_RPC_PORT,
            "rpcip": self.MM2_RPC_IP,
            "rpc_password": self.MM2_USERPASS,
            "passphrase": self.MM2_SEED,
            "seednodes": self.MM2_SEEDNODES,
            "metrics": self.MM2_METRICS
        }
        for i in conf:
            if conf[i]:
                if isinstance(conf[i], str):
                    conf[i] = conf[i].strip()
                    self.conf.update({i: conf[i]})
                elif isinstance(conf[i], int):
                    self.conf.update({i: int(conf[i])})
                elif conf[i] == "True":
                    self.conf.update({i: True})
                elif conf[i] == "False":
                    self.conf.update({i: False})
                elif conf[i] in ["None", "", "null"]:
                    self.conf.update({i: None})
        return conf
    
    def get_MM2_json(self):
        if os.path.exists("MM2.json"):
            update = False
            with open("MM2.json", "r") as f:
                return json.load(f)
        return {}
    
    def update_MM2_config(self):
        mm2_json = self.get_MM2_json()
        env_conf = self.get_conf_from_env()

        if env_conf["passphrase"] is not None and mm2_json["passphrase"] is not None:
            if env_conf["passphrase"] != mm2_json["passphrase"]:
                logger.error("Passphrase in MM2.json and .env are not the same! Please change one of them.")
                logger.error("To avoid overwriting and potential loss of seed, app will now exit.")
                sys.exit(1)
        for i in env_conf:
            if i in mm2_json:
                if mm2_json[i] is not None: self.conf.update({i: mm2_json[i]})
                elif env_conf[i] is not None: self.conf.update({i: env_conf[i]})
            elif env_conf[i] is not None: self.conf.update({i: env_conf[i]})
            else: self.validate_values(i)
        self.write_MM2_config()
        self.write_rpc_file()
        self.write_env_file()

    def validate_values(self, key):
        if key == "rpc_password": val = self.generate_rpc_pass()
        elif key == "passphrase": val = self.generate_seed()
        else: val = input(f"Please enter a value for {key}: ")
        if isinstance(val, int):
            val = int(val)
        if isinstance(val, str):
            val = val.strip()
        self.conf.update({key: val})

    def write_MM2_config(self):
        with open("MM2.json", "w+") as f:
            json.dump(self.conf, f, indent=4)
        logger.info("MM2.json file created.")

    def write_rpc_file(self):
        with open("rpc", "w+") as f:
            userpass = self.conf['rpc_password']
            rpc_ip = self.conf['rpcip']
            port = self.conf['rpcport']
            f.write(f'userpass="{userpass}"\n')
            f.write(f'rpcip="{rpc_ip}"\n')
            f.write(f'rpcport={port}\n')
        logger.info("rpc file created.")

    def write_env_file(self):
        with open(".env", "a+") as f:
            userpass = self.conf['rpc_password']
            f.write(f'MM2_USERPASS="{userpass}"\n')
        logger.info(".env file created.")

if __name__ == "__main__":
    MM2Config().update_MM2_config()