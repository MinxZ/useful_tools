"""
Optuna example that demonstrates a pruner for XGBoost.

In this example, we optimize the validation accuracy of cancer detection using XGBoost.
We optimize both the choice of booster model and their hyperparameters. Throughout
training of models, a pruner observes intermediate results and stop unpromising trials.
"""
import optparse

import lightgbm as lgb
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import optuna
import pandas as pd
import sklearn.datasets
import sklearn.metrics
from sklearn.model_selection import train_test_split
from tqdm import tqdm

parser = optparse.OptionParser(description='Create data')
parser.add_option('--medium_name', choices=['D1Y', 'D25', 'C15'], default='D25',
                  help='which medium to use')
(opts, args) = parser.parse_args()
medium_name = opts.medium_name

data_path = '/home/ec2-user/data/data'
val_year = '2017'


def relat_obj(labels, preds):
    grads = 2 * (preds / labels - 1) * (1 / labels) / labels.shape[0]
    hessian = 2 / (labels ** 2) / labels.shape[0]
    return grads, hessian


def relat_loss(labels, preds):
    return 'relat-err', np.mean((preds / labels - 1) ** 2), False


def digest_obj(labels, preds):
    preds = np.clip(preds, 1 / 52, 1e9)
    digest_err = labels / preds - 1
    d_digest_err = -labels / (preds ** 2)
    dd_digest_err = 2 * labels / (preds ** 3)

    large_grads = 2 * digest_err * d_digest_err
    large_hessian = 2 * (d_digest_err ** 2 + digest_err * dd_digest_err)

    small_grads = 0.1 * 2 * digest_err * d_digest_err
    small_hessian = 0.1 * 2 * (d_digest_err ** 2 + digest_err * dd_digest_err)

    grads = np.where((digest_err >= 0) & (digest_err <= 0.25), small_grads, large_grads) / labels.shape[0]
    hessian = np.where((digest_err >= 0) & (digest_err <= 0.25), small_hessian, large_hessian) / labels.shape[0]

    return grads, hessian


def digest_loss(labels, preds):
    preds = np.clip(preds, 1 / 52, 1e9)
    digest_err = labels / preds - 1
    loss = np.where((digest_err >= 0) & (digest_err <= 0.25), 0.1 * digest_err ** 2, digest_err ** 2)

    return 'digest-err', np.mean(loss), False


def objective(trial):

    X_data = np.load(f'{data_path}/X_data_{medium_name}.npz')
    Y_data = np.load(f'{data_path}/Y_data_{medium_name}.npz')
    years = list(map(int, X_data.files))

    # Split Train and Validation by year
    X_train = np.concatenate([X_data[str(year)] for year in years if year != val_year], axis=0)
    X_val = X_data[str(val_year)]
    y_train = np.concatenate([Y_data[str(year)] for year in years if year != val_year], axis=0)
    y_val = Y_data[str(val_year)]

    # choose loss_type to use
    loss_type = trial.suggest_categorical('loss_type', ['normal', 'log-loss', 'unshidted-log-loss'])
    loss_type2 = trial.suggest_categorical('loss_type2', ['normal', 'relat_loss', 'digest_loss'])

    if loss_type == 'unshifted-log-loss':
        y_train = np.log(y_train)
        y_val = np.log(y_val)
    elif loss_type == 'log-loss':
        y_train = np.log(y_train + 1)
        y_val = np.log(y_val + 1)

    dtrain = lgb.Dataset(X_train, label=y_train)
    dval = lgb.Dataset(X_val, label=y_val)

    param = {
        'objective': 'regression',
        'metric': 'l2',
        'verbosity': 2,
        'boosting_type': trial.suggest_categorical('boosting', ['gbdt', 'dart', 'goss']),
        'num_leaves': trial.suggest_int('num_leaves', 10, 1000),
        'learning_rate': trial.suggest_uniform('learning_rate', 0.2, 1.0),
        'feature_fraction': trial.suggest_uniform('feature_fraction', 0.0, 1.0),
        'max_bin': trial.suggest_int('max_bin', 63, 1000)
    }

    if param['boosting_type'] == 'dart':
        param['drop_rate'] = trial.suggest_loguniform('drop_rate', 1e-8, 1.0)
        param['skip_drop'] = trial.suggest_loguniform('skip_drop', 1e-8, 1.0)
        param['bagging_fraction'] = trial.suggest_uniform('bagging_fraction', 0.0, 1.0)
        param['bagging_freq'] = trial.suggest_int('bagging_freq', 2, 10)
    if param['boosting_type'] == 'goss':
        param['top_rate'] = trial.suggest_uniform('top_rate', 0.0, 1.0)
        param['other_rate'] = trial.suggest_uniform('other_rate', 0.0, 1.0 - param['top_rate'])

    special_control = ['relat-loss', 'digest-loss']
    special_loss = {'relat-loss': [relat_obj, relat_loss], 'digest-loss': [digest_obj, digest_loss]}

    param['num_iterations'] = 50
    # Add a callback for pruning.
    pruning_callback = optuna.integration.LightGBMPruningCallback(trial, 'l2')
    if loss_type2 in special_control:
        bst = lgb.train(param, dtrain, valid_sets=[dval],
                        callbacks=[pruning_callback],
                        fobj=special_loss[loss_type][0], feval=special_loss[loss_type][1])
    else:
        bst = lgb.train(
            param, dtrain, valid_sets=[dval], verbose_eval=False, callbacks=[pruning_callback])

    preds = bst.predict(X_val)

    if loss_type == 'normal':
        rmse = np.mean((preds - y_val)**2)**0.5
    else:
        rmse = np.mean((np.exp(preds) - np.exp(y_val))**2)**0.5

    return rmse


