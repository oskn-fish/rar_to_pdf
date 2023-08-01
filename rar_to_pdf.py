import os 
import glob
import img2pdf
import argparse
import patoolib
from logging import getLogger, DEBUG, INFO, StreamHandler
logger = getLogger(__name__)
handler = StreamHandler()
logger.setLevel(DEBUG)
handler.setLevel(DEBUG)
logger.addHandler(handler)


class GeneratePdfFolder():
    """ 
    os.path.basename -> filename.ext
    os.path.dirname -> /path/to/file
    os.path.split -> (/path/to/fie, filename.ext)
    os.path.splittext -> (/path/to/filename, .ext)
    os.path.join(path, to, file) -> path/to/file
    """
    def __init__(self, rar_path, output_path):
        if not output_path:
            output_path = os.path.splitext(rar_path)[0]
        self.output_path = output_path
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
        patoolib.extract_archive(rar_path, outdir=output_path)

    def generate_pdf_folder(self):
        self._recursive_img2pdf(self.output_path)

    def _recursive_img2pdf(self, path):
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
                file_path = self.output_path+"/"+os.path.basename(path)+".pdf"
                logger.debug(f"saving to {file_path} ...")
                with open(file_path, mode='wb') as f:
                    f.write(img2pdf.convert(images_path))
        
        for child in os.listdir(path):
            child_path = path+'/'+child
            if os.path.isdir(child_path):
                self._recursive_img2pdf(child_path)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("rar_path")
    parser.add_argument("-o", "--output_path")
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    GeneratePdfFolder(args.rar_path, args.output_path).generate_pdf_folder()
