import matplotlib.pyplot as plt
import glob
import os
from sklearn.metrics import classification_report
import math

with open(os.path.join("C:\\Users\\30698\\Desktop\\τεχνητη\\aclImdb\\imdb.vocab" ), 'r',encoding="utf8") as h:
        m=0
        n=0
        voc=list()
        for line in h:
            m=m+1
            n=n+1
            l=line.split()
            voc.append(l[0])


class Review:
    def __init__(self,t):
        self.words=[]
        self.type=t      #1 if positive -1 if negative

class Node:

    def __init__(self, posC, negC):
        self.posC = posC
        self.negC = negC
        self.word = None
        self.true = None
        self.false = None
        self.result = None

def Entropy(cprob):
    if (cprob==0 or cprob==1):
        return 0.0
    else:
        return - (cprob * math.log(cprob,2)) - ((1.0-cprob)*math.log(1.0-cprob,2))

def calculateIG(pos,neg,word):#i tha yparxoyn genika kapoia apo ayta kai den tha xreaiazetai na ta perasoume
    pc1=len(pos)/(len(pos)+len(neg))
    HC=Entropy(pc1)
    """"
    px1 # p(X=1) ->prob of x=1  p(x=0) -> 1-P(x=1)
    
    pc1x1 #p(c=1|x=1)   p(c=0|x=1) = 1-p(c=1|x=1)
    
    pc1x0 #p(c=1|x=0)   p(c=0|x=0) = 1-p(c=1|x=0)
    
    HCX1  # H(C=1|X=1)
    
    HCX0  #H(C=1|X=0) entropies na kseroume oti to x=1 kai x=0 antistoixa
    """
    
    cX1 =0         #count the examples in which this feature x= 1
    cC1X1=0        #count how many examples are c=1 given x=1
    cC1X0=0        #count how many examples are c=1 given x=0 
    
    #gia kathe example
    
    #an i leksi yparxei sto example cX1+=1
    
   # an i leksi yparxei sto example kai einai pos cC1X1+=1
    
    #an i leksi den yparxei sto example kai einai pos c1X0+=1
    
    examples=len(pos) + len(neg)
    
    for posReview in pos:
        if word in posReview.words:
            cX1+=1
            cC1X1+=1
        else:
            cC1X0+=1
    
    for negReview in neg:
        if word in negReview.words:
            cX1+=1
            
    
    px1 = cX1 / examples
    
    if cX1==0:
        pc1x1=0.0
    else: 
        pc1x1= cC1X1 / cX1
    
    if (cX1 == examples):
        pc1x0=0.0
    else:
        pc1x0= cC1X0 / (examples - cX1)
        
    
    HCX1 = Entropy(pc1x1)
    HCX0 = Entropy(pc1x0)
    
    IG= HC - ((px1 * HCX1) + ((1.0-px1)*HCX0))
    
    return IG

def MaxGain(posRev,negRev,features):
    maxGainWord=None
    maxGain=-1
    for word in features:
        gain=calculateIG(posRev,negRev,word)
        if gain > maxGain:
            maxGain=gain
            maxGainWord=word
    return maxGainWord

def classify(review):
    curNode = root
    result = None
    nodenumb=0
    while curNode != None:
        result = curNode.result
        if curNode.word in review:
            curNode = curNode.true
            nodenumb+=1
        else:
            curNode = curNode.false
            nodenumb+=1
       
    return result

def test():
    
    posC = negC = 0
    right=0
    all_lines=0
    test_score=list()
    test_results=list()
    filename="C:\\Users\\30698\\Desktop\\τεχνητη\\aclImdb\\test\\labeledBow.feat"
    with open(os.path.join(filename), 'r',encoding="utf8") as f:
        for line in f:
            all_lines+=1
            s=line.replace(":"," ")
            #line_words=()
            line_words=s.split()
            review=[]
            if(int(line_words[0])>=7):
                right_answer=1
                
            else:
                right_answer=-1
            for i in range(1,len(line_words)):
                if (i%2==1):
                    review.append(voc[int(line_words[i])])
            result=classify(review)
            if result==right_answer:
                right+=1
            test_score.append(right_answer)
            test_results.append(result)

    return right/all_lines,test_score,test_results

class ID3Tree:
    #def create(self,paradeigmata,pred,idiotites):
    def create(self,pos,neg,features,pred):
        node=Node(pos,neg)
       
        if(len(pos)==0 and len(neg)==0):
            node.result=pred
            return node
        elif(len(pos)>( (90.0*(len(pos)+len(neg)))/100 )):
            node.result=1
            return node
        elif(len(neg)>( (90.0*(len(pos)+len(neg)))/100 )):
            node.result=-1
            return node
        elif(len(pos)==0):
            node.result=-1
            return node
        elif(len(neg)==0):
            node.result=1
            return node
        elif (len(features)==0):
            if(len(pos)>len(neg)):
                node.result=1
                return node
            else:
                node.result=-1
                return node
        bestFeature=MaxGain(pos,neg,features)
        node.word=bestFeature
        
        if (len(pos)>len(neg)):
            node.result=1
            d=1
        else:
            node.result=-1
            d=-1
            
        
        posFeature1=[]
        negFeature1=[]
        posFeature0=[]
        negFeature0=[]
        
        for posReview in pos:
            if bestFeature in posReview.words:
                posFeature1.append(posReview)
            else:
                posFeature0.append(posReview)
                
        for negReview in neg:
            if bestFeature in negReview.words:
                negFeature1.append(negReview)
            else:
                negFeature0.append(negReview)
                
        features.remove(bestFeature)
        nextFeatures=features
        
        node.true=self.create(posFeature1,negFeature1,nextFeatures,d)
        node.false=self.create(posFeature0,negFeature0,nextFeatures,d)
        
        return node

