#%%
import os 
import glob
import img2pdf
import argparse
from logging import getLogger, DEBUG, INFO, StreamHandler
logger = getLogger(__name__)
handler = StreamHandler()
logger.setLevel(DEBUG)
handler.setLevel(DEBUG)
logger.addHandler(handler)


def recursive_img2pdf(path):
    images_path = glob.glob(glob.escape(path)+"/*.jpg")+glob.glob(glob.escape(path)+"/*.png")
    
    if images_path:
        images_path.sort()
        skip = False
        
        if os.path.isfile(path+".pdf"):
            ans = ''
            while ans not in ['y', 'n']:
                ans = input(f"'{path}.pdf' already exists. Do you want to overwrite? (y[Yes]/n[No])")
                ans = ans.lower()
            if ans == 'n':
                skip = True
                
        if not skip:
            logger.debug(f"saving to {path}.pdf ...")
            with open(path+".pdf", mode='wb') as f:
                f.write(img2pdf.convert(images_path))
    
    for child in os.listdir(path):
        child_path = path+'/'+child
        if os.path.isdir(child_path):
            recursive_img2pdf(child_path)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_path")    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    recursive_img2pdf(args.search_path)


# %%
