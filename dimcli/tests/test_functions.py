# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli 
"""

from __future__ import print_function

import unittest, os, sys, click
import configparser

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..core.utils import dimensions_url
from ..core.api import DslDataset
from ..shortcuts import *


class TestOne(unittest.TestCase):

    """
    Tests - DSL function wrappers 
    """

    click.secho("**TESTS**", fg="red")
    login(instance="live")
    d = Dsl()

    def test_001(self):
        click.secho("\nTEST 001: Extract concepts.", fg="green")
        # ----
        a = """
BACKGROUND: In order to make further gains in preventing newborn deaths, effective interventions are needed. Ultrasounds and newborn anthropometry are proven interventions to identify preterm birth complications, the leading cause of newborn deaths. The INTERGROWTH-21st global gestational dating and fetal and newborn growth standards prescribe optimal growth in any population. Jacaranda Health in Kenya was the first low-resource health facility to implement the standards and evaluate their feasibility and acceptability. OBJECTIVE: To capture patients' perceptions of ultrasound and newborn care before and during implementation of the INTERGROWTH-21st standards. METHODS: The study was conducted over two years before and during the introduction of the INTERGROWTH-21st standards. Fifty pregnant and/or newly delivered women were selected for in-depth interviews and focus group discussions using convenience and purposive sampling. Interviews were conducted by research assistants using semi-structured guides once in the pre-implementation phase and twice in the implementation phase. Interviews were transcribed, double-coded by two independent researchers and thematically analyzed together. Demographic information was obtained from hospital records. RESULTS: Patients reported being generally satisfied with ultrasound care when providers communicated effectively. Women reported a priority for ultrasound was that it allowed them to feel reassured. However, a clear need for better pre-screening information emerged consistently from patients. Women noted that factors facilitating their choosing to have an ultrasound included ensuring the well-being of the fetus and learning the sex. Barriers included wait times and financial constraints. Patients were generally satisfied with care using the newborn standards. CONCLUSIONS: As the INTERGROWTH-21st standards are implemented worldwide, understanding ways to facilitate implementation is critical. Increased and standardized communication about ultrasound should be provided before the procedure to increase satisfaction and uptake. Considering patient perspectives when integrating new standards or guidelines into routine clinical care will inform effective strategies in care provision, thus improving maternal and newborn health and survival."""
        click.secho("With scores", fg="magenta")
        print(extract_concepts(a, with_scores=True))
        click.secho("Without scores", fg="magenta")
        print(extract_concepts(a, with_scores=False))
        click.secho("Without scores, as dimcli.DslDataset", fg="magenta")
        print(extract_concepts(a, with_scores=False, as_df=False))
        # ----
        click.secho("Completed test succesfully", fg="green")



    def test_002(self):
        click.secho("\nTEST 002: Extract grants.", fg="green")
        # ----
        click.secho("With fundref", fg="magenta")
        print(extract_grants("R01HL117329",  fundref="100000050"))
        click.secho("With funder_name", fg="magenta")
        print(extract_grants("HL117648",  funder_name="NIH"))
        click.secho("Build a dataframe", fg="magenta")
        print(extract_grants("HL117648",  funder_name="NIH").as_dataframe())
        # ----
        click.secho("Completed test succesfully", fg="green")



    def test_003(self):
        click.secho("\nTEST 003: Extract classifications.", fg="green")
        # ----
        title="""Burnout and intentions to quit the practice among community pediatricians: 
        associations with specific professional activities"""
        abstract="""BACKGROUND: Burnout is an occupational disease expressed by loss of mental and physical energy due to prolonged and unsuccessful coping with stressors at work. A prior survey among Israeli pediatricians published in 2006 found a correlation between burnout and job structure match, defined as the match between engagement with, and satisfaction from, specific professional activities. The aims of the present study were to characterize the current levels of burnout and its correlates among community pediatricians, to identify changes over time since the prior survey, and to identify professional activities that may reduce burnout. METHODS: A questionnaire was distributed among pediatricians both at a medical conference and by a web-based survey. RESULTS: Of the 518 pediatricians approached, 238 (46%) responded to the questionnaire. High burnout levels were identified in 33% (95% CI:27-39%) of the respondents. Higher burnout prevalence was found among pediatricians who were not board-certified, salaried, younger, and working long hours. The greater the discrepancy between the engagement of the pediatrician and the satisfaction felt in the measured professional activities, the greater was the burnout level (p < 0.01). The following activities were especially associated with burnout: administrative work (frequent engagement, disliked duty) and research and teaching (infrequent engagement, satisfying activities). A comparison of the engagement-satisfaction match between 2006 and 2017 showed that the discrepancy had increased significantly in research (p < 0.001), student tutoring (P < 0.001), continuing medical education and participation in professional conferences (P = 0.0074), management (p = 0.043) and community health promotion (P = 0.006). A significant correlation was found between burnout and thoughts of quitting pediatrics or medicine (p < 0.001). CONCLUSIONS: Healthcare managers should encourage diversification of the pediatrician's job by enabling greater engagement in the identified anti-burnout professional activities, such as: participation in professional consultations, management, tutoring students and conducting research."""
        click.secho("With FORs", fg="magenta")
        print(extract_classification(title, abstract, "FOR").json)
        click.secho("With UOA", fg="magenta")
        print(extract_classification(title, abstract, "UOA").json)
        click.secho("Build a dataframe", fg="magenta")
        print(extract_classification(title, abstract, "FOR").as_dataframe())
        click.secho("Without specifying a system - use all", fg="magenta")
        print(extract_classification(title, abstract))
        # ----
        click.secho("Completed test succesfully", fg="green")



if __name__ == "__main__":
    unittest.main()
