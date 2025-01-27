import os
import pandas as pd

global current_path
global androidTags
    
current_path = os.getcwd()

tags_path = os.path.join(current_path,'Android_Tags.csv')
androidTags = pd.read_csv(tags_path, index_col=None)