def train(filename):
    trainPosData=[]
    trainNegData=[]
    with open(os.path.join(filename), 'r',encoding="utf8") as f:
        for line in f:
            s=line.replace(":"," ")
            #line_words=()
            line_words=s.split()
            if int(line_words[0])>=7:
                type=1      #positive review
            else:
                type=-1     #negative review   
            
            reviewData=Review(type)
            for i in range(1,len(line_words)):
                if (i%2==1):                           #se autes tis theseis vriskontai oi aritmoi twn leksewn pou antistoixoyn sto vocabulary pou iparxoun sto keimeno
                    word=voc[int(line_words[i])]    
                    reviewData.words.append(word)
            if type==1:
                trainPosData.append(reviewData)
            else:
                trainNegData.append(reviewData)

        return (trainPosData,trainNegData)

filepath="C:\\Users\\30698\\Desktop\\τεχνητη\\aclImdb\\train\\labeledBow.feat"
#uniqueWords = []
pos , neg = train(filepath)

x_axis=[100,1000,5000,10000,22000]
train_accuracy=[]
test_accuracy=[]
round=0
for d in x_axis:
    print("STARTING TRAINING, ROUND: ",round+1)
    data=int(d/2)
    trainpos=pos[:data]
    trainneg=neg[:data]
    hc=Entropy(len(trainpos)/(len(trainpos)+len(trainneg)))
    print("id3")
    branchcount=0
    tree=ID3Tree()
    selectedFeatures=list()
    #seed(18)
    for i in range(20,500):
        selectedFeatures.append(voc[i])
    root=tree.create(trainpos,trainneg,selectedFeatures,1)
    train_right=0
    train_score=list()
    results=list()
    for review in trainpos:
        result=classify(review.words)
        if(result==1):
            train_right+=1
        results.append(result)
        train_score.append(1)
    for reviewneg in trainneg:
        result=classify(reviewneg.words)
        if(result==-1):
            train_right+=1
        results.append(result)
        train_score.append(-1)
    accuracy=train_right/(data*2)
    print("TRAINING CLASSIFICATION REPORT WITH |||",x_axis[round],"||| ","TRAINING DATA BELOW")
    
    print(classification_report(train_score, results,zero_division=0))
    train_accuracy.append(accuracy)
    #print(rights/(data*2))
    devPos=pos[data:int(data*1.1)]
    devNeg=pos[data:int(data*1.1)]
    maxn=0
    maxm=0
    maxRight=-1
    for n in range(20,150,30):
        for m in range(n+100,n+500,100):
            devRight=0
            selectedFeatures=list()
            for j in range(n,m):
                selectedFeatures.append(voc[j])
            root=tree.create(trainpos,trainneg,selectedFeatures,1)
            for devPosReview in devPos:
                if(classify(devPosReview.words)==1):
                    devRight+=1

            for devNegReview in devNeg:
                if(classify(devNegReview.words)==1):
                    devRight+=1

            if devRight>maxRight:
                maxRight=devRight
                maxn=n
                maxm=m
            #print("Accuracy on n=",n," and m=",m," :",devRight/(0.1*data*2) )
    print("N WHICH WILL BE SENT FROM DEV TO TRAIN IS: ", maxn)
    print("M WHICH WILL BE SENT FROM DEV TO TRAIN IS: ", maxm)
    print("MAXIMUM ACCURACY ON DEV DATA IS: ",maxRight/(0.1*data*2))
    for i in range (maxn,maxm):
        selectedFeatures.append(voc[i])
    root=tree.create(trainpos,trainneg,selectedFeatures,1)
    test_acc,test_score,test_results=test()
    print("MAXIMUM ACCURACY ON TEST DATA FOR N=", maxn,", M=", maxm, " IS:",test_acc)
    test_accuracy.append(test_acc)
    print("TEST CLASSIFICATION REPORT WITH |||25000||| TEST DATA BELOW")    
    print(classification_report(test_score, test_results,zero_division=0))  
    round+=1

plt.xlabel('Dataset size')
plt.ylabel('TrainAccuracy')
plt.plot(x_axis,train_accuracy)
plt.savefig('trainAccuracyId3.png')

plt.xlabel('Dataset size')
plt.ylabel('TestAccuracy')
plt.plot(x_axis,test_accuracy)
plt.savefig('testAccuracyId3.png')
plt.show()