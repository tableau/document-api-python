import contextlib
import os
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET

try:
    from distutils2.version import NormalizedVersion as Version
except ImportError:
    from distutils.version import LooseVersion as Version

MIN_SUPPORTED_VERSION = Version("9.0")


class TableauVersionNotSupportedException(Exception):
    pass


def xml_open(filename):
    # Determine if this is a twb or twbx and get the xml root
    if zipfile.is_zipfile(filename):
        tree = get_xml_from_archive(filename)
    else:
        tree = ET.parse(filename)
    file_version = Version(tree.getroot().attrib.get('version', '0.0'))
    if file_version < MIN_SUPPORTED_VERSION:
        raise TableauVersionNotSupportedException(file_version)
    return tree


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d)


def find_file_in_zip(zip_file):
    for filename in zip_file.namelist():
        try:
            with zip_file.open(filename) as xml_candidate:
                ET.parse(xml_candidate).getroot().tag in (
                    'workbook', 'datasource')
                return filename
        except ET.ParseError:
            # That's not an XML file by gosh
            pass


def get_xml_from_archive(filename):
    with zipfile.ZipFile(filename) as zf:
        with zf.open(find_file_in_zip(zf)) as xml_file:
            xml_tree = ET.parse(xml_file)

    return xml_tree


def build_archive_file(archive_contents, zip_file):
    for root_dir, _, files in os.walk(archive_contents):
        relative_dir = os.path.relpath(root_dir, archive_contents)
        for f in files:
            temp_file_full_path = os.path.join(
                archive_contents, relative_dir, f)
            zipname = os.path.join(relative_dir, f)
            zip_file.write(temp_file_full_path, arcname=zipname)


def save_into_archive(xml_tree, filename, new_filename=None):
    # Saving a archive means extracting the contents into a temp folder,
    # saving the changes over the twb/tds in that folder, and then
    # packaging it back up into a specifically formatted zip with the correct
    # relative file paths

    if new_filename is None:
        new_filename = filename

    # Extract to temp directory
    with temporary_directory() as temp_path:
        with zipfile.ZipFile(filename) as zf:
            xml_file = find_file_in_zip(zf)
            zf.extractall(temp_path)
        # Write the new version of the file to the temp directory
        xml_tree.write(os.path.join(
            temp_path, xml_file), encoding="utf-8", xml_declaration=True)

        # Write the new archive with the contents of the temp folder
        with zipfile.ZipFile(new_filename, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
            build_archive_file(temp_path, new_archive)


def _save_file(container_file, xml_tree, new_filename=None):
    if zipfile.is_zipfile(container_file):
        save_into_archive(xml_tree, container_file, new_filename)
    else:
        xml_tree.write(container_file, encoding="utf-8", xml_declaration=True)
