import asyncio

allowed = {"R": "Rock", "P": "Paper", "S": "Scissor"}


async def handle_echo(reader, writer):
    data = await reader.read(5)
    if data != b"START":
        writer.write(b"WRONG!")
        await writer.drain()
        writer.close()
        return

    writer.write(b"OK")
    await writer.drain()
    while True:
        answer = input("Rock paper or scissor : ").upper()
        writer.write(b"OK")
        await writer.drain()
        data = await reader.read(2)
        print(data)
        assert data == b"OK"
        writer.write(answer.encode())
        await writer.drain()
        player_answer = await reader.read(1)
        player_answer = player_answer.decode("utf-8").upper()
        if answer == player_answer:
            print(f"You both picked {allowed.get(answer)}. It's a draw")
        elif (answer == "R" and player_answer == "S") or (answer == "P" and player_answer == "R") or (
                answer == "S" and player_answer == "P"):
            print(
                f"Yayy! You picked {allowed.get(answer)} and the other player picked {allowed.get(player_answer)} so you won!")
        else:
            print(
                f"Aww Sad! You picked {allowed.get(answer)} and the other player  picked {allowed.get(player_answer)} so you lost!")

        game = input("Do you want to continue (Y/N) : ")
        if game == "Y":
            continue
        else:
            writer.close()
            await writer.wait_closed()
            break


async def main():
    server = await asyncio.start_server(
        handle_echo, '', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())