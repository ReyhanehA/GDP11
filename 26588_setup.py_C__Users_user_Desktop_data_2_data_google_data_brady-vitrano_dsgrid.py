import setuptools
import os
import sys

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

setuptools.setup(
    name="dsgrid",
    version='0.1.6',
    description="Build and Manage a Selenium Grid using Docker.",
    packages=['dsgrid', 'dsgrid.tests'],
    author="Brady Vitrano",
    author_email="bjvitrano@gmail.com",
    license="Apache",
    keywords="docker selenium grid firefox phantomjs chrome",
    url="https://github.com/brady-vitrano/dsgrid",
    entry_points={
        'console_scripts': [
            'dsgrid = dsgrid.shell:main'
        ]
    },
    install_requires=[
        'docker-py',
        'mock'
    ],
    data_files=[
        ("dsgrid/files/firefox", [os.path.join(SOURCE_DIR, "dsgrid/files/firefox/Dockerfile"),
                                  os.path.join(SOURCE_DIR, "dsgrid/files/firefox/register-node.sh")]),
        ("dsgrid/files/phantomjs", [os.path.join(SOURCE_DIR, "dsgrid/files/phantomjs/Dockerfile"),
                                    os.path.join(SOURCE_DIR, "dsgrid/files/phantomjs/register-node.sh")]),
        ("dsgrid/files/selenium", [os.path.join(SOURCE_DIR, "dsgrid/files/selenium/Dockerfile")]),
        ("dsgrid/files/chrome", [os.path.join(SOURCE_DIR, "dsgrid/files/chrome/Dockerfile"),
                                 os.path.join(SOURCE_DIR, "dsgrid/files/chrome/run.sh")])
    ],
    long_description="Selenium Grid in Docker"
)
