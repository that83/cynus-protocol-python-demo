# -*- coding: utf-8 -*-
"""Gửi một lệnh tới robot cờ CYNUS: bật lật bàn (robot chơi quân trắng)."""
import asyncio
from bleak import BleakClient, BleakScanner

PAR_NOTIFICATION_CHARACTERISTIC = "FFF1"
FLIP_ON_CMD = b"set flip board on\r\n"


async def main():
    print("Đang quét thiết bị CYNUS-...")
    devices = await BleakScanner.discover()
    matches = [d for d in devices if d.name and str(d.name).startswith("CYNUS-")]

    if not matches:
        print("Không tìm thấy thiết bị CYNUS-.")
        return

    if len(matches) == 1:
        addr = matches[0].address
        print("Kết nối:", matches[0])
    else:
        for i, d in enumerate(matches):
            print(i, ":", d)
        choice = int(input("Chọn số thiết bị: "))
        addr = matches[choice].address

    device = await BleakScanner.find_device_by_address(
        addr, cb=dict(use_bdaddr=False)
    )
    if device is None:
        print("Không tìm thấy địa chỉ:", addr)
        return

    async with BleakClient(device) as client:
        print("Đã kết nối. Gửi: set flip board on")
        await client.write_gatt_char(PAR_NOTIFICATION_CHARACTERISTIC, FLIP_ON_CMD)
        print("Xong.")

    print("Đã ngắt kết nối.")


if __name__ == "__main__":
    asyncio.run(main())
