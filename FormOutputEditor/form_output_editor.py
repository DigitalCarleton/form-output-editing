"""
A small module to read in a TSV file and produce an altered copy
according to specifications in a JSON file.

:run: python3 form_output_editor <config_file>
:arg config_file: location/filename of the JSON configuration
    file to use; required

:file: form_output_editor.py
:author: Luna Yee, 03-07-2019
"""

import csv
import json
import sys
from shutil import copyfile
from string import Template


def load_config(config_file):
    """
    Loads a JSON configuration for this instantiation. The config file
    should be provided by the user and have the structure outlined in
    the README.

    :param config_file: <string> specifying the location of the JSON
        file
    :return: <dict> of configuration specifications
    """
    with open(config_file) as jsonfile:
        config = json.load(jsonfile)

    return config


def load_data(data_sheet):
    """
    Loads the data from a TSV spreadsheet, and returns it as a list
    of OrderedDict objects.

    :param data_sheet: <string> specifying the location of the source
        TSV file
    :return: <OrderedDict>[] listing dictionaries for each content row,
        with the headers (from row 1) as keys to the related data
    """
    # DictReader will turn each row of data into an OrderedDict
    # using the first row in the TSV (the field names) as keys
    with open(data_sheet, newline='') as tsvfile:
        data_reader = csv.DictReader(tsvfile, dialect='excel-tab')
        # Save each row of data into a list of entries
        data = []
        for row in data_reader:
            data.append(row)

    return data


def write_data(target_sheet, data):
    """
    Writes the data in a list of OrderedDict objects to a TSV spreadsheet.
    Each OrderedDict should connect the headers (as keys) to the data (as
    values) for one row.

    :param target_sheet: <string> specifying the location to which to
        write the new TSV file; must be write-able
    """
    # Retrieve key names as header fields from an entry
    fieldnames = data[0].keys()
    # DictReader will turn each row of data into an OrderedDict
    # using the first row in the TSV (the field names) as keys
    with open(target_sheet, 'w', newline='') as tsvfile:
        data_writer = csv.DictWriter(tsvfile, fieldnames, dialect='excel-tab')
        # Write first row (the field names)
        data_writer.writeheader()
        # Write each row of (revised) data
        for entry in data:
            data_writer.writerow(entry)


def gen_filename(entry, template, rename_fields):
    """
    Given a Template, fields to use, and the data of a given entry,
    generates a filename for that entry. Uses the built-in
    Template.safe_substitute() method.

    :param entry: <OrderedDict> mapping keys as headers to data in values
    :param template: <Template> to use when generating filenames; currently
        does not guarantee uniqueness
    :param rename_fields: <dict> with used fields as keys; can optionally
        include <dict> values that indicate modifications to the cell data
        to be made before inclusion in the filename
    :return: <string> filename for the entry according to the template
    """
    template = Template(template)
    # Mapping template: instances of each key will be replaced with the value
    mapping = dict()
    # Retrieve keys and values of rename_fields as tuples in a list
    fields = rename_fields.items()
    for item in fields:
        field, instrs = item
        # Target for field reference is value of field modified per edit_params
        mapping[field] = edit_value(entry[field], instrs)
    # Substitute placeholders with modified values in mapping
    filename = template.safe_substitute(mapping)

    return filename


def edit_value(value, instrs):
    """
    Edits a <string> of data according to a set of instructions given by
    a <dict>. Current supported instructions: "truncate", "replace",
    "remove". See README and comments below for more information.

    :param value: <string> data to edit
    :param instrs: <dict> of instructions for how the value should be
        edited; see README > Config > "renameFields" for more
    :return: <string> edited data, per instrs
    """
    edited = value
    # Execute truncate instruction
    '''
    Truncates the value at the first instance of to_truncate
    (the associated string)
    '''
    if "truncate" in instrs:
        to_truncate = instrs["truncate"]
        truncate_index = edited.find(to_truncate)
        if truncate_index > -1:
            edited = edited[:truncate_index]
    # Execute replace instruction
    '''
    Replaces all instances of to_replace (the first string in the
    associated list-like) in the value with to_insert (the second
    string in the associated list-like)
    '''
    if "replace" in instrs:
        to_replace, to_insert = instrs["replace"]
        edited = edited.replace(to_replace, to_insert)
    # Execute remove instruction
    '''
    Removes all instances of to_remove (the associated string) from
    the value
    '''
    if "remove" in instrs:
        to_remove = instrs["remove"]
        edited = edited.replace(to_remove, '')

    return edited


