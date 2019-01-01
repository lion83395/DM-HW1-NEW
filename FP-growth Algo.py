import time
def load_data_set():
    
    data_set1 = [['0', '6', '7', '8', '9'],
               ['4', '5', '6', '8'],
               ['0', '7'],
               ['4', '6', '7', '8'],
               ['0', '5', '7', '8', '9'],
               ['0', '1', '3', '4', '5', '7', '8','9'],
               ['2','3','5','6','7','9'],
               ['0','3','4','5','6','8']]
    data_set =[['6','38','47','49','55','63','67','69','74','78','83'],
               ['8','34','50','71'],
               ['36','45','51','52','61','62','63'],
               ['7','17','35','36','39','41','42','52','53','55','73','81','85','87'],
               ['9','11','18','35','38','42','63','69','81','93','97'],
               ['8','21','25','39','40','43','59','80'],
               ['7','8','10','14','38','60','69','83','85','93'],
               ['8','17','36','38','43','63','83'],
               ['8','38','45','57','62','73','85'],
               ['0','7','11','12','15','23','26','29','46','50','63','73','85','86','91','92']]
   
      
                
    return data_set


def transfertoFrozenDataSet(data_set):
    frozenDataSet = {}
    for elem in data_set:
        frozenDataSet[frozenset(elem)] = 1
    return frozenDataSet


class TreeNode:
    def __init__(self, nodeName, count, nodeParent):
        self.nodeName = nodeName
        self.count = count
        self.nodeParent = nodeParent
        self.nextSimilarItem = None
        self.children = {}

    def increaseC(self, count):
        self.count += count


def createFPTree(frozenDataSet, minSup):
    
    headPointTable = {}
    for items in frozenDataSet:
        for item in items:
            headPointTable[item] = headPointTable.get(item, 0) + frozenDataSet[items]
    headPointTable = {k:v for k,v in headPointTable.items() if v >= minSup}
    frequentItems = set(headPointTable.keys())
    if len(frequentItems) == 0: return None, None

    for k in headPointTable:
        headPointTable[k] = [headPointTable[k], None]
    fptree = TreeNode("null", 1, None)
    
    for items,count in frozenDataSet.items():
        frequentItemsInRecord = {}
        for item in items:
            if item in frequentItems:
                frequentItemsInRecord[item] = headPointTable[item][0]
        if len(frequentItemsInRecord) > 0:
            orderedFrequentItems = [v[0] for v in sorted(frequentItemsInRecord.items(), key=lambda v:v[1], reverse = True)]
            updateFPTree(fptree, orderedFrequentItems, headPointTable, count)

    return fptree, headPointTable


def updateFPTree(fptree, orderedFrequentItems, headPointTable, count):
    
    if orderedFrequentItems[0] in fptree.children:
        fptree.children[orderedFrequentItems[0]].increaseC(count)
    else:
        fptree.children[orderedFrequentItems[0]] = TreeNode(orderedFrequentItems[0], count, fptree)

        if headPointTable[orderedFrequentItems[0]][1] == None:
            headPointTable[orderedFrequentItems[0]][1] = fptree.children[orderedFrequentItems[0]]
        else:
            updateHeadPointTable(headPointTable[orderedFrequentItems[0]][1], fptree.children[orderedFrequentItems[0]])
    
    if(len(orderedFrequentItems) > 1):
        updateFPTree(fptree.children[orderedFrequentItems[0]], orderedFrequentItems[1::], headPointTable, count)


def updateHeadPointTable(headPointBeginNode, targetNode):
    while(headPointBeginNode.nextSimilarItem != None):
        headPointBeginNode = headPointBeginNode.nextSimilarItem
    headPointBeginNode.nextSimilarItem = targetNode
 

def getPrefixPath(headPointTable, headPointItem):
    prefixPath = {}
    beginNode = headPointTable[headPointItem][1]
    prefixs = ascendTree(beginNode)
    if((prefixs != [])):
        prefixPath[frozenset(prefixs)] = beginNode.count

    while(beginNode.nextSimilarItem != None):
        beginNode = beginNode.nextSimilarItem
        prefixs = ascendTree(beginNode)
        if (prefixs != []):
            prefixPath[frozenset(prefixs)] = beginNode.count
    return prefixPath


def mineingFPTree(headPointTable, prefix, frequentPatterns, minSup):
   
    headPointItems = [v[0] for v in sorted(headPointTable.items(), key = lambda v:v[1][0])]
    if(len(headPointItems) == 0): return

    for headPointItem in headPointItems:
        newPrefix = prefix.copy()
        newPrefix.add(headPointItem)
        support = headPointTable[headPointItem][0]
        frequentPatterns[frozenset(newPrefix)] = support

        prefixPath = getPrefixPath(headPointTable, headPointItem)
        if(prefixPath != {}):
            conditionalFPtree, conditionalHeadPointTable = createFPTree(prefixPath, minSup)
            if conditionalHeadPointTable != None:
                mineingFPTree(conditionalHeadPointTable, newPrefix, frequentPatterns, minSup)


def ascendTree(treeNode):
    prefix = []
    while((treeNode.nodeParent != None) and (treeNode.nodeParent.nodeName != 'null')):
        treeNode = treeNode.nodeParent
        prefix.append(treeNode.nodeName)
    return prefix


def removeString(set, str):
    tempSet = []
    for elem in set:
        if(elem != str):
            tempSet.append(elem)
    tempFrozenSet = frozenset(tempSet)
    return tempFrozenSet


def GenerateRule(frequentPatterns, minConf, rules):
    for frequentset in frequentPatterns:
        if(len(frequentset) > 1):
            getttRules(frequentset,frequentset, rules, frequentPatterns, minConf)


def getttRules(frequentset,currentset, rules, frequentPatterns, minConf):
    for frequentElem in currentset:
        subSet = removeString(currentset, frequentElem)
        confidence = frequentPatterns[frequentset] / frequentPatterns[subSet]
        if (confidence >= minConf):
            flag = False
            for rule in rules:
                if(rule[0] == subSet and rule[1] == frequentset - subSet):
                    flag = True
            if(flag == False):
                rules.append((subSet, frequentset - subSet, confidence))

            if(len(subSet) >= 2):
                getttRules(frequentset, subSet, rules, frequentPatterns, minConf)


if __name__=='__main__':
    starttime = time.time()
    data_set = load_data_set()
    frozenDataSet = transfertoFrozenDataSet(data_set)
    minSupport = 3
    fptree, headPointTable = createFPTree(frozenDataSet, minSupport)
  
    frequentPatterns = {}
    prefix = set([])
    mineingFPTree(headPointTable, prefix, frequentPatterns, minSupport)
    print("frequent patterns:","           ","support")
    print("=" *50)
    for item in frequentPatterns:
        print(item,"            ",frequentPatterns[item])
    print("=" *50)
    print("\n")
    minConf = 0.5
    rules = []
    GenerateRule(frequentPatterns, minConf, rules)
   
    print("association rules:")
    print("=" *50)
    for rule in rules :
        print(rule)
    print("=" *50)
    endtime =  time.time()
    print("It takes %d milliseconds to find the above patterns" %((endtime-starttime) * 1000))