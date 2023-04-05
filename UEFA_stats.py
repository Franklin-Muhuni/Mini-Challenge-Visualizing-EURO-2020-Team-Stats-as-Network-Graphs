
import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup as bs
from config import match_ids
from config import CACHE
from config import URL

async def get_html(session, match_id):
    url = f'{URL}{match_id}/'
    if url in CACHE:
        return CACHE[url]
    async with session.get(url) as response:
        text = await response.text()
        CACHE[url] = text
        return text

async def main():
    async with aiohttp.ClientSession() as session:
        match_df_list = []
        tasks = [get_html(session, match_id) for match_id in match_ids]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            soup = bs(response, 'html.parser')
            teams = soup.find_all('title')
            stats = soup.find_all('pk-list-stat-item', class_='js-live-stat')

            home_data = {'statistic': [], 'team': [], 'team_stats': []}
            away_data = {'statistic': [], 'team': [], 'team_stats': []}

            for stat in stats:
                home_data['statistic'].append(stat['label'])
                away_data['statistic'].append(stat['label'])
                home_data['team_stats'].append(stat['data'])
                away_data['team_stats'].append(stat['second-data'])
            for team in teams:
                match_team = team.text.split('|', 1)
                match_team = match_team[0].rstrip().split('-', 1)
                for _ in home_data['statistic']:
                    home_data['team'].append(match_team[0])
                    away_data['team'].append(match_team[1])

            home_match_df = pd.DataFrame.from_dict(home_data)
            if not home_match_df.empty:
                match_df_list.append(home_match_df)
            away_match_df = pd.DataFrame.from_dict(away_data)
            if not away_match_df.empty:
                match_df_list.append(away_match_df)

        matches_df = pd.concat(match_df_list, ignore_index=True)
        matches_df['team_stats'] = pd.to_numeric(matches_df['team_stats'], errors='coerce')

        stat_name = [r for r, _ in matches_df.groupby('statistic')['statistic']]
        team_stats = matches_df.groupby(['statistic', 'team'])['team_stats'].mean().reset_index()
        df_dict = {_: df for _, df in team_stats.groupby('statistic')}

        for i, stat_df in enumerate(df_dict.values()):
            stat_df['statistic'] = [*range(1, 25)]
            stat_df.rename(columns={'statistic': 'Id', 'team': 'Label', 'team_stats': 'Weight'}, inplace=True)
            stat_df.to_csv(f'{stat_name[i]}.csv', index=False)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())