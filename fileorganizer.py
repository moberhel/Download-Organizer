from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# folders to track
source_directory = "/Users/Max Oberhellman/Downloads"
dest_audio_directory = "/Users/Max Oberhellman/Desktop/Audio"
dest_video_directory = "/Users/Max Oberhellman/Desktop/Video"
dest_image_directory = "/Users/Max Oberhellman/Desktop/Images"
dest_document_directory = "/Users/Max Oberhellman/Desktop/Documents"
dest_leclab_directory = "/Users/Max Oberhellman/Desktop/Documents/LectureLabs"
dest_programming_directory = "/Users/Max Oberhellman/Desktop/Projects"
dest_other_directory = "/Users/Max Oberhellman/Desktop/Other"


# below are the extensions for images, videos, audio, documents, and programming
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

programming_extensions = [".exe", ".py", ".js", ".s", ".c", ".htm", ".html", ".jsp", ".css", ".class", ".swift", ".cpp",
                      ".php", ".cs", ".cgi", ".pl", ".h", ".java", ".sh", ".vb"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # if there's a file with the same name, this keeps on adding 1 till it's unique
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # this will run whenever there is a change in the source directory 
    def on_modified(self, event):
        with scandir(source_directory) as entries:
            for entry in entries:
                name = entry.name
                dest = self.check_file_destination(name)
                move_file(dest, entry, name)
                logging.info(f"Moved video file: {name}")

    # .upper is there for file extensions in upper case
    def check_file_destination(self, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                return dest_image_directory
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                return dest_video_directory
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                return dest_document_directory
        for programming_extension in programming_extensions:
            if name.endswith(programming_extension) or name.endswith(programming_extension.upper()):
                return dest_programming_directory
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                return dest_audio_directory
        return dest_other_directory


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_directory
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()