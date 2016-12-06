from pywpasupplicant.wpa_ctrl import DirectWPAInterface


def test_interface():
    iface = DirectWPAInterface()

    iface.ctrl_request("SCAN")
