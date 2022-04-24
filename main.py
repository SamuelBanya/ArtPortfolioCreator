import os
# from dotenv import dotenv_values
from dotenv import load_dotenv
from pathlib import Path
import os
from pathlib import Path
from pathlib import PurePath
from pathlib import PosixPath
import pprint
import itertools
from wand.image import Image as wand_image
import wand
import pendulum
import shutil

# Global Variables:
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
WEBSITE_PATH = os.getenv("WEBSITE_PATH")
print('WEBSITE_PATH: ' + str(WEBSITE_PATH))
# art_gallery_path = '/var/www/musimatic/images/ArtGallery'
art_portfolio_path = str(WEBSITE_PATH) + str("/images/ArtPortfolio")
WEBSITE_ADDRESS = os.getenv("WEBSITE_ADDRESS")
print('WEBSITE_ADDRESS: ' + str(WEBSITE_ADDRESS))
WEBSITE_FULL_ADDRESS = os.getenv("WEBSITE_FULL_ADDRESS")
print('WEBSITE_FULL_ADDRESS: ' + str(WEBSITE_FULL_ADDRESS))
PROJECT_DIRECTORY = os.getenv("PROJECT_DIRECTORY")
print('PROJECT_DIRECTORY: ' + str(PROJECT_DIRECTORY))

def create_art_portfolio():
    art_portfolio_path_exists = Path(art_portfolio_path).exists()
    if not art_portfolio_path_exists:
        print('art_portfolio_path is false: art portfolio directory does NOT exist')
        print('\n\n')
        print('Creating "/images/ArtPortfolio" directory')
        # https://csatlas.com/python-create-directory/
        Path(art_portfolio_path).mkdir()
    os.chdir(art_portfolio_path)

def create_thumbnails():
    print('CALLING create_thumbnails() FUNCTION...')
    picture_directories = list(filter(os.path.isdir, os.listdir(art_portfolio_path)))
    for directory in picture_directories:
        print('Checking for thumbnails directory')
        # thumbs_path = str('/var/www/musimatic/images/ArtGallery/' + str(directory) + '/thumbs')
        thumbs_path = str(str(art_portfolio_path) + "/" + str(directory) + '/thumbs')
        print('thumbs_path: ' + str(thumbs_path))
        # Check if a thumbnails directory exist
        thumbs_path_exists = Path(thumbs_path).exists()
        if thumbs_path_exists:
            print('thumbs_path_exists is true: thumbnail directory exists')
        # if not thumbails directory:  
        if not thumbs_path_exists:
            print('thumbs_path_exists is false: thumbnail directory does NOT exist')
            # mkdir thumbnails
            # https://csatlas.com/python-create-directory/
            Path(thumbs_path).mkdir()
        # Create globs for each file type
        picture_paths_jpg = (x.resolve() for x in Path(directory).glob("*.jpg"))
        picture_paths_png = (x.resolve() for x in Path(directory).glob("*.png"))
        picture_paths = itertools.chain(picture_paths_jpg, picture_paths_png)
        picture_paths_strings = [str(p) for p in picture_paths]
        # Cycle through each picture_path string
        print('Cycling through each picture_path string')
        for picture_path in picture_paths_strings:
            # Use PosixPath() to split path parts accordingly
            current_filename = PosixPath(picture_path).name
            current_stem = PosixPath(picture_path).stem
            current_parent = PosixPath(picture_path).parent
            print('current_filename: ' + str(current_filename))
            print('current_stem: ' + str(current_stem))
            print('current_parent: ' + str(current_parent))
            thumb_image_version = str(str(current_parent) + '/thumbs/thumb_' + current_filename)
            # https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists/
            thumb_image_version_exists = Path(thumb_image_version).exists()
            print('thumb_image_version: ' + str(thumb_image_version))
            print('thumb_image_version_exists: ' + str(thumb_image_version_exists))
            # if not thumbnails/image.ext:
            if not thumb_image_version_exists:
                print('Creating new thumbnail image...')
                with wand_image(filename = picture_path) as image:
                    with image.clone() as thumbnail:
                        thumbnail.thumbnail(175, 150)
                        thumbnail.save(filename=thumb_image_version)


