import asyncio

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for boil in range(1,5):
        await asyncio.sleep(10/power)
        print(f'Силач {name} поднял : {boil}')
    print(f'Силач {name} закончил соревнование.')

async def start_tournament():
    strongman1 = asyncio.create_task(start_strongman('Pasha', 3))
    strongman2 = asyncio.create_task(start_strongman('Denis', 4))
    strongman3 = asyncio.create_task(start_strongman('Apollon', 5))
    await strongman1
    await strongman2
    await strongman3


asyncio.run(start_tournament())