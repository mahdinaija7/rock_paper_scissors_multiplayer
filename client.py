import asyncio


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '', 8888)

    print(f'Send: {"START"!r}')
    writer.write("START".encode())
    await writer.drain()

    data = await reader.read(100)

    assert data == b"OK"

    print(f'Received: {data.decode()!r}')
    while True:
        player1 = input("1>").upper()
        writer.write("OK".encode())
        await writer.drain()
        data = await reader.read(100)
        assert data == b"OK"
        print(f'Received: {data.decode()!r}')
        print('Close the connection')
        writer.write(player1.encode())
        await writer.drain()
        data = await reader.read(100)
        player2 = data.decode()
        print(player2)
        allowed = {"R": "Rock", "P": "Paper", "S": "Scissor"}

        if player1 == player2:
            print(f"You both picked {allowed.get(player1)}. It's a draw")
        elif (player1 == "R" and player2 == "S") or (player1 == "P" and player2 == "R") or (
                player1 == "S" and player2 == "P"):
            print( f"Yayy! You picked {allowed.get(player1)} and the computer picked {allowed.get(player2)} so you won!")
        else:
            print(f"Aww Sad! You picked {allowed.get(player1)} and the computer picked {allowed.get(player2)} so you lost!")

        con=input("want to continue ")
        if con.upper() not in ("Y","YES"):
            break



asyncio.run(tcp_echo_client('START'))
