from mcstatus import MinecraftServer

while True:
    try:
        server = MinecraftServer.lookup('52.166.6.60')
        print('Trying...\n')
        status = server.status()
        print(status.latency)
    except Exception as error:
        print('Something went wrong:{0}'.format(error))