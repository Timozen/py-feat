#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit, os, sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import zipfile

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = {}
with open("feat/version.py") as f:
    exec(f.read(), version)

extra_setuptools_args = dict(
    tests_require=['pytest']
)

class CustomInstall(install):
    def run(self):
        def _post_install():
            import wget
            import os, sys

            def get_resource_path():
                for p in sys.path:
                    if os.path.isdir(p) and "feat" in os.listdir(p):
                        return os.path.join(p, "feat", "resources")

            if os.path.exists(os.path.join(get_resource_path(), "fer_aug_model.h5")):
                print("Fex model already exists; skipping download.")
            else:
                print("Downloading FEX emotion model.")
                try:
                    fex_emotion_model = "https://github.com/cosanlab/feat/releases/download/v0.1/fer_aug_model.h5"
                    wget.download(fex_emotion_model, get_resource_path())
                except:
                    try:
                        fex_emotion_model = "https://www.dropbox.com/s/d3yhtsqggqcrjl2/fer_emotion_model.h5?dl=1"
                        wget.download(fex_emotion_model, get_resource_path())
                    except:
                        print("FeX emotion model failed to download")

                if os.path.exists(os.path.join(get_resource_path(), "fer_aug_model.h5")):
                    print("\nFEX emotion model downloaded successfully.\n")
                else:
                    print("Something went wrong. Model not found in directory.")

            if os.path.exists(os.path.join(get_resource_path(), "lbfmodel.yaml")):
                print("Landmark already exists; skipping download.")
            else:
                print("Downloading landmark detection model.")
                try:
                    lbfmodel = "https://github.com/cosanlab/feat/releases/download/v0.1/lbfmodel.yaml"
                    wget.download(lbfmodel, get_resource_path())
                except:
                    try:
                        lbfmodel = "https://www.dropbox.com/s/cqune0z1bwf79zy/lbfmodel.yaml?dl=1"
                        wget.download(lbfmodel, get_resource_path())
                    except:
                        print("Landmark model failed to download")

            if os.path.exists(os.path.join(get_resource_path(), "align_net.pth")):
                print("\nAU Detection Model Parameters downloaded successfully.\n")
            else:
                print("Downloading JAA Net AU Occurence model.")
                try:
                    jaanet_params = "https://github.com/cosanlab/feat/releases/download/v0.1/JAANetparams.zip"
                    wget.download(jaanet_params, get_resource_path())
                    with zipfile.ZipFile(os.path.join(get_resource_path(), "JAANetparams.zip"), 'r') as zip_ref:
                        zip_ref.extractall(os.path.join(get_resource_path()))
                except:
                    print("JAA parameters failed to download")

                if os.path.exists(os.path.join(get_resource_path(), "align_net.pth")):
                    print("\nAU Detection Model Parameters downloaded successfully.\n")
                else:
                    print("Something went wrong. Model not found in directory.")

            if os.path.exists(os.path.join(get_resource_path(), "DRMLNetParams.pth")):
                print("\nDRML NET model downloaded successfully.\n")
            else:
                try:
                    print("Downloading DRML model.")
                    drml_model = "https://github.com/cosanlab/feat/releases/download/v0.1/DRMLNetParams.pth"
                    wget.download(drml_model, get_resource_path())
                    if os.path.exists(os.path.join(get_resource_path(), "DRMLNetParams.pth")):
                        print("\nLandmark detection model downloaded successfully.\n")
                    else:
                        print("Something went wrong. Model not found in directory.")
                except:
                    print("DRML model failed to download.")
                    
        atexit.register(_post_install)
        install.run(self)

setup(
    name='py-feat',
    version=version['__version__'],
    description="Facial Expression Analysis Toolbox",
    long_description="",
    author="Jin Hyun Cheong, Tiankang Xie, Sophie Byrne, Nathaniel Hanes, Luke Chang ",
    author_email='jcheong0428@gmail.com',
    url='https://github.com/cosanlab/feat',
    packages=find_packages(include=['feat', 'bin/*']),
    package_data = {'feat': ['resources/*','tests/*','tests/data/*']},
    scripts=['bin/detect_fex.py', 'bin/download_models.py'],
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords=['feat','face','facial expression','emotion'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='feat/tests',
    cmdclass={'install':CustomInstall},
    **extra_setuptools_args
)


