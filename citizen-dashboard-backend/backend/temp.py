import pandas as pd

# Load the CSV file
df = pd.read_csv('citizen-dashboard-backend/backend/items_data.csv')

# Sluggify all titles (make lowercase and underscored)
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# Make data in columns speakers, origin and summary into string by extracting the value of key 'default'
def extract_default_value(json_string):
    try:
        json_object = eval(json_string)
        return json_object.get('default', '')
    except Exception as e:
        return ''

df['speakers'] = df['speakers'].apply(extract_default_value)
df['origin'] = df['origin'].apply(extract_default_value)
df['summary'] = df['summary'].apply(extract_default_value)

# Remove the unnamed_0 column
df = df.drop('unnamed:_0', axis=1)

# Save the modified DataFrame to a new CSV file
df.to_csv('citizen-dashboard-backend/backend/modified_items_data.csv', index=False)