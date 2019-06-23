import os
import tarfile


def compress_dataset(dir, name, files):
  tgz_file = os.path.join(dir, name + '.tgz')
  with tarfile.open(tgz_file, "w:gz") as tar:
    for file in files:
      path = os.path.realpath(file)
      name = os.path.basename(path)
      tar.add(path, arcname=name)


def main():
  os.makedirs('dist', exist_ok=True)

  compress_dataset('dist', 'WN16S-ID', [
    'dataset/edges_as_id_all.tsv',
    'dataset/map_entity_id_to_text.tsv',
    'dataset/map_relation_id_to_text.tsv'
  ])
  compress_dataset('dist', 'WN16S', [
    'dataset/edges_as_text_all.tsv',
  ])


if __name__ == '__main__':
  main()