study = optuna.create_study(pruner=optuna.pruners.MedianPruner(n_warmup_steps=10))
study.optimize(objective, n_trials=30)

X_data = np.load(f'{data_path}/X_data_{medium_name}.npz')
Y_data = np.load(f'{data_path}/Y_data_{medium_name}.npz')
years = list(map(int, X_data.files))

# Split Train and Validation by year
X_train = np.concatenate([X_data[str(year)] for year in years if year != val_year], axis=0)
X_val = X_data[str(val_year)]
y_train = np.concatenate([Y_data[str(year)] for year in years if year != val_year], axis=0)
y_val = Y_data[str(val_year)]

# param = {'objective': 'regression',
#         'metric': 'l2',
#         'verbosity': 2,
# 'loss_type': 'log-loss', 'loss_type2': 'digest_loss', 'boosting': 'gbdt', 'num_leaves': 959, 'learning_rate': 0.5867534714907668, 'feature_fraction': 0.39089008474159037, 'max_bin': 677}


param = study.best_params
loss_type = param['loss_type']
loss_type2 = param['loss_type2']
del param['loss_type']
del param['loss_type2']
# choose loss_type to use
if loss_type == 'unshifted-log-loss':
    y_train = np.log(y_train)
    y_val = np.log(y_val)
elif loss_type == 'log-loss':
    y_train = np.log(y_train + 1)
    y_val = np.log(y_val + 1)

dtrain = lgb.Dataset(X_train, label=y_train)
dval = lgb.Dataset(X_val, label=y_val)

special_control = ['relat-loss', 'digest-loss']
special_loss = {'relat-loss': [relat_obj, relat_loss], 'digest-loss': [digest_obj, digest_loss]}
if loss_type2 in special_control:
    bst = lgb.train(param, dtrain, valid_sets=[dval],
                    fobj=special_loss[loss_type][0], feval=special_loss[loss_type][1])
else:
    bst = lgb.train(param, dtrain, valid_sets=[dval])

preds = bst.predict(X_val)
if loss_type == 'unshifted-log-loss':
    y_val = np.exp(y_val)
    preds = np.exp(preds)
elif loss_type == 'log-loss':
    y_val = np.exp(y_val) - 1
    preds = np.exp(preds) - 1
rmse = np.mean((preds - y_val)**2)**0.5


