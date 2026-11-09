import os
import glob
import pandas as pd

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)

PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

def get_top_songs(limit=100):

    files = sorted(glob.glob(os.path.join(PROCESSED_DIR, 'Streaming_History_Audio_*.json')))

    all_df = []
    for f in files:
        df = pd.read_json(f)
        all_df.append(df)
    df = pd.concat(all_df, ignore_index=True)

    top_song = df['master_metadata_track_name'].value_counts().head(limit)

    return top_song

if __name__ == '__main__':
    print("\nTop 100 songs:")

    top_song = get_top_songs()

    rank = 1
    for song, plays in top_song.items():
        print(f"{rank}, {song} -- {plays} plays")
        rank += 1 

