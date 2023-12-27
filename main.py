from src.getPeers import getPeers
from src.getMagnets import getMagnetsFromPage
import pandas as pd


def getOurIp():
  return get('https://api.ipify.org').content.decode('utf8')


def getPeersFromGames(amount=50):
  peers = []
  blockedTrackers = []
  for i in range(amount//10):
    magnets = getMagnetsFromPage(i)
    for magnet in magnets:
      newPeers, newBlockedTrackers = getPeers(magnet, blockedTrackers)
      peers += newPeers
      blockedTrackers += newBlockedTrackers
      blockedTrackers = list(set(blockedTrackers))
  peers = list(set(peers))
  return peers


def writeIpsToFile(peers):
  with open("ipAddresses.txt", "w") as f:
    for peer in peers:
      f.write(f"{peer}\n")
  

def writeIpsToCSV(peers):
  df = pd.DataFrame([{"ip": ip, "proxy": None, "country": None, "evaluated": False} for ip in peers])
  df.to_csv("ipAddresses.csv", index=False)

if __name__ == "__main__":
  peers = getPeersFromGames(300)
  writeIpsToCSV(peers)
  print("Successfully wrote peers: ", len(peers))