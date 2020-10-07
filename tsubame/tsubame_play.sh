git config --global credential.helper store
ssh-add -K ~/.ssh/id_rsa

export PATH="/gs/hs0/tga-tslab/mingxin/anaconda3/bin:$PATH"  ## if use anaconda or miniconda

conda create -n dstc84 python=3.6 tqdm
conda env remove -n dstc84

pip install wheel
python -m wheel install tensorflow-1.13.1-cp36-cp36m-linux_x86_64.whl
pip install tensorflow-1.13.1-cp36-cp36m-linux_x86_64.whl

conda activate base
conda activate dstc84

conda activate dstc84
cd /gs/hs0/tga-tslab/mingxin/dstc8_track4
module load \
  intel/19.0.0.117 \
  cuda/10.0.130 \
  tinker/8.1.2 \
  tmux/2.7 \
  cudnn/7.4 \
  nccl/2.4.2

git config --global user.email "z670172581@icloud.com"
git config --global user.name "MinxZ"

node=q
# rm $store.log
# rm ${store}_err.log
# rm -r output_ckpt_dir_$store
mkdir output_ckpt_dir_$store
# bash dstc8_track4_zero_shot_Schema-Guided_DST/main/main.sh $train_batch_size $embedding_dim $model $store
# qsub -g tga-tslab -o $store.log -e ${store}_err.log -N $33 dstc8_track4_zero_shot_Schema-Guided_DST/main/tsubame.sh
qsub -g tga-tslab -o xxx.log -e _err.log -N d3q tsubame.sh
qsub -g tga-tslab -o xxx.log -e _err.log -N ddqn_raw tsubame.sh

ps ax | grep python

cd /gs/hs0/tga-tslab/mingxin/

export PATH=/usr/local/cuda-10.0/bin:/usr/local/cuda-10.0/NsightCompute-2019.1${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
