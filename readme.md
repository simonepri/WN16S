<h1 align="center">
  WN16S
</h1>
<p align="center">
  <a href="https://github.com/simonepri/WN16S/releases/latest/download/WN16S.tgz"><img src="https://img.shields.io/github/downloads/simonepri/WN16S/latest/WN16S.tgz.svg" alt="github downloads"/></a>
  <a href="https://github.com/simonepri/WN16S/releases"><img src="https://img.shields.io/github/tag/simonepri/WN16S.svg" alt="dataset download" /></a>
  <a href="https://en.wikipedia.org/wiki/tab-separated_values"><img src="https://img.shields.io/badge/format-tsv-e67e22.svg" alt="dataset format" /></a>
  <a href="https://wordnet.princeton.edu/"><img src="https://img.shields.io/badge/source-WordNet-2ecc71.svg" alt="dataset source" /></a>
  <a href="https://github.com/simonepri/WN16S/tree/master/license"><img src="https://img.shields.io/github/license/simonepri/WN16S.svg" alt="software license" /></a>
</p>
<br />
<p align="center">
  WordNet dataset with semantic relations only
</p>

## Motivation
In [WordNet][wn] two kinds of relations are recognized: lexical and semantic. Lexical relations hold between word forms (lemmas); semantic relations hold between word meanings (synsets).

I wanted to have a dataset with the lexical relations filtered out to build synset embeddings based only on the semantic relations of the WN graph.

## Structure
In the [dataset folder][dataset], you can find different `tsv` files the meaning of which is explained hereafter.

| file name | purpose |
| --------- | ------- |
| `synset2id.tsv`   | File that maps the 117659 WordNet's synsets to a numeric id. |
| `relation2id.tsv` | File that maps the 16 WordNet's semantic relations to a numeric id. |
| `edge2id_all.tsv` | File that contains all the edges of the WordNet's semantic subgraph as triples ids (synset 1, relation, synset 2).
| `edge2id_*.tsv`   | Files that contain only the edges of type %.

## Download
A compressed version of the dataset can be downloaded from the [release page][releases] or by clicking [here][download].

## Source
The dataset is generated using [nltk][nltk] and is a subset of the [WordNet][wn] dataset.

## License
All source code of this project is licensed under the MIT License - see the [license][license] file for details.

[dataset]: https://github.com/simonepri/WN16S/tree/master/dataset
[releases]: https://github.com/simonepri/WN16S/releases/latest
[download]: https://img.shields.io/github/downloads/simonepri/WN16S/latest/WN16S.tgz.svg
[license]: https://github.com/simonepri/WN16S/tree/master/license

[wn]: https://wordnet.princeton.edu
[nltk]: https://github.com/nltk/nltk
