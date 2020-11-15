#%%
def places_summary(places):
    total_place = len(places)
    places_name = [place["name"] for place in places]

    print("Simple Summary Report")
    print("-" * 10)
    print(f"Total of {total_place} places.")
    print(f"Places: {places_name}")
    print('-' * 10 + '\n')

# %%
