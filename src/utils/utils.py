def find_changes_between_lists(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    added = list(set2 - set1)
    removed = list(set1 - set2)

    return added, removed