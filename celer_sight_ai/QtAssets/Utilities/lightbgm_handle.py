import numpy as np
import cv2
import time
# from catboost import CatBoostClassifier


def run():
    # find_best_filter()
    # return
    fg1 = cv2.imread('img_2/forground.png',cv2.IMREAD_GRAYSCALE)
    bg1 = cv2.imread('img_2/background.png',cv2.IMREAD_GRAYSCALE)
    img = cv2.imread('img_2/img.png')
    model = train_light_model(img,fg1, bg1, lr= 0.5 ,\
         rand_samples=0.5, n_estimators = 80, reduce_by=2 )
    # model = train_model(img,fg1, bg1, lr= 0.01 , rand_samples=4000, n_estimators = 80, reduce_by=1 )
    return

    img_tiles = getTiles(img , img.shape[0]//2 , img.shape[1]//2)
    bg1_tiles = getTiles(bg1 , bg1.shape[0]//2 , bg1.shape[1]//2)
    fg1_tiles = getTiles(fg1 , fg1.shape[0]//2 , fg1.shape[1]//2)
    for i in range(len(img_tiles)):
        img_tile = img_tiles[i]
        model = train_model(img_tiles[i],fg1_tiles[i], bg1_tiles[i], lr= 0.5 ,  n_estimators = 80, reduce_by=2 )
        return


def find_best_filter():
    fg1 = cv2.imread('img_2/forground.png',cv2.IMREAD_GRAYSCALE)
    bg1 = cv2.imread('img_2/background.png',cv2.IMREAD_GRAYSCALE)
    img = cv2.imread('img_2/img.png')
    filters = ['doGabor','doSobel','doLaplace','doGradient','doVariance']

    combinations = []
    import itertools as it
    for i in range(len(filters)-1):
        for x in it.combinations(filters,i):
            if len(x)>0:
                filters_use ={
                    'doGabor' :'doGabor' in x,
                    'doSobel' :'doSobel' in x,
                    'doLaplace' :'doLaplace' in x,
                    'doGradient' :'doGradient' in x,
                    'doVariance' :'doVariance' in x
                }
                # model = train_model(img,fg1, bg1, lr= 0.5 ,\
                #     rand_samples=0.5, n_estimators = 80, reduce_by=1,
                #     doGabor = filters['doGabor'],doSobel =  filters['doSobel'],\
                #         doLaplace =  filters['doLaplace'],doGradient= filters['doGradient'] , doVariance = filters['doVariance'])

def getTiles(im, tile_H, tile_W):
    M = tile_H
    N = tile_W
    tiles = [im[x:x+M,y:y+N] for x in range(0,im.shape[0],M) for y in range(0,im.shape[1],N)]
    return tiles

# def iterate_runs():

#     accuracies = []
#     samples = []
#     times = []
#     lrs = []
#     lr_range = [0.5]#, 0.1, 0.05, 0.01]#, 0.005, 0.001]
#     #runn many modes and record 
#     for lr in lr_range:
#         for i in range(3000 ,28000 ,1000):
#             acc1 , time1 = run_model(lr= lr ,  n_estimators = 80 , rand_samples =i)
#             accuracies.append(acc1)
#             times.append(time1)
#             samples.append(i)
#             lrs.append(lr)

#             # df2 = pd.DataFrame([acc1 ,time1 ,  i , lr], columns=list('AB'), index=['acc', 'time' , 'samples', 'lr'])
#     ind = np.argsort(samples)

#     accuracies =  np.array(accuracies)#[ind]
#     samples =  np.array(samples)#[ind]
#     times =  np.array(times)#[ind]
#     lrs =  np.array(lrs)#[ind]
#     data = {
#             'accuracies': accuracies,
#             'samples' : samples,
#             'times' : times,
#             'lrs' : lrs
#     }
#     df = pd.DataFrame(data,columns=['accuracies',  'samples',  'times', 'lrs'])

#     # print("sampleas are {} , accuracies are {}".format(samples ,accuracies ))
#     plot(data)
#     return

def plot(data):
    import matplotlib.pyplot as plt
    plt.style.use('classic')
    import seaborn as sns
    sns.set()
    # same plotting code as above!
    # plt.plot(x, y)
    sns.lineplot(data=data, palette="tab10", linewidth=2.5,x="samples", y="accuracies",hue='lrs')
    # plt.legend('ABCDEF', ncol=2, loc='upper left');
    plt.show()
    sns.boxplot(x="lrs", y="times", data=data)
    plt.show()

def train_light_model(img , fg1, bg1, lr= 0.1 , n_estimators = 80,\
     rand_samples = None ,reduce_by= 1 ,doGabor =True,doSobel =  True,\
              doLaplace = True,doGradient= True , doVariance = True):

    from sklearn.model_selection import train_test_split


    fg1 = cv2.resize(fg1,(fg1.shape[0]//reduce_by , fg1.shape[1]//reduce_by))
    bg1 = cv2.resize(bg1,(bg1.shape[0]//reduce_by , bg1.shape[1]//reduce_by))
    img = cv2.resize(img,(img.shape[0]//reduce_by , img.shape[1]//reduce_by))
    
    fg1 = fg1>1
    bg1 = bg1>1


    #create ml canvas labels:
    ml_label_canvas = np.zeros((img.shape[0],img.shape[1]), dtype = np.uint8)
    ml_label_canvas[fg1] = 2
    ml_label_canvas[bg1] = 1

    img_channels = []
    for i in range(3):
        img_channels.append(img[:,:,i])

    df = prep_1ch(img_channels,ml_label_canvas )
    import time
    if doGabor:
        start = time.time()
        df = featureGabor(img_channels ,df ,MODE='dirty' )
        df = df.run()
        print("gabor takes ", time.time()- start)
    if doSobel:
        start = time.time()
        df = featureSobel(img_channels ,df ,MODE='normal' )
        df = df.run()
        print("featureSobel takes ", time.time()- start)

    if doLaplace:
        start = time.time()
        df = featureGaussianLaplace(img_channels ,df ,MODE='dirty' )
        df = df.run()
        print("featureGaussianLaplace takes ", time.time()- start)

    if doGradient:
        start = time.time()
        df = featureGaussianGradientMagnitude(img_channels ,df ,MODE='dirty' )
        df = df.run()
        print("featureGaussianGradientMagnitude takes ", time.time()- start)

    if doVariance:
        start = time.time()
        df = featureVarianceFilter(img_channels ,df ,MODE='dirty' )
        df = df.run()
        print("featureVarianceFilter takes ", time.time()- start)


    df = df[(df.labels == 1) | (df.labels == 2)]
    if rand_samples != None:
        print("samples are ",rand_samples)
        chosen_idx = np.random.choice(df.shape[0]-1, replace=False, size=int(rand_samples*df.shape[0]))
        df = df.iloc[chosen_idx]


    print("dataframe shape ", df.shape)
    labels = df.pop("labels")
    df_array_X = df.to_numpy()

    df_array_X, df_array_X_val, labels, labels_val = train_test_split(df_array_X, labels, test_size=0.1, random_state=42)
    # df_array_X_t, df_array_X, labels_t, labels = train_test_split(df_array_X, labels, test_size=0.1, random_state=42)


    # labels = df_array_X.pop("labels")
    # df_array_X = df_array_X.to_numpy()
    fit_params={
                "early_stopping_rounds":3, 
                "eval_metric" : 'logloss', 
                "eval_set" : [(df_array_X_val,labels_val)],
                'eval_names': ['valid'],
                'verbose': 100,
                'feature_name': 'auto', # that's actually the default
                'categorical_feature': 'auto' # that's actually the default
            }

    num_round = 20
    import time
    start = time.time()
    max_depth = 10
    # clf = CatBoostClassifier( iterations=5)
    import lightgbm as lgb
    clf = lgb.LGBMClassifier(num_leaves=int(( 2^(max_depth))*0.65), max_depth=max_depth,  #LGBMClassifier
                            random_state=314, 
                            silent=True, 
                            metric='None', 
                            n_jobs=4, 
                            n_estimators=n_estimators,
                            colsample_bytree=0.9,
                            subsample=0.9,
                            learning_rate=lr)
    print('dataframe shape before fit ',df_array_X.shape)
    bst = clf.fit(df_array_X, labels)#, **fit_params)
    # bst = lgb.train(param, train_data, num_round)
    ml_label_canvas = np.zeros((img.shape[0],img.shape[1]), dtype = np.uint8)
    print('training took ', time.time() - start)

    img_channels = []
    for i in range(3):
        img_channels.append(img[:,:,i])

    # pred = model.predict_proba(x)[:,1]>0.7
    df = prep_1ch(img_channels,ml_label_canvas )
    labels = df.pop("labels")

    gaborF = featureGabor(img_channels ,df ,MODE='dirty')
    df = gaborF.run()
    df_array_X = df.to_numpy()
    # print(ypred)
    start = time.time()
    # ypred = model.predict_proba(df_array_X)


    loss = getLoss(bst , df_array_X_val, labels_val )
    time_took = time.time() - start
    print("prediction took : ",time_took)
    if loss == None:
        loss = 1
    # print("accuracy is {} and time is {}".format(acc1, time1))

    acc = getLoss(bst, df_array_X_val, labels_val)
    print("accuracy is ",acc)
    # ypred_prob = ypred[:,0]
    # ypred = ypred[:,1]
    # ypred = ypred.reshape(img.shape[0], img.shape[1])
    # cv2.imshow('ypred' ,((ypred>0.75)*250).astype(np.uint8))
    # cv2.waitKey()


def getLoss(model,x,y):
    pred = model.predict_proba(x)[:,1]>0.7
    from sklearn.metrics import accuracy_score
    pred = pred +1
    accuracy=accuracy_score(y, pred)
    # print("accuracy is ", accuracy)
    return accuracy
def prep_1ch(img,labels):
    import pandas as pd
    #Save original image pixels into a data frame. This is our Feature #1.
    # img_1d = img.reshape(-1)
    labels_1d = labels.reshape(-1)

    df = pd.DataFrame()
    df['labels'] = labels_1d
    df['img_r'] = img[2].reshape(-1)
    df['img_g'] = img[1].reshape(-1)
    df['img_b'] = img[0].reshape(-1)

    return df 


#try fitting and measure time for each dataset size starting from zero

def hyperparameter_search():

    from scipy.stats import randint as sp_randint
    from scipy.stats import uniform as sp_uniform
    param_test ={'num_leaves': sp_randint(6, 50), 
                'min_child_samples': sp_randint(100, 500), 
                'min_child_weight': [1e-5, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4],
                'subsample': sp_uniform(loc=0.2, scale=0.8), 
                'colsample_bytree': sp_uniform(loc=0.4, scale=0.6),
                'reg_alpha': [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
                'reg_lambda': [0, 1e-1, 1, 5, 10, 20, 50, 100]}
    #This parameter defines the number of HP points to be tested
    n_HP_points_to_test = 100

    import lightgbm as lgb
    from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

    #n_estimators is set to a "large value". The actual number of trees build will depend on early stopping and 5000 define only the absolute maximum
    clf = lgb.LGBMClassifier(max_depth=-1, random_state=314, silent=True, metric='None', n_jobs=4, n_estimators=5000)




class featureGabor():
    def __init__(self,channels = None, orgDf = None ,MODE = 'normal'):
        self.orgDf = orgDf
        self.type = 'Gabor'
        self.num = 0
        self.channels = channels
        self.computeChannels = [True,True,True]
        if MODE == 'normal':
            self.normal()
        elif MODE == 'dirty':
            self.dirty()
        elif MODE == 'quality':
            self.quality()
    def dirty(self):
        self.lambdaRange = [0, 2]
        self.thetaRange = [1,3,4,6]
        self.sigmaRange = [0.1]
        self.gammaRange = [None]
        self.kernalSizeRange = [9]
    def normal(self):
        self.lambdaRange = [0, 1,2]
        self.thetaRange = [1,2,3,4,5,6]
        self.sigmaRange = [0.1]
        self.gammaRange = [None]
        self.kernalSizeRange = [9]
    def quality(self):
        self.lambdaRange = [0, 1,2]
        self.thetaRange = [1,2,3,4,5,6]
        self.sigmaRange = [0.1]
        self.gammaRange = [None]
        self.kernalSizeRange = [7,9,11]

    def thetaNormalize(self,theta):
        return theta/ 4. * np.pi

    def lambdaNormalize(self,lam):
        return lam * (np.pi/2)
    def run(self):
        self.num = 0
        for i in range(len(self.channels)):
            if self.computeChannels[i]:
                for kernalSizeRange in self.kernalSizeRange:
                    for sigmaRange in self.gammaRange:
                        for thetaRange in self.thetaRange:
                            for lambdaRange in self.lambdaRange:
                                
                                kernel = cv2.getGaborKernel((kernalSizeRange, kernalSizeRange), 2, self.thetaNormalize(thetaRange), self.lambdaNormalize(lambdaRange), sigmaRange, ktype=cv2.CV_32F)   
                                self.orgDf[self.type +str(self.num)] = cv2.filter2D(self.channels[i], cv2.CV_8UC3, kernel).reshape(-1)
                                self.num +=1
        return self.orgDf




class featureSobel():
    def __init__(self,channels = None, orgDf = None,MODE = 'quality'):
        self.orgDf = orgDf
        self.type = 'Sobel'
        self.num = 0
        self.channels = channels
        self.computeChannels = [True,True,True]

        if MODE == 'normal':
            self.normal()
        elif MODE == 'dirty':
            self.dirty()
        elif MODE == 'quality':
            self.quality()
    def dirty(self):
        self.sigmaRange = [1]
    def normal(self):
        self.sigmaRange = [0, 2]

    def quality(self):
        self.sigmaRange = [0, 1,2]

    def run(self):
        for i in range(3):
            self.orgDf[self.type +str(self.num)] = _Sobel(self.channels[i]).reshape(-1)
        return self.orgDf

def _Sobel(im):
    from scipy import ndimage
    dx = ndimage.sobel(im, 0)  # horizontal derivative
    dy = ndimage.sobel(im, 1)  # vertical derivative
    mag = np.hypot(dx, dy)  # magnitude
    
    myMax = np.max(mag)
    if myMax == None or myMax == 0:
        return mag
    mag *= 255.0 / np.max(mag)  # normalize (Q&D)

    return mag


class featureGaussianLaplace():
    def __init__(self,channels = None, orgDf = None,MODE = 'quality'):
        self.orgDf = orgDf
        self.type = 'GaussianLaplace'
        self.num = 0
        self.channels = channels
        self.computeChannels = [True,True,True]
        self.sigmaRange = [0, 1,2,3,4,5]
        if MODE == 'normal':
            self.normal()
        elif MODE == 'dirty':
            self.dirty()
        elif MODE == 'quality':
            self.quality()


    def dirty(self):
        self.sigmaRange = [0, 3]
    def normal(self):
        self.sigmaRange = [0, 2,3,5]

    def quality(self):
        self.sigmaRange = [0, 1,2,3,4,5]

    def sigmaNormalize(self,sigma):
        return 0.5*(sigma+1)

    def run(self):
        from scipy import ndimage
        self.num = 0
        for i in range(len(self.channels)):
            if self.computeChannels[i]:
                for sigmaRange in self.sigmaRange:
                    
                    self.orgDf[self.type +str(self.num)]  = cv2.normalize(ndimage.gaussian_laplace(self.channels[i], sigma=self.sigmaNormalize(sigmaRange)), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U).reshape(-1)
                    self.num+=1
        return self.orgDf


class featureGaussianGradientMagnitude():
    def __init__(self,channels = None, orgDf = None,MODE = 'quality'):
        self.orgDf = orgDf
        self.type = 'GaussianGradientMagnitude'
        self.num = 0
        self.channels = channels
        self.computeChannels = [True,True,True]
        self.sigmaRange = [0, 1,2,3,4,5]
        if MODE == 'normal':
            self.normal()
        elif MODE == 'dirty':
            self.dirty()
        elif MODE == 'quality':
            self.quality()
    def dirty(self):
        self.sigmaRange = [0, 3]
    def normal(self):
        self.sigmaRange = [0,1, 3,5]

    def quality(self):
        self.sigmaRange = [0, 1,2,3,4,5]

    def sigmaNormalize(self,sigma):
        return 2*(sigma+1)

    def run(self):
        from scipy import ndimage
        self.num = 0
        for i in range(len(self.channels)):
            if self.computeChannels[i]:
                for sigmaRange in self.sigmaRange:

                    self.orgDf[self.type +str(self.num)] = cv2.normalize(ndimage.gaussian_gradient_magnitude(self.channels[i], sigma=self.sigmaNormalize(sigmaRange)), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U).reshape(-1)
                    self.num+=1
        return self.orgDf


class featureVarianceFilter():
    def __init__(self,channels = None, orgDf = None, MODE = 'quality'):
        self.orgDf = orgDf
        self.type = 'VarianceFilter'
        self.num = 0
        self.channels = channels
        self.computeChannels = [True,True,True]
        self.sigmaRange = [0, 1,2]
        if MODE == 'normal':
            self.normal()
        elif MODE == 'dirty':
            self.dirty()
        elif MODE == 'quality':
            self.quality()
    def dirty(self):
        self.sigmaRange = [2]
    def normal(self):
        self.sigmaRange = [0,1, 3,4]

    def quality(self):
        self.sigmaRange = [0, 1,2,3,4,5]

    def sigmaNormalize(self,sigma):
        return ((sigma*2)+1)*3

    def run(self):
        self.num = 0
        for i in range(len(self.channels)):
            if self.computeChannels[i]:
                for sigmaRange in self.sigmaRange:

                    self.orgDf[self.type +str(self.num)] = cv2.normalize(self.variance_filter(self.channels[i],self.sigmaNormalize(sigmaRange)), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U).reshape(-1)
                    self.num+=1
        return self.orgDf

    def variance_filter(self, img, VAR_FILTER_SIZE ):
        """
        this filter is usefull for getting scratch features
        """
        from scipy import ndimage

        img = img.astype(np.float)

        rows, cols = img.shape[0], img.shape[1]
        win_rows, win_cols = VAR_FILTER_SIZE, VAR_FILTER_SIZE
        win_mean = ndimage.uniform_filter(img, (win_rows, win_cols))
        win_sqr_mean = ndimage.uniform_filter(img**2, (win_rows, win_cols))
        win_var = win_sqr_mean - win_mean**2
        return win_var

if __name__ == '__main__':
    run()