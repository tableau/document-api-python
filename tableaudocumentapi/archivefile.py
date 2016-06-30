import contextlib
import os
import shutil
import tempfile
import zipfile

import xml.etree.ElementTree as ET


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d)


def find_file_in_zip(zip, ext):
    for filename in zip.namelist():
        if os.path.splitext(filename)[-1].lower() == ext[:-1]:
            return filename


def get_xml_from_archive(filename):
    file_type = os.path.splitext(filename)[-1].lower()
    with temporary_directory() as temp:
        with zipfile.ZipFile(filename) as zf:
            zf.extractall(temp)
            xml_file = find_file_in_zip(zf, file_type)
            xml_tree = ET.parse(os.path.join(temp, xml_file))

    return xml_tree


def build_archive_file(archive_contents, zip):
    for root_dir, _, files in os.walk(archive_contents):
        relative_dir = os.path.relpath(root_dir, archive_contents)
        for f in files:
            temp_file_full_path = os.path.join(
                archive_contents, relative_dir, f)
            zipname = os.path.join(relative_dir, f)
            zip.write(temp_file_full_path, arcname=zipname)


def save_into_archive(xml_tree, filename, new_filename=None):
    # Saving a archive means extracting the contents into a temp folder,
    # saving the changes over the twb in that folder, and then
    # packaging it back up into a specifically formatted zip with the correct
    # relative file paths

    if new_filename is None:
        new_filename = filename

    # Extract to temp directory
    with temporary_directory() as temp_path:
        file_type = os.path.splitext(filename)[-1].lower()
        with zipfile.ZipFile(filename) as zf:
            twb_file = find_file_in_zip(zf, file_type)
            zf.extractall(temp_path)
        # Write the new version of the twb to the temp directory
        xml_tree.write(os.path.join(
            temp_path, twb_file), encoding="utf-8", xml_declaration=True)

        # Write the new archive with the contents of the temp folder
        with zipfile.ZipFile(new_filename, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
            build_archive_file(temp_path, new_archive)
