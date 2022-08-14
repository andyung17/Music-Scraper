from pyppeteer import launch
from bs4 import BeautifulSoup
from items import Item
import asyncio
import re
import os 

async def pyppeteer_test(songnameInput):
    print('about to launch pyppeteer')
    browser = await launch(defaultViewPort=None,handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    print('about to launch pyppeteer')
    page = await browser.newPage()
    await page.goto("https://aniplaylist.com/", timeout=1000000)
    await page.waitForSelector('input[id=songSearch]')
    await page.click('input[id=songSearch]')
    await page.goto("https://aniplaylist.com/" + songnameInput, timeout=1000000)
    print('browser launched!')
    soup = BeautifulSoup(await page.content(), 'html.parser')
    await browser.close()
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)

async def get_song_data(songnameInput):
    sampleString = await pyppeteer_test(songnameInput)
    sampleString = sampleString[sampleString.find('Show more Clear filters'):]

    sampleStringList= re.split(', |/|-|!', sampleString)

    resultList = []

    # Filtering out the non song entries
    for i in sampleStringList:
        if i.find('by') != -1:
            resultList.append(i)
    print(resultList)

    animeName = []
    songType = []
    songName = []
    artistCreator = []
    songPlatform = []


    for i in resultList:
        if i.find('Opening') != -1:
            track = 0
            temp = 0
            for character in i[:i.find('Opening') - 1]:
                track+=1
                if(character.isalpha() == True and temp == 0):
                    temp = track 
            if(i.find("Clear filters") != -1):
                temp = i.find("Clear filters") + 14
            animeName.append(i[temp:i.find('Opening') - 1])
            songType.append('OP')
            i = ''.join([x for x in i if not x.isdigit()])
            i = re.sub(' +', ' ', i)
            if(i.find('(ep') != -1):
                nameIndex = i.find(')')
                songName.append(i[nameIndex + 1: i.find('by') - 1])
            else:
                songName.append(i[i.find('Opening') + 11: i.find('by') - 1])
            
            i = ''.join([x for x in i if not x.isdigit()])
            i = re.sub(' +', ' ', i)

            if(i.find('Spotify') != -1):
                songPlatform.append("Spotify")
                artistCreator.append(i[i.find('by') + 3: i.find('Spotify') - 1])
            elif(i.find('Apple Music') != -1):
                songPlatform.append("Apple Music")
                artistCreator.append(i[i.find('by') + 3: i.find('Spotify') - 1])
            else:
                songPlatform.append("Other")
                artistCreator.append('Unknown')

            i = ''.join([x for x in i if not x.isdigit()])
            print(i)

        elif i.find('Ending') != -1:
            track = 0
            temp = 0
            for character in i[:i.find('Ending') - 1]:
                track+=1
                if(character.isalpha() == True and temp == 0):
                    temp = track 
            if(i.find("Clear filters") != -1):
                temp = i.find("Clear filters") + 14
            animeName.append(i[temp:i.find('Ending') - 1])
            songType.append('ED')
            i = ''.join([x for x in i if not x.isdigit()])
            i = re.sub(' +', ' ', i)
            if(i.find('(ep') != -1):
                nameIndex = i.find(')')
                songName.append(i[nameIndex + 2: i.find('by') - 1])
            else:
                songName.append(i[i.find('Ending') + 10: i.find('by') - 1])
            if(i.find('Spotify') != -1):
                songPlatform.append("Spotify")
                artistCreator.append(i[i.find('by') + 3: i.find('Spotify') - 1])
            elif(i.find('Apple Music') != -1):
                songPlatform.append("Apple Music")
                artistCreator.append(i[i.find('by') + 3: i.find('Spotify') - 1])
            else:
                songPlatform.append("Other")
                artistCreator.append('Unknown')
            
    data = {
        'animeName': animeName,
        'songType': songType,
        'songName': songName,
        'artistCreator': artistCreator,
        'songPlatform': songPlatform
    }

    return data


