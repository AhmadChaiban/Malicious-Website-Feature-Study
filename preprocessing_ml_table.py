import pandas as pd
import numpy as np 
import sys
from tqdm import tqdm

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier


def make_columns_for_embs(features_scaled, name):
    feats_all_embdeddings = pd.DataFrame(features_scaled)

    all_embeddings_columns = []
    for i in range(len(feats_all_embdeddings.columns)):
        all_embeddings_columns.append(f'{name}_set_{i}')

    feats_all_embdeddings.columns = all_embeddings_columns
    
    return feats_all_embdeddings, all_embeddings_columns


def perform_pca(n_components, scaled_embeddings):
    pca = PCA(n_components=n_components, svd_solver='arpack')
    return pca.fit_transform(scaled_embeddings)


def scale_features(embeddings_to_scale):
    scaler = MinMaxScaler()
    return scaler.fit_transform(embeddings_to_scale)


def feature_selection(k, scaled_embeddings, name, df_surtur):
    
    """
    k: Integer, number of features to select
    scaled_embeddings: the scaled features to apply chi2 to. 
    name: string for naming the columns 
    
    """
    
    emb_new = SelectKBest(chi2, k=k).fit_transform(scaled_embeddings, df_surtur['label'])
    emb_new = pd.DataFrame(emb_new)

    emb_array = []
    for i in tqdm(range(len(emb_new.columns))):
         emb_array.append(f'{name}_emb_{i+20}')

    emb_new.columns = emb_array
    return emb_new


def make_classification(features_to_keep, df_surtur):
    
    """ 
    Takes the required columns as input into the dataset 
    and performs training and prediction with XGBoost.
    
    features_to_keep: list of strings
    
    """
    
    X = df_surtur[features_to_keep]
    X = X.drop(columns = ['label', 'content', 'hostname', 'url', 'js', 
                          'domain', 'google_is_safe', 'ip_address'])
    y = df_surtur['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=20)
    
    param_grid = {
                'min_child_weight': [1, 5, 10],
                'gamma': [1, 1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10],
                'subsample': [0.6, 0.8, 1.0],
                'colsample_bytree': [0.6, 0.8, 1.0],
                'max_depth': [3, 4, 5, 6, 7, 8, 9, 10],
                'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5],
                'n_estimators': [100, 120, 150, 165, 180, 200, 300, 1000],
                'tree_method': ['auto', 'exact', 'approx', 'hist', 'gpu_hist'],
                'booster': ['gbtree', 'gblinear', 'dart']
                
                }
    
#     xgboost_model = XGBClassifier(verbosity=0, 
#                               max_depth=7,
#                               min_child_weight=1,
#                               n_estimators=165,
#                               colsample_bylevel=1,
#                               colsample_bytree=1, 
#                               num_parallel_tree=1,
#                               learning_rate=0.3,
#                               tree_method='exact', 
#                               booster='dart',
#                               gamma=1e-10,
#                               alpha=0,
#                               scale_pos_weight= 1,  # 1.375520774687535,
#                               subsample=1,
#                               n_jobs=-1)

    xgboost_model = XGBClassifier()

    folds = 3
    param_comb = 5

    skf = StratifiedKFold(n_splits=folds, shuffle = True, random_state = 1001)
    
    random_search = RandomizedSearchCV(xgboost_model, 
                                       param_distributions=param_grid, 
                                       n_iter=param_comb, 
                                       scoring='roc_auc', 
                                       n_jobs=-1, 
                                       cv=skf.split(X_train,y_train), 
                                       verbose=3, 
                                       random_state=1001)

    random_search.fit(X_train, y_train)

    # xgboost_model.fit(X_train, y_train)
    
    # y_pred = xgboost_model.predict(X_test)

    y_pred_train = random_search.predict(X_train)

    y_pred_test = random_search.predict(X_test)
    
    print(f'Train Accuracy_score = {accuracy_score(y_train, y_pred_train)}')
    print(f'Test Accuracy_score = {accuracy_score(y_test, y_pred_test)}')
    print('\n')
    print(classification_report(y_test, y_pred_test, target_names=['benign', 'malicious'], digits=4))
    
    print(f'best_estimator = {}')
    
    feat_imp = random_search.feature_importances_
    feat_dict = {}

    for i in range(len(feat_imp)):
        feat_dict[X.columns[i]] = feat_imp[i]

    feat_dict = {k: v for k, v in sorted(feat_dict.items(), key=lambda item: item[1], reverse=True)}

    print("{:<25} {:<25}".format('Feature' ,'Importance'))
    for k, v in feat_dict.items():
        num = v
        print("{:<25} {:<25%}".format(k, num))

    