import asyncio
from bleak import BleakClient

address = "CF:79:AF:79:0B:36"
MODEL_NBR_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"

async def main(address):
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()
        for thing in services:
            print(thing)

            # if (thing):
            #   print(services[thing])
        rw_charac = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
        answer = await client.write_gatt_char(rw_charac, b'import device', response=True)
        answer2 = await client.write_gatt_char(rw_charac, b'print(device.battery_level())', response=True)
        # print(answer)
        # await client.write_gatt_char('', '\x03\x01')
        # await client.write_gatt_char('', 'import device')
        # await client.write_gatt_char('', 'print(device.is_charging())')
        # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        # print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))