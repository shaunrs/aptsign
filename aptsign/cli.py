import sys

import logging

import subprocess
import yaml

import apt

from aptsign import Package, Filters


def verify():
    logging.basicConfig(format='aptsign %(message)s', level=logging.INFO)

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
    logging.debug("Package Filename: %s", filename)

    pkg = Package(cache)

    # Allow PackageNotFound to bubble up
    # dpkg should not continue if we are unable to verify the package
    pkg.by_filename(filename)

    logging.debug("Package name: %s", pkg)

    # Generate the filters from configuration file
    filters = Filters()
    for _, repo in config['repositories'].items():
        filters.new(repo['filter'], repo['app'])

    # Pass the package through the filter list, get a list of matching filters
    # We now have a list of filters which tell us what to do
    package_filter = filters.is_match(pkg)

    # If there was no match found, ignore this package
    if not package_filter:
        logging.info("No filter found, skipping signature checks..")
        return

    logging.info("Matched filter: \"%s\"", package_filter)
    logging.info("Validating signatures for %s using '%s'", pkg, package_filter.app)

    command = "{} {}".format(package_filter.app, pkg.filename)

    logging.debug("Passing to command '%s'", command)

    try:
        output = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        logging.error("ERROR: Signature verification check FAILED")
        logging.error(error.output)

        sys.exit(error.returncode)
    else:
        logging.info(output)
