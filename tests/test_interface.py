from pywpasupplicant.wpa_ctrl import WPAInterface


def test_interface():
    iface = WPAInterface()

    iface.request("SCAN")
