# UEFA Team Match Statistics Visualized
A small project where EURO Season 2020 match data is scraped off the web and re-organized for visualization in Gephi. Individual nodes, their colour and sizes represents a team, the tournament round they reached and the extent of the particular perfomance metric (Ex. Avg Possession %). Each edge represents a game played, while the direction of the edge points towards the team that won the match.

<p align="center">
  <img width="450" height="337" src="https://i.imgur.com/hNvSfzR.png">
</p>

# Match Statistics
The data from this project was taken from [UEFA.com](https://www.uefa.com/uefaeuro/history/seasons/2020/). The config.py file contains the piece of code that creates the links. The BeautifulSoup4, aiohttp and asyncio modules were used to asynchronously issue requests and extract data from each match played in the tournament.
