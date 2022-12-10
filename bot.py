import discord
import wikipedia
import requests
import re
import key

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    
    # only respond to messages from other users (not the bot itself)
    if message.author == client.user:
        return

    # check if the message starts with the !wiki command
    if message.content.startswith("!wiki"):

        # get the query from the message
        query = message.content[6:]

        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
        }

        response = requests.get(key.endpoint, params=params)

        try:
            results = response.json()["query"]["search"]
            page_id = results[0]["pageid"]

            # use the wikipedia.search method to find articles on Wikipedia
            topresults = wikipedia.search(query)
            await message.channel.send('**Here are the top results for your search:**')
            arrayresults = []
            sentresults = ""
            for i in range(len(topresults)):
                arrayresults.append(str(int(i)+1) + '. ' + topresults[i])
            for i in range(len(arrayresults)):
                sentresults = sentresults + arrayresults[i] + "\n"
            await message.channel.send(sentresults)
        except:
            await message.channel.send('Your search term is not valid, or has no results on wikipedia. Try searching for a more specific or valid term.')

        # Prints the ID of the page searched on Python Console
        print('Page searched: ' + str(page_id))

        try:
            summary = wikipedia.page(pageid=page_id).summary

            # Use the regex pattern to search for and match the brackets and their contents
            pattern = re.compile(r"\(listen.*?\)")
            # Use the regex pattern to search for and match empty normal brackets
            pattern2 = re.compile(r"\(\s*\)")

            # Use the replace() method to remove the matched brackets and their contents
            summary = pattern.sub("", summary)
            # Use the replace() method to remove the matched empty brackets
            summary = pattern2.sub("", summary)

            await message.channel.send('**Displaying summary for the most relevant search result:**')

            # send the summary to the channel
            if len(summary)>2000:
                while len(summary)>1:
                    await message.channel.send(summary[:2000])
                    summary = summary[2000:]
            else:
                await message.channel.send(summary)
        except:
            await message.channel.send('Your search term leads to a disambiguation page or is not valid. Try searching for a more specific or valid term.')
       
client.run(key.token)
