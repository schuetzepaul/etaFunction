#! /usr/bin/env python

import numpy as np
import sys
import argparse
import math

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description="Test the effect of using the eta function with noise and thresholds on the detector resolution.")

parser.add_argument("-e", "--events", help="Number of events", type=int, default=10000)
parser.add_argument("-n", "--noise", help="Noise in electrons", type=float, default=0)
parser.add_argument("-t", "--threshold", help="Charge threshold", type=float, default=0)
parser.add_argument("-s", "--noshare", type=str2bool, nargs='?', const=True, default=0, help="No charge sharing.")
parser.add_argument("-a", "--atan", type=str2bool, nargs='?', const=False, default=0, help="Use an atan function as eta function (instead of a linear function).")

args = parser.parse_args()

nevents = args.events
noise = args.noise
threshold = args.threshold
noShare = args.noshare
usAtan = args.atan

xmin = -55./2.
xmax = 55./2.

def etaFunc(xin):
    off = 0.
    if noShare:
        off = 0.5

    retval = math.atan(xin/10)/math.pi + 0.5
    retval = (xin-xmin)/(xmax-xmin)*(1.-2.*off)+off
    return retval
    
def centerOfGravity(y1,y2):
    return (y1*xmin+y2*xmax)/(y1+y2)


from ROOT import TH1D,TCanvas,TRandom

hin = TH1D("hin","x_in",100,xmin*2.,xmax*2.)
hout = TH1D("hout","x_out",100,xmin*2.,xmax*2.)
hres = TH1D("hres","residual",100,-30.,30.)

nev = 1000

rang = TRandom()

thickness = 150
chargePerUm = 77
totalCharge = chargePerUm*thickness


for i in range(0,nevents):
    xin = rang.Uniform(xmin,xmax)
    hin.Fill(xin)

    leftCharge = (1-etaFunc(xin))*totalCharge
    rightCharge = (etaFunc(xin))*totalCharge

    #print "Pos: " + str(xin)
    #print "Charge: " + str(leftCharge) + " " + str(rightCharge)

    leftCharge += rang.Gaus(0,noise)
    rightCharge += rang.Gaus(0,noise)
    
    if leftCharge<threshold:
        leftCharge=0
    if rightCharge<threshold:
        rightCharge=0
    
    cog = centerOfGravity(leftCharge,rightCharge)

    #print "COG: " + str(cog)

    hout.Fill(cog)

    hres.Fill(cog-xin)


c1 = TCanvas("c1", "Window XP", 900,900)

c1.Divide(2,2)

c1.cd(1)
hin.Draw()

c1.cd(2)
hout.Draw()

c1.cd(3)
hres.Draw()


blah = raw_input("Press enter")
