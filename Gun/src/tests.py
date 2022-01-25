
async def test(gun):
    print("Starting testing")

    print("########## Setting team")
    await gun.handleMessage(addr=0, data=1)
    await asyncio.sleep(3)

    print("########## Testing reload without ammo")
    await gun._reload()
    await asyncio.sleep(3)

    print("########## Settting maxAmmo")
    await gun.handleMessage(addr=1, data=10)
    await asyncio.sleep(3)

    print("########## Testing reload with ammo")
    await gun._reload()
    await asyncio.sleep(3)

    print("########## Settting lives")
    await gun.handleMessage(addr=2, data=3)
    await asyncio.sleep(3)

    print("########## Shooting")
    await gun._shoot()
    await asyncio.sleep(3)

    print("########## Getting shot by same team")
    await gun.handleMessage(addr=120, data=1)
    await asyncio.sleep(3)

    print("########## Getting shot by different team")
    await gun.handleMessage(addr=120, data=2)
    await asyncio.sleep(3)

    print("Testing done")