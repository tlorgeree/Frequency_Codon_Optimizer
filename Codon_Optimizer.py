import os
import time
import csv
def Main():
    print("""Welcome to the Codon Frequency Optimizer! For easiest use, ensure that
    you are running the program from its original folder!
    ****NOTE: Make sure the sequence you are optimizing begins with the first
    nucleotide and is in the correct reading frame!****""")

    #Get and validify sequence
    valid_mRNA = True
    seq = input("Please input your DNA or mRNA sequence: ")
    try:
        seq_str = str(seq)
    except:
        print("Sequence has invalid characters. Terminating program.")
        return "invalid"
    mRNA_seq = ""

    if ((seq_str.find("U") != -1) or (seq_str.find("c") != -1)
        or (seq_str.find("a") != -1) or (seq_str.find("g") != -1)
        or (seq_str.find("u") != -1)):
        for char in seq_str:
            if ((char == "U") or (char =="u")
                or (char == "t")):
                mRNA_seq += "T"
            elif (char == "g"): mRNA_seq += "G"
            elif (char == "c"): mRNA_seq += "C"
            elif (char == "a"): mRNA_seq += "A"
            else: mRNA_seq += char
    else: mRNA_seq = seq #if no typing corrections
    for char in mRNA_seq:
        if ((char != "A") and (char != "T")
            and (char != "C") and (char !="G")):
            valid_mRNA = False
            print("WRONG")
    if valid_mRNA == True:
        print("It's good")
        print(mRNA_seq)
    else:
        print("Sequence has invalid characters. Terminating program.")
        return "invalid"

    seq_start = mRNA_seq.find("ATG")
    if (seq_start == -1):
        print("This sequence has no start codon. Continue?")
        seq_cont = input("[Y]es or [N]o: " )
        if ((seq_cont == "Y") or (seq_cont == "y")
               or (seq_cont == "N") or (seq_cont == "n")):
            cont = True
        else: cont = False
        while (cont == False):
            seq_cont = input("Invalid response. Continue?\n[Y]es or [N]o: ")
            if ((seq_cont == "Y") or (seq_cont == "y")
               or (seq_cont == "N") or (seq_cont == "n")):
                cont = True

            print(str(cont))
        if ((seq_cont == "N") or (seq_cont == "n")):
            print("Terminating program.")
            return "invalid"
        else: print("Proceeding.")

    #import host codon sequence
    #sequences obtained from GenScript site
    try:
        print("Script executed from: ")
        print(os.path.dirname(os.path.realpath("Frequency Codon Optimizer.ipynb")))
        path = os.path.dirname(os.path.realpath("Frequency Codon Optimizer.ipynb"))
        print("The path is: " + path)
    except:
        valid_path = False
        path = input("Couldn't find active directory for this script. Please input the active directory: ")
        while (valid_path == False):
            if (os.path.isdir(path) == False):
                path = input("Input directory was invalid, please try again or enter 'Q' to quit: ")
                if ((path == "Q") or (path == "q")): return "invalid"
            else: valid_path = True

    print("Found directory. Moving Forward")
    print(path + "\\Template_Organisms")
    if (os.path.isdir(path + "\\Template_Organisms") == True):
        path_files = path + "\\Template_Organisms"
        i = 1
        dir_items = []
        print("Found template folder, listing template files: ")
        for file in os.listdir(path_files):
            print("\t" + str(i) + ": " + file)
            i+=1
            dir_items.append(file)

    else:
        print("Template_Organisms folder is not at listed directory. Terminating program.")
        return "invalid"
    valid_codon_freq = False
    while (valid_codon_freq == False):
        ##Select host organism
        host_codon_sel = input("Please input the number that corresponds with the host organism or 'Q' to quit: ")
        if ((host_codon_sel == "Q") or (host_codon_sel == "q")): return "invalid"
        host_codon_sel_valid = False
        while (host_codon_sel_valid == False):
            try:
                host_codon_int = int(host_codon_sel)
                if ((host_codon_int < (len(dir_items) + 1)) and (host_codon_int > 0)):
                    host_codon_sel_valid = True
                else:
                    host_codon_sel = input("""Input was not within the list range. Please input the number that
                    corresponds with the host organism or 'Q' to quit: """)
            except: host_codon_sel = input("""Input was not an integer. Please input the number that
            corresponds with the host organism or 'Q' to quit: """)
            if ((host_codon_sel== "Q") or (host_codon_sel == "q")): return "invalid"

        print("Selected host organism file: " + dir_items[host_codon_int-1])
        host_codon = dir_items[host_codon_int-1]

        ##Select Target codon frequency
        targ_codon_sel = input("""Please input the number that corresponds with the target organism
        codon frequency or 'Q' to quit: """)
        if ((targ_codon_sel == "Q") or (targ_codon_sel == "q")): return "invalid"
        targ_codon_sel_valid = False
        while (targ_codon_sel_valid == False):
            try:
                targ_codon_int = int(targ_codon_sel)
                if ((targ_codon_int < (len(dir_items) + 1)) and (targ_codon_int > 0)):
                    targ_codon_sel_valid = True
                else:
                    targ_codon_sel = input("""Input was not within the list range. Please input the number that
                    corresponds with the target organism codon frequency or 'Q' to quit: """)
            except: targ_codon_sel = input("""Input was not an integer. Please input the number that
            corresponds with the target organism codon frequency or 'Q' to quit: """)
            if ((targ_codon_sel== "Q") or (targ_codon_sel == "q")): return "invalid"

        print("Selected target organism file: " + dir_items[targ_codon_int-1])
        targ_codon = dir_items[targ_codon_int-1]

        if (targ_codon_int == host_codon_int):
            print("The selected host and target organisms are the same.\nPlease select 2 different organisms.")
        else: valid_codon_freq = True

    host_file_path = path_files + "\\" + dir_items[host_codon_int-1]
    targ_file_path = path_files + "\\" + dir_items[targ_codon_int-1]

    #store file contents in parallel arrays
    with open(host_file_path, "rt") as x:
        reader = csv.DictReader(x)
        host_codons = [row["Triplet"]for row in reader]
        x.close()
    with open(host_file_path, "rt") as x:
        reader = csv.DictReader(x)
        host_aa = [row["Amino acid"] for row in reader]
        x.close()
    with open(host_file_path, "rt") as x:
        reader = csv.DictReader(x)
        host_freqs = [row["Fraction"] for row in reader]
        x.close()
    with open(targ_file_path, "rt") as x:
        reader = csv.DictReader(x)
        targ_codons = [row["Triplet"]for row in reader]
        x.close()
    with open(targ_file_path, "rt") as x:
        reader = csv.DictReader(x)
        targ_aa = [row["Amino acid"] for row in reader]
        x.close()
    with open(targ_file_path, "rt") as x:
        reader = csv.DictReader(x)
        targ_freqs = [row["Fraction"] for row in reader]
        x.close()

    ## convert original sequence to AA and store frequencies
    seq_len = len(mRNA_seq)
    curr_codon = ""
    new_aa_seq = ""
    curr_freq = []
    for i in range(0,seq_len):
        curr_codon += mRNA_seq[i]
        if (len(curr_codon) == 3):
            for index, j in enumerate(host_codons):
                if curr_codon == j:
                    new_aa_seq += host_aa[index]
                    curr_freq.append(host_freqs[index])
                    break;

            curr_codon = ""
    print("The current seq is: " + new_aa_seq)

    targ_len = len(targ_codons)
    output_seq = ""
    new_aa_len = len(new_aa_seq)
    print("Converted aa seq len is: " + str(new_aa_len))
    freq_closest = -1
    codon_closest = ""

    for i in range(0, new_aa_len):
        for j in range(0, targ_len):
            if (new_aa_seq[i] == targ_aa[j]):
                if (freq_closest == -1):
                    freq_closest = targ_freqs[j]
                    codon_closest = targ_codons[j]
                else:
                    k = host_codons.index(targ_codons[j])
                    if (abs(float(curr_freq[i]) - float(freq_closest))
                        > abs(float(curr_freq[i]) - float(targ_freqs[j]))):

                        freq_closest = targ_freqs[j]
                        codon_closest = targ_codons[j]
        output_seq += codon_closest
        freq_closest = -1

    print("The output is: " + output_seq)

response = Main()
