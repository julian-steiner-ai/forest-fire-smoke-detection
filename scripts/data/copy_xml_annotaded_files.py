import os
import shutil
import pathlib
import argparse

parser = argparse.ArgumentParser(
    description="Sample TensorFlow XML-to-TFRecord converter")
parser.add_argument("-s",
                    "--source_dir",
                    help="",
                    type=str)
parser.add_argument("-d",
                    "--destination_dir",
                    help="",
                    type=str)

args = parser.parse_args()

def collect_images_with_xml_annotations(dir):
    images_with_annotations = []
    xml_files = list(pathlib.Path(dir).glob("*.xml"))
    for xml_file in xml_files:
        for image_file in get_image_file_to_xml_file(xml_file):
            images_with_annotations.append((image_file, xml_file))
    return images_with_annotations

def get_image_file_to_xml_file(xml_file):
    image_files = [file for file in list(pathlib.Path(str(xml_file.parent)).glob(f"{xml_file.stem}.*")) if not file.name.endswith('xml')]
    return image_files

def copy_images_with_annotations(destination_dir, images_with_annotations):
    for image_path, xml_path in images_with_annotations:
        shutil.copyfile(image_path, os.path.join(destination_dir, image_path.name))
        shutil.copyfile(xml_path, os.path.join(destination_dir, xml_path.name))

def get_source_dir():
    if args.source_dir:
        return args.source_dir
    raise ValueError

def get_destination_dir():
    if args.destination_dir:
        return args.destination_dir
    raise ValueError

def main():
    source_dir = get_source_dir()
    destination_dir = get_destination_dir()
    images_with_annotations = collect_images_with_xml_annotations(source_dir)
    copy_images_with_annotations(destination_dir, images_with_annotations)

if __name__ == '__main__':
    main()