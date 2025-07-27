import os
import sys

def join_utf8_files(input_dir, output_file, recursive=False):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        if recursive:
            for root, _, files in os.walk(input_dir):
                for filename in files:
                    if filename.lower().endswith('.utf8'):
                        file_path = os.path.join(root, filename)
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                            outfile.write('\n')
        else:
            for filename in os.listdir(input_dir):
                file_path = os.path.join(input_dir, filename)
                if os.path.isfile(file_path) and filename.lower().endswith('.utf8'):
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')

if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Usage: python utf8_join.py <input_directory> <output_file> [--recursive]")
        sys.exit(1)
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    recursive = len(sys.argv) == 4 and sys.argv[3] == "--recursive"
    join_utf8_files(input_dir, output_file, recursive)