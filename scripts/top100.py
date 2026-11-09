import pandas as pd
import glob
import os

# After running this program and doing some simple stats :)
# Pink Floyd is 13.64% of my top 100 listening (2,993 / 21,957 plays)
# Statistically, I'm listening to them every 8th song

# --- Get top 100 artists ----------------------------

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)

PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

def get_top_artists(limit=100):

    files = sorted(glob.glob(os.path.join(PROCESSED_DIR, 'Streaming_History_Audio_*.json')))

    # Load and merge all JSON files into a consolidated DataFrame
    all_dfs = []
    for f in files:
        df = pd.read_json(f)
        all_dfs.append(df)
    df = pd.concat(all_dfs, ignore_index=True) 

    # Tally occurrences of each artists and keeping the top 100 results
    top_artists = df['master_metadata_album_artist_name'].value_counts().head(limit)

    return top_artists

if __name__ == '__main__':
    print("\nTop 100 artists:")
    
    top_artists = get_top_artists()

    # Iterate through the top artists and print a numbered list of play counts
    rank = 1
    for artist, plays in top_artists.items():
        print(f"{rank}. {artist} -- {plays} plays")
        rank += 1
