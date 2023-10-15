import pandas as pd

column_names = [
    'name', 'landmass', 'zone', 'area', 'population', 'language', 'religion',
    'bars', 'stripes', 'colours', 'red', 'green', 'blue', 'gold', 'white', 'black',
    'orange', 'mainhue', 'circles', 'crosses', 'saltires', 'quarters', 'sunstars',
    'crescent', 'triangle', 'icon', 'animate', 'text', 'topleft', 'botright'
]

df = pd.read_csv('flag.data', names=column_names)
landmass_names = {
    1: 'N.America',
    2: 'S.America',
    3: 'Europe',
    4: 'Africa',
    5: 'Asia',
    6: 'Oceania'
}
df['landmass_name'] = df['landmass'].map(landmass_names)
print(df.columns)
print(df['colours'])
# print(df['landmass_name'].value_counts(normalize=True))
# print(df.value_counts(normalize=True))
# df.groupby()