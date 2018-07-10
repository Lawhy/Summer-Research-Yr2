# En2Chi-Transliteration
This is a summer project regarding to the problem set of English-to-Chinese transliteration. 
The project is initialized and supervised by Shay Cohen and Joana Ribeiro from the NLP group of the University of Edinburgh.
The details of this project is in the report file.

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
python preprocess.py \
-train_src data/src-train.txt \
-train_tgt data/tgt-train.txt \
-valid_src data/src-val.txt \
-valid_tgt data/tgt-val.txt \
-save_data data/demo
```

- Training:
(Assume: cur_directory=/disk/ocean/lhe/en2chi/nmt-py/models/bs)

```
python ../../OpenNMT-py/train.py 
-data bs{2 5 10 15 cls} # name of the preprocessed data
-save_model bs{2 5 10 15 cls} # name of the model
-train_steps 16000 
-seed 7 
-start_decay_step 7000 
-save_checkpoint_steps 50 
-keep_checkpoint 20
-train_from # (optional for retraining)
-gpuid 1  # (specify gpu device)

```

- Translate:
(Assume: cur_directory = /disk/ocean/lhe/en2chi/nmt-py)

```
python OpenNMT-py/translate.py 
-model models/bs{2 5 10 15 cls}/bs{2 5 10 15 cls}_step_NUMBER.pt 
-src data/bs{2 5 10 15 cls}/en2chi_dev_eng.txt 
-output results/bs{2 5 10 15 cls}/dev/bs{2 5 10 15 cls}_dev_NUMBER.txt 
-replace_unk 
-verbose
```

