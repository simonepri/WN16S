#!/usr/bin/env python3

import os
import tarfile

import nltk
from nltk.corpus import wordnet as wn

DOWNLOAD_DIR = 'downloads'
DATA_DIR = 'dataset'


def download_wornet(wn_download_path):
  nltk.data.path.append(wn_download_path)
  nltk.download('wordnet', wn_download_path, quiet = True)


def export_edges(wn_data_path):
  EDGES_COUNT = 0

  RELS = [
    'hypernyms', 'instance_hypernyms',
    'hyponyms', 'instance_hyponyms',
    'member_holonyms', 'substance_holonyms', 'part_holonyms',
    'member_meronyms', 'substance_meronyms', 'part_meronyms',
    'attributes',
    'entailments',
    'causes',
    'also_sees',
    'verb_groups',
    'similar_tos'
  ]

  file_edges_name_all = os.path.join(wn_data_path, 'edges_as_text_all.tsv')
  with open(file_edges_name_all, 'w+') as f:
    for rel_name in RELS:
      for syn1_obj in wn.all_synsets():
        syn1_name = syn1_obj.name()
        for syn2_obj in getattr(syn1_obj, rel_name)():
          syn2_name = syn2_obj.name()
          print(syn1_name + '\t' + rel_name + '\t' + syn2_name, file = f, flush = True)

          EDGES_COUNT += 1

  return EDGES_COUNT


def main():
  wn_download_path = os.path.realpath(DOWNLOAD_DIR)
  wn_data_path = os.path.realpath(DATA_DIR)

  os.makedirs(wn_download_path, exist_ok = True)
  os.makedirs(wn_data_path, exist_ok = True)

  download_wornet(wn_download_path)

  export_edges(wn_data_path)


if __name__ == '__main__':
  main()
