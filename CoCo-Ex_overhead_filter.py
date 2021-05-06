import pandas as pd
from glob import glob
from argparse import ArgumentParser

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('--inputfile',
                        dest='inputfile',
                        help='The path to the inputfile (output of entity_extraction.py) for which nodes should be selected.',
                        required=False,
                        default=None)
    parser.add_argument('--inputdir',
                        dest='inputdir',
                        help='if more than one inputfile should be parsed, GLOB path to the inputfiles',
                        required=False,
                        default=None)
    parser.add_argument('--outputfile',
                        dest='outputfile',
                        help='The path to the inputfile (output of entity_extraction.py) for which nodes should be selected.')
    parser.add_argument('--exactmatch',
                        dest='exactmatch',
                        help="Whether or not to check for exact match. When checking for this, you don't need to add any similarity metrics.",
                        action='store_true')
    parser.add_argument('--exactmatch_lemmas',
                        dest='exactmatch_lemmas',
                        help="Whether or not to check if the lemmatized concepts are an exact match. When checking for this, you don't need to add any similarity metrics.",
                        action='store_true')
    parser.add_argument('--exactmatch_normalized',
                        dest='exactmatch_normalized',
                        help="Whether or not to check if the normalized concepts are an exact match. When checking for this, you don't need to add any similarity metrics.",
                        action='store_true')
    parser.add_argument('--len_diff_tokenlevel',
                        dest='len_diff_token',
                        help="Maximum number of tokens by which the two concepts may differ to be allowed.")
    parser.add_argument('--len_diff_charlevel',
                        dest='len_diff_char',
                        help="Maximum number of characters by which the two concepts may differ to be allowed.")
    parser.add_argument('--dice_coefficient',
                        dest='dice',
                        help="Minimum dice coefficient that needs to be reached to keep the concept.")
    parser.add_argument('--dice_coefficient_lemmas',
                        dest='dice_lemmas',
                        help="Minimum dice coefficient that needs to be reached between lemmatized concepts to keep the concept.")
    parser.add_argument('--dice_coefficient_normalized',
                        dest='dice_normalized',
                        help="Minimum dice coefficient that needs to be reached between normalized concepts to keep the concept.")
    parser.add_argument('--jaccard_index',
                        dest='jaccard',
                        help="Minimum jaccard index that needs to be reached to keep the concept.")
    parser.add_argument('--jaccard_index_lemmas',
                        dest='jaccard_lemmas',
                        help="Minimum jaccard index that needs to be reached between lemmatized concepts to keep the concept.")
    parser.add_argument('--jaccard_index_normalized',
                        dest='jaccard_normalized',
                        help="Minimum jaccard index that needs to be reached between normalized concepts to keep the concept.")
    parser.add_argument('--med',
                        dest='med',
                        help="Maximum levenshtein (minimum edit) distance that concepts may have in order to be kept.")
    parser.add_argument('--med_lemmas',
                        dest='med_lemmas',
                        help="Maximum levenshtein (minimum edit) distance that lemmatized concepts may have in order to be kept.")
    parser.add_argument('--med_normalized',
                        dest='med_normalized',
                        help="Maximum levenshtein (minimum edit) distance that normalized concepts may have in order to be kept.")
    parser.add_argument('--wmd',
                        dest='wmd',
                        help="Maximum Word Mover's Distance that concepts may have in order to be kept.")
    parser.add_argument('--wmd_lemmas',
                        dest='wmd_lemmas',
                        help="Maximum Word Mover's Distance that lemmatized concepts may have in order to be kept.")
    parser.add_argument('--wmd_normalized',
                        dest='wmd_normalized',
                        help="Maximum Word Mover's Distance that normalized concepts may have in order to be kept.")
    parser.add_argument('--cosine_sim',
                        dest='cos',
                        help="Minimum cosine similarity that concepts must have in order to be kept.")
    parser.add_argument('--cosine_sim_lemmas',
                        dest='cos_lemmas',
                        help="Minimum cosine similarity that lemmatized concepts must have in order to be kept.")
    parser.add_argument('--cosine_sim_normalized',
                        dest='cos_normalized',
                        help="Minimum cosine similarity that normalized concepts must have in order to be kept.")

    args = parser.parse_args()

    if (args.inputfile == None) and (args.inputdir == None):
        raise Exception("You have to specify either an inputfile or input directory!")

    if (args.inputfile) and (not args.inputdir):
        glob_path = args.inputfile
    else:
        glob_path = args.inputdir

    if args.outputfile:
        outpath = args.outputfile
        # python for "touch outpath"
        outfile = open(outpath, "w")
        outfile.close()
    else:
        raise Exception("Please specify an output path. I know it isn't strictly required - but just do it. Seriously.")
    
    phrases_mapping = dict()
    with open("phrases_simplification_mapping.txt") as f:
        for line in f:
            phrase, simplification = line.strip().split("\t")
            phrases_mapping[phrase] = simplification
    
    for fn in sorted(glob(glob_path)):

        with open(fn, encoding='utf-8') as f:
            df = pd.read_csv(f, sep='\t', header=0, error_bad_lines=False, warn_bad_lines=False, encoding="utf-8")

        if (args.len_diff_token):
            df = df[(df['LEN-DIFF-TOKEN'] != 'None') ]
            df = df[(df["LEN-DIFF-TOKEN"].astype(int) < int(args.len_diff_token))]
        if (args.len_diff_char):
            df = df[(df['LEN-DIFF-CHAR'] != 'None')]
            df = df[(df["LEN-DIFF-CHAR"].astype(int) < int(args.len_diff_char))]
        if (args.dice):
            df = df[(df['DICE'] != 'None')]
            df = df[(df["DICE"].astype(float) > float(args.dice))]
        if (args.dice_normalized):
            df = df[(df['DICE-NOSTOPS'] != 'None')]
            df = df[(df["DICE-NOSTOPS"].astype(float) > float(args.dice_normalized))]

        grouped=df.groupby(["###SENT-ID",'SENT'])
        
        with open(outpath, "a", encoding="utf-8") as f:
            for sent, rest in grouped:
                node_line_numbers = rest["NODE"].index
                nodes = set()
                for nr in node_line_numbers:
                    nodes.add((rest.loc[nr,"NODE"], rest.loc[nr,"PHRASE-TYPE"]))
                    if rest.loc[nr,"NODE-LEMMATIZED"] != "None":
                        nodes.add((rest.loc[nr,"NODE-LEMMATIZED"], rest.loc[nr,"PHRASE-TYPE"]))
                f.write("{}\t{}\t{}\t{}\n".format(sent[0].split("_")[0], sent[0].split("_")[1], sent[1], "".join(["[{}|{}]".format(node, phrases_mapping[tag]) for node, tag in nodes])))
