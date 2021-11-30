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

acute_infection = Diagnosis('Acute infecction', {Criterion(IgMaHBc_pos, True), Criterion(aHBs_pos, False), Criterion(aHBc_pos, True), Criterion(aHDV_neg, True), Criterion(HBsAg_pos, True)})
chronic_infection = Diagnosis('Chronic infecction', {Criterion(IgMaHBc_pos, False), Criterion(aHBs_pos, False), Criterion(aHBc_pos, True), Criterion(aHDV_neg, True), Criterion(HBsAg_pos, True)})
uncertain1 = Diagnosis('Uncertain configuration 1', {Criterion(aHBs_pos, True), Criterion(aHBc_pos, True), Criterion(aHDV_neg, True), Criterion(HBsAg_pos, True)})
uncertain2 = Diagnosis('Uncertain configuration 2', {Criterion(aHBc_pos, False), Criterion(aHDV_neg, True), Criterion(HBsAg_pos, True)})
hepBD = Diagnosis('Hepatitis B+D', {Criterion(aHDV_neg, False), Criterion(HBsAg_pos, True)})
unclear_poss_resolved = Diagnosis('Unclear (possibly resolved)', {Criterion(aHBc_pos, True), Criterion(aHBs_pos, False), Criterion(HBsAg_pos, False)})
no_suspicion = Diagnosis('Healthy not vaccinated or suspicious', {Criterion(aHBc_pos, False), Criterion(aHBs_pos, False), Criterion(HBsAg_pos, False)})

#Defining an issue

hepB_pred = Issue('Hepatitis B predictions', {acute_infection, chronic_infection, uncertain1, uncertain2, hepBD, unclear_poss_resolved, no_suspicion})

#Building a test tree

matrix = Matrix(hepB_pred)
matrix.construct_tree()

matrix.node.to_png("result_example_medical1.png")
