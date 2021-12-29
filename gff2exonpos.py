import argparse
import pysam

def args_parser():
    '''parser the argument from terminal command'''
    parser=argparse.ArgumentParser(prog = "PROG", formatter_class = argparse.RawDescriptionHelpFormatter, description=" \n\
        Usage: python gtf_info.py -gff <gff> -O <output> ")
    parser.add_argument("-gff", "--gff", help = "gff annotation file (sorted and indexed). ")
    parser.add_argument("-O", "--output", help="output prefix. ")
    args = parser.parse_args()
    return args

def attributes_Parent(attribute):
    '''parse attribute field and return gene id '''
    exon_parent = attribute.split("Parent")[-1].split(";")[0].split(":")[-1]
    return exon_parent

def parse_gff(args):
    '''parse gtf for gene location. '''
    gff = args.gff
    output = args.output
    gff_df = pysam.TabixFile(gff, parser = pysam.asGTF(), threads = 2)
    ###
    gene = open(output + ".txt", "w")
    gene.write("transcript\tcontig\tstart\tend\tstrand\n")
    ###
    for i in gff_df.fetch():
        if i.feature == "exon":
            atb = i.attributes
            transcript = attributes_Parent(atb)
            tig = i.contig
            st = i.start + 1
            ed = i.end
            strand = i.strand
            gene.write(f"{transcript}\t{tig}\t{st}\t{ed}\t{strand}\n")
    gene.close()

def main():
    args = args_parser()
    parse_gff(args)

##############
### Run it ###
##############

if __name__ == "__main__":
    main()