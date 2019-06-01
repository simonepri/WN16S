#!/usr/bin/env python3

import os
import tarfile

import nltk
from nltk.corpus import wordnet as wn

DOWNLOAD_DIR = 'downloads'
DATA_DIR = 'dataset'
DIST_DIR = 'dist'

def nltk_download_wornet(wn_download_path):
  nltk.data.path.append(wn_download_path)
  nltk.download('wordnet', wn_download_path, quiet = True)

def nltk_map_synsets_to_id(wn_data_path):
  SYN_TO_ID = {}
  ID_TO_SYN = [syn.name() for syn in wn.all_synsets()]
  SYNS_COUNT = 0

  syn_2_id_file = os.path.join(wn_data_path, 'synset2id.tsv')
  with open(syn_2_id_file, 'w+') as f_syn:
    #print('syn_name\tsyn_id', file = f_syn, flush = True)
    for id, syn_obj in enumerate(wn.all_synsets()):
      name = syn_obj.name()
      print(name + '\t' + str(id), file = f_syn, flush = True)

      SYN_TO_ID[name] = id
      SYNS_COUNT += 1

  return (SYN_TO_ID, ID_TO_SYN, SYNS_COUNT)

def nltk_map_relations_to_id(wn_data_path):
  REL_TO_ID = {}
  ID_TO_REL = [
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
  RELS_COUNT = 0

  rel_2_id_file = os.path.join(wn_data_path, 'relation2id.tsv')
  with open(rel_2_id_file, 'w+') as f_rel:
    #print('rel_name\trel_id', file = f_rel, flush = True)
    for id, rel_name in enumerate(ID_TO_REL):
      print(rel_name + '\t' + str(id), file = f_rel, flush = True)

      REL_TO_ID[rel_name] = id
      RELS_COUNT += 1

  return (REL_TO_ID, ID_TO_REL, RELS_COUNT)

def nltk_map_edges_to_id(wn_data_path, syn_to_id, rel_to_id):
  EDGES_COUNT = 0

  edge2id_all_file = os.path.join(wn_data_path, 'edge2id_all.tsv')
  with open(edge2id_all_file, 'w+') as f_all:
    #print('syn_head_id\tsyn_rel_id\tsyn_tail_id', file = f_all, flush = True)
    for rel_name in rel_to_id:
      rel_sid = str(rel_to_id[rel_name]);
      edge2id_rel_file = os.path.join(wn_data_path, 'edge2id_' + rel_name + '.tsv')
      with open(edge2id_rel_file, 'w+') as f_rel:
        #print('syn_head_id\tsyn_rel_id\tsyn_tail_id', file = f_rel, flush = True)
        for syn1_name in syn_to_id:
          syn1_obj = wn.synset(syn1_name)
          syn1_sid = str(syn_to_id[syn1_name]);
          for syn2_obj in getattr(syn1_obj, rel_name)():
            syn2_name = syn2_obj.name()
            syn2_sid = str(syn_to_id[syn2_name]);
            print(syn1_sid + '\t' + rel_sid + '\t' + syn2_sid, file = f_all, flush = True)
            print(syn1_sid + '\t' + rel_sid + '\t' + syn2_sid, file = f_rel, flush = True)

            EDGES_COUNT += 1

  return EDGES_COUNT

def compress_dataset(wn_data_path, wn_dist_path):
  wn16s_tgz_file = os.path.join(wn_dist_path, 'WN16S.tgz')
  with tarfile.open(wn16s_tgz_file, "w:gz") as tar:
    tar.add(wn_data_path, arcname = '')

def main():
  wn_download_path = os.path.realpath(DOWNLOAD_DIR)
  wn_data_path = os.path.realpath(DATA_DIR)
  wn_dist_path = os.path.realpath(DIST_DIR)

  os.makedirs(wn_download_path, exist_ok = True)
  os.makedirs(wn_data_path, exist_ok = True)
  os.makedirs(wn_dist_path, exist_ok = True)

  nltk_download_wornet(wn_download_path)

  SYN_TO_ID, _, SYNS_COUNT = nltk_map_synsets_to_id(wn_data_path)
  REL_TO_ID, _, RELS_COUNT = nltk_map_relations_to_id(wn_data_path)
  EDGES_COUNT = nltk_map_edges_to_id(wn_data_path, SYN_TO_ID, REL_TO_ID)

  compress_dataset(wn_data_path, wn_dist_path)

if __name__ == '__main__':
  main()
