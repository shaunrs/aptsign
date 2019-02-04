from setuptools import setup

setup(
    name="aptsign",
    version="0.1",
    author="Shaun S",
    url="https://github.com/shaunrs/aptsign",
    description="Conditionally validate signatures on Debian packages",
    packages=[
        "aptsign",
    ],
    entry_points={
        'console_scripts': [
            'aptsign-verify = aptsign.cli:verify'
        ]
    },
    install_requires=[
        "pyyaml",
    ],
    data_files=[
        ('etc', [
            "etc/aptsign.yml.example",
            "etc/aptsign.yml"
        ]),
        ('etc/apt/apt.conf.d', [
            "etc/60aptsign",
        ])
    ]
)
