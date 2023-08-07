import os 
import sys
import glob
import img2pdf
import argparse
import patoolib
from logging import getLogger, DEBUG, INFO, StreamHandler
from PIL import Image
logger = getLogger(__name__)
handler = StreamHandler()
logger.setLevel(DEBUG)
handler.setLevel(DEBUG)
logger.addHandler(handler)


class GeneratePdfFolder():
    def __init__(self, input_path, output_path):
        # setting default output path
        if not output_path:
            output_path = os.path.splitext(input_path)[0]
        self.output_path = output_path
        
        # making a directory if input is a rar file
        if not os.path.isdir(input_path):
            os.mkdir(self.output_path)
            patoolib.extract_archive(input_path, outdir=output_path)
            
            
    def _img2pdf(self, pdf_name: str, images_path: list):
        if not images_path:
            return 
        
        images_path.sort()
        skip = False # if overwriting
        
        new_pdf_path = os.path.join(self.output_path, pdf_name+".pdf")
        if os.path.isfile(new_pdf_path):
            ans = ''
            while ans not in ['y', 'n']:
                ans = input(f"'{new_pdf_path}.pdf' already exists. Do you want to overwrite? (y[Yes]/n[No])")
                ans = ans.lower()
            if ans == 'n':
                skip = True
                
        if not skip:                
            file_path = new_pdf_path
            logger.debug(f"saving to {file_path} ...")
            with open(file_path, mode='wb') as f:
                f.write(img2pdf.convert(images_path))
        
        
    def _extract_filename(self, filepath: str):
       return os.path.splitext(os.path.basename(filepath))[0]

    def generate_pdf_folder(self, pwd: str = None):
        if not pwd:
            pwd = self.output_path

        # check if pwd contains same filename files with different extension
        images_path_webp = glob.glob(glob.escape(pwd)+"/*.webp")
        images_path_jpg = glob.glob(glob.escape(pwd)+"/*.jpg")+glob.glob(glob.escape(pwd)+"/*.JPG")
        images_path_png = glob.glob(glob.escape(pwd)+"/*.png")+glob.glob(glob.escape(pwd)+"/*.PNG")
        
        filenames_webp = set(map(self._extract_filename, images_path_webp))
        filenames_jpg = set(map(self._extract_filename, images_path_jpg))
        filenames_png = set(map(self._extract_filename, images_path_png))
        
        duplication = (filenames_webp & filenames_jpg) | (filenames_webp & filenames_png) | (filenames_jpg & filenames_png)
        
        if duplication:
            ans = ""
            while not ans in ["q", "s"]:
                print("Following duplicate filenames detected. [Q]uit/[S]kip")
                print(",".join(duplication))
                ans = input()
                ans = ans.lower()
            if ans == "q":
                sys.exit()
            elif ans == "s":
                return 
        
        # convert webp files to jpg files
        if images_path_webp:
            print("converting to jpg files...")
            to_be_deleted_path = []
            for image_webp_path in images_path_webp:
                image_ect = Image.open(image_webp_path)
                new_image_jpg_path = os.path.join(os.path.splitext(image_webp_path)[0]+".jpg")
                to_be_deleted_path.append(new_image_jpg_path)
                image_ect.save(new_image_jpg_path)
        
        # convert image files to a pdf file
        images_path = to_be_deleted_path+images_path_jpg+images_path_png
        self._img2pdf(os.path.basename(pwd), images_path)
        
        # remove temporary jpg file created above
        if to_be_deleted_path:
            print("removing temporary files...")
            for to_delete in to_be_deleted_path:
                os.remove(to_delete)
        
        # search in child directories
        for child in os.listdir(pwd):
            child_path = os.path.join(pwd, child)
            if os.path.isdir(child_path):
                self.generate_pdf_folder(child_path)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("-o", "--output_path")
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    GeneratePdfFolder(args.input_path, args.output_path).generate_pdf_folder()
