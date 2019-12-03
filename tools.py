from array import array
import pandas as pd
import numpy as np
#-----------------------------Neighborsfinder----------------
def getData(a,*args):
    if str(args) != '()':
        b = args[0]
        result = pd.read_csv(b)
        result = result.values[:,0]     #[:,1]
        data = pd.read_csv(a)
        A = data.values.tolist()
        return A, result
    else:
        data = pd.read_csv(a)
        A = data.values.tolist()
        return A


def nodfinder(A,i,m,N):
    count = 0
    for act in range(N):
        if (A[i][act] == 1):
            if(count == m):
                s = act+1
                return s
            count = count + 1

#return ACtion  for node i  according to p[i][ri]
def Action_selector(t,i,p,A,r, N):
    s = 0
    a0 = 0
    m=0
    rand = np.random.uniform(0, 1)
    for m in range ( 0, r[i]):
         if (a0 <= rand < a0 + p[t][i][m]):
            break
         else:
             a0 = a0+p[t][i][m]
         s = nodfinder(A,i,m,N)
    return s, m

def edgeounter(r,N):          #find number of edges
    degree = 0
    for i in range(N):
        degree = r[i]+degree
    return (degree/2)

def decoder(S, u, mVC, currentComponent):
    mVC[u] = currentComponent
    if mVC[ S[u] ] == 0:
        mVC[u] = decoder(S, S[u], mVC, currentComponent)
    else:
        mVC[u] = mVC[S[u]]
    return mVC[u]


def Q(mVC,A,edge,r,N):
    temp = 0
    for p in range(0,N):
        for q in range(0,N):
            if(mVC[p]==mVC[q]):
                temp= temp +( A[p][q] -( (r[p] * r[q]) / (2*edge)))

    Q=temp/(2*edge)
    return Q

def Eresponce(Q,Qbest,MVC,N,t,A,beta):
        for i in range(0,N):
            buf1 = MVC[t][i]
            c = 1            #raghavan
            cp = 0

            for k in range(N):
                if (A[i][k] == 1):
                    buf2 = MVC[t][k]
                    if (buf1 == buf2):
                        c = c + 1
                    else:
                        cp = cp + 1

            if( (Q>= Qbest) & (cp <= c) ):
                beta[t][i]=0        #reward

            else:
                beta[t][i]=1        #penalty
        return beta[t]


def update_Qbest( Qbest ,Qfinal, t):            # function for updating Q best according to env.response

    if(Qfinal[t]> Qbest):
       Qbest = Qfinal[t]
    return Qbest



# def update_wzd(i,m,beta,w,z,t,D,r,d):                          #func of updating W and Z          #stiiiillll neeed work**************
#     b = beta[t][i]             # bedoone for ham mishe nevesht
#     action= 0
#     for action in range(0,r[i]):
#         if ( m == action & b == 1 ):
#             w[i][m] = w[i][m]
#             z[i][m] = z[i][m]+1
#         if (m == action & b == 0):
#             w[i][m] = w[i][m] + 1
#             z[i][m] = z[i][m] + 1
#     d[i][m] = w[i][m] / (z[i][m]+ 0.000000000000000001)
#     # print ('action',action,'m',m,'rrrr',r[i])
#     maxv = max (d[i])
#     D[i] = d[i].index(maxv)    #index of the best action for this node after this action
#     return D[i] # q?action


def update_wzd(i,m,beta,w,z,t,D,r,d):                          #func of updating W and Z          #stiiiillll neeed work**************
    b = beta[t][i]# bedoone for ham mishe nevesht
    z[i][m] = z[i][m] + 1
    w[i][m] = w[i][m]+(1-b)
    # ------------------------------------------------
    #  tooo maghale soft detector meybodiii
    #  d[i]=w[i]./z[i]
    #------------------------------------------------
  #index of the best action for this node after this action
    return w[i],z[i] # q?action



def cprp_update(p,i,bestactionindex,t,alpharate,r):
    for action in range(r[i]):
        if ( bestactionindex != action):
            p[t + 1][i][action] = float((1 - alpharate) * p[t][i][action])
        if ( bestactionindex == action):
            p[t+1][i][bestactionindex]=float( p[t][i][bestactionindex]+ alpharate *(1 - p[t][i][bestactionindex]))


    return p[t+1][i]


