import sys

import subprocess
import yaml

import apt

from aptsign import Package, Filters


def verify():
    # remove/purge gives nothing on stdin
    # install gives filename
    input_filenames = []

    for line in sys.stdin:
        input_filenames.append(line.strip())

    with open('/etc/aptsign.yml') as _file:
        config = yaml.load(_file)

    cache = apt.Cache()

    for filename in input_filenames:
        process_package(config, filename, cache)


def process_package(config, filename, cache):
    print("DEBUG: Filename: {}".format(filename))

    pkg = Package(cache)

    # Allow PackageNotFound to bubbe up
    # dpkg should not continue if we are unable to verify the package
    pkg.by_filename(filename)

    print("DEBUG: Package name: {}".format(pkg))

    # Generate the filters from configuration file
    filters = Filters()
    for _, repo in config['repositories'].items():
        filters.new(repo['filter'], repo['app'])

    # Pass the package through the filter list, get a list of matching filters
    # We now have a list of filters which tell us what to do
    package_filter = filters.is_match(pkg)

    # If there was no match found, ignore this package
    if not package_filter:
        print("No filter found, skipping signature checks..")
        return

    print("DEBUG: Matched filter: \"{}\"".format(package_filter))
    print("Validating signatures for {} using '{}'".format(pkg, package_filter.app))

    command = "{} {}".format(package_filter.app, pkg.filename)

    print("DEBUG: command '{}'".format(command))
    try:
        subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        print("ERROR: Signature verification check FAILED")
        sys.exit(error.returncode)
