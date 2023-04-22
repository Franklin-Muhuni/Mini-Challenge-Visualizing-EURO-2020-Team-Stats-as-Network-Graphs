# UEFA Team Match Statistics Visualized
A small project where EURO Season 2020 match data is scraped off the web and re-organized for visualization in Gephi. Individual nodes and their sizes represents a team and the extent of the particular perfomance metric (Ex. Avg Possession %).
# Match Statistics
The data from this project was taken from [UEFA.com](https://www.uefa.com/uefaeuro/history/seasons/2020/). The config.py file contains the piece of code that creates the links. The BeautifulSoup4, aiohttp and asyncio modules were used to asyncronously issue requests and extract data from each match played in the tournament.
