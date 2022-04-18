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
                # create_thumbnail(path_to_image, thumbnail_path)                        
                # with Image(filename = picture_path) as image:
                # https://www.geeksforgeeks.org/wand-thumbnail-function-python/
                with wand_image(filename = picture_path) as image:
                    with image.clone() as thumbnail:
                        thumbnail.thumbnail(175, 150)
                        thumbnail.save(filename=thumb_image_version)

                        
def create_thumbnails_gifs():
    print('CALLING create_thumbnails() FUNCTION...')
    os.chdir(art_portfolio_path)
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
            Path(thumbs_path).mkdir()
        # Create globs for each file type
        picture_paths_gif = (x.resolve() for x in Path(directory).glob("*.gif"))
        picture_paths = itertools.chain(picture_paths_gif)
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
            thumb_image_version_exists = Path(thumb_image_version).exists()
            print('thumb_image_version: ' + str(thumb_image_version))
            print('thumb_image_version_exists: ' + str(thumb_image_version_exists))
            # if not thumbnails/image.ext:
            if not thumb_image_version_exists:
                print('Creating new thumbnail gif image...')
                # Taken from this SO post:
                # https://stackoverflow.com/questions/9988517/resize-gif-animation-pil-imagemagick-python
                # TODO: Create thumbnail versions of GIF images

                
def main():
    # Create CSS style sheet using project's example:
    # https://stackoverflow.com/questions/55600606/how-can-i-create-a-css-file-in-python
    # with open('WEBSITE_PATH' + '/css/artgallery.css', 'w') as stylesheet:
        # stylesheet.write(cssTextDecoded)
    # https://www.geeksforgeeks.org/python-copy-contents-of-one-file-to-another-file/
    # Copy over the 'artgallery.css' file from the project to the user's '/css/artgallery.css' file using 'WEBSITE_PATH"
    css_file_path = str(WEBSITE_PATH + '/css/artportfolio.css')
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
        f.write('<title>Art Portfolio</title>')
        f.write('<meta charset="utf-8"/>')
        # f.write('<link rel="stylesheet" href="https://musimatic.xyz/css/artgallery.css" type="text/css"/>')
        f.write('<link rel="stylesheet" href="./css/artportfolio.css" type="text/css"/>')        
        f.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/ui@4.0/dist/fancybox.css"/>')        
        f.write('<link rel="shortcut icon" type="image/ico" href="favicon/artportfolio.ico"/>')
        f.write('</head>')        
        f.write('<body>')
        print('CREATING LEFT MENU')
        f.write('<div id="left_menu">')
        f.write('<h1>Art Portfolio</h1>')
        # f.write('<a href="http://www.musimatic.xyz">BACK TO HOMEPAGE</a>')
        f.write('<a href="' + str(WEBSITE_FULL_ADDRESS) + '">BACK TO HOMEPAGE</a>')
        current_date_eastern = pendulum.now('America/New_York').format('dddd, MMMM D, YYYY')
        current_time_eastern = pendulum.now('America/New_York').format('hh:mm:ss A')        
        f.write('<p>Last Time Updated:</p>')
        f.write('<p>' + str(current_date_eastern) + ' at ' + str(current_time_eastern) + ' EDT</p>')
        # f.write('<a href="https://git.musimatic.xyz/ArtGalleryCreator/tree/">Source Code Link</a>')
        f.write('<a href="https://github.com/SamuelBanya/ArtPortfolioCreator">Source Code Link</a>')
        f.write('<br />')
        f.write('<h2>Sections</h2>')
        # art_gallery_path = '/var/www/musimatic/images/ArtGallery'
        os.chdir(art_portfolio_path)
        # Adding revision so that latest artwork shows up on top of gallery page:
        # https://docs.python.org/3/howto/sorting.html
        picture_directories = sorted(filter(os.path.isdir, os.listdir(art_portfolio_path)), reverse=True)
        for directory in picture_directories:
            picture_directory_anchor = str('<a href="#' + str(directory) + '">' + str(directory) + '</a>')
            f.write(picture_directory_anchor)
            f.write('<br />')
        f.write('</div>')

        print('CREATING IMAGE GALLERY FOR RIGHT SIDE')
        f.write('<div id="right_art_portfolio">')

        print('WORKING ON CREATING IMG TAGS')
        for directory in picture_directories:
            picture_directory_header = str('<h1 id="' + str(directory) + '">' + str(directory) + '</h1>')
            f.write(picture_directory_header)
            f.write('<br />')
            # SO Post on Globs:
            # https://stackoverflow.com/questions/4568580/python-glob-multiple-filetypes
            picture_paths_jpg = (x.resolve() for x in Path(directory).glob("*.jpg"))
            picture_paths_png = (x.resolve() for x in Path(directory).glob("*.png"))
            # TODO: Once I fix the 'create_thumbnails_gifs()' function, return to this:
            # picture_paths_gif = (x.resolve() for x in Path(directory).glob("*.gif"))            
            # picture_paths = itertools.chain(picture_paths_jpg, picture_paths_png, picture_paths_gif)
            picture_paths = itertools.chain(picture_paths_jpg, picture_paths_png)
            # SO Post on string replacement:
            # https://stackoverflow.com/questions/9452108/how-to-use-string-replace-in-python-3-x            
            # picture_paths_strings = [str(p).replace('/var/www/musimatic/', 'https://musimatic.xyz/') for p in picture_paths]
            picture_paths_strings = [str(p) for p in picture_paths]            
            # pprint.pprint(picture_paths_strings)   
            for picture_path in picture_paths_strings:
                current_filename = PosixPath(picture_path).name
                current_stem = PosixPath(picture_path).stem
                current_parent = PosixPath(picture_path).parent
                # regular_image_version = str(picture_path).replace('/var/www/musimatic/', 'https://musimatic.xyz/')
                regular_image_version = str(picture_path).replace(str(WEBSITE_PATH + '/'), str(WEBSITE_ADDRESS + '/'))
                thumb_image_version = str(str(current_parent) + '/thumbs/thumb_' + current_filename)
                # thumb_image_version = str(thumb_image_version).replace('/var/www/musimatic/', 'https://musimatic.xyz/')
                thumb_image_version = str(thumb_image_version).replace(str(WEBSITE_PATH + '/'), str(WEBSITE_ADDRESS + '/'))
                print('thumb_image_version: ' + str(thumb_image_version))
                picture_img_tag = str('<a data-fancybox="gallery" href="' + str(regular_image_version) + '" data-fancybox="' + str(current_filename) + '" data-caption="' + str(current_filename) + '"><img src="' + str(thumb_image_version) + '"/></a>')
                f.write(picture_img_tag)
        # Sealing off right side of page's div tag for the image gallery portion:
        f.write('</div>')
        f.write('<script src="https://cdn.jsdelivr.net/npm/@fancyapps/ui@4.0/dist/fancybox.umd.js"></script>')
        # f.write('<script type="text/javascript" src="https://musimatic.xyz/js/artgallery.js"></script>')
        f.write('<script type="text/javascript" ' + 'src="' + str(WEBSITE_ADDRESS) + '/js/artportfolio.js"></script>')
        f.write('</body>')
        f.write('</html>')
        print('ART PORTFOLIO COMPLETE!')

        
if __name__ == '__main__':
    create_art_portfolio()
    create_thumbnails()
    # create_thumbnails_gifs()
    main()
