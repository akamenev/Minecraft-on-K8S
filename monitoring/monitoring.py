from kubernetes import client, config
from mcstatus import MinecraftServer
import redis
import os
import time

# # loading kube config from .kube dir on the server
config.load_kube_config()
v1=client.CoreV1Api()
ret = v1.list_service_for_all_namespaces(watch=False)

r = redis.StrictRedis(
    host='minecraftmonitor.redis.cache.windows.net', 
    port=6380, 
    db=0,
    password=os.environ.get('REDIS_PASS'),
    ssl=True
    )

while True:
    print("Parsing k8s Services to find Minecraft servers...\n")
    for i in ret.items:
        # checking if the service has an ingress and if the name of the service contains 'minecraft-server' in name
        if i.status.load_balancer.ingress and 'minecraft-server' in i.metadata.name:
            print("[Found] {0} at {1}".format(i.metadata.name, i.status.load_balancer.ingress[0].ip))
            print("Quering {0} ...".format(i.metadata.name))
            # lookin up for a server by its IP
            server = MinecraftServer.lookup(i.status.load_balancer.ingress[0].ip)
            # cheking the server's status
            status = server.status()
            print("{0} has {1} players and latency {2} ms".format(i.metadata.name, status.players.online, status.latency))
            
    
            print("Submiting to Redis...")
            
            r.set(i.metadata.name, (i.status.load_balancer.ingress[0].ip, status.players.online, status.latency))
    
            r.set('{0}.address'.format(i.metadata.name), i.status.load_balancer.ingress[0].ip)
            r.set('{0}.online'.format(i.metadata.name), status.players.online)
            r.set('{0}.latency'.format(i.metadata.name), status.latency)
            print("Done\n----------------------")
    time.sleep(30)
        