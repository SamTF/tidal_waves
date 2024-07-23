# Tidal Waves
**Tidal Waves** is a Discord bot that displays tidal information for a particular beach. It shows:
- the time of the high and low tides
- the height of the tides
- current weather conditions
- current time

## Output
There are 3 ways in which **Tidal Waves** displays information. These are:
- a dynamically generated image (PNG)
- an embed
- a standard text message

## Usage
`/tide [spot] [time_period] [type]`
1. `Spot` - Dropdown menu of available locations
2. `Time_period` - Today, Tomorrow, Weekly
3. `Type` - Image, Embed, Message

## Example
Examples of a given command and the corresponding output generated.

`/tide Comporta today image`

![Comporta](https://i.imgur.com/kdiSMKN.png)

The white needle represents the current time. The big number in the top right is the current weather at the location. These two pieces of data are only shown when fetching information for the current day/

`/tide Nazaré tomorrow image`

![Nazaré](https://i.imgur.com/OWfxTOy.png)

`/tide "São Pedro de Moel" today embed`

![São Pedro de Moel](https://i.imgur.com/bVPtjW6.png)

### See the commands LIVE in action:

![Animated GIF!!](https://i.imgur.com/z0XhgCr.gif)

## Spots
Since I am currently fetching the data by web-scraping (a free API is too limited, sadly), the locations for which **Tidal Waves** reports are pre-selected and not dynamic. If you would like me to add a particular beach, just let me know.

## Invite Link
[Invite the bot to your server!](https://discord.com/oauth2/authorize?client_id=457626744879448075&scope=bot&permissions=2147796992)
