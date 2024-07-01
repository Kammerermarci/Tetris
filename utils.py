def add_lists(list1,list2):
    result = []
    for sublist in list2:
        new_sublist = []
        for i in range(len(sublist)):
            new_sublist.append(list1[0][i] + sublist[i])
        result.append(new_sublist)
    return(result)

def add_same_lists(list1,list2):
    result = []
    for i in range(len(list1)):
        new_sublist = []
        for j in range(len(list1[i])):
            new_sublist.append(list1[i][j]+list2[i][j])
        result.append(new_sublist)
    return(result)

def substract_lists(list1,list2):
    result = []
    for sublist in list2:
        new_sublist = []
        for i in range(len(sublist)):
            new_sublist.append(sublist[i] - list1[0][i])
        result.append(new_sublist)
    return(result)