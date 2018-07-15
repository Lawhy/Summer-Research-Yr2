# Transliteration
This is a summer project regarding to the problem set of multi-lingual transliteration. <br />
The project is initialized and supervised by Shay Cohen and Joana Ribeiro from the NLP group of the University of Edinburgh.<br />
The details of this project is in the report file.<br />

---

# Experiment 

### Setup

1. Download a usable Anaconda:

```
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
```

2. Bash it and remember to store it in somewhere with enough space (e.g. /disk/ocean)

3. Create conda environment, save the PATH, and activate:

```
conda create -n pytorch python=2.7
source ~/.bashrc
source activate pytorch
```

4. Install Pytorch with CUDA-9:

```
conda install pytorch torchvision cuda91 -c pytorch
```

5. Install openNMT-py and its dependency:

```
git clone https://github.com/OpenNMT/OpenNMT-py
cd OpenNMT-py
pip install -r requirements.txt
```

### Commands

- Preprocess:

```
python PATH_FOR_OpenNMT/OpenNMT-py/preprocess.py
-train_src data/en_tra.txt
-train_tgt data/ch_tra.txt
-valid_src data/en_dev.txt
-valid_tgt data/ch_dev.txt
```

- Training:
(Assume: cur_directory=/disk/ocean/lhe/en2chi/nmt-py/models/bs)

```
python PATH_FOR_OpenNMT/OpenNMT-py/train.py
-data data/bs
-save_model bs
-train_steps 12500
-seed 7
-start_decay_step 8000
-save_checkpoint_steps 100
-keep_checkpoint 10
-decay_steps 1000
-gpuid 1
-learning_rate 0.8

```

- Translate:

```
for i in {checkpoint_start_NUMBER..checkpoint_end_NUMBER..checkpoint_save_STEPS}
do
python PATH_FOR_OpenNMT/OpenNMT-py/translate.py
-model bs_step_$i.pt
-src data/en_dev.txt
-output infer/bs_dev_$i.txt
-replace_unk
-verbose
-gpu 1
done
```
- check WER: 
(Get wer.py from NMT-py directory)
```
# (In python3 venv)
for i in {checkpoint_start_NUMBER..checkpoint_end_NUMBER..checkpoint_save_STEPS}; 
do 
   python wer.py bs_dev_$i.txt ch_dev.txt; 
   echo $i; 
done
```

### Citation
- OpenNMT-py:<br />
   https://github.com/OpenNMT/OpenNMT-py
