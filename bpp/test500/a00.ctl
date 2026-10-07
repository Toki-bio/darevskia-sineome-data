seed = 11
seqfile = noarm.txt
Imapfile = noarm.Imap.txt
jobname = a00
speciesdelimitation = 0
speciestree = 0
species&tree = 5  val nai mix unp unm
                  2   1   1   1   1
                  (mix,(((nai,unm),unp),val));
usedata = 1
nloci = 472
cleandata = 0
thetaprior = invgamma 3 0.01
tauprior = invgamma 3 0.02
finetune = 1
print = 1 0 0 0
burnin = 10000
sampfreq = 4
nsample = 20000
threads = 4
