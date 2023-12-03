import pandas as pd
import numpy as np
import networkx as nx
from random import seed, random
import matplotlib.pyplot as plt

df = pd.read_csv('./Magazine_Subscriptions.csv', names=['asin', 'reviewerID', 'overall', 'unixReviewTime'])
from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(df, test_size=0.1, random_state=42)

train_edges = []
test_edges = []

train_users = set()
test_users = set()

items = set()

for index, row in train_set.iterrows():
  items.add(row['asin'])
  train_edges.append((row['asin'], row['reviewerID']))
  train_users.add(row['reviewerID'])

for index, row in test_set.iterrows():
  items.add(row['asin'])
  test_edges.append((row['asin'], row['reviewerID']))
  test_users.add(row['reviewerID'])

G = nx.Graph()
G.add_nodes_from(train_users, bipartite=0)
G.add_nodes_from(items, bipartite=1)
G.add_edges_from(train_edges)


'GRM : sort all objects in descending order of degree and recommend with highest degrees'

# Get the nodes in the items partition
items_nodes = [node for node in G.nodes if G.nodes[node]['bipartite'] == 1]

# Calculate degrees for nodes in the items partition
item_degrees = nx.degree(G, items_nodes)

# Convert to a dictionary if needed
item_degrees_dict = dict(item_degrees)

# Print or use the DataFrame
df = pd.DataFrame(list(item_degrees_dict.items()), columns=['Item', 'Degree'])

# Sort the DataFrame in descending order of degree
df = df.sort_values(by='Degree', ascending=False)

k=10
top10_df = df.head(10)
# print(top10_df)

from test_GRM import GRM_match
result_m_list = GRM_match(G, top10_df, test_users)
print(result_m_list[:50])

from test_GRM import GRM_total
result_total_items = GRM_total(G, test_users)
print(result_total_items[:50])


' only keep test_users with items >= 3 '
# create a data frame with test_user, result_m_list, result_total_list
# if result_total_list < 3 then disregard test_user

test_users_list = list(test_users)
data = {
    'user': test_users_list,
    'desired': result_m_list,
    'total': result_total_items
}

GRM_df = pd.DataFrame(data)
GRM_df_3 = GRM_df[GRM_df['total'] >= 3]
print(GRM_df_3)


'evaluation by averaging all users ratios'
GRM_df_3['ratio'] = GRM_df_3['desired'] / GRM_df_3['total']
score = sum(GRM_df_3['ratio']) / len(GRM_df_3['ratio'])
print(score)

'number of test users '
num_users_total_less_than_3 = (GRM_df['total'] < 3).sum()
print(f"Number of users with total purchases less than 3: {num_users_total_less_than_3}")
