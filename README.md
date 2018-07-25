# Transliteration
This is a summer project regarding to the problem set of multi-lingual transliteration. <br />
The project is initialized and supervised by Shay Cohen and Joana Ribeiro from the NLP group of the University of Edinburgh.<br />
The details of this project is in the 
[report file](https://docs.google.com/document/d/1XQTABQMb8yKXFJmztmp0CIdFN2FmdXLmDAEXUzzUbMI/edit?usp=sharing)<br />

---

# Experiment 

### Setup

1. Download a usable Anaconda:

```bash
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
```

2. Bash it and remember to store it in somewhere with enough space (e.g. /disk/ocean)

3. Create conda environment, save the PATH, and activate:

```bash
conda create -n pytorch python=2.7
source ~/.bashrc
source activate pytorch
```

4. Install Pytorch with CUDA-9:

```bash
conda install pytorch torchvision cuda91 -c pytorch
```

5. Install openNMT-py and its dependency:

```bash
git clone https://github.com/OpenNMT/OpenNMT-py
cd OpenNMT-py
pip install -r requirements.txt
```
### Using convenient scripts in NMT-py/scripts
Prerequisites: <br />
1. Main Directory: main_dir=/disk/ocean/lhe/transliteration/nmt-py # You can change the value of main_dir in the bash scripts<br />
2. OpenNMT-py in the Main Directory: main_dir/OpenNMT-py <br />
3. Data Directory: main_dir/data # in the following format<br />
![Alt text](data.pdf)

### Individual Commands

- Preprocess:

```bash
python PATH_FOR_OpenNMT/OpenNMT-py/preprocess.py
-train_src data/en_tra.txt
-train_tgt data/ch_tra.txt
-valid_src data/en_dev.txt
-valid_tgt data/ch_dev.txt
-save_data data/DEMO # suggested naming: bs(baseline) or {2 4 5 7 9 10 12 15}(cluster number)
```

- Training:
(Assume: cur_directory=/disk/ocean/lhe/en2chi/nmt-py/models/bs)

```bash
python PATH_FOR_OpenNMT/OpenNMT-py/train.py
-data data/DEMO # Any name generated from the preprocessing
-save_model MODEL # suggested naming: bs(baseline) or {2 4 5 7 9 10 12 15}(cluster number)
-train_steps 15000 
-seed 7
-start_decay_step 8000
-save_checkpoint_steps 100
-keep_checkpoint 10
-decay_steps 1000
-learning_rate 0.8
-gpuid 1
-log_file logs/DEMO.log # Save the training details
```

- Translate:

```bash
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
```bash
# (In python3 venv)
for i in {checkpoint_start_NUMBER..checkpoint_end_NUMBER..checkpoint_save_STEPS}; 
do 
   python wer.py bs_dev_$i.txt ch_dev.txt; 
   echo $i; 
done
```
- check CER:
Use the script here: https://github.com/belambert/asr-evaluation
And do similar for-loop as above.

### Citation
- OpenNMT-py:<br />
   https://github.com/OpenNMT/OpenNMT-py
