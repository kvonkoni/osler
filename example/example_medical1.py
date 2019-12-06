#!/usr/bin/env python

import os,sys

lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from osler.assertion import Assertion
from osler.criterion import Criterion
from osler.diagnosis import Diagnosis
from osler.issue import Issue
from osler.engine import Matrix

#Defining assertions

HBsAg_pos = Assertion("HBsAg = positive")
aHDV_neg= Assertion("anti-HDV = negative")
aHBc_pos = Assertion("anti-HBc = positive")
aHBs_pos = Assertion("anti-HBs = positive")
IgMaHBc_pos = Assertion("IgM anti-HBc = positive")

#Defining diagnoses

acute_infection = Diagnosis('Acute infecction', {IgMaHBc_pos.true(), aHBs_pos.false(), aHBc_pos.true(), aHDV_neg.true(), HBsAg_pos.true()})
chronic_infection = Diagnosis('Chronic infecction', {IgMaHBc_pos.false(), aHBs_pos.false(), aHBc_pos.true(), aHDV_neg.true(), HBsAg_pos.true()})
uncertain1 = Diagnosis('Uncertain configuration 1', {aHBs_pos.true(), aHBc_pos.true(), aHDV_neg.true(), HBsAg_pos.true()})
uncertain2 = Diagnosis('Uncertain configuration 2', {aHBc_pos.false(), aHDV_neg.true(), HBsAg_pos.true()})
hepBD = Diagnosis('Hepatitis B+D', {aHDV_neg.false(), HBsAg_pos.true()})
unclear_poss_resolved = Diagnosis('Unclear (possibly resolved)', {aHBc_pos.true(), aHBs_pos.false(), HBsAg_pos.false()})
no_suspicion = Diagnosis('Healthy not vaccinated or suspicious', {aHBc_pos.false(), aHBs_pos.false(), HBsAg_pos.false()})
#cured = Diagnosis('Cured', {aHBc_pos.true(), aHBs_pos.true(), HBsAg_pos.false()})
#vaccinated = Diagnosis('Vaccinated', {aHBc_pos.false(), aHBs_pos.true(), HBsAg_pos.false()})

#Defining an issue

hepB_pred = Issue('Hepatitis B predictions', {acute_infection, chronic_infection, uncertain1, uncertain2, hepBD, unclear_poss_resolved, no_suspicion})

#Building a test tree

matrix = Matrix(hepB_pred)
matrix.construct_tree(debug=True)

matrix.node.to_png("result_example_medical1.png")
