# BRAX Labeler: Brazilian Portuguese adaptation of Chexpert Labeler

The main difference resides in the fact that NegBio doesn't work for Portuguese, so we adapt Brazillian Negex triggers to detect negation and uncertainty. In this code we use [EasyNegex repository](https://github.com/fuchsfelipel/easyNegex) implementation of Negex.

## Prerequisites

Please install following dependencies or use the Dockerized labeler (see below).

1. Clone the [EasyNegex repository](https://github.com/fuchsfelipel/easyNegex) to the root of this repository:

```Shell
git clone https://github.com/fuchsfelipel/easyNegex
```

2. Make the virtual environment:

```Shell
conda env create -f environment.yml
```

3. Activate the virtual environment:

```Shell
conda activate chexpert-label
```

4. Install NLTK data:

```Shell
python -m nltk.downloader universal_tagset punkt wordnet
```

## Usage
Place reports in a headerless, single column csv `{reports_path}`. Each report must be contained in quotes if (1) it contains a comma or (2) it spans multiple lines. See [sample_reports.csv](https://raw.githubusercontent.com/stanfordmlgroup/chexpert-labeler/master/sample_reports.csv) (with output [labeled_reports.csv](https://raw.githubusercontent.com/stanfordmlgroup/chexpert-labeler/master/labeled_reports.csv))for an example.

```Shell
python label.py --reports_path {reports_path}
```

Run `python label.py --help` for descriptions of all of the command-line arguments.


## Contributions
This repository builds upon the work of [CheXpert](https://github.com/stanfordmlgroup/chexpert-labeler), [Negex](https://code.google.com/archive/p/negex/) and [EasyNegex](https://github.com/fuchsfelipel/easyNegex).


## Citing
If you're using the BRAX labeler forked from CheXpert labeling tool, please cite [BRAX](https://arxiv.org/abs/1901.07031) paper and [CheXpert](https://arxiv.org/abs/1901.07031) as a reference.
