import pandas as pd

# Read the original CSV file into a DataFrame
df = pd.read_csv('NetflixViewingHistory.csv')

# Split the "Title" column into separate columns for "Title," "Subtitle," and "Season"
split_titles = df['Title'].str.split(':', expand=True)
df['Title'] = split_titles[0].str.strip()
df['Subtitle'] = split_titles[1].str.strip() if len(split_titles.columns) > 1 else None
df['Season'] = split_titles[2].str.strip() if len(split_titles.columns) > 2 else None

# Drop duplicates to keep only unique base titles
unique_df = df.drop_duplicates(subset=['Title'])

# Drop the "Date" column
unique_df = unique_df.drop(columns=['Date'])

# Define the keywords to remove
keywords = ["Episodio", "Temporada", "Season", "Parte", "Part", "Vol.", "Capítulo", "Chapter", "Miniserie"]

# Remove keywords from 'Subtitle' and 'Season' columns
for keyword in keywords:
    unique_df.loc[unique_df['Subtitle'].str.contains(keyword, na=False), 'Season'] = ''
    unique_df['Subtitle'] = unique_df['Subtitle'].str.replace(keyword, '', regex=False)
    unique_df['Season'] = unique_df['Season'].str.replace(keyword, '', regex=False)

# Remove numbers from 'Subtitle' and 'Season' columns
unique_df['Subtitle'] = unique_df['Subtitle'].str.replace('\d+', '', regex=True)
unique_df['Season'] = unique_df['Season'].str.replace('\d+', '', regex=True)

# Merge the modified 'Subtitle' and 'Season' column strings with the unmodified 'Title' Column
unique_df['Title'] = unique_df['Title'] + ' ' + unique_df['Subtitle'].fillna('') + ' ' + unique_df['Season'].fillna('')

# Keep only the 'Title' column
unique_df = unique_df[['Title']]


# Save the new CSV file
unique_df.to_csv('titles.csv', index=False)

# Get the 'Title' column as a list
titles = unique_df['Title'].tolist()
# Print each title with a counter
for i, title in enumerate(titles, start=1):
    print(f"{i}. {title}")
input("Press Enter to continue...")
