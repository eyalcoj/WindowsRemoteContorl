def find_changes_between_lists(list1, list2):
    # Convert lists to sets
    set1 = set(list1)
    set2 = set(list2)

    # Find added and removed items
    added = list(set2 - set1)   # Elements in list2 but not in list1
    removed = list(set1 - set2) # Elements in list1 but not in list2

    return added, removed