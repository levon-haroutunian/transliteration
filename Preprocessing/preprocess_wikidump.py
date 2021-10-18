"""
    Script for preprocessing a set of wikidump files
    after extraction with wikiextractor.
    
    Output files have no doc id tags and one sentence per line.
    
    Maintains organizational structure of original directory,
    with the same names for each corresponding subdirectory and file.
"""

import glob, re, argparse
from pathlib import Path

# constants
SEP = "___SEP-MARKER___"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--in_dir", help="name of input directory")
    parser.add_argument("--out_dir", help="name of output directory",
                        default="preprocessed", type=str)
    parser.add_argument("--seps", type=str, default=".",
                        help='string concatenation of all acceptable\
                            line separators. e.g., to separate by periods\
                                and commas, use --seps ".,".')
    parser.add_argument("--encoding", type=str, default='utf8',
                        help="document encoding")
                            
    args = parser.parse_args()
    
    # writing over existing files is not allowed        
    if Path(args.out_dir).is_dir():
        raise Exception(
            f"Choose a different directory name or delete existing directory {args.out_dir}.")
    
    # regex patterns
    re_in_dir = re.compile(r'{}(.*)'.format(args.in_dir))
    re_tags = re.compile(r"<[^<>]*>")
    re_newline = re.compile(r"\n+")
    re_esc_seps = re.compile("([" + re.escape(args.seps) + "]+\s*)")
    re_sep_marker = re.compile(SEP)
    
    for file in glob.iglob(args.in_dir + "/**", recursive=True):
        new_file = args.out_dir + '/' + re_in_dir.search(file).group(1)
        orig_path = Path(file)
        new_path = Path(new_file)
        
        # create corresponding subdirectories
        if orig_path.is_dir():
            new_path.mkdir()
            
        else:
            # read in text
            full_contents = orig_path.read_text(encoding=args.encoding)
            
            # remove all 'doc id' tags
            full_contents = re_tags.sub("", full_contents)
            
            # mark all separators, add newlines
            full_contents = re_esc_seps.sub(r"\1" + SEP, full_contents)
            full_contents = re_sep_marker.sub(r"\n", full_contents)
            
            # one chunk per line
            full_contents = re_newline.sub("\n", full_contents)
            full_contents = full_contents.lstrip()
            
            # write new file
            new_path.write_text(full_contents, encoding=args.encoding)
            