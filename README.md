# Apt Signature Verification

Conditional signature verification for apt.

## Why this tool exists

### The threat

[diagram?]

Take the following scenario:
1. We produce our own deb packages to distribute to servers
1. We use a third-party service (example: Packagecloud), or our own repo
1. An adversary gains access to the repo and injects a malicious package, example: `htop`
1. Third-party provider, or we, sign the manifest file - putting a stamp of approval on the malicious package
1. We distribute and install the malicious package on every server, as root (also see recent `apt` vulnerability)

For this reason we may decide to sign our custom packages before uploading them to Packagecloud.

However validating this signature using available tooling poses many issues.


### The issues

There are few good options for performing package integrity verification when using Debian's apt.

They consist broadly of:

1. debsig-verify
   Cumbersome to configure but reasonable integrity assertions.
   Integrates directly into dpkg by disabling the `no-debsig` option in any Debian distribution.
1. dpkg-verify
   Good concept. Could be brought up to modern standards.
   No integration into existing tooling, must be manually run against packages.

Both options have a serious flaw in operation: They are **either** ON or OFF. All in.


### On or off?

Take the following scenario:
1. We use debian package repo's to obtain the majority of our tools, and security updates
1. We use our own repo to provide custom tooling - we do not have good control over manifest signing (think: Packagecloud)
    1. As a result we use debsign to sign the packages


With debsig-verify turned OFF (default): No signatures are verified, we are exposed to malicious package injection in our repo
With debsig-verify turned ON: our packages install just fine, but nothing from the Debian repos is signed - thus our setup is hobbled


The ideal scenario consists broadly of:
1. We can enable signature verification on a per-repo basis
1. All packages for a matching repo are verified, and failing verification will **not** be installed
1. All packages for a non-matching repo (think: Debian) bypass verification and are installed as normal (we trust their manifest signing)
1. We can use any signature verification mechanism on a per-repo basis: one may use dpkg-sig and another debsign on the same system


Hence: aptsign-verify -- conditional signature verification for apt.


## Installation

`pip install aptsign`


## Configuration

Copy the example configuration into place:

`cp /usr/local/etc/aptsign.yml.example /etc/aptsign.yml`

Modify the configuration to point to your signed-package repository.


### Hook into apt

Copy the apt-hook script into place:

`cp /usr/local/etc/apt/apt.conf.d/60aptsign /etc/apt/apt.conf.d/`


## Run apt-get

`apt-get install mypackage`