def main():
    # Create CSS style sheet using project's example:
    # https://stackoverflow.com/questions/55600606/how-can-i-create-a-css-file-in-python
    # with open('WEBSITE_PATH' + '/css/artgallery.css', 'w') as stylesheet:
        # stylesheet.write(cssTextDecoded)
    # https://www.geeksforgeeks.org/python-copy-contents-of-one-file-to-another-file/
    # Copy over the 'artgallery.css' file from the project to the user's '/css/artgallery.css' file using 'WEBSITE_PATH"
    print('PROJECT_DIRECTORY: ' + str(PROJECT_DIRECTORY))    
    print('WEBSITE_PATH: ' + str(WEBSITE_PATH))
    css_file_path = str(WEBSITE_PATH + '/css/artportfolio.css')
    print('css_file_path: ' + str(css_file_path))
    shutil.copyfile(str(PROJECT_DIRECTORY) + '/artportfolio.css', css_file_path)

    # Create JS script for art gallery page using project's example:
    js_file_path = str(WEBSITE_PATH + '/js/artportfolio.js')
    shutil.copyfile(str(PROJECT_DIRECTORY) + '/artportfolio.js', js_file_path)
    
    # Create favicon:
    favicon_file_path = str(WEBSITE_PATH + '/favicon/artportfolio.ico')
    shutil.copyfile(str(PROJECT_DIRECTORY) + '/artportfolio.ico', favicon_file_path)
    
    print('CALLING main() FUNCTION...')
    # with open('/var/www/musimatic/pythonprojectwebsites/ArtGallery/artgallery.html', 'w') as f:
    with open(str(WEBSITE_PATH) + '/index.html', 'w') as f:
        f.write('<!DOCTYPE html>')
        f.write('<html>')
        f.write('<head>')
        f.write('<meta charset="UTF-8"/>')
        f.write('<title>SamBanya.com: Art Portfolio Site Of Sam Banya</title>')
        f.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@4.0/dist/fancybox.css"/>')
        f.write('<link rel="stylesheet" href="https://unpkg.com/tailwindcss@2.2.19/dist/tailwind.min.css"/>')
        f.write('<link rel="stylesheet" href="css/artportfolio.css"/>')
        f.write('</head>')
        f.write('<body>')
        f.write('<div id="navbarDiv">')
        f.write('<ul>')
        f.write('<li class="navbar"><a href="https://www.sambanya.com/index.html">Portfolio</a></li>')
        f.write('<li class="navbar"><a href="https://www.sambanya.com/artgallery.html">Art Gallery</a></li>')
        f.write('<li class="navbar"><a href="https://www.sambanya.com/music.html">Music</a></li>')
        f.write('</ul>')
        f.write('</div>')
        f.write('<br />')
        f.write('<div id="content">')
        current_date_eastern = pendulum.now('America/New_York').format('dddd, MMMM D, YYYY')
        current_time_eastern = pendulum.now('America/New_York').format('hh:mm:ss A')
        print('Last Time Updated:')
        print(str(current_date_eastern) + ' at ' + str(current_time_eastern))
        os.chdir(art_portfolio_path)
        picture_directories = sorted(filter(os.path.isdir, os.listdir(art_portfolio_path)), reverse=True)
        for directory in picture_directories:
            picture_paths_jpg = (x.resolve() for x in Path(directory).glob("*.jpg"))
            picture_paths_png = (x.resolve() for x in Path(directory).glob("*.png"))
            picture_paths = itertools.chain(picture_paths_jpg, picture_paths_png)
            picture_paths_strings = [str(p) for p in picture_paths]
            f.write('<div class="flex flex-wrap gap-5 justify-center max-w-5xl mx-auto px-6">')
            for picture_path in picture_paths_strings:
                current_filename = PosixPath(picture_path).name
                current_stem = PosixPath(picture_path).stem
                current_parent = PosixPath(picture_path).parent
                regular_image_version = str(picture_path).replace(str(WEBSITE_PATH + '/'), str(WEBSITE_ADDRESS + '/'))
                thumb_image_version = str(str(current_parent) + '/thumbs/thumb_' + current_filename)
                thumb_image_version = str(thumb_image_version).replace(str(WEBSITE_PATH + '/'), str(WEBSITE_ADDRESS + '/'))
                print('thumb_image_version: ' + str(thumb_image_version))
                picture_img_tag = str('<a data-fancybox="gallery" href="' + str(regular_image_version) + '" data-fancybox="' + str(current_filename) + '" data-caption="' + str(current_filename) + '"><img src="' + str(thumb_image_version) + '"/></a>')
                f.write(picture_img_tag)
            # Seal off picture based div tag section
            f.write('</div>')
            # Seal off 'content' based div tag
            f.write('</div>')
            f.write('<!-- Fancybox JS Script via CDN: -->')
            f.write('<script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@4.0/dist/fancybox.umd.js"></script>')
            f.write('</body>')
            f.write('</html>')
            print('ART PORTFOLIO COMPLETE!')


if __name__ == '__main__':
    create_art_portfolio()
    create_thumbnails()
    main()
