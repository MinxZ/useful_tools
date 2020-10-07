
import optparse

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import optuna
import sklearn.datasets
import sklearn.ensemble
import sklearn.model_selection
import sklearn.svm

parser = optparse.OptionParser(description='Create data')
parser.add_option('--medium_name', choices=['D1Y', 'D25', 'C15'], default='C15',
                  help='which medium to use')
(opts, args) = parser.parse_args()
medium_name = opts.medium_name

data_path = '/home/ec2-user/data/data'
val_year = '2017'


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

    max_depth = int(trial.suggest_loguniform('max_depth', 2, 8))
    n_estimators = int(trial.suggest_loguniform('n_estimators', 50, 150))
    min_samples_leaf = int(trial.suggest_loguniform('min_samples_leaf', 1, 500))
    max_features = trial.suggest_categorical('max_features', ['Auto', 'sqrt', '0.2'])
    rf = sklearn.ensemble.RandomForestRegressor(n_estimators=n_estimators,
                                                max_depth=max_depth,
                                                min_samples_leaf=min_samples_leaf,
                                                random_state=1,
                                                max_features="auto",
                                                oob_score=True,
                                                n_jobs=-1)

    rf.fit(X_train, y_train)
    preds = rf.predict(X_val)

    if loss_type == 'normal':
        rmse = np.mean((preds - y_val)**2)**0.5
    else:
        rmse = np.mean((np.exp(preds) - np.exp(y_val))**2)**0.5

    return rmse


study = optuna.create_study()
study.optimize(objective, n_trials=30)

X_data = np.load(f'{data_path}/X_data_{medium_name}.npz')
Y_data = np.load(f'{data_path}/Y_data_{medium_name}.npz')
years = list(map(int, X_data.files))

# Split Train and Validation by year
X_train = np.concatenate([X_data[str(year)] for year in years if year != val_year], axis=0)
X_val = X_data[str(val_year)]
y_train = np.concatenate([Y_data[str(year)] for year in years if year != val_year], axis=0)
y_val = Y_data[str(val_year)]

param = study.best_params
loss_type = param['loss_type']
loss_type2 = param['loss_type2']
# choose loss_type to use
if loss_type == 'unshifted-log-loss':
    y_train = np.log(y_train)
    y_val = np.log(y_val)
elif loss_type == 'log-loss':
    y_train = np.log(y_train + 1)
    y_val = np.log(y_val + 1)

max_depth = int(param['max_depth'])
n_estimators = int(param['n_estimators'])
min_samples_leaf = int(param['min_samples_leaf'])
max_features = param['max_features']
rf = sklearn.ensemble.RandomForestRegressor(n_estimators=n_estimators,
                                            max_depth=max_depth,
                                            min_samples_leaf=min_samples_leaf,
                                            random_state=1,
                                            max_features="auto",
                                            oob_score=True,
                                            n_jobs=-1)

rf.fit(X_train, y_train)
preds = rf.predict(X_val)

if loss_type == 'unshifted-log-loss':
    y_val = np.exp(y_val)
    preds = np.exp(preds)
elif loss_type == 'log-loss':
    y_val = np.exp(y_val) - 1
    preds = np.exp(preds) - 1
rmse = np.mean((preds - y_val)**2)**0.5

print('Random forest')
print('Number of finished trials: {}'.format(len(study.trials)))
print('Best trial:')
trial = study.best_trial
print('  Value: {}'.format(trial.value))

print('  Params: ')
for key, value in trial.params.items():
    print('    {}: {}'.format(key, value))


print(f'rmse: {rmse}')
print(f'relative error: {np.mean(np.abs(preds - y_val))/np.mean(y_val)}')

with open(f'{data_path}/{medium_name}.txt', "a") as text_file:
    text_file.write('RF\n')
    text_file.write('Number of finished trials: {}\n'.format(len(study.trials)))
    text_file.write('Best trial:\n')
    text_file.write('  Value: {}\n'.format(trial.value))
    text_file.write('  Params: \n')
    for key, value in trial.params.items():
        text_file.write('    {}: {}\n'.format(key, value))
    text_file.write(f'rmse: {rmse}\n')
    text_file.write(f'relative error: {np.mean(np.abs(preds - y_val))/np.mean(y_val)}\n')


"""
Random forest
Number of finished trials: 30
Best trial:
  Value: 23.88294336757342
  Params:
    loss_type: normal
    loss_type2: relat_loss
    max_depth: 25.173194275721563
    n_estimators: 187.5013926645581
    min_samples_leaf: 1.9969577308933834
    max_features: 0.2
rmse: 23.88294336757342
relative error: 0.3086795545902801
"""


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

plt.savefig(f'{data_path}/Histrogram_rf_{medium_name}.png')
