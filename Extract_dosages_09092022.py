import argparse

parser = argparse.ArgumentParser(description="Dosage de Local Ancestry")

required = parser.add_argument_group("Mandatory arguments")
required.add_argument('-t', '--tsv', help = "TSV from RFMix with RFMix2 template", required = True)
required.add_argument('-a', '--anc', help = "Ancestry to calculate dosage", required = True)
required.add_argument('-o', '--output', help = "Output file", required = True)
required.add_argument('-P', '--pos_list', help = "SNP positions", required = True, default='')


optional = parser.add_argument_group("Optional arguments")
#optional.add_argument('-P', '--pos_list', help = "SNP positions", required = False, default='')


args = parser.parse_args()

tsvFile = args.tsv
anc = args.anc
outputFile = args.output
position_list = args.pos_list

file1 = open(tsvFile)

countLine = 0

indList = []
dictPosteriori = {}



for line in file1:
    if countLine == 1:
        headerLine = line.strip().split("\t")
    elif countLine > 1:
        split = line.strip().split("\t")

        pos = int(split[1])

        for i in range(4, len(split)):
            splitHeader = headerLine[i].split(":::")
            if anc == splitHeader[2]:
                if pos not in dictPosteriori:
                    dictPosteriori[pos] = {}
                if splitHeader[0] not in dictPosteriori[pos]:
                    if splitHeader[0] not in indList:
                        indList.append(splitHeader[0])
                    dictPosteriori[pos][splitHeader[0]] = 0.0
                dictPosteriori[pos][splitHeader[0]] = dictPosteriori[pos][splitHeader[0]] + float(split[i])

    countLine = countLine + 1


fileOut_covar = open(f"{outputFile}.covar", "w")
fileOut_psam = open(f"{outputFile}.psam", "w")
fileOut_pvar = open(f"{outputFile}.pvar", "w")


countline_file2 = 0


if position_list != '':

    file2 = open(position_list)

    keysInt = []
    for key in dictPosteriori:
        keysInt.append(key)

    keysInt.sort()

    fileOut_pvar.write(f"#CHROM\tPOS\tID\n")
    for line_file2 in file2:
        row = line_file2.strip().split("\t")
        posInt = int(row[1])
        #print(f"usei {posInt} ")
        #fileOut_pvar.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")
        for i in range(len(keysInt)):

            if i == 0 and countline_file2 == 0:
                fileOut_psam.write(f"#IDD\n")
                for ind in dictPosteriori[keysInt[i]]:
                        fileOut_psam.write(f"{ind}\n")

            if i == 0:
                if posInt < keysInt[i]:
                    #print(f"A posicao {posInt} não existe")
                    break

            if i + 1 != len(keysInt):
                if posInt >= keysInt[i] and posInt < keysInt[i + 1]:
                    fileOut_pvar.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")
                    #print(f"Imprimindo o {keysInt[i]}")
                    countind = 1
                    for ind in dictPosteriori[keysInt[i]]:
                        if countind < len(indList):
                            fileOut_covar.write(f"{dictPosteriori[keysInt[i]][ind]}\t")
                        else:
                            fileOut_covar.write(f"{dictPosteriori[keysInt[i]][ind]}\n")
                        countind = countind + 1
                    #fileOut.write(f"\n")
                    break
            else:
                countind = 1
                if posInt >= keysInt[i]:
                    fileOut_pvar.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")
                    #print(f"Imprimindo o {keysInt[i]}")
                    for ind in dictPosteriori[keysInt[i]]:
                        if countind < len(indList):
                            fileOut_covar.write(f"{dictPosteriori[keysInt[i]][ind]}\t")
                        else:
                            fileOut_covar.write(f"{dictPosteriori[keysInt[i]][ind]}\n")
                        countind = countind + 1
                    break

        countline_file2 = countline_file2 + 1

    fileOut_covar.close()
    fileOut_psam.close()
    fileOut_pvar.close()
