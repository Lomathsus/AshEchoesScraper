from mwclient import Site


def get_all_categories():
    wiki = Site("wiki.biligame.com/bjhl", path="/")
    categories = wiki.allcategories()
    for category in categories:
        print(category.name)


get_all_categories()
