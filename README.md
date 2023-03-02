# Project Generation Cookiecutter (🚧🚧🚧 WORK IN PROGRESS 🚧🚧🚧)

This cookiecutter provides a quick and easy way to create new projects for any data science.

It was inspired by [Cookiecutter AI4ER] (https://github.com/ai4er-cdt/ai4er-cookiecutter) itself inspired by [Cookiecutter DataScience](https://drivendata.github.io/cookiecutter-data-science/)

The current version of this cookiecutter allows you to automatically set up:

1. A useful folderstructure for notebooks, source code, documentation, etc.
2. Automatically create a symlink to your data folder for easy and unified data access.
3. Automatically initialize as github repo and link to an existing (empty!) repository on github.com

## Prerequisites

Please make sure that you have a working version of `python` (>= 3.0) and `cookiecutter` (>=1.7) installed.
To install cookiecutter, simply use

`pip install --user cookiecutter`
or
`conda install cookiecutter`

For more information on the installation of cookiecutter, see [here](https://cookiecutter.readthedocs.io/en/1.7.2/installation.html).

## Usage

To use this cookiecutter, you simply type the following into your command line (Note: `cookiecutter` must be installed as prerequisite).

> `cookiecutter https://github.com/odietric/cookiecutter-lightning-hydra.git`

The cookiecutter will then automatically prompt you to set project names, etc.

## Questions

For any questions, please contact [Olivier Dietrich](mailto:odietrich@geod.baug.ethz.ch).
