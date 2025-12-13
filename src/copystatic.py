import os
import shutil

def copy_from_source_to_destination(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    source_items = os.listdir(source)
    for item in source_items:
        source_item_path = os.path.join(source, item)
        destination_item_path = os.path.join(destination, item)

        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, destination_item_path)
            print(f"Copying file: {source_item_path} -> {destination_item_path}")
        else:
            os.mkdir(destination_item_path)
            copy_from_source_to_destination(source_item_path, destination_item_path)