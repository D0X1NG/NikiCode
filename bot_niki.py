from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import os
import sys
from discord import Game
import socket
import subprocess
import nmap
from mcstatus import MinecraftServer
from quarry.net.auth import OfflineProfile
from twisted.internet import defer, reactor
from quarry.net.client import ClientFactory, SpawningClientProtocol
import random
import requests


print("")
print("---------------")
print("Starting bot...")
print("---------------")
print("")

os.system("cls")
print("")
print("---------------")
print("Connecting...")
print("---------------")
print("")

subdomains = ["www", "build", "web", "dev", "staff", "mc", "play", "sys", "node1", "node2", "node3", "builder", "developer", "test", "test1", "forum", "bans", "baneos", "ts", "ts3", "sys1", "sys2", "mods", "bungee", "bungeecord", "array", "spawn", "server", "help", "client", "api", "smtp", "s1", "s2", "s3", "s4", "server1", "server2", "jugar", "login", "mysql", "phpmyadmin", "demo", "na", "eu", "us", "es", "fr", "it", "ru", "support", "developing", "discord", "backup", "buy", "buycraft", "go", "dedicado1", "dedi", "dedi1", "dedi2", "dedi3", "minecraft", "prueba", "pruebas", "ping", "register", "cdn", "stats", "store", "serie", "buildteam", "info", "host", "jogar", "proxy", "vps", "ovh", "partner", "partners", "appeals", "appeal", "store-assets"]

#TOKEN
f = open("token.txt", "r")
TOKEN = f.readlines()[0].replace("\n", "")
f.close()

client = discord.Client()
b = Bot(command_prefix = "ayy")

class BotClientProtocol(SpawningClientProtocol):
    pass

class BotClientFactory(ClientFactory):
    protocol = BotClientProtocol


def check(url):
    try:
        request = requests.get(url) #Here is where im getting the error
        if request.status_code == 200:
            return True
    except:
        return False

@b.event
async def on_ready():
    os.system("cls")
    print("Connected!")

@b.event
async def on_message(message):
    msg = message.content
    print(str(message.guild) + " : " + str(message.channel))

    if (msg.split()[0] == "-subscan"):
        domain = msg.split()[1]
        await message.channel.send("> --- Subdomains of " + domain + " ---")
        for subdomain in subdomains:
            try:
                fullsub = str(subdomain)+"."+str(domain)
                ipofsub = socket.gethostbyname(str(fullsub))

                await message.channel.send("> " + fullsub + " - " + ipofsub)
            except:
                pass
    
    if (msg.split()[0] == "-dedscan"):
        domain = msg.split()[1]
        await message.channel.send("> --- Dedicated servers of " + domain + " ---")

        ip_list = []
        ais = socket.getaddrinfo(domain,0,0,0,0)
        for result in ais:
            ip_list.append(result[-1][0])
            ip_list = list(set(ip_list))

        for x in range(len(ip_list)):
            await message.channel.send("> " + ip_list[x])
    
    if (msg.split()[0] == "-help"):
        await message.channel.send("```css\n--- [Comandos ToxicBot] ---\n--- By [Niki#8160] ---\n \nPrefix: -\n \n-subscan [dominio]: Escanea subdominios de ese dominio\n-dedscan [dominio]: Muestra los servidores dedicados de ese dominio\n-sqliscan [url]: Escanea la url para encontrar vulnerabilidades sql injection```")

    if (msg.split()[0] == "-sqliscan"):
        url = msg.split()[1]
        if (url[len(url) - 1]) != "/":
            url += "/"

        await message.channel.send("> --- Vulnerable pages of " + url + " ---")
        
        f = open("keywords.txt", "r")
        keywords = f.readlines()
        f.close()

        working = []

        for x in range(len(keywords)):
            keywords[x].replace("\n", "")

        for x in range(len(keywords)):
            keyword = keywords[x].replace("\n", "")
            keywordurl = url + keyword + ".php?id=" + str(random.randint(1, 100))
            if (check(keywordurl)):
                working.append(keywordurl)
                print("Working: " + keywordurl)
                await message.channel.send("> Found: " + keywordurl)
            else:
                print("Not working: " + keywordurl)
        
        if (len(working) == 0):
            await message.channel.send("> No vulnerable pages were found!")

    if (msg.split()[0] == "-ipinfo"):
        ip = msg.split()[1]

        await message.channel.send("> --- Info of " + ip + " ---")

        proc = subprocess.Popen(["curl", "ipinfo.io/" + ip], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        out = out.decode().replace("\n", "").replace("{", "").replace("}","").replace('"', "")

        if ("Wrong ip" in out):
            proc2 = subprocess.Popen(["curl", "ipinfo.io/" + socket.gethostbyname(ip)], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc2.communicate()
            out = out.decode().replace("\n", "").replace("{", "").replace("}","").replace('"', "")

        info = out.split(",")

        for x in range(len(info)):
            if (info[x].split()[0] != "readme:"):
                await message.channel.send("> " + info[x])
    
    if (msg.split()[0] == "!kickall"):
        ip = msg.split()[1]
        port = int(msg.split()[2])
        profiles = []
        factories = []

        await message.channel.send("> Connecting...")
        server = MinecraftServer(ip, port)

        await message.channel.send("> Getting status...")
        status = server.status()

        await message.channel.send("> Getting players...")
        print(status.description)
        players = status.description

        await message.channel.send("> Kicking all players...")
        
        for x in range(len(players)):
            profiles.append(OfflineProfile(players[x]))
            factories.append(BotClientFactory(profiles[x]))
            factories[x] = factories[x].connect(ip, port)
            
        reactor.run()

        await message.channel.send("> Kickall completed!")

try:
    b.run(TOKEN, bot = True)
except KeyboardInterrupt:
    sys.exit()
