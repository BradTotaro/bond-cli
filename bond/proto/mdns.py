from zeroconf import ServiceBrowser, Zeroconf
import bond.database


class Listener:
    def __init__(self, on_success):
        self.on_success = on_success

    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        bondid = info.name.split(".")[0]
        ip = ".".join([str(ord(chr(byte))) for byte in info.addresses[0]])
        port = info.port
        bond.database.set_bond(bondid, "ip", ip)
        bond.database.set_bond(bondid, "port", port)
        self.on_success({"bondid": bondid, "ip": ip, "port": port})


class Scanner(object):
    def __init__(self, on_success):
        self.zeroconf = Zeroconf()
        self.listener = Listener(on_success=on_success)
        browser = ServiceBrowser(self.zeroconf, "_bond._tcp.local.", self.listener)

    def __del__(self):
        del self.listener
        self.zeroconf.close()
