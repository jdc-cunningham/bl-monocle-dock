import asyncio
from bleak import BleakClient

address = ""
MODEL_NBR_UUID = ""

async def main(address):
    async with BleakClient(address) as client:
        print('connected')
        await client.write_gatt_char('', '\x03\x01')
        await client.write_gatt_char('', 'import device')
        await client.write_gatt_char('', 'print(device.is_charging())')
        # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        # print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))