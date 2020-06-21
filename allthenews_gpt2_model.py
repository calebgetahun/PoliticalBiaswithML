# -*- coding: utf-8 -*-
"""Copy of allthenews_GPT2_rightist.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QFaZDI-hFqQPErDEXhlYfRM_vK0G-eEe

### Initialize
"""

gpu_info = !nvidia-smi
gpu_info = '\n'.join(gpu_info)
if gpu_info.find('failed') >= 0:
  print('Select the Runtime → "Change runtime type" menu to enable a GPU accelerator, ')
  print('and then re-execute this cell.')
else:
  print(gpu_info)

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x
!pip install -q gpt-2-simple
import gpt_2_simple as gpt2
from datetime import datetime

gpt2.download_gpt2(model_name="124M")

gpt2.mount_gdrive()

# Auth_code = " 4/zAEOlUhHXqOzOeDJiGtoY52sUcZM_PoL_PgsWeFkrREF8-gwz0_e5iM "



!pip install -U -q kaggle
!mkdir -p .kaggle

import json

token = {"username":"ruthranchandrasekar","key":"e969db0314e4da42b6d23f68a449fb78"}

with open('/content/.kaggle/kaggle.json', 'w') as file:
    json.dump(token, file)

!cp /content/.kaggle/kaggle.json ~/.kaggle/kaggle.json

!kaggle datasets download -d snapcrack/all-the-news -p /content

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/

#!unzip /content/all-the-news.zip -d /content/

"""### Play with data"""

# All our modules 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Merging all the datasets together
d1 = pd.read_csv('articles1.csv', encoding = 'utf-8')
d2 = pd.read_csv('articles2.csv', encoding = 'utf-8')
d3 = pd.read_csv('articles3.csv', encoding = 'utf-8')
data = pd.concat([d1, d2, d3])

data.head()

# Remove NULL and NAN
data['content'] = data['content'].fillna("")
data['title'] = data['title'].fillna("")
content = data['content']
titles = data["title"]

final_right = data[data['publication'].str.contains("Fox")]
final_right = final_right[['title','content']]
final_right.head()

#final_right['title'] = '<startoftext> ' + '[TITLE] ' + final_right['title'].astype(str)
#final_right['content'] = '[CONTENT] ' + final_right['content'].astype(str) + ' <endoftext>'
#final_right.to_csv( "rightcontent.csv", index=False, encoding='utf-8-sig')

final_right['content'].to_csv("rightcontent.txt",header=None, index=None, sep='\t', mode='a')

"""## Finetune GPT-2

The next cell will start the actual finetuning of GPT-2. It creates a persistent TensorFlow session which stores the training config, then runs the training for the specified number of `steps`. (to have the finetuning run indefinitely, set `steps = -1`)

The model checkpoints will be saved in `/checkpoint/run1` by default. The checkpoints are saved every 500 steps (can be changed) and when the cell is stopped.

The training might time out after 4ish hours; make sure you end training and save the results so you don't lose them!

**IMPORTANT NOTE:** If you want to rerun this cell, **restart the VM first** (Runtime -> Restart Runtime). You will need to rerun imports but not recopy files.

Other optional-but-helpful parameters for `gpt2.finetune`:


*  **`restore_from`**: Set to `fresh` to start training from the base GPT-2, or set to `latest` to restart training from an existing checkpoint.
* **`sample_every`**: Number of steps to print example output
* **`print_every`**: Number of steps to print training progress.
* **`learning_rate`**:  Learning rate for the training. (default `1e-4`, can lower to `1e-5` if you have <1MB input data)
*  **`run_name`**: subfolder within `checkpoint` to save the model. This is useful if you want to work with multiple models (will also need to specify  `run_name` when loading the model)
* **`overwrite`**: Set to `True` if you want to continue finetuning an existing model (w/ `restore_from='latest'`) without creating duplicate copies.
"""

sess = gpt2.start_tf_sess()
file_name = "rightcontent.txt"

gpt2.finetune(sess,
              dataset=file_name,
              model_name='124M',
              steps=8000,
              restore_from='fresh',
              run_name='run_right_7000',
              print_every=10,
              sample_every=200,
              save_every=500,
              )

gpt2.copy_checkpoint_to_gdrive(run_name='run_right_7000')

"""You're done! Feel free to go to the **Generate Text From The Trained Model** section to generate text based on your retrained model.

## Load a Trained Model Checkpoint

Running the next cell will copy the `.rar` checkpoint file from your Google Drive into the Colaboratory VM.
"""

gpt2.copy_checkpoint_from_gdrive(run_name='run_right_7000')

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run_right_7000')

"""## Generate Text From The Trained Model

After you've trained the model or loaded a retrained model from checkpoint, you can now generate text. `generate` generates a single text from the loaded model.
"""

gpt2.generate(sess, run_name='run_right_7000')

gpt2.generate(sess, run_name='run_right_7000',
              length=100,
              temperature=.7,
              nsamples=10,
              batch_size=10,
              prefix="Allowing more immigrants to come into the United States will",
              truncate="<|endoftext|>",
              include_prefix=True
              )

#gen_file = 'gpt2_gentext_{:%Y%m%d_%H%M%S}.txt'.format(datetime.utcnow())
gpt2.generate(sess, run_name='run_right_7000',
              length=100,
              temperature=.7,
              nsamples=10,
              batch_size=10,
              prefix="<|startoftext|>[WP] Many foreign immigrants have come to the United States [RESPONSE]",
              truncate="<|endoftext|>",
              include_prefix=True
              )

# may have to run twice to get file to download
from google.colab import files
files.download(gen_file)