def get_ext(filename):
    """
    Returns the extension of the file given by filename.

    :param filename: <string> name/location of a file, with
        extension included
    :return: <string> extension, including '.', of given filename
    """
    ext_index = filename.rfind('.')
    assert ext_index > -1
    ext = filename[ext_index:]

    return ext


def rename_keys(entry, aliases):
    """
    Renames the keys in a <dict>-like object to a set of aliases.
    Does not guarantee to preserve order, but preserves values.

    :param entry: <dict>-like whose keys to edit
    :param aliases: <dict> that has keys to rename as its keys and
        desired new names as their values
    """
    alias_list = aliases.items()
    for alias in alias_list:
        oldkey, newkey = alias
        # TODO: add logic to ensure no overwrites
        entry[newkey] = entry.pop(oldkey)


def delete_keys(entry, delete_fields):
    """
    Deletes all keys in a <dict-like> object that match items
    in a list of <string>s, along with their values.

    :param entry: <dict>-like whose keys to edit
    :param delete_fields: <string>[] that lists any and all
        keys to delete.
    """
    for to_delete in delete_fields:
        entry.pop(to_delete)


def rename_files(config, data):
    """
    Copies all files in some source directory to a target
    directory, renaming according to specifications in the config.
    See README > Config > Rename Files for more information.

    :param config: <dict> containing configuration information
    :param data: <OrderedDict>[] containing the data of the
        source spreadsheet by row; must include a field with
        the filenames in the source directory
    """
    # Collect relevant data from config
    srcdir = config["sourceFileDir"] if "sourceFileDir" \
                                           in config else ''
    dstdir = config["targetFileDir"] if "targetFileDir" \
                                           in config else ''
    file_field = config["filenameField"]
    assert file_field in data[0].keys()
    template = config["renameTemplate"]
    rename_fields = config["renameFields"]
    # For every entry in the data, copy the image with the revised
    # name to the destination provided
    for entry in data:
        src_filename = entry[file_field]
        dst_filename = gen_filename(entry, template, rename_fields)
        dst_filename += get_ext(src_filename)
        # TODO: add logic to test for illegal characters
        # TODO: add logic to avoid overwrites
        copyfile(srcdir + src_filename, dstdir + dst_filename)
        entry[file_field] = dst_filename


def alias_fields(config, data):
    """
    Renames fields (headers/keys) in the data according to
    specifications in the config. See README > Config > Alias
    Fields for more information.

    :param config: <dict> containing configuration information
    :param data: <OrderedDict>[] containing the data of the
        source spreadsheet by row
    """
    # Collect relevant data from config
    aliases = config["aliases"]
    # For every entry in the data, change key names from
    # the keys of aliases to their respective values
    for entry in data:
        rename_keys(entry, aliases)


def delete_fields(config, data):
    """
    Deletes fields (headers/keys with their associated values)
    in the data according to specifications in the config. See
    README > Config > Delete Fields for more information.

    :param config: <dict> containing configuration information
    :param data: <OrderedDict>[] containing the data of the
        source spreadsheet by row
    """
    # Collect relevant data from config
    delete_flag = config["deleteFlag"]
    # Retrieve key names as header fields from an entry
    fieldnames = data[0].keys()
    # Find all fields whose names include delete_flag
    delete_fields = [field for field in fieldnames
                     if field.find(delete_flag) > -1]
    # For every entry in the data, delete items whose
    # keys contain the delete_flag
    for entry in data:
        delete_keys(entry, delete_fields)


def main(config, data):
    """
    Edits the data from the source TSV (does not impact the source
    TSV) according to specifications in the config, then writes the
    data to some destination, also specified in the config. See
    README > Config for a full description of tools available.

    :param config: <dict> containing configuration information
    :param data: <OrderedDict>[] containing the data of the
        source spreadsheet by row
    """
    # Rename pictures
    if config["renameFiles"]:
        rename_files(config, data)
    # Rename fields while preserving values
    if config["aliasFields"]:
        alias_fields(config, data)
    # Delete fields whose names include some sentinel
    if config["deleteFields"]:
        delete_fields(config, data)

    write_data(config["targetSheet"], data)


if __name__ == "__main__":
    # Need one argument: JSON file location
    if len(sys.argv) < 2:
        print('metadata_compile requires 1 argument: "config_file"', file=sys.stderr)
        sys.exit(1)
    config_file = sys.argv[1]
    config = load_config(config_file)
    data = load_data(config["sourceSheet"])
    if len(data) < 1:
        print('no data to operate on; terminating', file=sys.stderr)
        sys.exit(1)
    main(config, data)