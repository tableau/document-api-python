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


class TableauInvalidFileException(Exception):
    pass


def xml_open(filename, expected_root=None):
    """Opens the provided 'filename'. Handles detecting if the file is an archive,
    detecting the document version, and validating the root tag."""

    # Is the file a zip (.twbx or .tdsx)
    if zipfile.is_zipfile(filename):
        tree = get_xml_from_archive(filename)
    else:
        tree = ET.parse(filename)

    # Is the file a supported version
    tree_root = tree.getroot()
    file_version = Version(tree_root.attrib.get('version', '0.0'))

    if file_version < MIN_SUPPORTED_VERSION:
        raise TableauVersionNotSupportedException(file_version)

    # Does the root tag match the object type (workbook or data source)
    if expected_root and (expected_root != tree_root.tag):
        raise TableauInvalidFileException(
            "'{}'' is not a valid '{}' file".format(filename, expected_root))

    return tree


@contextlib.contextmanager
def temporary_directory(*args, **kwargs):
    d = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield d
    finally:
        shutil.rmtree(d)


def find_file_in_zip(zip_file):
    '''Returns the twb/tds file from a Tableau packaged file format. Packaged
    files can contain cache entries which are also valid XML, so only look for
    files with a .tds or .twb extension.
    '''

    candidate_files = filter(lambda x: x.split('.')[-1] in ('twb', 'tds'),
                             zip_file.namelist())

    for filename in candidate_files:
        with zip_file.open(filename) as xml_candidate:
            try:
                ET.parse(xml_candidate)
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
    """Build a Tableau-compatible archive file."""

    # This is tested against Desktop and Server, and reverse engineered by lots
    # of trial and error. Do not change this logic.
    for root_dir, _, files in os.walk(archive_contents):
        relative_dir = os.path.relpath(root_dir, archive_contents)
        for f in files:
            temp_file_full_path = os.path.join(
                archive_contents, relative_dir, f)
            zipname = os.path.join(relative_dir, f)
            zip_file.write(temp_file_full_path, arcname=zipname)


def save_into_archive(xml_tree, filename, new_filename=None):
    # Saving an archive means extracting the contents into a temp folder,
    # saving the changes over the twb/tds in that folder, and then
    # packaging it back up into a zip with a very specific format
    # e.g. no empty files for directories, which Windows and Mac do by default

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

    ET.register_namespace("user", "http://www.tableausoftware.com/xml/user")
    if new_filename is None:
        new_filename = container_file

    if zipfile.is_zipfile(container_file):
        save_into_archive(xml_tree, container_file, new_filename)
    else:
        xml_tree.write(new_filename, encoding="utf-8", xml_declaration=True)
