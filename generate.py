#!/usr/bin/env python3

import os
import tarfile

import nltk
from nltk.corpus import wordnet as wn

DOWNLOAD_DIR = 'downloads'
DATA_DIR = 'dataset'
DIST_DIR = 'dist'

def download_wornet(wn_download_path):
  nltk.data.path.append(wn_download_path)
  nltk.download('wordnet', wn_download_path, quiet = True)

def export_map_synsets(wn_data_path):
  SYN_TO_ID = {}
  ID_TO_SYN = [syn.name() for syn in wn.all_synsets()]
  SYNS_COUNT = 0

  file_id_to_name = os.path.join(wn_data_path, 'synset_id_to_name.tsv')
  with open(file_id_to_name, 'w+') as f:
    #print('syn_id\tsyn_name', file = f, flush = True)
    for syn_id, syn_obj in enumerate(wn.all_synsets()):
      syn_name = syn_obj.name()
      print(str(syn_id) + '\t' + syn_name, file = f, flush = True)

      SYN_TO_ID[syn_name] = syn_id
      SYNS_COUNT += 1

  file_name_to_id = os.path.join(wn_data_path, 'synset_name_to_id.tsv')
  with open(file_name_to_id, 'w+') as f:
    #print('syn_name\tsyn_id', file = f, flush = True)
    for syn_name, syn_id in sorted(SYN_TO_ID.items()):
      print(syn_name + '\t' + str(syn_id), file = f, flush = True)

  return (SYN_TO_ID, ID_TO_SYN, SYNS_COUNT)

def export_map_relations(wn_data_path):
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

  file_id_to_name = os.path.join(wn_data_path, 'relation_name_to_id.tsv')
  with open(file_id_to_name, 'w+') as f:
    #print('rel_id\trel_name', file = f, flush = True)
    for rel_id, rel_name in enumerate(ID_TO_REL):
      print(str(rel_id) + '\t' + rel_name, file = f, flush = True)

      REL_TO_ID[rel_name] = rel_id
      RELS_COUNT += 1

  file_name_to_id = os.path.join(wn_data_path, 'relation_id_to_name.tsv')
  with open(file_name_to_id, 'w+') as f:
    #print('rel_name\trel_id', file = f, flush = True)
    for rel_name, rel_id in sorted(REL_TO_ID.items()):
      print(rel_name + '\t' + str(rel_id), file = f, flush = True)

  return (REL_TO_ID, ID_TO_REL, RELS_COUNT)

def export_edges(wn_data_path, syn_to_id, rel_to_id):
  EDGES_COUNT = 0
  EDGES_COUNT_REL = {}
  for rel_name in rel_to_id: EDGES_COUNT_REL[rel_name] = 0

  file_edges_id_all = os.path.join(wn_data_path, 'edges_as_id_all.tsv')
  file_edges_name_all = os.path.join(wn_data_path, 'edges_as_name_all.tsv')
  with open(file_edges_id_all, 'w+') as fei, open(file_edges_name_all, 'w+') as fen:
    #print('syn_head_id\tsyn_rel_id\tsyn_tail_id', file = fei, flush = True)
    #print('syn_head_name\tsyn_rel_name\tsyn_tail_name', file = fen, flush = True)
    for rel_name in rel_to_id:
      rel_sid = str(rel_to_id[rel_name]);
      file_edges_id_rel = os.path.join(wn_data_path, 'edges_as_id_' + rel_name + '.tsv')
      file_edges_name_rel = os.path.join(wn_data_path, 'edges_as_name_' + rel_name + '.tsv')
      with open(file_edges_id_rel, 'w+') as feri, open(file_edges_name_rel, 'w+') as fern:
        #print('syn_head_id\tsyn_rel_id\tsyn_tail_id', file = feri, flush = True)
        #print('syn_head_name\tsyn_rel_name\tsyn_tail_name', file = fern, flush = True)
        for syn1_name in syn_to_id:
          syn1_obj = wn.synset(syn1_name)
          syn1_sid = str(syn_to_id[syn1_name]);
          for syn2_obj in getattr(syn1_obj, rel_name)():
            syn2_name = syn2_obj.name()
            syn2_sid = str(syn_to_id[syn2_name]);
            print(syn1_sid + '\t' + rel_sid + '\t' + syn2_sid, file = fei, flush = True)
            print(syn1_name + '\t' + rel_name + '\t' + syn2_name, file = fen, flush = True)
            print(syn1_sid + '\t' + rel_sid + '\t' + syn2_sid, file = feri, flush = True)
            print(syn1_name + '\t' + rel_name + '\t' + syn2_name, file = fern, flush = True)

            EDGES_COUNT += 1
            EDGES_COUNT_REL[rel_name] += 1

  return (EDGES_COUNT, EDGES_COUNT_REL)

def export_counts(wn_data_path, syns_count, rels_count, edges_count, edges_count_rel):
  file_count_synsets = os.path.join(wn_data_path, 'count_synsets.txt')
  with open(file_count_synsets, 'w+') as f:
    print(syns_count, file = f, flush = True)
  file_count_relations = os.path.join(wn_data_path, 'count_relations.txt')
  with open(file_count_relations, 'w+') as f:
    print(syns_count, file = f, flush = True)
  file_count_edges_all = os.path.join(wn_data_path, 'count_edges_all_.txt')
  with open(file_count_edges_all, 'w+') as f:
    print(edges_count, file = f, flush = True)
  for rel_name in edges_count_rel:
    file_count_edges_rel = os.path.join(wn_data_path, 'count_edges_' + rel_name + '.txt')
    with open(file_count_edges_rel, 'w+') as f:
      print(edges_count_rel[rel_name], file = f, flush = True)

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

  download_wornet(wn_download_path)

  SYN_TO_ID, _, SYNS_COUNT = export_map_synsets(wn_data_path)
  REL_TO_ID, _, RELS_COUNT = export_map_relations(wn_data_path)
  EDGES_COUNT, EDGES_COUNT_REL = export_edges(wn_data_path, SYN_TO_ID, REL_TO_ID)

  export_counts(wn_data_path, SYNS_COUNT, RELS_COUNT, EDGES_COUNT, EDGES_COUNT_REL)

  compress_dataset(wn_data_path, wn_dist_path)

if __name__ == '__main__':
  main()
