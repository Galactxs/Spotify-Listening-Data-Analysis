import pandas as pd
import os
import glob

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)

PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

def random_song(skip_filter: str = "any"):

    '''
    filter options:
        "any" = all songs regardless of if skipped or not
        "skipped = songs where skipped = True
        "played" = songs wheere skipped = False
    '''

    files = sorted(glob.glob(os.path.join(PROCESSED_DIR, 'Streaming_History_Audio_*.json')))

    all_df = []
    for f in files:
        df = pd.read_json(f)
        all_df.append(df)
    combined_df = pd.concat(all_df, ignore_index=True)

    combined_df = combined_df.drop_duplicates(subset=["master_metadata_track_name","master_metadata_album_artist_name"])

    if skip_filter == "skipped":
        combined_df = combined_df[combined_df["skipped"] == True]
    elif skip_filter == "played":
        combined_df = combined_df[combined_df["skipped"] == False]

    if combined_df.empty:
        print(f"no songs found in filter: '{skip_filter}'")
        return None
    
    song = combined_df.sample(1).iloc[0]

    return {
        "track": song.get("master_metadata_track_name", "Unknown Track"),
        "artist": song.get("master_metadata_album_artist_name"),
        "skipped": song.get("skipped")
    }


if __name__ == "__main__":
    print("filter options: any, skipped, played")
    user_input = input("show songs that were: (any | skipped | played)").strip().lower()

    if user_input not in ("any", "skipped", "played"):
        print("invalid option. Defauting to any")
        user_input = "any"
    
    result = random_song(skip_filter=user_input)

    if result:
        if result["skipped"]:
            status = "skipped"
        else:
            status = "played"
        print(f"\n{result['track']} by {result['artist']}")

    