print('LightGBM')
print('Number of finished trials: {}'.format(len(study.trials)))
print('Best trial:')
trial = study.best_trial
print('  Value: {}'.format(trial.value))
print('  Params: ')
for key, value in trial.params.items():
    print('    {}: {}'.format(key, value))
print(f'rmse: {rmse}')
print(f'relative error: {np.mean(np.abs(preds - y_val))/np.mean(y_val)}')

#
# print('LightGBM')
# print('Number of finished trials: {}'.format(30))
# print('Best trial:')
# print('  Params: ')
# for key, value in param.items():
#     print('    {}: {}'.format(key, value))
# print(f'rmse: {rmse}')
# print(f'relative error: {np.mean(np.abs(preds - y_val))/np.mean(y_val)}')


with open(f'{data_path}/{medium_name}.txt', "a") as text_file:
    text_file.write('LightGBM\n')
    text_file.write('Number of finished trials: {}\n'.format(len(study.trials)))
    text_file.write('Best trial:\n')
    text_file.write('  Value: {}\n'.format(trial.value))
    text_file.write('  Params: \n')
    for key, value in trial.params.items():
        text_file.write('    {}: {}\n'.format(key, value))
    text_file.write(f'rmse: {rmse}\n')
    text_file.write(f'relative error: {np.mean(np.abs(preds - y_val))/np.mean(y_val)}\n')


"""
LightGBM
Number of finished trials: 30
Best trial:
  Value: 28.51992099409426
  Params:
    loss_type: log-loss
    loss_type2: normal
    boosting: goss
    num_leaves: 515
    learning_rate: 0.16462505224326837
    feature_fraction: 0.16948741020627645
    max_bin: 951
    top_rate: 0.5183040819680741
    other_rate: 0.2953835343758239
rmse: 28.51992099409426
relative error: 0.21062741255962814
"""

# bst = lgb.train(param, dtrain, 50, valid_sets=[dval])

# preds = bst.predict(X_val)
# if loss_type == 'unshifted-log-loss':
#     y_val = np.exp(y_val)
#     preds = np.exp(preds)
# elif loss_type == 'log-loss':
#     y_val = np.exp(y_val) - 1
#     preds = np.exp(preds) - 1
# rmse = np.mean((preds - y_val)**2)**0.5


def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.
    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.
    Returns:
    --------
        mask : A numobservations-length boolean array.
    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    if len(points.shape) == 1:
        points = points[:, None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


figs, axes = plt.subplots(2, 3, figsize=(30, 20))

errs = (preds - y_val).astype(np.float32)
abs_errs = np.abs(errs).astype(np.float32)
relat_errs = (errs / y_val).astype(np.float32)

errs = errs[~is_outlier(errs)]
abs_errs = abs_errs[~is_outlier(abs_errs)]
relat_errs = relat_errs[~is_outlier(relat_errs)]
axes[0][0].hist(errs, bins=50)
axes[0][0].set_title('Error histrogram')

axes[0][1].hist(abs_errs, bins=50)
axes[0][1].set_title('Absolute error histrogram')

axes[0][2].hist(relat_errs, bins=50)
axes[0][2].set_title('Relative error histrogram')

digest = (y_val / preds).astype(np.float32)
digest = digest[~is_outlier(digest)]
digest_err = np.mean(np.abs(digest - 1))
axes[1][0].hist(digest, bins=50)
axes[1][0].set_title('Digest error histrogram')

axes[1][1].hist(np.abs(digest), bins=50)
axes[1][1].set_title('Absolute digest error histogram')

outlier_idx = is_outlier(y_val) | is_outlier(preds)
min_data = 0
GT = y_val[~outlier_idx]
PRED = preds[~outlier_idx]
max_data = max([GT.max(), PRED.max()])
X_plot = np.linspace(min_data, max_data, 1000)
axes[1][2].set_xlim((min_data, max_data))
axes[1][2].set_ylim((min_data, max_data))
axes[1][2].set_xlabel('GT')
axes[1][2].set_ylabel('pred')
axes[1][2].plot(X_plot, X_plot)
axes[1][2].scatter(GT, PRED, s=2)

plt.savefig(f'{data_path}/Histrogram_light_{medium_name}.png')
