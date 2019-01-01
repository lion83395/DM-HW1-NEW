import time
def load_data_set():
    """data set from IBM Quest Synthetic Data Generator"""
    data_set = [['0', '6', '7', '8', '9'],
               ['4', '5', '6', '8'],
               ['0', '7'],
               ['4', '6', '7', '8'],
               ['0', '5', '7', '8', '9'],
               ['0', '1', '3', '4', '5', '7', '8','9'],
               ['2','3','5','6','7','9'],
               ['0','3','4','5','6','8']]

    return data_set


def create_C1(data_set):
    """ C1:存放所有1 item set"""
    C1 = set()
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1


def is_apriori(Ck_item, Lksub1):
    """測試是否滿足apriori property"""
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True


def create_Ck(Lksub1, k):
    """產生item set"""
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck


def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    """把Ck轉成Lk"""
    Lk = set()
    item_count = {}
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk


def generate_L(data_set, k, min_support):
    
    support_data = {}
    C1 = create_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k+1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data


def generate_big_rules(L, support_data, min_conf):
    """找出association rules"""
    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list


if __name__ == "__main__":
    starttime = time.time()
    data_set = load_data_set()
    L, support_data = generate_L(data_set, k=3, min_support=0.3)
    big_rules_list = generate_big_rules(L, support_data, min_conf=0.5)
    for Lk in L:
        print ("=" *50)
        print ("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
        print ("=" *50)
        for freq_set in Lk:
            print (freq_set,"            " ,support_data[freq_set])
        print("\n")
    
    print ("association rules")
    for item in big_rules_list:
        print (item[0], "=>", item[1], "confidence: ", item[2])
    endtime =  time.time()
    print("It takes %d milliseconds to find the above patterns" %((endtime-starttime) * 1000))