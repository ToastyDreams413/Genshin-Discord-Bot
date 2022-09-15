from random import randint
import json

f = open("Data.json")
charData = json.load(f)

import nextcord
from nextcord import Interaction, ButtonStyle
from nextcord.ext import commands
from nextcord.ui import Button, View

intents = nextcord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = "!", intents = intents)

spabyssRankings = [ 1, 2, 3, 4, 5, 6, 7, "eight", "nine", 10, 11, 12, 13, 14, "fifteen", 16, 17, 18, 19, 20, 21, 22, 23, 24, "twenty-five", 26, 27, 28 ]
spabyssLevels = [ 1, 2, 3, 4, 5, 6, 7, "eight", "nine", 10, 11, 12, 13, 14, "fifteen", 16, 17, 18, 19, 20, 21, 22, 23, 24, "twenty-five", 26, 27, 28 ]
spabyssConstellations = [ 1, 2, 3, 4, 5, 6, 7, "eight", "nine", 10, 11, 12, 13, 14, "fifteen", 16, 17, 18, 19, 20, 21, 22, 23, 24, "twenty-five", 26, 27, 28 ]


@client.event
async def on_ready():
  print("online!")



def getRankingsEmbed(start, end):
  global spabyssRankings, spabyssLevels, spabyssConstellations
  em = nextcord.Embed(color = 0x0080ff, title = "Spiral Abyss Character Rankings")
  for i in range (start - 1, end):
    em.add_field(name = (str(i + 1) + ". " + str(spabyssRankings[i])), value = ("Avg level: " + str(spabyssLevels[i]) + "\nAvg constellation: " + str(spabyssConstellations[i])))
  em.set_footer(text = "Page " + str(start // 10 + 1) + " of " + str((len(spabyssRankings) + 9) // 10))
  return em



@client.slash_command(name = "update", description = "updates data that may be outdated", guild_ids = [1018416430619840563, 921229631175143435])
async def updateCommand(interaction: nextcord.Interaction, item: str):
  from selenium import webdriver
  driver = webdriver.Chrome(executable_path = r"")
  spiralAbyssURL = "https://spiralabyss.org/"
  if item != "spiralchars":
    message = await interaction.response.send_message("not a valid thing to update!")
    return
  message = await interaction.response.send_message("successfully started update on spiral abyss character info!")
  spabyssRankings.clear()
  spabyssLevels.clear()
  spabyssConstellations.clear()
  url = "https://spiralabyss.org/"
  driver.get(url)
  for i in range (49):
    charPath = "/html/body/div/div[1]/div[1]/main/div/table[1]/tbody/tr[" + str(i + 1) + "]/td[2]"
    curChar = driver.find_element("xpath", charPath)
    spabyssRankings.append(curChar.text)

    charInfoPath = "/html/body/div/div[1]/div[1]/main/div/table[2]/tbody/tr[" + str(i + 1) + "]/td[2]"
    curCharInfo = driver.find_element("xpath", charInfoPath)
    curLine = curCharInfo.text
    curLine = curLine.split(" ")
    spabyssLevels.append(curLine[0][2:])
    spabyssConstellations.append(curLine[2][1:])

  await message.edit("successfully updated spiral abyss character info!")



curLow = None
curHigh = None
leftButton = None
rightButton = None
linkButton = None
rankingsMessage = None
@client.slash_command(name = "spiralchars", description = "gives the rankings and info on characters used in the Spiral Abyss", guild_ids = [1018416430619840563, 921229631175143435])
async def spiralcharsCommand(interaction: nextcord.Interaction):

  global curLow, curHigh, leftButton, rightButton, linkButton, rankingsMessage, spabyssRankings

  rankingsMessage = None

  curLow = 1
  curHigh = 10
  em = getRankingsEmbed(curLow, curHigh)

  leftButton = Button(label = "<", style = ButtonStyle.blurple)
  rightButton = Button(label = ">", style = ButtonStyle.blurple)
  linkButton = Button(label = "website", url = "https://spiralabyss.org/")

  async def leftButtonPress(interaction):
    global curLow, curHigh, leftButton, rightButton, linkButton, spabyssRankings
    if curLow == 1:
      return
    curLow -= 10
    curHigh -= 10
    em = getRankingsEmbed(curLow, curHigh)
    await rankingsMessage.edit(embed = em, view = curView)
  
  async def rightButtonPress(interaction):
    global curLow, curHigh, leftButton, rightButton, linkButton, spabyssRankings
    if curHigh >= len(spabyssRankings):
      return
    curLow += 10
    curHigh += 10
    em = getRankingsEmbed(curLow, min(curHigh, len(spabyssRankings)))
    await rankingsMessage.edit(embed = em, view = curView)
  
  leftButton.callback = leftButtonPress
  rightButton.callback = rightButtonPress
  
  curView = View(timeout = 60)
  curView.add_item(leftButton)
  curView.add_item(rightButton)
  curView.add_item(linkButton)

  rankingsMessage = await interaction.response.send_message(embed = em, view = curView)



def createBuildPage1(charName):
  global charData
  curChar = charData["chars"][charName]
  em = nextcord.Embed(color = 0x0080ff, title = charName + " Guide")
  em.set_thumbnail(url = curChar["image"])
  em.add_field(name = "Overview", value = (curChar["description"] + "\n\n**Element:** " + curChar["element"] + "\n\n**Weapon type:** " + curChar["weapon-type"]))
  return em

def createBuildPage2(charName):
  global charData
  curChar = charData["chars"][charName]
  em = nextcord.Embed(color = 0x0080ff, title = charName + " Guide")

def createWeaponsOverviewPage(charName):
  global charData
  em = nextcord.Embed(color = 0x0080ff, title = charName + " Guide")
  em.set_thumbnail(url = charData["weapon-type-pics"][charData["chars"][charName]["weapon-type"]])
  em.add_field(name = "Weapons Overview", value = charData["chars"][charName]["weapons-description"])
  return em

def create5StarWeaponPage(charName, weaponNum):
  global charData
  em = nextcord.Embed(color = 0x0080ff, title = charName + " - 5 Star Weapons Guide")
  em.set_thumbnail(url = charData["weapon-pics"][charData["chars"][charName]["five-star-weapons"][weaponNum]])
  em.add_field(name = charData["chars"][charName]["five-star-weapons"][weaponNum], value = charData["chars"][charName]["five-star-weapon-descriptions"][charData["chars"][charName]["five-star-weapons"][weaponNum]])
  em.set_footer(text = "Page " + str(weaponNum + 1) + " of " + str(len(charData["chars"][charName]["five-star-weapons"])))
  return em

def create4StarWeaponPage(charName, weaponNum):
  global charData
  em = nextcord.Embed(color = 0x0080ff, title = charName + " - 4 Star Weapons Guide")
  em.set_thumbnail(url = charData["weapon-pics"][charData["chars"][charName]["four-star-weapons"][weaponNum]])
  em.add_field(name = charData["chars"][charName]["four-star-weapons"][weaponNum], value = charData["chars"][charName]["four-star-weapon-descriptions"][charData["chars"][charName]["four-star-weapons"][weaponNum]])
  em.set_footer(text = "Page " + str(weaponNum + 1) + " of " + str(len(charData["chars"][charName]["four-star-weapons"])))
  return em

def createArtifactsOverviewPage(charName):
  global charData
  em = nextcord.Embed(color = 0x0080ff, title = charName + " Guide")
  em.set_thumbnail(url = charData["artifact-pics"][charData["chars"][charName]["artifact-set"]])
  em.add_field(name = "Artifacts Overview", value = charData["chars"][charName]["artifacts-description"])
  return em

def createMainstatsPage(charName):
  global charData
  em = nextcord.Embed(color = 0x0080ff, title = charName + " Guide")
  em.add_field(name = "Sands: " + charData["chars"][charName]["mainstats"][0], value = charData["chars"][charName]["sands-description"])
  em.add_field(name = "Goblet: " + charData["chars"][charName]["mainstats"][1], value = charData["chars"][charName]["sands-description"])
  em.add_field(name = "Circlet: " + charData["chars"][charName]["mainstats"][2], value = charData["chars"][charName]["sands-description"])
  return em

def createSubstatsPage(charName):
  global charData
  em = nextcord.Embed(color = 0x0080ff, title = charName + " Guide")
  em.add_field(name = "Artifact Substats", value = charData["chars"][charName]["substats-description"])
  return em

def createTeamsOverviewPage(charName):
  global charData
  em = nextcord.Embed(color = 0x0080ff, title = charName + " Guide")
  em.add_field(name = "Teams", value = charData["chars"][charName]["teams-description"])
  return em

def createTeamPage(charName, teamNum):
  global charData
  curChar = charData["chars"][charName]
  em = nextcord.Embed(color = 0x0080ff, title = charName + " Team Comps: " + curChar["team-names"][teamNum - 1], description = curChar["team-descriptions"][curChar["team-names"][teamNum - 1]])
  c = 0
  for team in curChar["teams"]:
    c += 1
    if c == teamNum:
      for member in curChar["teams"][team]:
        em.add_field(name = member, value = curChar["teams"][team][member])
      break
  em.set_footer(text = "Page " + str(teamNum) + " of " + str(len(curChar["team-names"])))
  return em



@client.slash_command(name = "info", description = "gives info on how to build a specific character, team comps, etc", guild_ids = [1018416430619840563, 921229631175143435])
async def buildCommand(interaction: nextcord.Interaction, char: str):
  global charData
  curPage = "overview"
  infoMessage = None
  char = char.title()
  if char not in charData["chars"]:
    await interaction.response.send_message(char + " is either not an existing playable Genshin character or they haven't been added to this bot yet.")
    return
  em = createBuildPage1(char)

  weaponsButton = Button(label = "Weapons", style = ButtonStyle.blurple)
  artifactsButton = Button(label = "Artifacts", style = ButtonStyle.blurple)
  teamsButton = Button(label = "Teams", style = ButtonStyle.blurple)

  backButton = Button(label = "back", style = ButtonStyle.green)

  weaponsOverviewButton = Button(label = "Overview", style = ButtonStyle.blurple)
  fiveStarWeaponsButton = Button(label = "Five star", style = ButtonStyle.blurple)
  fourStarWeaponsButton = Button(label = "Four star", style = ButtonStyle.blurple)

  weaponPage = 0
  backFromWeaponsButton = Button(label = "back", style = ButtonStyle.green)
  previousFiveStarWeaponButton = Button(label = "<", style = ButtonStyle.blurple)
  nextFiveStarWeaponButton = Button(label = ">", style = ButtonStyle.blurple)
  previousFourStarWeaponButton = Button(label = "<", style = ButtonStyle.blurple)
  nextFourStarWeaponButton = Button(label = ">", style = ButtonStyle.blurple)

  artifactsOverviewButton = Button(label = "Overview", style = ButtonStyle.blurple)
  mainstatsButton = Button(label = "Main Stats", style = ButtonStyle.blurple)
  substatsButton = Button(label = "Substats", style = ButtonStyle.blurple)

  teamPage = 0
  teamsOverviewButton = Button(label = "Overview", style = ButtonStyle.blurple)
  nextTeamButton = Button(label = ">", style = ButtonStyle.blurple)
  previousTeamButton = Button(label = "<", style = ButtonStyle.blurple)

  curView = View(timeout = 5)

  async def backButtonPress(interaction):
    nonlocal char, weaponsButton, artifactsButton, teamsButton, curPage
    curPage = "overview"
    em = createBuildPage1(char)
    curView = View(timeout = 60)
    curView.add_item(weaponsButton)
    curView.add_item(artifactsButton)
    curView.add_item(teamsButton)
    await infoMessage.edit(embed = em, view = curView)

  async def weaponsButtonPress(interaction):
    nonlocal char, curView, backButton, weaponsOverviewButton, fiveStarWeaponsButton, fourStarWeaponsButton, infoMessage, curPage
    if curPage == "weapons-overview":
      return
    curPage = "weapons-overview"
    em = createWeaponsOverviewPage(char)
    curView = View(timeout = 60)
    curView.add_item(backButton)
    curView.add_item(weaponsOverviewButton)
    curView.add_item(fiveStarWeaponsButton)
    curView.add_item(fourStarWeaponsButton)
    await infoMessage.edit(embed = em, view = curView)
  
  async def weaponsOverviewPress(interaction):
    nonlocal char, curView, infoMessage, curPage
    if curPage == "weapons-overview":
      return
    curPage = "weapons-overview"
    em = createWeaponsOverviewPage(char)
    await infoMessage.edit(embed = em)
  
  async def fiveStarWeaponsButtonPress(interaction):
    nonlocal char, curView, backButton, weaponsOverviewButton, fiveStarWeaponsButton, fourStarWeaponsButton, infoMessage, curPage, backFromWeaponsButton, previousFiveStarWeaponButton, nextFiveStarWeaponButton
    curPage = "five-star-weapons"
    em = create5StarWeaponPage(char, 0)
    curView = View(timeout = 60)
    curView.add_item(backFromWeaponsButton)
    curView.add_item(previousFiveStarWeaponButton)
    curView.add_item(nextFiveStarWeaponButton)
    await infoMessage.edit(embed = em, view = curView)

  async def nextFiveStarWeaponButtonPress(interaction):
    nonlocal char, infoMessage, weaponPage
    if weaponPage + 1 >= len(charData["chars"][char]["five-star-weapons"]):
      return
    weaponPage += 1
    em = create5StarWeaponPage(char, weaponPage)
    await infoMessage.edit(embed = em)
  
  async def previousFiveStarWeaponButtonPress(interaction):
    nonlocal char, infoMessage, weaponPage
    if weaponPage <= 0:
      return
    weaponPage -= 1
    em = create5StarWeaponPage(char, weaponPage)
    await infoMessage.edit(embed = em)
  
  async def fourStarWeaponsButtonPress(interaction):
    nonlocal char, curView, backButton, weaponsOverviewButton, infoMessage, curPage, backFromWeaponsButton, previousFourStarWeaponButton, nextFourStarWeaponButton
    curPage = "four-star-weapons"
    em = create4StarWeaponPage(char, 0)
    curView = View(timeout = 60)
    curView.add_item(backFromWeaponsButton)
    curView.add_item(previousFourStarWeaponButton)
    curView.add_item(nextFourStarWeaponButton)
    await infoMessage.edit(embed = em, view = curView)
  
  async def nextFourStarWeaponButtonPress(interaction):
    nonlocal char, infoMessage, weaponPage
    if weaponPage + 1 >= len(charData["chars"][char]["four-star-weapons"]):
      return
    weaponPage += 1
    em = create4StarWeaponPage(char, weaponPage)
    await infoMessage.edit(embed = em)
  
  async def previousFourStarWeaponButtonPress(interaction):
    nonlocal char, infoMessage, weaponPage
    if weaponPage <= 0:
      return
    weaponPage -= 1
    em = create4StarWeaponPage(char, weaponPage)
    await infoMessage.edit(embed = em)
  
  async def artifactsButtonPress(interaction):
    nonlocal char, curView, backButton, artifactsOverviewButton, mainstatsButton, substatsButton, infoMessage, curPage
    if curPage == "artifacts-overview":
      return
    curPage = "artifacts-overview"
    em = createArtifactsOverviewPage(char)
    curView = View(timeout = 60)
    curView.add_item(backButton)
    curView.add_item(artifactsOverviewButton)
    curView.add_item(mainstatsButton)
    curView.add_item(substatsButton)
    await infoMessage.edit(embed = em, view = curView)
  
  async def artifactsOverviewPress(interaction):
    nonlocal char, curView, infoMessage, curPage
    if curPage == "artifacts-overview":
      return
    curPage = "artifacts-overview"
    em = createArtifactsOverviewPage(char)
    await infoMessage.edit(embed = em)
  
  async def mainstatsButtonPress(interaction):
    nonlocal char, curView, infoMessage, curPage
    if curPage == "mainstats":
      return
    curPage = "mainstats"
    em = createMainstatsPage(char)
    await infoMessage.edit(embed = em)
  
  async def substatsButtonPress(interaction):
    nonlocal char, curView, infoMessage, curPage
    if curPage == "substats":
      return
    curPage = "substats"
    em = createSubstatsPage(char)
    await infoMessage.edit(embed = em)
  
  async def teamsButtonPress(interaction):
    nonlocal char, curView, backButton, teamsOverviewButton, nextTeamButton, previousTeamButton, infoMessage, curPage, teamPage
    if curPage == "teams-overview":
      return
    curPage = "teams-overview"
    teamPage = 0
    em = createTeamsOverviewPage(char)
    curView = View(timeout = 60)
    curView.add_item(backButton)
    curView.add_item(teamsOverviewButton)
    curView.add_item(previousTeamButton)
    curView.add_item(nextTeamButton)
    await infoMessage.edit(embed = em, view = curView)
  
  async def teamsOverviewPress(interaction):
    nonlocal char, curView, infoMessage, curPage
    if curPage == "teams-overview":
      return
    curPage = "teams-overview"
    em = createTeamsOverviewPage(char)
    await infoMessage.edit(embed = em)

  async def nextTeamButtonPress(interaction):
    nonlocal char, infoMessage, curPage, teamPage
    curPage = "team-pages"
    if teamPage >= len(charData["chars"][char]["team-names"]):
      return
    teamPage += 1
    em = createTeamPage(char, teamPage)
    await infoMessage.edit(embed = em)
  
  async def previousTeamButtonPress(interaction):
    nonlocal char, infoMessage, curPage, teamPage
    curPage = "team-pages"
    if teamPage <= 1:
      return
    teamPage -= 1
    em = createTeamPage(char, teamPage)
    await infoMessage.edit(embed = em)
  
  weaponsButton.callback = weaponsButtonPress
  artifactsButton.callback = artifactsButtonPress
  teamsButton.callback = teamsButtonPress
  
  backButton.callback = backButtonPress

  weaponsOverviewButton.callback = weaponsOverviewPress
  fiveStarWeaponsButton.callback = fiveStarWeaponsButtonPress
  fourStarWeaponsButton.callback = fourStarWeaponsButtonPress
  backFromWeaponsButton.callback = weaponsButtonPress
  nextFiveStarWeaponButton.callback = nextFiveStarWeaponButtonPress
  previousFiveStarWeaponButton.callback = previousFiveStarWeaponButtonPress
  nextFourStarWeaponButton.callback = nextFourStarWeaponButtonPress
  previousFourStarWeaponButton.callback = previousFourStarWeaponButtonPress

  artifactsOverviewButton.callback = artifactsOverviewPress
  mainstatsButton.callback = mainstatsButtonPress
  substatsButton.callback = substatsButtonPress

  teamsOverviewButton.callback = teamsOverviewPress
  nextTeamButton.callback = nextTeamButtonPress
  previousTeamButton.callback = previousTeamButtonPress
  
  curView.add_item(weaponsButton)
  curView.add_item(artifactsButton)
  curView.add_item(teamsButton)
  
  infoMessage = await interaction.response.send_message(embed = em, view = curView)



pity = {}
inv = {}
chars = {}
weapons = {}
pullData = {}
standardBanner5StarsChars = [ "Keqing", "Diluc", "Qiqi", "Jean", "Mona" ]
standardBanner4StarsChars = [ "Collei", "Dori", "Sayu", "Heizou", "Sucrose", "Chongyun", "Diona", "Rosaria", "Beidou", "Fischl", "Kujou Sara", "Kuki Shinobu", "Razor", "Gorou", "Ningguang", "Noelle", "Yun Jin", "Barbara", "Xingqiu", "Bennett", "Thoma", "Xiangling", "Xinyan", "Yanfei" ]
starters = [ "Kaeya", "Lisa", "Amber" ]
standardBanner5StarWeapons = [ "Amos' Bow", "Skyward Harp", "Lost Prayer to the Sacred Winds", "Skyward Atlas", "Skyward Pride", "Wolf's Gravestone", "Primordial Jade Winged-Spear", "Skyward Spine", "Aquila Favonia", "Skyward Blade" ]
standardBanner4StarWeapons = [ "Favonius Warbow", "Rust", "Sacrifical Bow", "The Stringless", "Eye of Perception", "Favonius Codex", "Sacrificial Fragments", "The Widsith", "Favonius Greatsword", "Rainslasher", "Sacrifical Greatsword", "The Bell", "Dragon's Bane", "Favonius Lance", "Favonius Sword", "Lion's Roar", "Sacrifical Sword", "The Flute" ]
threeStarWeapons = [ "Raven Bow", "Sharpshooter's Oath", "Slingshot", "Emerald Orb", "Magic Guide", "Thrilling Tales of Dragon Slayers", "Bloodtainted Greatsword", "Debate Club", "Ferrous Shadow", "Black Tassel", "Cool Steel", "Harbinger of Dawn", "Skyrider Sword" ]
eventFourStarChars = {
  "Kokomi" : [ "Dori", "Xingqiu", "Sucrose" ],
  "Ganyu" : [ "Dori", "Xingqiu", "Sucrose" ],
  "Tighnari" : [ "Collei", "Diona", "Fischl" ],
  "Zhongli" : [ "Collei", "Diona", "Fischl" ],
  "Yoimiya" : [ "Yun Jin", "Xinyan", "Bennett" ],
  "Kazuha" : [ "Heizou", "Thoma", "Ningguang" ],
  "Klee" : [ "Heizou", "Thoma", "Ningguang" ],
  "Itto" : [ "Kuki Shinobu", "Gorou", "Chongyun" ],
  "Yelan" : [ "Yanfei", "Barbara", "Noelle" ],
  "Xiao" : [ "Yanfei", "Barbara", "Noelle" ],
  "Ayaka" : [ "Rosaria", "Razor", "Sayu" ],
  "Venti" : [ "Sucrose", "Xiangling", "Yun Jin" ],
  "Ayato" : [ "Sucrose", "Xiangling", "Yun Jin" ],
  "Shogun" : [ "Bennett", "Xinyan", "Kujou Sara" ],
  "Yae Miko" : [ "Thoma", "Fischl", "Diona" ],
  "Shenhe" : [ "Chongyun", "Ningguang", "Yunjin" ],
  "Albedo" : [ "Bennett", "Rosaria", "Noelle" ],
  "Eula" : [ "Bennett", "Rosaria", "Noelle" ],
  "Hu Tao" : [ "Thoma", "Sayu", "Diona" ],
  "Childe" : [ "Chongyun", "Ningguang", "Yanfei" ],
  "Keqing" : [ "Barbara", "Bennett", "Ningguang" ]
}
bannerPics = {
  "Kokomi" : "https://img.gamewith.net/img/647812c7922a1717bf2ca21553d8813d.jpeg",
  "Ganyu" : "https://img.gamewith.net/img/37909c586cc09852067eaf5b35d086ad.jpg",
  "Tighnari" : "https://img.gamewith.net/img/3ded645e48bd9c5bc285a4190258ffba.jpeg",
  "Zhongli" : "https://img.gamewith.net/img/cd0beb5d1ba178301e4bbcf6a976cbf6.jpeg",
  "Yoimiya" : "https://img.gamewith.net/img/b907030e7db1bca0241ee15ff57a73a0.jpg",
  "Kazuha" : "https://img.gamewith.net/img/b3a19a070352528747dc7dc279f60a55.jpeg",
  "Klee" : "https://img.gamewith.net/img/b8881e6927c8e56f690a8d9325087f39.jpg",
  "Itto" : "https://img.gamewith.net/img/460af403e008fec309e40099036b0f8e.jpg",
  "Yelan" : "https://img.gamewith.net/img/8d3fe7e828fdf59b84ac22a89dc13aa7.jpeg",
  "Xiao" : "https://img.gamewith.net/img/c6dc01bb776a41a28854b7c189b3406b.jpeg",
  "Ayaka" : "https://img.gamewith.net/img/65060a3ab937056335931d33b2672aab.jpg",
  "Venti" : "https://img.gamewith.net/img/23d5084ba515a6ae83f8286ba8fb156f.jpg",
  "Ayato" : "https://img.gamewith.net/img/aaf8e47acfe146c7169e4b8c05f30255.jpg",
  "Shogun" : "https://img.gamewith.net/img/230303a411656663227c2e22b59eb9f6.jpg",
  "Yae Miko" : "https://img.gamewith.net/img/ab04d2a7d46a493e13bb7c85a990d330.jpeg",
  "Shenhe" : "https://img.gamewith.net/img/e5dbe9c9860877f7d914c1474ef61291.jpeg",
  "Albedo" : "https://img.gamewith.net/img/7d95b44e2d1892df5f09ceaf8de6e5e1.jpg",
  "Eula" : "https://img.gamewith.net/img/c510aa8eb4017d817ed6a9b96aab3cb9.jpg",
  "Hu Tao" : "https://img.gamewith.net/img/504e9908d5b223f966b1736287f62f22.jpg",
  "Childe" : "https://img.gamewith.net/img/143fef8e1867ec491d59488a88146a94.jpeg",
  "Keqing" : "https://img.gamewith.net/img/431d3f8ec1df7f256369d901024d5d5d.jpg",
  "Standard" : "https://static.wikia.nocookie.net/gensin-impact/images/b/bd/Wanderlust_Invocation_2020-11-11.png/revision/latest?cb=20201111132059"
}
itemPics = {
  "Kokomi" : "https://i.ytimg.com/vi/DrcdbyTauB0/maxresdefault.jpg",
  "Ganyu" : "https://imageio.forbes.com/specials-images/imageserve/5ffd962b8fc4cdd11164c6ad/Ganyu/960x0.jpg?format=jpg&width=960",
  "Tighnari" : "https://preview.redd.it/qsi96qdx2mj91.png?auto=webp&s=6db2fd1669e6d68a194c340384b345de13581b23",
  "Zhongli" : "https://imageio.forbes.com/specials-images/imageserve/5fc638a1eb99296ea9a124a6/0x0.jpg?format=jpg&width=1200",
  "Yoimiya" : "https://assets2.rockpapershotgun.com/genshin-impact-yoimiya-pull.jpg/BROK/thumbnail/1600x900/format/jpg/quality/80/genshin-impact-yoimiya-pull.jpg",
  "Kazuha" : "https://assets2.rockpapershotgun.com/genshin-impact-kazuha-pull.jpg/BROK/thumbnail/1600x900/quality/100/genshin-impact-kazuha-pull.jpg",
  "Klee" : "https://assets2.rockpapershotgun.com/genshin-impact-klee-pull.jpg/BROK/thumbnail/1600x900/format/jpg/quality/80/genshin-impact-klee-pull.jpg",
  "Itto" : "https://staticg.sportskeeda.com/editor/2021/12/90e1f-16395960658639-1920.jpg",
  "Yelan" : "https://pbs.twimg.com/media/FPSc7grXwAwMd0n?format=jpg&name=4096x4096",
  "Xiao" : "https://i0.wp.com/www.alphr.com/wp-content/uploads/2021/06/Xiao-Wish-Art.jpg?resize=690%2C388&ssl=1",
  "Ayaka" : "https://i.ytimg.com/vi/CmuipgprhAE/maxresdefault.jpg",
  "Venti" : "http://pm1.narvii.com/7874/2f3ebddc7a85f447c8a6e400064a829e8b08e601r1-2048-996v2_uhq.jpg",
  "Ayato" : "https://i.ytimg.com/vi/YNRJ1u7-ZSI/maxresdefault.jpg",
  "Shogun" : "https://i.ytimg.com/vi/aj-8ul2QIGg/maxresdefault.jpg",
  "Yae Miko" : "https://staticg.sportskeeda.com/editor/2022/02/abfb6-16449849300953-1920.jpg",
  "Shenhe" : "https://i.ytimg.com/vi/kTyP-nR30n8/maxresdefault.jpg",
  "Albedo" : "https://i.ytimg.com/vi/uvCUH8XZdvg/maxresdefault.jpg",
  "Eula" : "https://i.pinimg.com/originals/88/76/09/887609ce04a3de015d5141e9408485d4.jpg",
  "Hu Tao" : "https://1401700980.rsc.cdn77.org/data/images/full/98721/genshin-impact-hu-tao-full-banner-lasts-for-2-weeks-release-date-and-more-rosaria-to-be-update-1-4s-only-new-hero.png",
  "Childe" : "https://imageio.forbes.com/specials-images/imageserve/5fabe4ac89f888a88c7ab378/Genshin-Impact/960x0.jpg?format=jpg&width=960",
  "Keqing" : "https://bang-phinf.pstatic.net/a/32c3g3/h_3haUd018bng85ordrnmdrah_qv20nu.jpg",

  "Mona" : "https://www.tehvidya.com/wp-content/uploads/2021/02/pulled-mona-in-genshin.jpg",
  "Jean" : "https://imageio.forbes.com/specials-images/imageserve/5f8443d5c7d100fa8de119ec/Genshin-Impact/960x0.jpg?format=jpg&width=960",
  "Diluc" : "https://assets2.rockpapershotgun.com/diluc-pull-screen.jpg/BROK/resize/1920x1920%3E/format/jpg/quality/80/diluc-pull-screen.jpg",
  "Qiqi" : "https://i.pinimg.com/originals/d3/84/dd/d384ddfb4b748e71cb5d188d021bc6fe.png",

  "Primordial Jade Winged-Spear" : "https://static.wikia.nocookie.net/e8a1f054-c3b9-448f-85b4-acc5fc782aa1/scale-to-width/755",
  "Amos' Bow" : "",
  "Skyward Harp" : "",
  "Lost Prayer to the Sacred Winds" : "",
  "Skyward Atlas" : "",
  "Skyward Pride" : "",
  "Wolf's Gravestone" : "",
  "Primordial Jade Winged-Spear" : "",
  "Skyward Spine" : "",
  "Aquila Favonia" : "",
  "Skyward Blade" : "",

  "Favonius Warbow" : "https://static.wikia.nocookie.net/gensin-impact/images/8/85/Weapon_Favonius_Warbow.png/revision/latest/scale-to-width-down/74?cb=20201120003145",
  "Rust" : "https://static.wikia.nocookie.net/gensin-impact/images/1/1c/Weapon_Rust.png/revision/latest/scale-to-width-down/74?cb=20201120002437",
  "Sacrifical Bow" : "https://static.wikia.nocookie.net/gensin-impact/images/e/ec/Weapon_Sacrificial_Bow.png/revision/latest/scale-to-width-down/74?cb=20201120002607",
  "The Stringless" : "https://static.wikia.nocookie.net/gensin-impact/images/7/71/Weapon_The_Stringless.png/revision/latest/scale-to-width-down/74?cb=20201116035406",
  "Eye of Perception" : "https://static.wikia.nocookie.net/gensin-impact/images/6/6c/Weapon_Eye_of_Perception.png/revision/latest/scale-to-width-down/74?cb=20201116033703",
  "Favonius Codex" : "https://static.wikia.nocookie.net/gensin-impact/images/3/36/Weapon_Favonius_Codex.png/revision/latest/scale-to-width-down/74?cb=20201116033719",
  "Sacrificial Fragments" : "https://static.wikia.nocookie.net/gensin-impact/images/6/6c/Weapon_Sacrificial_Fragments.png/revision/latest/scale-to-width-down/74?cb=20220316013323",
  "The Widsith" : "https://static.wikia.nocookie.net/gensin-impact/images/f/f0/Weapon_The_Widsith.png/revision/latest/scale-to-width-down/74?cb=20201119201814",
  "Favonius Greatsword" : "https://static.wikia.nocookie.net/gensin-impact/images/9/9c/Weapon_Favonius_Greatsword.png/revision/latest/scale-to-width-down/74?cb=20201119235934",
  "Rainslasher" : "https://static.wikia.nocookie.net/gensin-impact/images/d/d4/Weapon_Rainslasher.png/revision/latest/scale-to-width-down/74?cb=20201119235128",
  "Sacrifical Greatsword" : "https://static.wikia.nocookie.net/gensin-impact/images/1/17/Weapon_Sacrificial_Greatsword.png/revision/latest/scale-to-width-down/74?cb=20201120004023",
  "The Bell" : "https://static.wikia.nocookie.net/gensin-impact/images/6/6e/Weapon_The_Bell.png/revision/latest/scale-to-width-down/74?cb=20201116035344",
  "Dragon's Bane" : "https://static.wikia.nocookie.net/gensin-impact/images/2/24/Weapon_Dragon%27s_Bane.png/revision/latest/scale-to-width-down/74?cb=20201116033629",
  "Favonius Lance" : "https://static.wikia.nocookie.net/gensin-impact/images/5/57/Weapon_Favonius_Lance.png/revision/latest/scale-to-width-down/74?cb=20201116154512",
  "Favonius Sword" : "https://static.wikia.nocookie.net/gensin-impact/images/9/90/Weapon_Favonius_Sword.png/revision/latest/scale-to-width-down/74?cb=20201116033811",
  "Lion's Roar" : "https://static.wikia.nocookie.net/gensin-impact/images/e/e6/Weapon_Lion%27s_Roar.png/revision/latest/scale-to-width-down/74?cb=20201119232745",
  "Sacrifical Sword" : "https://static.wikia.nocookie.net/gensin-impact/images/a/a0/Weapon_Sacrificial_Sword.png/revision/latest/scale-to-width-down/74?cb=20201120010840",
  "The Flute" : "https://static.wikia.nocookie.net/gensin-impact/images/6/63/Weapon_The_Flute.png/revision/latest/scale-to-width-down/74?cb=20201119203316",

  "Fischl" : "https://imageio.forbes.com/specials-images/imageserve/5f75d1fc084cda6cd348ab4d/Genshin-Impact/960x0.jpg?format=jpg&width=960",
  "Noelle" : "https://oyster.ignimgs.com/mediawiki/apis.ign.com/genshin-impact/a/a1/Genshin_Impact_20200929215315.jpg",
  "Razor" : "https://oyster.ignimgs.com/mediawiki/apis.ign.com/genshin-impact/a/a4/Genshin_Impact_20200930104526.jpg?width=1280",
  "Thoma" : "https://i0.wp.com/thefanboyseo.com/wp-content/uploads/2021/09/FB_IMG_1630947005550.jpg?fit=720%2C393&ssl=1",
  "Dori" : "https://theclick.gg/wp-content/uploads/2022/06/Genshin-Impact-Dori-Splash-Art.jpg",
  "Sayu" : "https://preview.redd.it/j8lr2t8lnig71.png?auto=webp&s=8109c78a4cfb551a373c78b984e99e0a8c8dd907",
  "Heizou" : "https://static1.srcdn.com/wordpress/wp-content/uploads/2022/05/Genshin-Impact-Heizou-Elemental-Burst-Skills.jpg",
  "Sucrose" : "https://i.ytimg.com/vi/6GEusRp1ctg/maxresdefault.jpg",
  "Chongyun" : "https://i.ytimg.com/vi/GT7hXvWE6o8/maxresdefault.jpg",
  "Diona" : "https://i.ytimg.com/vi/IEZssiWDRGc/maxresdefault.jpg",
  "Rosaria" : "https://static.wikia.nocookie.net/gensin-impact/images/f/f6/Character_Rosaria_Thumb.png/revision/latest/scale-to-width-down/74?cb=20220601032845",
  "Beidou" : "https://i.ytimg.com/vi/-V_xHI8oO4s/maxresdefault.jpg",
  "Kujou Sara" : "https://i.ytimg.com/vi/qrkbEqhkwpg/maxresdefault.jpg",
  "Kuki Shinobu" : "https://upload-os-bbs.hoyolab.com/upload/2022/06/21/208355467/0a76abfd4e3efa4bba9773eca58b0f85_4208640393469713449.jpg?x-oss-process=image/resize,s_600/quality,q_80/auto-orient,0/interlace,1/format,jpg",
  "Gorou" : "https://preview.redd.it/u5q9gmv181981.png?width=640&crop=smart&auto=webp&s=fe83c8937e3a415f8cbad601a36dbf4d5f62a9ba",
  "Ningguang" : "https://i.ytimg.com/vi/BtX73h3WGy4/maxresdefault.jpg",
  "Yun Jin" : "https://pbs.twimg.com/media/FIRe-KzWUAAA5CS?format=jpg&name=large",
  "Barbara" : "https://www.alphr.com/wp-content/uploads/2021/04/HP-7.png",
  "Xingqiu" : "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/1a2212b9-af4a-4302-9499-08be7aaa7ff2/de950go-c1747469-9717-4368-a9b4-0d44cf6d3407.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzFhMjIxMmI5LWFmNGEtNDMwMi05NDk5LTA4YmU3YWFhN2ZmMlwvZGU5NTBnby1jMTc0NzQ2OS05NzE3LTQzNjgtYTliNC0wZDQ0Y2Y2ZDM0MDcuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.eq3yhHwK-ymsiqC1tBUAOJGP9ReQWBX6IakdDE6nGCM",
  "Bennett" : "https://assets2.rockpapershotgun.com/bennett-pull-screen.png/BROK/resize/1920x1920%3E/format/jpg/quality/80/bennett-pull-screen.png",
  "Xiangling" : "https://assets2.rockpapershotgun.com/genshin-impact-xiangling-summoned.jpg/BROK/resize/1920x1920%3E/format/jpg/quality/80/genshin-impact-xiangling-summoned.jpg",
  "Xinyan" : "https://i.ytimg.com/vi/NTKEcK2mX08/maxresdefault.jpg",
  "Yanfei" : "https://i.ytimg.com/vi/ARqDUJ2yJMM/maxresdefault.jpg",
  "Collei" : "https://static.wikia.nocookie.net/gensin-impact/images/7/79/Character_Collei_Card.png/revision/latest/scale-to-width-down/281?cb=20220711041855",

  "Raven Bow" : "https://static.wikia.nocookie.net/gensin-impact/images/d/d0/Weapon_Raven_Bow.png/revision/latest/scale-to-width-down/74?cb=20201116034840",
  "Sharpshooter's Oath" : "https://static.wikia.nocookie.net/gensin-impact/images/5/52/Weapon_Sharpshooter%27s_Oath.png/revision/latest/scale-to-width-down/74?cb=20201116035135",
  "Slingshot" : "https://static.wikia.nocookie.net/gensin-impact/images/c/ca/Weapon_Slingshot.png/revision/latest/scale-to-width-down/74?cb=20201116035308",
  "Emerald Orb" : "https://static.wikia.nocookie.net/gensin-impact/images/c/ca/Weapon_Slingshot.png/revision/latest/scale-to-width-down/74?cb=20201116035308",
  "Magic Guide" : "https://static.wikia.nocookie.net/gensin-impact/images/3/39/Weapon_Magic_Guide.png/revision/latest/scale-to-width-down/74?cb=20201119232047",
  "Thrilling Tales of Dragon Slayers" : "https://static.wikia.nocookie.net/gensin-impact/images/1/19/Weapon_Thrilling_Tales_of_Dragon_Slayers.png/revision/latest/scale-to-width-down/74?cb=20201119201736",
  "Bloodtainted Greatsword" : "https://static.wikia.nocookie.net/gensin-impact/images/4/4a/Weapon_Bloodtainted_Greatsword.png/revision/latest/scale-to-width-down/74?cb=20201119233531",
  "Debate Club" : "https://static.wikia.nocookie.net/gensin-impact/images/7/74/Weapon_Debate_Club.png/revision/latest/scale-to-width-down/74?cb=20201116033616",
  "Ferrous Shadow" : "https://static.wikia.nocookie.net/gensin-impact/images/e/e9/Weapon_Ferrous_Shadow.png/revision/latest/scale-to-width-down/74?cb=20201120003242",
  "Black Tassel" : "https://static.wikia.nocookie.net/gensin-impact/images/4/43/Weapon_Black_Tassel.png/revision/latest/scale-to-width-down/74?cb=20201116033134",
  "Cool Steel" : "https://static.wikia.nocookie.net/gensin-impact/images/9/9c/Weapon_Cool_Steel.png/revision/latest/scale-to-width-down/74?cb=20201119233444",
  "Harbinger of Dawn" : "https://static.wikia.nocookie.net/gensin-impact/images/2/23/Weapon_Harbinger_of_Dawn.png/revision/latest/scale-to-width-down/74?cb=20201119233056",
  "Skyrider Sword" : "https://static.wikia.nocookie.net/gensin-impact/images/3/34/Weapon_Skyrider_Sword.png/revision/latest/scale-to-width-down/74?cb=20201116035206"
}

# creates the gif with the pull animation
def createOnePullGif(pullType):
  em = nextcord.Embed(color = 0x0080ff, title = "One Pull")
  if pullType == 5:
    em.set_image(url = "https://c.tenor.com/rOuL0G1uRpMAAAAC/genshin-impact-pull.gif")
  elif pullType == 4:
    em.set_image(url = "https://c.tenor.com/pVzBgcp1RPQAAAAd/genshin-impact-animation.gif")
  else:
    em.set_image(url = "https://c.tenor.com/-0gPdn6GMVAAAAAC/genshin3star-wish.gif")
  return em

def createTenPullGif(pullType):
  em = nextcord.Embed(color = 0x0080ff, title = "Ten Pull")
  if pullType == 5:
    em.set_image(url = "https://c.tenor.com/wnmtDWo-mUwAAAAd/genshin-genshin-impact.gif")
  else:
    em.set_image(url = "https://playerassist.com/wp-content/uploads/2021/09/wish-10x-4star_GIF.gif")
  return em

def createItemPage(item, totalPulls, pageNum):
  em = nextcord.Embed(color = 0x0080ff, title = str(totalPulls) + " Pull")
  if item in standardBanner5StarsChars or item in bannerPics or item in standardBanner5StarWeapons:
    em.add_field(name = "🟡 5 Star 🟡", value = item)
  elif item in standardBanner4StarsChars or item in standardBanner4StarWeapons:
    em.add_field(name = "🟣 4 Star 🟣", value = item)
  else:
    em.add_field(name = "🔵 3 Star 🔵", value = item)
  em.set_image(url = itemPics[item])
  em.set_footer(text = "Page " + str(pageNum) + " of " + str(totalPulls))
  return em

def createPullOverviewPage(pulls):
  em = nextcord.Embed(color = 0x008ff, title = "10 Pull Overview")
  for item in pulls:
    if item in standardBanner5StarsChars or item in bannerPics or item in standardBanner5StarWeapons:
      em.add_field(name = "🟡 5 Star 🟡", value = item)
    elif item in standardBanner4StarsChars or item in standardBanner4StarWeapons:
      em.add_field(name = "🟣 4 Star 🟣", value = item)
    else:
      em.add_field(name = "🔵 3 Star 🔵", value = item)
  return em

# returns the name of the char/item
def createOnePull(userId, charName):
  global inv, pity, standardBanner5StarsChars, standardBanner4StarsChars, standardBanner4StarWeapons, threeStarWeapons, eventFourStarChars, bannerPics, chars, weapons, pullData
  if userId not in pity:
    pity[userId] = [0, 0, False, False, 0, 0, 0, 0] # event-5-star-pity, event-4-star-pity, guarantee-5-star, guarantee-4-star, standard-5-star-pity, standard-4-star-pity, 5-star-chars-vs-weapons, 4-star-chars-vs-weapons
    weapons[userId] = { "five-stars" : {}, "four-stars" : {}, "three-stars" : {} }
    chars[userId] = { "five-stars" : {}, "four-stars" : {} }
    pullData[userId] = { "standard-pulls" : 0, "event-pulls" : 0, "50/50 losses" : 0, "five-star-chars" : 0, "four-star-chars" : 0, "five-star-weapons" : 0, "four-star-weapons" : 0, "three-star-weapons" : 0 }
  


  if charName == "Standard":
    pullData[userId]["standard-pulls"] += 1
    rate = 0.6
    pity[userId][4] += 1
    pity[userId][5] += 1
    if pity[userId][4] == 90:
      rate = 100
    elif pity[userId][4] > 75:
      rate = (pity[userId][4] - 75) * 6 + 0.6
    rng = randint(1, 1000)
    if rng <= rate * 10: # 5 star
      pullIsChar = True
      curRng = randint(1, 2)
      if curRng == 1:
        pullIsChar = False
      if pity[userId][6] == 2:
        pity[userId][6] = 0
        pullIsChar = False
      elif pity[userId][6] == -2:
        pity[userId][6] = 0
        pullIsChar = True
      else:
        if pullIsChar:
          if pity[userId][6] == 1:
            pity[userId][6] = 2
          else:
            pity[userId][6] = 1
        else:
          if pity[userId][6] == -1:
            pity[userId][6] = -2
          else:
            pity[userId][6] = -1
      if pullIsChar:
        curItem = standardBanner5StarsChars[randint(0, 4)]
        if curItem in chars[userId]["five-stars"]:
          chars[userId]["five-stars"][curItem][0] += 1
          chars[userId]["five-stars"][curItem][1].append(pity[userId][4])
        else:
          chars[userId]["five-stars"][curItem] = [1, [pity[userId][4]]]
        pity[userId][4] = 0
        return [curItem, 5]

      else:
        curItem = standardBanner5StarWeapons[randint(0, 9)]
        if curItem in weapons[userId]["five-stars"]:
          weapons[userId]["five-stars"][curItem][0] += 1
          weapons[userId]["five-stars"][curItem][1].append(pity[userId][4])
        else:
          weapons[userId]["five-stars"][curItem] = [1, [pity[userId][4]]]
        pity[userId][4] = 0
        return [curItem, 5]
    
    elif rng <= rate * 10 + 60 + pity[userId][5] or pity[userId][5] == 10:
      pullIsChar = True
      curRng = randint(1, 2)
      if curRng == 1:
        pullIsChar = False
      if pity[userId][7] == 2:
        pity[userId][7] = 0
        pullIsChar = False
      elif pity[userId][7] == -2:
        pity[userId][7] = 0
        pullIsChar = True
      else:
        if pullIsChar:
          #print("woiejf")
          if pity[userId][7] == 1:
            pity[userId][7] = 2
          else:
            pity[userId][7] = 1
        else:
          #print("wtf")
          if pity[userId][7] == -1:
            pity[userId][7] = -2
          else:
            pity[userId][7] = -1
      #print("pullIsChar: " + str(pullIsChar) + " pity: " + str(pity[userId][7]))
      pity[userId][5] = 0        
      if pullIsChar:
        curChar = standardBanner4StarsChars[randint(0, len(standardBanner4StarsChars) - 1)]
        if curChar in chars[userId]["four-stars"]:
          chars[userId]["four-stars"][curChar] += 1
        else:
          chars[userId]["four-stars"][curChar] = 1
        pullData[userId]["four-star-chars"] += 1
        return [curChar, 4] # get a standard banner 4 star char
      curWeapon = standardBanner4StarWeapons[randint(0, len(standardBanner4StarWeapons) - 1)]
      if curWeapon in weapons[userId]["four-stars"]:
        weapons[userId]["four-stars"][curWeapon] += 1
      else:
        weapons[userId]["four-stars"][curWeapon] = 1
      pullData[userId]["four-star-weapons"] += 1
      return [curWeapon, 4] # else get standard banner 4 star weapon
    
    else:
      curWeapon = threeStarWeapons[randint(0, len(threeStarWeapons) - 1)]
      if curWeapon in weapons[userId]["three-stars"]:
        weapons[userId]["three-stars"][curWeapon] += 1
      else:
        weapons[userId]["three-stars"][curWeapon] = 1
      pullData[userId]["three-star-weapons"] += 1
      return [curWeapon, 3]



  pity[userId][0] += 1
  pity[userId][1] += 1
  pullData[userId]["event-pulls"] += 1
  rate = 1.6
  if pity[userId][0] == 90:
    rate = 100
  elif pity[userId][0] > 75:
    rate = (pity[userId][0] - 75) * 6 + 1.6
  rng = randint(1, 1000)
  if rng <= rate * 10: # 5 star
    if not pity[userId][2]:
      rng = randint(1, 2)
      if rng == 1: # winning 50/50
        if charName in chars[userId]["five-stars"]:
          chars[userId]["five-stars"][charName][0] += 1
          chars[userId]["five-stars"][charName][1].append(pity[userId][0])
        else:
          chars[userId]["five-stars"][charName] = [1, [pity[userId][0]]]
        pullData[userId]["five-star-chars"] += 1
        pity[userId][0] = 0
        return [charName, 5]
      else: # losing 50/50
        pity[userId][2] = True
        curLoss = standardBanner5StarsChars[randint(0, 4)]
        if curLoss in chars[userId]["five-stars"]:
          chars[userId]["five-stars"][curLoss][0] += 1
          chars[userId]["five-stars"][curLoss][1].append(pity[userId][0])
        else:
          chars[userId]["five-stars"][curLoss] = [1, [pity[userId][0]]]
        pity[userId][0] = 0
        pullData[userId]["five-star-chars"] += 1
        pullData[userId]["50/50 losses"] += 1
        return [curLoss, 5]
    else:
      if charName in chars[userId]["five-stars"]:
        chars[userId]["five-stars"][charName][0] += 1
        chars[userId]["five-stars"][charName][1].append(pity[userId][0])
      else:
        chars[userId]["five-stars"][charName] = [1, [pity[userId][0]]]
      pity[userId][0] = 0
      pity[userId][2] = False
      pullData[userId]["five-star-chars"] += 1
      return [charName, 5]
  elif rng <= rate * 10 + 60 + pity[userId][1] or pity[userId][1] == 10: # 4 star
    if not pity[userId][3]:
      rng = randint(1, 2)
      if rng == 1:
        pity[userId][1] = 0
        curChar = eventFourStarChars[charName][randint(0, 2)]
        if curChar in chars[userId]["four-stars"]:
          chars[userId]["four-stars"][curChar] += 1
        else:
          chars[userId]["four-stars"][curChar] = 1
        pullData[userId]["four-star-chars"] += 1
        return [curChar, 4]
      else:
        pity[userId][1] = 0
        pity[userId][3] = True
        rng = randint(1, 11)
        if rng <= 5:
          curChar = standardBanner4StarsChars[randint(0, len(standardBanner4StarsChars) - 1)]
          if curChar in chars[userId]["four-stars"]:
            chars[userId]["four-stars"][curChar] += 1
          else:
            chars[userId]["four-stars"][curChar] = 1
          pullData[userId]["four-star-chars"] += 1
          return [curChar, 4] # get a standard banner 4 star char
        curWeapon = standardBanner4StarWeapons[randint(0, len(standardBanner4StarWeapons) - 1)]
        if curWeapon in weapons[userId]["four-stars"]:
          weapons[userId]["four-stars"][curWeapon] += 1
        else:
          weapons[userId]["four-stars"][curWeapon] = 1
        pullData[userId]["four-star-weapons"] += 1
        return [curWeapon, 4] # else get standard banner 4 star weapon
    else:
      pity[userId][1] = 0
      pity[userId][3] = False
      curChar = eventFourStarChars[charName][randint(0, 2)]
      if curChar in chars[userId]["four-stars"]:
        chars[userId]["four-stars"][curChar] += 1
      else:
        chars[userId]["four-stars"][curChar] = 1
      pullData[userId]["four-star-chars"] += 1
      return [curChar, 4]
  else:
    curWeapon = threeStarWeapons[randint(0, len(threeStarWeapons) - 1)]
    if curWeapon in weapons[userId]["three-stars"]:
      weapons[userId]["three-stars"][curWeapon] += 1
    else:
      weapons[userId]["three-stars"][curWeapon] = 1
    pullData[userId]["three-star-weapons"] += 1
    return [curWeapon, 3]
  


def createTenPull(userId, charName):
  global chars, weapons
  pullType = 3
  res = []
  for i in range (10):
    curPull = createOnePull(userId, charName)
    res.append(curPull[0])
    pullType = max(pullType, curPull[1])
    if curPull[0] in standardBanner4StarsChars or curPull[0] in standardBanner5StarsChars or curPull[0] in bannerPics:
      if curPull[0] in chars[userId]:
        chars[userId][curPull[0]] += 1
      else:
        chars[userId][curPull[0]] = 1
    else:
      if curPull[0] in weapons[userId]:
        weapons[userId][curPull[0]] += 1
      else:
        weapons[userId][curPull[0]] = 1
  res.insert(0, pullType)
  return res



@client.slash_command(name = "banner", description = "opens the banner for a character for the wishing simulator", guild_ids = [1018416430619840563, 921229631175143435])
async def banner(interaction: nextcord.Interaction, char: str):
  global charData, inv, pity, bannerPics
  wishingMessage = None
  char = char.title()
  if char == "S":
    char = "Standard"
  if char == "Arataki" or char == "Arrataki" or char == "Aratakki" or char == "Arattaki" or char == "Arataki Itto" or char == "Arrataki Itto" or char == "Aratakki Itto" or char == "Arattaki Itto":
    char = "Itto"
  if char == "Barbatos":
    char = "Venti"
  if char == "Tartaglia":
    char = "Childe"
  if char == "Sangonomiya" or char == "Sangonomiya Kokomi" or char == "Koko":
    char = "Kokomi"
  if char == "Hutao":
    char = "Hu Tao"
  if char == "Kamisato Ayato":
    char = "Ayato"
  if char == "Kamisato Ayaka":
    char = "Ayaka"
  if char == "Yae":
    char = "Yae Miko"
  if char == "Raiden" or char == "Raiden Shogun" or char == "Raiden Shougun" or char == "Shougun" or char == "Ei" or char == "Raiden Ei" or char == "Shougun Ei" or char == "Shogun Ei":
    char = "Shogun"
  if char not in bannerPics:
    em = nextcord.Embed(color = 0x0080ff, title = "Error", description = "Either that character isn't a playable genshin character yet or they haven't been added to this bot.")
    await interaction.response.send_message(embed = em)
    return
  curTitle = ""
  if char == "Weapon":
    curTitle = "Weapon Banner"
  elif char == "Standard":
    rate = 0.6
    curTitle == "Standard Banner"
  else:
    curTitle = char + "'s Banner"
  em = nextcord.Embed(color = 0x0080ff, title = curTitle)
  em.set_image(url = bannerPics[char])

  curUser = str(interaction.user.id)

  pageNum = 0
  pulled = []

  onePullButton = Button(label = "1 Pull", style = ButtonStyle.blurple)
  tenPullButton = Button(label = "10 Pull", style = ButtonStyle.blurple)
  nextButton = Button(label = "next", style = ButtonStyle.green)
  skipButton = Button(label = "skip", style = ButtonStyle.red)

  async def onePullButtonPress(interaction):
    nonlocal char, curUser, nextButton, pulled, wishingMessage
    if str(interaction.user.id) != curUser:
      return
    pullRes = createOnePull(curUser, char)
    pulled = pullRes[0]
    pullType = pullRes[1]
    curView = View()
    curView.add_item(nextButton)
    em = createOnePullGif(pullType)
    pulled = [pulled]
    await wishingMessage.edit(embed = em, view = curView)
  
  async def tenPullButtonPress(interaction):
    nonlocal char, curUser, nextButton, skipButton, pulled, wishingMessage
    if str(interaction.user.id) != curUser:
      return
    pullRes = createTenPull(curUser, char)
    pullType = pullRes[0]
    pulled = pullRes[1:]
    curView = View()
    curView.add_item(nextButton)
    curView.add_item(skipButton)
    em = createTenPullGif(pullType)
    await wishingMessage.edit(embed = em, view = curView)
  
  async def nextButtonPress(interaction):
    nonlocal char, curUser, onePullButton, tenPullButton, pulled, curTitle, pageNum, wishingMessage
    if str(interaction.user.id) != curUser:
      return
    pageNum += 1
    if pageNum > len(pulled):
      if pageNum == 11:
        em = createPullOverviewPage(pulled)
        await wishingMessage.edit(embed = em)
      else:
        pageNum = 0
        em = nextcord.Embed(color = 0x0080ff, title = curTitle)
        em.set_image(url = bannerPics[char])
        curView = View(timeout = 60)
        curView.add_item(onePullButton)
        curView.add_item(tenPullButton)
        await wishingMessage.edit(embed = em, view = curView)
    else:
      em = createItemPage(pulled[pageNum - 1], len(pulled), pageNum)
      await wishingMessage.edit(embed = em)
  
  async def skipButtonPress(interaction):
    nonlocal char, curUser, onePullButton, tenPullButton, pulled, curTitle, pageNum, wishingMessage
    if str(interaction.user.id) != curUser:
      return
    pageNum = 11
    em = createPullOverviewPage(pulled)
    await wishingMessage.edit(embed = em)

  
  onePullButton.callback = onePullButtonPress
  tenPullButton.callback = tenPullButtonPress
  nextButton.callback = nextButtonPress
  skipButton.callback = skipButtonPress

  curView = View(timeout = 60)
  curView.add_item(onePullButton)
  curView.add_item(tenPullButton)

  wishingMessage = await interaction.response.send_message(embed = em, view = curView)




@client.slash_command(name = "pity", description = "tells you how much pity you're at (event/weapon/standard)", guild_ids = [1018416430619840563, 921229631175143435])
async def banner(interaction: nextcord.Interaction, banner: str):
  global pity
  banner = banner.title()
  if banner == "E" or banner == "Event":
    if str(interaction.user.id) not in pity:
      await interaction.response.send_message("You are at 0 event banner pity!")
    await interaction.response.send_message("You are at " + str(pity[str(interaction.user.id)][0]) + " event banner pity!")
  elif banner == "S" or banner == "Standard":
    if str(interaction.user.id) not in pity:
      await interaction.response.send_message("You are at 0 standard banner pity!")
    await interaction.response.send_message("You are at " + str(pity[str(interaction.user.id)][4]) + " standard banner pity!")
  elif banner == "W" or banner == "Weapon":
    await interaction.response.send_message("That banner hasn't been added yet.")
  else:
    await interaction.response.send_message("That's not a valid banner!")


def createFiveStarCharsPage(userId, cLow, cHigh):
  global chars, pullData
  em = nextcord.Embed( color = 0x0080ff, title = "Five Star Characters")
  c = 0
  for char in chars[userId]["five-stars"]:
    c += 1
    if c >= cLow and c <= cHigh:
      curString = str(c) + ". " + char + " c" + str(min(chars[userId]["five-stars"][char][0] - 1, 6))
      if chars[userId]["five-stars"][char][0] > 7:
        curString += " (" + str(chars[userId]["five-stars"][char][0] - 7) + " extra)"
      curString2 = "Pity Obtained: "
      curLen = len(chars[userId]["five-stars"][char][1])
      for i in range (curLen):
        curString2 += str(chars[userId]["five-stars"][char][1][i])
        if i != curLen - 1:
          curString2 += ", "
      em.add_field(name = curString, value = curString2)
  em.set_footer(text = "Page " + str((cLow + 4) // 5) + " of " + str((pullData[userId]["five-star-chars"] + 4) // 5))
  return em

def createFourStarCharsPage(userId, cLow, cHigh):
  global chars, pullData
  em = nextcord.Embed( color = 0x0080ff, title = "Four Star Characters")
  c = 0
  for char in chars[userId]["four-stars"]:
    c += 1
    if c >= cLow and c <= cHigh:
      curString = str(c) + ". " + char + " c" + str(min(chars[userId]["four-stars"][char] - 1, 6))
      curString2 = ""
      if chars[userId]["four-stars"][char] > 7:
        curString2 += " (" + str(chars[userId]["four-stars"][char] - 7) + " extra)"
      else:
        curString2 = "0 extra"
      em.add_field(name = curString, value = curString2)
  em.set_footer(text = "Page " + str((cLow + 4) // 5) + " of " + str((pullData[userId]["four-star-chars"] + 4) // 5))
  return em



@client.slash_command(name = "chars", description = "shows you a list of your characters", guild_ids = [1018416430619840563, 921229631175143435])
async def banner(interaction: nextcord.Interaction):
  global chars, pullData
  charsMessage = ""
  curUser = str(interaction.user.id)
  curLow = 0
  curHigh = 10
  totalPity = 0
  pullCount = 0
  overviewString = ""
  if curUser not in chars:
    overviewString = "You haven't made any pulls yet!"
  else:
    if pullData[curUser]["five-star-chars"] == 0:
      averagePity = "N/A"
    else:
      for char in chars[curUser]["five-stars"]:
        for res in chars[curUser]["five-stars"][char][1]:
          totalPity += res
          pullCount += 1
      averagePity = round(totalPity / pullCount, 2)
    overviewString = "Total Standard Pulls: " + str(pullData[curUser]["standard-pulls"]) + "\nTotal Event Pulls: " + str(pullData[curUser]["event-pulls"]) + "\n5 Star Characters: " + str(pullData[curUser]["five-star-chars"]) + "\n4 Star Characters: " + str(pullData[curUser]["four-star-chars"]) + "\n50/50s Lost: " + str(pullData[curUser]["50/50 losses"])
    overviewString += "\nAverage Pity for 5 Star: " + str(averagePity)
  
  fiveStarCharsButton = Button(label = "Five Stars", style = ButtonStyle.blurple)
  fourStarCharsButton = Button(label = "Four Stars", style = ButtonStyle.blurple)
  backButton = Button(label = "back", style = ButtonStyle.green)
  previousFiveStarsButton = Button(label = "<", style = ButtonStyle.blurple)
  nextFiveStarsButton = Button(label = ">", style = ButtonStyle.blurple)
  previousFourStarsButton = Button(label = "<", style = ButtonStyle.blurple)
  nextFourStarsButton = Button(label = ">", style = ButtonStyle.blurple)

  async def fiveStarCharsPress(interaction):
    nonlocal charsMessage, curLow, curHigh, previousFiveStarsButton, nextFiveStarsButton, backButton, curUser
    if str(interaction.user.id) != curUser:
      return
    curLow = 1
    curHigh = 5
    em = createFiveStarCharsPage(curUser, curLow, curHigh)
    curView = View(timeout = 60)
    curView.add_item(backButton)
    curView.add_item(previousFiveStarsButton)
    curView.add_item(nextFiveStarsButton)
    charsMessage = await interaction.edit(embed = em, view = curView)
  
  async def fourStarCharsPress(interaction):
    nonlocal charsMessage, curLow, curHigh, previousFourStarsButton, nextFourStarsButton, backButton, curUser
    if str(interaction.user.id) != curUser:
      return
    curLow = 1
    curHigh = 5
    em = createFourStarCharsPage(curUser, curLow, curHigh)
    curView = View(timeout = 60)
    curView.add_item(backButton)
    curView.add_item(previousFourStarsButton)
    curView.add_item(nextFourStarsButton)
    charsMessage = await interaction.edit(embed = em, view = curView)
  
  async def fiveStarsPreviousPress(interaction):
    nonlocal charsMessage, curLow, curHigh, curUser
    if str(interaction.user.id) != curUser:
      return
    if curLow == 1:
      return
    curLow -= 5
    curHigh -= 5
    em = createFiveStarCharsPage(curUser, curLow, curHigh)
    charsMessage = await interaction.edit(embed = em)
  
  async def fiveStarsNextPress(interaction):
    nonlocal charsMessage, curLow, curHigh, curUser
    if str(interaction.user.id) != curUser:
      return
    if curHigh >= pullData[curUser]["five-star-chars"]:
      return
    curLow += 5
    curHigh += 5
    em = createFiveStarCharsPage(curUser, curLow, curHigh)
    charsMessage = await interaction.edit(embed = em)
  
  async def fourStarsPreviousPress(interaction):
    nonlocal charsMessage, curLow, curHigh, curUser
    if str(interaction.user.id) != curUser:
      return
    if curLow == 1:
      return
    curLow -= 5
    curHigh -= 5
    em = createFourStarCharsPage(curUser, curLow, curHigh)
    charsMessage = await interaction.edit(embed = em)
  
  async def fourStarsNextPress(interaction):
    nonlocal charsMessage, curLow, curHigh, curUser
    if str(interaction.user.id) != curUser:
      return
    if curHigh >= pullData[curUser]["four-star-chars"]:
      return
    curLow += 5
    curHigh += 5
    em = createFourStarCharsPage(curUser, curLow, curHigh)
    charsMessage = await interaction.edit(embed = em)
  
  async def backButtonPress(interaction):
    nonlocal charsMessage, curLow, curHigh, overviewString, curUser
    if str(interaction.user.id) != curUser:
      return
    curLow = 1
    curHigh = 10
    em = nextcord.Embed(color = 0x0080ff, title = "Characters", description = overviewString)
    curView = View(timeout = 60)
    curView.add_item(fiveStarCharsButton)
    curView.add_item(fourStarCharsButton)
    charsMessage = await interaction.edit(embed = em, view = curView)
    

  fiveStarCharsButton.callback = fiveStarCharsPress
  fourStarCharsButton.callback = fourStarCharsPress

  previousFiveStarsButton.callback = fiveStarsPreviousPress
  nextFiveStarsButton.callback = fiveStarsNextPress
  previousFourStarsButton.callback = fourStarsPreviousPress
  nextFourStarsButton.callback = fourStarsNextPress
  backButton.callback = backButtonPress

  curView = View(timeout = 60)

  curView.add_item(fiveStarCharsButton)
  curView.add_item(fourStarCharsButton)

  em = nextcord.Embed(color = 0x0080ff, title = "Characters", description = overviewString)

  charsMessage = await interaction.response.send_message(embed = em, view = curView)



client.run("")