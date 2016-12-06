from passlib.utils.pbkdf2 import pbkdf2

from pywpasupplicant.wpa_ctrl import DirectWPAInterface
import re
import logging

logger = logging.getLogger(__name__)


## while scanning
# Selected interface 'wlan0'
# wpa_state=SCANNING
# address=44:39:c4:9c:5d:18
# uuid=48d80c13-db56-5c6c-9ff9-08c7c93fc3fe

## while connected
# bssid=04:bf:6d:8d:3c:29
# freq=2412
# ssid=Zoetrope Labs
# id=0
# mode=station
# pairwise_cipher=CCMP
# group_cipher=CCMP
# key_mgmt=WPA2-PSK
# wpa_state=COMPLETED
# ip_address=192.168.1.240
# address=44:39:c4:9e:ff:ce
# uuid=673c07fe-b909-5ce4-ac32-35fa5fe9d68c

STATE_REGEX = re.compile(r"\s*wpa_state=(?P<state>\w+)")

CONNECTED_REGEXES = {
    "frequency": re.compile(r"""freq=(?P<frequency>[0-9]+)"""),             # match frequency
    "name": re.compile(r"""\bssid=(?P<name>[\w\- ]+)"""),                   # ssid name
    "state": re.compile(r"""wpa_state=(?P<state>\w+)"""),                   # actual state
    "ip_address": re.compile(r"""ip_address=(?P<ip_address>[0-9\.]+)"""),   # ip address
    "mac": re.compile(r"""address=(?P<mac>(\w{2}:){5}\w{2})"""),            # mac
    "key_mgmt": re.compile(r"""key_mgmt=(?P<key_mgmt>[\w\-]+)"""),          # key mgmt type
}

# Selected interface 'wlan0'
# bssid / frequency / signal level / flags / ssid
# b8:27:eb:b5:3e:a3       2437    -63     [WPA2-PSK-CCMP][ESS] Ambie-Bridge-6-16
# 04:bf:6d:8d:3c:29       2412    -79     [WPA2-PSK-CCMP][WPS][ESS] Zoetrope Labs
SCAN_RESULTS_REGEX = re.compile(r"""
    (?P<ssid>                           # whole ssid group
        (?P<mac>(\w{2}:){5}\w{2})\s+    # match mac address
        (?P<frequency>[0-9]+)\s+        # match frequency
        (?P<signal>-[0-9]+)\s+          # signal level
        (?P<flags>(\[[^\]]+\])+)\s+     # flags
        (?P<name>[\w\- ]+)              # ssid name
    )""", re.VERBOSE)


class WPAInterface(DirectWPAInterface):
    def scan(self):
        self.ctrl_request("SCAN")

    def scan_results(self):
        try:
            results = self.ctrl_request("SCAN_RESULTS")
        except RuntimeError:
            logger.exception("Error calling wpa_cli scan_results")

            return {}

        matches = self.SCAN_RESULTS_REGEX.finditer(results)

        match_keys = [
            "frequency",
            "signal",
            "flags",
            "mac",
        ]

        unwound = {
            i.group("name"): {
                j: i.group(j) for j in match_keys
            } for i in matches
        }

        logger.debug("Scan results: %s", unwound)

        return unwound

    def set_network(self, ssid, psk):
        # As in wpa passphrase 2.5
        hashed_psk_bytes = pbkdf2(psk, ssid, 4096, 32)
        # Get into the correct format
        hashed_psk = hashed_psk_bytes.encode("hex")

        self.ctrl_request("SET_NETWORK 0 ssid {}".format(ssid))
        self.ctrl_request("SET_NETWORK 0 psk {}".format(hashed_psk))

        self.ctrl_request("ENABLE_NETWORK 0")
        self.ctrl_request("SAVE")
        self.ctrl_request("RECONFIGURE")

    def get_network_info(self):
        result = self.ctrl_request("STATUS")

        matches = self.STATE_REGEX.search(result)

        if matches.group("state") == "COMPLETED":
            logger.debug("Connected to wifi")

            unwound = {}

            for i in self.CONNECTED_REGEXES:
                match = self.CONNECTED_REGEXES[i].search(result)

                if match:
                    unwound[i] = match.group(i)
                else:
                    unwound[i] = "unknown"
        else:
            logger.debug("Not connected to wifi")

            unwound = {
                "state": matches.group("state"),
            }

        return unwound

    def forget_network(self):
        self.ctrl_request("SET_NETWORK 0 ssid Tk9UIEEgUkVBTCBTU0lE")
        self.ctrl_request("SET_NETWORK 0 psk Tk9UIEEgUkVBTCBTU0lE")

        self.ctrl_request("SAVE")

    def disable_network(self):
        self.ctrl_request("DISABLE_NETWORK 0")

        self.ctrl_request("SAVE")
