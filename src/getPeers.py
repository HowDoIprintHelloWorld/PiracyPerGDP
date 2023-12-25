from requests import get
import urllib.parse
from textwrap import wrap
from binascii import hexlify, unhexlify


separator = "-"*40+"\n"


def cleanIP(ip):
  newIP = ""
  numbers = "1234567890."
  for c in ip:
    if c in numbers:
      newIP += c
  return newIP

def getPeers(contents):
  contents = str(contents)
  if "peers" not in contents:
    return []
  peers = contents[contents.index("peers"):]
  peers = peers[peers.index(":")+1:]
  peers = [part for part in peers.split("ip") if part.strip()]
  peers = [part[part.index(":")+1:] for part in peers]
  peers = [part[:part.index(":")] for part in peers]
  peers = [part[:-1] for part in peers]
  peers = [part for part in peers if part.count(".") >= 1]
  peers = [cleanIP(part) for part in peers]
  return peers
    

def getTrackersFromFile():
  with open("trackers.txt", "r") as f:
    return f.read().split()


def getTrackersFromMagnet(magnet):
    trackers = []
    magnet = magnet.split("&tr=")
    trackers = [urllib.parse.unquote(entry) for entry in magnet if "http" in entry]

    return trackers


def getHash(magnet):
  magnet = magnet[:magnet.index("&dn")]
  magnet = magnet[::-1]
  magnet = magnet[:magnet.index(":")][::-1]
  magnet = unhexlify(magnet)
  # print(magnet, unhexlify(magnet))
  magnet = urllib.parse.quote_plus(magnet[:20])
  return magnet




def bittorrentGetPeers(response: str):
    
    response = str(response)
    peers = response.split(":ip")
    peers = [ip for ip in peers if ip.count(".")>= 3]
    peers = [ip[ip.index(":")+1:] for ip in peers if ip.count(":")]
    peers = [ip[:ip.index(":")] for ip in peers if ip.count(":")]
    peers = [ip[:-1] for ip in peers]
    return peers


def trackerToHost(tracker):
    host = tracker.replace("http://", "").replace("https://", "")
    host = host.replace("/announce", "")
    return host


"""
http://tracker.openbittorrent.com:80/announce?
info_hash=%f1%d2*%92F%9b%c3%10%cb%ce%0b%90%b5%40%82(%adW%b2%90
&peer_id=-qB4600-sddVoF~tXQ2V&port=2238
&uploaded=0&downloaded=0&left=3183476736&corrupt=0&key=ABABFC1D
&event=started&numwant=200&compact=1&no_peer_id=1&supportcrypto=1&redundant=0
"""



def runTorrentCheck(hash, trackers, blockedTrackers):
  peers = []
  for tracker in trackers:
    if tracker in blockedTrackers:
      print("Skipped tracker: ", tracker)
      continue
    try:
      # request = tracker+"""?info_hash=""" + hash+"""&peer_id=ABCDDFGHIJKLMNOPQRST&port=6881&uploaded=60&downloaded=50&left=987&compact=0&numwant=100"""
      request = tracker+f"?info_hash={hash}&peer_id=-qB4600-nA!vWWt!z!vx&port=2238&uploaded=0&downloaded=0&left=3844260802&corrupt=0&key=B0690BDB&event=started&numwant=200&compact=0&no_peer_id=1&supportcrypto=0&redundant=0"
      contents = get(request.replace(" ", ""), params={"Host": trackerToHost(tracker), "User-Agent": "qBittorrent/4.6.0"}, timeout=3).content
      if "invalid" in str(contents).lower():
        continue
      newPeers = bittorrentGetPeers(str(contents))
      print(separator, tracker, "Found: ", len(newPeers))
      peers += newPeers
      # print(contents, "\n", separator, "\n\n")
    except Exception as e:
        print("Temporarily blocked tracker: ", tracker)
        blockedTrackers.append(tracker)
        pass
  return list(set(peers)), blockedTrackers



def getPeers(magnet, blockedTrackers):
  trackers = getTrackersFromMagnet(magnet)
  hash = getHash(magnet)
  print("\n\n",separator, "RUNNING FOR HASH: "+hash)
  peers, blockedTrackers = runTorrentCheck(hash, trackers, blockedTrackers)
  peers = [cleanIP(peer) for peer in peers]
  return peers, blockedTrackers


