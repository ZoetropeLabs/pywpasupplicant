from pywpasupplicant.wpa_ctrl import DirectWPAInterface


def test_interface():
    iface = DirectWPAInterface("/var/run/wpa_supplicant/wlx98ded014d040")

    iface.ctrl_request("SCAN")
