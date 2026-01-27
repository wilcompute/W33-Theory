import pandas as pd

df = pd.read_csv(r'C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data\_v23\v23\Q_triangles_with_centers_Z2_S3_fiber6.csv')

print('Max index in u:', df['u'].max())
print('Max index in v:', df['v'].max())
print('Max index in w:', df['w'].max())
print('Min index:', min(df['u'].min(), df['v'].min(), df['w'].min()))
print()
print('Sample rows:')
print(df[['u', 'v', 'w', 'centers']].head(10))
print()
print('Centers column type:', df['centers'].dtype)
print('Sample centers values:')
print(df['centers'].head(10).values)
