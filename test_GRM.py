
'Test GRM : top k=10 recommendation items that a user actual purchased / a users all purchased items'

# test users that actually purchased = each test user has m edge with the k items
def GRM_match(G, top10_df, test_users):
    m_list = []  
    for u in test_users:
        m = 0  # Initialize m for each user
        for i in top10_df['Item']:  # Access 'Item' column in top10_df
            if G.has_edge(u, i):
                m += 1
        m_list.append(m)  
    return m_list

# total number of items each test_user purchased
def GRM_total(G, test_users) :
    t_list = []
    for u in test_users:
        if G.has_node(u) :
            t_list.append(G.degree(u))
        
        else:
            t_list.append(0)
    return t_list


        


