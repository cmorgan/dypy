PRODUCT_ID  = 0xc626
VENDOR_ID   = 0x046d

handle = 0
device = 0

for bus in usb.busses():
    for dev in bus.devices:
        if dev.idVendor == VENDOR_ID and dev.idProduct == PRODUCT_ID:
            print 'found SpaceNavigator'
            device = dev
            break

assert device.idVendor == VENDOR_ID
assert device.idProduct == PRODUCT_ID

config = device.configurations[0]
interface = config.interfaces[0][0]
endpoint = interface.endpoints[0]

handle = device.open()
handle.setConfiguration(config)
handle.claimInterface(interface)
handle.setAltInterface(interface)
handle.reset()

handle.releaseInterface()            