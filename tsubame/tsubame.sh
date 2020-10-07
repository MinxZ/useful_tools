#!/bin/sh
#$ -cwd                      ## Execute a job in current directory
#$ -l h_node=1               ## Use number of node
#$ -l h_rt=24:00:00          ## Running job time


export PATH="/gs/hs0/tga-tslab/mingxin/anaconda3/bin:$PATH"  ## if use anaconda or miniconda
. /etc/profile.d/modules.sh  ## Initialize module commands
module load \
  intel/19.0.0.117 \
  cuda/10.0.130 \
  tinker/8.1.2 \
  cudnn/7.4 \
  nccl/2.4.2

source activate d3q
cd /gs/hs0/tga-tslab/mingxin/
cd D3Q/D3Q/src/

nohup sh example.sh > custom-out.log &
# sh example.sh
python draw_figure.py
