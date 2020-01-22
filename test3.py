#!/usr/bin/env python

from midiutil import MIDIFile
import random

degrees  = [ 62, 64, 65, 67, 69, 71, 72,74]  # MIDI note number
##degrees = [66,68,70,71,72,74,75,76,77]
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 100   # In BPM
volume   = 100  # 0-127, as per the MIDI standard
transpose = -1
octaves = 2
shft = random.randint(0,12)

for i, degree in enumerate(degrees):
    degrees[i] = degree + shft

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)
degreeslist = [degrees]
ndegrees = []
for i in range(1,octaves):
    ndegrees1 = []
    ndegrees2 = []
    ndegrees3 = []
    for j in range(0, len(degrees)):
        ndegrees.append(degrees[j]+12*i)
        ndegrees.append(degrees[j]-12*i)
        ndegrees1.append(degrees[j]+12*i)
        ndegrees2.append(degrees[j]-12*i)
        ndegrees3.append(degrees[j]+12*i)
        ndegrees3.append(degrees[j]-12*i)
    degreeslist.append(ndegrees1)
    degreeslist.append(ndegrees2)
    degreeslist.append(ndegrees3)
ndegrees += degrees
#degrees = ndegrees
degreeslist.append(ndegrees)
## build song 
phrs = 100
rpt = [1,2,3,8]
nrpt = [1,2,3,8]
phrslen = [4,8,12,16,20,24,28,32,36]
phrslensets = []
phrssets = 5
sng = []
rptphrs = 0
phrslens = 0
nts = {}
ntlen = [0.25,.5,.75, 1]

def buildphrslensets(phrslen, phrssets):
    phrslensets = []
    for i in range(0, phrssets):
        phrsnum = random.randint(2,len(phrslen)-1)
        nphrs = []
        maxphrs = random.randint(2,36)
        for j in range (0, phrsnum):
            nphrs.append(random.randint(2,maxphrs))
        phrslensets.append(nphrs)
    return phrslensets

def buildphrase(degrees, phrslen, ntlen):
    def buildtimedistr(timed):
        timedists = []
        for i in range(0,9):
            timedist = []
            for j in range(0, random.randint(3,10)):
                timedist.append(random.choice(timed))
            timedists.append(timedist)
        return timedists

    nts = []
    picklen = 500
    picklen = random.randint(6,picklen)
    ## assign weights
    nweights = []
    for i in range(0, picklen):
        if len(nweights) == 0:
            nweights.append(random.random()*.35+.65)
        else:
            nweights.append(random.random()*.5+.5)##nweights[-1]*(random.random()*.05+.95))
    ## sum nweights 
    snweights = sum(nweights)

    for i,wght in enumerate(nweights):
        nweights[i] = wght/snweights 
        
    ## assign time distribution
    timedistr = [.75,.75,.7,.55,.5,.5,.5,.45,.4,.35,.3,.25,.25,.25,.25,.15]
    timedistr2 = [.35,.3,.25,.25,.25,.25,.2,.15]
    timedistr3 = [.5,.25,.25,.25,.2]
    timedistr4 = [1.0,.85,.75,.5]
    timedistr5 = [.75, 1.0,.65,.5,.25]
    timedistr6 = [.5, .75, 1.0]
    timedistr7 = [2.0, 1.75, 1.5]
    timedistr8 = [3.0, 4.0,1.0]
    tdist2 = [timedistr,timedistr2,timedistr3,timedistr4, timedistr5] ##timedistr6, timedistr7, timedistr8]
    tdist = random.choice(tdist2)
    tpicks = []
    timedistrs = buildtimedistr(tdist)
    timedistr = random.choice(timedistrs)
    for i in range(0, picklen):
        tpicks.append(random.choice(timedistr))

    ## pick picklen notes
    npicks = []
    for i in range(0, picklen):
        npicks.append([tpicks[i], random.choice(degrees)])
    nts = random.choices(population=npicks, weights=nweights,k=phrslen)
    print(nts)
    # for i in range(0, phrslen):
    #     ntp = random.choice(degrees)
    #     nttp = random.choice(ntlen)
    #     np = {}
    #     np[ntp] = nttp
    #     nts.append(np)
    return nts

randomshft = [[-4,-2,0,2,4], [-12,-6,0,6,12], [-9,-6,-3,0,3,6,9],[-8,-4,0,4,8],[0]]
rshft = random.choice(randomshft)
def setArrangement(oldwphrs, phrs, randomshft):
    def transposePhrs(tphrase, sft = 0):
        i = 0
        copyphrs = []
        for ti, nt in tphrase:
            copyphrs.append([ti, nt+sft])
            i += 1
        return copyphrs

    ## oldwphrs length
    tphlen = 0 ## total phrase time
    nts = []  
    #randomshft = [-3,-1,0,1,3]
    for i in range(0, len(oldwphrs)):
        ind = random.randint(0,len(oldwphrs)-1)
        rptphrlen = oldwphrs[ind][1]
        for j in range(0,rptphrlen):
            rshft = random.choice(randomshft)
            ns = transposePhrs(oldwphrs[ind][0], rshft)
            nts += ns##oldwphrs[ind][0]
    return nts     

ants = []
oldwphrs = []  
phrslensets = buildphrslensets(phrslen, phrssets)      
for i in range(0, phrs):
    wphrs = []
    
    if rptphrs == 0:
        rptphrs = random.choice(rpt)
        nts = {}
        nphrslen = random.choice(phrslensets)
        phrslens = random.choice(nphrslen)
        npdegrees = random.choice(degreeslist)
        wphrs = buildphrase(npdegrees, phrslens, ntlen)
        oldwphrs.append([wphrs,rptphrs])
        # ants += wphrs
    # else:
    #     ants += wphrs 
    rptphrs -= 1
ants = setArrangement(oldwphrs,phrs,rshft)
ttime = 0
for time, pitch in ants:
    ttime += time
    MyMIDI.addNote(track, channel, pitch+transpose, ttime, duration, volume)

with open("C:\\Users\\chris\\MuiscPy\\major-scale.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)