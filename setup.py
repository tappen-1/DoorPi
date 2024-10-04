# -*- coding: utf-8 -*-

import os
import uuid
import sys
import urllib.request
import importlib

# Check for pip, setuptools and wheel
try:
    import pip
    import setuptools
    import wheel
except ImportError as exp:
    print("install missing pip now (%s)" % exp)
    from get_pip import main as check_for_pip
    old_args = sys.argv
    sys.argv = [sys.argv[0]]
    try:
        check_for_pip()
    except SystemExit as e:
        if e.code == 0:
            os.execv(sys.executable, [sys.executable] + old_args)
        else:
            print("install pip failed with error code %s" % e.code)
            sys.exit(e.code)

base_path = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('metadata', os.path.join(base_path, 'doorpi', 'metadata.py'))
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)

def parse_string(raw_string):
    for meta_key in dir(metadata):
        if not meta_key.startswith('__'):
            raw_string = raw_string.replace('!!%s!!' % meta_key,  str(getattr(metadata, meta_key)))
    return raw_string

def read(filename, parse_file_content=False, new_filename=None):
    with open(os.path.join(base_path, filename)) as f:
        file_content = f.read()
    if parse_file_content:
        file_content = parse_string(file_content)
    if new_filename:
        with open(os.path.join(base_path, new_filename), 'w') as f:
            f.write(file_content)
        return new_filename
    return file_content

from setuptools import setup, find_packages
from pip._internal.req import parse_requirements
install_reqs = parse_requirements(os.path.join(base_path, 'requirements.txt'), session=uuid.uuid1())
reqs = [str(req.requirement) for req in install_reqs]  # Changed 'req' to 'requirement' for pip compatibility

setup_dict = dict(
    license=metadata.license,
    name=metadata.package,
    version=metadata.version,
    author=metadata.authors[0],
    author_email=metadata.authors_emails[0],  # Korrigiert auf 'authors_emails'
    maintainer=metadata.authors[0],
    maintainer_email=metadata.authors_emails[0],  # Korrigiert auf 'authors_emails'
    url=metadata.url,
    keywords=metadata.keywords,
    description=metadata.description,
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: Free for non-commercial use',
        'Natural Language :: German',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Internet Phone',
        'Topic :: Communications :: Telephony',
        'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
        'Topic :: Multimedia :: Video :: Capture',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=reqs,
    platforms=["any"],
    use_2to3=False,
    zip_safe=False,  # don't use eggs
    entry_points={
        'console_scripts': [
            'doorpi_cli = doorpi.main:entry_point'
        ]
    }
)


def main():
    try:
        if os.name == 'posix' and os.geteuid() == 0 and \
                not os.path.isfile(metadata.daemon_file) and not os.path.exists(metadata.daemon_file):
            with open(metadata.daemon_file, "w") as daemon_file:
                for line in urllib.request.urlopen(metadata.daemon_online_template):  # urllib2 -> urllib.request
                    daemon_file.write(parse_string(line.decode('utf-8')))  # Python 3 requires decode
            os.chmod(metadata.daemon_file, 0o755)
    except: pass

    setup(**setup_dict)

if __name__ == '__main__':
    main()