# def Lpr_updatep(p,i):   #workkkkkkkkkkkk on this
#     rrr=r[i]
#               #M=1 mm=9
#     for action in range(rrr):
#         if ( beta[t][i]==0 & M == action):
#             # print('1111 condision')
#             print("beta isss",beta[t][i])
#             print('p t i m',t,i,M,'is:',p[t][i][M])
#             p[t+1][i][M]=float(p[t][i][M]+alpharate*(1-p[t][i][M]))
#
#             # print('p[t+1][i][action]:', p[t + 1][i][action])
#
#         if( beta[t][i]==0 & M!=action):
#             # print('2222 condision')
#             p[t+1][i][action]=float((1-alpharate)*p[t][i][action])
#
#         #-----------------------------PENALTY UPDTE
#
#         if (beta[t][i]==1 & action== M):
#             # print('item',(1 - betarate) * p[t][i][M])
#             p[t + 1][i][M] = float((1 - betarate) * p[t][i][M])
#             # print('3333 condision')
#
#         if(beta[t][i]==1 & action!= M):
#             # print('444 condision')
#             # print('p[t][i][action]:',t,i,p[t][i][action])
#             # print('item',(betarate/(rrr-1))+(1-betarate)*(p[t][i][action]))
#             p[t+1][i][action]=float((betarate/(rrr-1))+(1-betarate)*(p[t][i][action]))
#             # print('p[t+1][i][action]:', p[t+1][i][action])
#
#     # print('p is:',t+1,'for node i',i ,p[t+1][i])
#     return p[t+1][i]


def teminationcondition1(Qfinal,term1,t ):
    if(abs(Qfinal[t] - Qfinal[t-1])!= 0):
        term1=0
        return 1, term1
    else:
        term1 =1+ term1
        if( term1 >= 2000 ):
            return 0,term1
        else:
            return 1,term1


def deltacounter(MVC,N,t):
    delta=0
    for i in range(N):
        # print('mvc t n',MVC[t])
        # print('mvc t-1 n', MVC[t-1])
        if(MVC[t][i]!=MVC[t-1][i]):
            # print('in loop',MVC[t][i],MVC[t-1][i])
            delta=delta+1
            # print('detaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa is',delta)
    return delta

def teminationcondition2(Delta,term2,t ):

    if(Delta[t]!= 0):
        term2=0
        #print('delta is changing',Delta[t])           #uncomment later
        return 1, term2
    else:
        term2 =1+ term2
        if( term2 >= 100 ):
            return 0,term2
        else:
            return 1,term2



def lablematrixcreator(mvc):
    N=len(mvc)
    clstr=len(set(mvc))
    L=[[0] * clstr for i in range(N)]
    for n in range(0,N):
        L[n][mvc[n]-1]=1;

    #print(L)
    return L


#Purity ---- https://gist.github.com/jhumigas/010473a456462106a3720ca953b2c4e2
from sklearn.metrics import accuracy_score

def purity_score(y_true, y_pred):
    """Purity score

    To compute purity, each cluster is assigned to the class which is most frequent
    in the cluster [1], and then the accuracy of this assignment is measured by counting
    the number of correctly assigned documents and dividing by the number of documents.
    We suppose here that the ground truth labels are integers, the same with the predicted clusters i.e
    the clusters index.

    Args:
        y_true(np.ndarray): n*1 matrix Ground truth labels
        y_pred(np.ndarray): n*1 matrix Predicted clusters

    Returns:
        float: Purity score

    References:
        [1] https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html
    """
    # matrix which will hold the majority-voted labels
    y_voted_labels = np.zeros(y_true.shape)
    # Ordering labels
    ## Labels might be missing e.g with set like 0,2 where 1 is missing
    ## First find the unique labels, then map the labels to an ordered set
    ## 0,2 should become 0,1
    labels = np.unique(y_true)
    ordered_labels = np.arange(labels.shape[0])
    for k in range(labels.shape[0]):
        y_true[y_true == labels[k]] = ordered_labels[k]
    # Update unique labels
    labels = np.unique(y_true)
    # We set the number of bins to be n_classes+2 so that
    # we count the actual occurence of classes between two consecutive bin
    # the bigger being excluded [bin_i, bin_i+1[
    bins = np.concatenate((labels, [np.max(labels) + 1]), axis=0)

    for cluster in np.unique(y_pred):
        hist, _ = np.histogram(y_true[y_pred == cluster], bins=bins)
        # Find the most present label in the cluster
        winner = np.argmax(hist)
        y_voted_labels[y_pred == cluster] = winner

    return accuracy_score(y_true, y_voted_labels)

def normalize(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm


def softm(MVC,ov):
    MaxNumberComunities = max(set(MVC))
    T,N= np.size(MVC)
    softm = [[0] * N for row in range(MaxNumberComunities)

    for t in range(0,T):         #matrix cluster va node ha ro tashkil bedim
        for n in range(0,N):
            i= MVC[t][n];
            softm[i][n] = softm[i][n]+1;


    for k in range(0,N):             #normalize  kardan vector har node
        softm = normalize(softm[][k])

    Thresh=1/ov+1
    softm[softm > Thresh] = 1
    softm[softm < Thresh] = 0







     return softm;