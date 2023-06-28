# Projection analysis and association analysis accounting for local ancestry 
## Projection analysis using Eigensoft

* Eigensoft details at https://github.com/chrchang/eigensoft/blob/master/POPGEN/README
* The pipeline to perform PCA using EIGENSTRAT is available at https://github.com/chrchang/eigensoft/tree/master/EIGENSTRAT

To perform PCA projection using Eigensoft you need to add the parameter "poplistname" and include a list of populations in which all other individuals will be projected onto.

### Description of "poplistname" parameter in EIGENSTRAT manual:
"poplistname:   If wishing to infer eigenvectors using only individuals from a 
  subset of populations, and then project individuals from all populations 
  onto those eigenvectors, this input file contains a list of population names,
  one population name per line, which will be used to infer eigenvectors.  
  It is assumed that the population of each individual is specified in the 
  indiv file.  Default is to use individuals from all populations"
  

## Projection analysis using ADMIXTURE:

* The European P allele frequency matrix is available at https://github.com/mateushg1/CRGGH/

* This is a pipeline from the ADMIXTURE manual (https://dalexander.github.io/admixture/admixture-manual.pdf) to run projection analysis using the P allele frequency matrix from ADMIXTURE analysis.


### Description:
ADMIXTURE now allows loading of learned allele frequencies from the .P files. For two
datasets with the same set of SNPs, clusters can be learned using the unsupervised mode
of ADMIXTURE on the first dataset; subsequently, the learned clusters and ancestry
proportions from the first dataset can be provided as input used to project the second
dataset with the -P option.


### Example: 
Suppose reference.bed is the PLINK binary file containing reference panels
and study.bed is the PLINK binary file containing study samples. The following sequence
of commands can be used to learn population structure from the reference panel and project
the study individuals on it:


#### Verify the two datasets have the same set of SNPs

diff -s reference.bim study.bim

#### Run unsupervised ADMIXTURE with K=2
admixture reference.bed 2
#### Use learned allele frequencies as (fixed) input to next step
cp reference.2.P study.2.P.in
#### Run projection ADMIXTURE with K=2
admixture -P study.bed 2"

## Association analysis accounting for local ancestry

### Software required:
* plink/2.3-alpha 
* python 3
* zstd/1.4.7/gcc-10.2.0

#The pipeline to perform RFMix1 analysis can be found in https://github.com/MataLabCCF/Tractor/tree/master/ScriptsRFMix1
#Details on how to use PLINK2 with description of flags can be found in https://www.cog-genomics.org/plink/2.0/


#### Transform PLINK files to PLINK 2 format (.pgen and .pvar)

plink2 --bfile < PLINK1 file name without extension (.bed/.bim/.fam) > --make-pgen -out < PLINK2 file name without extension (.pgen/.psam/.pvar) >


#### Extract RFMix local ancestry dosages and create PLINK 2 local covariate files 

python Extract_dosages_09092022.py -t < RFMIX probability calls with extension (.fb.tsv) > -a < Ancestry name in the header of RFMIX file> -P < PLINK2 file name with extension (.pvar) >
-o < output name >


#### Compressing covar files (the local covariates can be very large!)

for chr in {1..22}; do
zstd chr${chr}_local.covar
done

#### Association analysis adjusting for covariates and local covariates (e.g., local ancestry)

plink2 --pfile < PLINK2 file name without extension (.pgen/.pvar) > --glm omit-ref  --pheno < phenotype file with extension > / 
--covar < covariates files with extension > local-covar= < local covariate file with extension (.covar.zst) > local-psam= < local covariate file with extension (.psam) > local-pvar= < local covariate file with extension (.pvar) > --covar-variance-standardize -out < association output file > --threads 20




