# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Unit tests for Dimcli - functions

python -m dimcli.tests.test_functions

"""

from __future__ import print_function

import unittest, os, sys, click

from .. import *
from ..core.auth import USER_CONFIG_FILE_PATH
from ..core.api import DslDataset
from ..utils import *
from ..functions import *

from .settings import API_INSTANCE


class TestOne(unittest.TestCase):

    """
    Tests - DSL function wrappers 
    """

    click.secho("**test_functions.py**", fg="red")
    login(instance=API_INSTANCE)
    d = Dsl()

    def test_001(self):
        click.secho("\nTEST 001: Extract concepts.", bg="green")
        # ----
        a = """
BACKGROUND: In order to make further gains in preventing newborn deaths, effective interventions are needed. Ultrasounds and newborn anthropometry are proven interventions to identify preterm birth complications, the leading cause of newborn deaths. The INTERGROWTH-21st global gestational dating and fetal and newborn growth standards prescribe optimal growth in any population. Jacaranda Health in Kenya was the first low-resource health facility to implement the standards and evaluate their feasibility and acceptability. OBJECTIVE: To capture patients' perceptions of ultrasound and newborn care before and during implementation of the INTERGROWTH-21st standards. METHODS: The study was conducted over two years before and during the introduction of the INTERGROWTH-21st standards. Fifty pregnant and/or newly delivered women were selected for in-depth interviews and focus group discussions using convenience and purposive sampling. Interviews were conducted by research assistants using semi-structured guides once in the pre-implementation phase and twice in the implementation phase. Interviews were transcribed, double-coded by two independent researchers and thematically analyzed together. Demographic information was obtained from hospital records. RESULTS: Patients reported being generally satisfied with ultrasound care when providers communicated effectively. Women reported a priority for ultrasound was that it allowed them to feel reassured. However, a clear need for better pre-screening information emerged consistently from patients. Women noted that factors facilitating their choosing to have an ultrasound included ensuring the well-being of the fetus and learning the sex. Barriers included wait times and financial constraints. Patients were generally satisfied with care using the newborn standards. CONCLUSIONS: As the INTERGROWTH-21st standards are implemented worldwide, understanding ways to facilitate implementation is critical. Increased and standardized communication about ultrasound should be provided before the procedure to increase satisfaction and uptake. Considering patient perspectives when integrating new standards or guidelines into routine clinical care will inform effective strategies in care provision, thus improving maternal and newborn health and survival."""
        click.secho("With scores", fg="magenta")
        print(extract_concepts(a, scores=True))
        click.secho("Without scores", fg="magenta")
        print(extract_concepts(a, scores=False))
        click.secho("Without scores, as dimcli.DslDataset", fg="magenta")
        print(extract_concepts(a, scores=False, as_df=False))
        # ----
        click.secho("Completed test succesfully", fg="green")



    def test_002(self):
        click.secho("\nTEST 002: Extract grants.", bg="green")
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
        click.secho("\nTEST 003: Extract classifications.", bg="green")
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


    def test_004(self):
        click.secho("\nTEST 004: Extract affiliations.", bg="green")
        # ----
        click.secho("Return json, no results", fg="magenta")
        print(extract_affiliations("nothing", as_json=True))

        click.secho("Return DF, no results", fg="magenta")
        print(extract_affiliations("nothing"))

        click.secho("Return DF, valid results", fg="magenta")
        print(extract_affiliations("london college cambridge, new york university"))

        click.secho("Return DF, multiple results including failing ones", fg="magenta")
        print(extract_affiliations(["london college cambridge", "universita di roma", "universita sapienza ", "nothing"]))        
        
        input_data_struct = [
            {"name":"london college cambridge",
            "city":"",
            "state":"",
            "country":""},
            {"name":"milano bicocca",
            "city":"Milano",
            "state":"",
            "country":"Italy"},
            {"name":"nothing",
            "city":"Milano",
            "state":"",
            "country":"Italy"}, 
            {"name":"nothing",
            "city":"",
            "state":"",
            "country":""}, 
        ]
        click.secho("Return DF, structured data, multiple results including failing ones", fg="magenta")
        print(extract_affiliations(input_data_struct))
        # ----

        click.secho("Completed test succesfully", fg="green")




    def test_005(self):
        click.secho("\nTEST 005: Identify experts.", bg="green")
        # ----

        click.secho("No text, no results", fg="magenta")
        print(identify_experts("", verbose=True))

        text = """It is a truism among scientists that our enterprise benefits humanity because of the technological breakthroughs that follow in discovery's wake. And it is a truism among historians that the relation between science and technology is far more complex and much less linear than people often assume. Before the 19th century, invention and innovation emerged primarily from craft traditions among people who were not scientists and who were typically unaware of pertinent scientific developments. The magnetic compass, gunpowder, the printing press, the chronometer, the cotton gin, the steam engine and the water wheel are among the many examples. In the late 1800s matters changed: craft traditions were reconstructed as “technology” that bore an important relation to science, and scientists began to take a deeper interest in applying theories to practical problems. A good example of the latter is the steam boiler explosion commission, appointed by Congress to investigate such accidents and discussed in Scientific American's issue of March 23, 1878. Still, technologists frequently worked more in parallel with contemporary science than in sequence. Technologists—soon to be known as engineers—were a different community of people with different goals, values, expectations and methodologies. Their accomplishments could not be understood simply as applied science. Even in the early 20th century the often loose link between scientific knowledge and technological advance was surprising; for example, aviation took off before scientists had a working theory of lift. Scientists said that flight by machines “heavier than air” was impossible, but nonetheless airplanes flew."""

        click.secho("Long text, no options", fg="magenta")
        print(identify_experts(text, verbose=True))

        click.secho("Long text, misc options", fg="magenta")
        print(identify_experts(text, max_concepts=3, connector="AND", source="grants", verbose=True))

        click.secho("Long text, conflict options", fg="magenta")
        print(identify_experts(text, conflicts=["ur.012331705127.09", "ur.013104324735.47"], verbose=True))

        # ----

        click.secho("Completed test succesfully", fg="green")



    def test_006(self):
        click.secho("\nTEST 006: Build reviewers matrix.", bg="green")
        # ----

        click.secho("No text, no results", fg="magenta")
        try:
            print(build_reviewers_matrix("", "", verbose=True))
        except:
            pass

        click.secho("Some text, random candidates, returns no results", fg="magenta")
        print(build_reviewers_matrix(["lorem", "some"], ["ur.1234", "ur.4354w6"], verbose=True))

        abstracts = [
            {
            'id' : 'A1',
            'text' : """We describe monocrystalline graphitic films, which are a few atoms thick but are nonetheless stable under ambient conditions,
        metallic, and of remarkably high quality. The films are found to be a two-dimensional semimetal with a tiny overlap between
        valence and conductance bands, and they exhibit a strong ambipolar electric field effect such that electrons and
        holes in concentrations up to 10 per square centimeter and with room-temperature mobilities of approximately 10,000 square
        centimeters per volt-second can be induced by applying gate voltage.
        """
            },
            {
            'id' : "A2",
            'text' : """The physicochemical properties of a molecule-metal interface, in principle, can play a significant role in tuning the electronic properties 
        of organic devices. In this report, we demonstrate an electrode engineering approach in a robust, reproducible molecular memristor that 
        enables a colossal tunability in both switching voltage (from 130 mV to 4 V i.e. >2500% variation) and current (by ~6 orders of magnitude). 
        This provides a spectrum of device design parameters that can be “dialed-in” to create fast, scalable and ultralow energy organic 
        memristors optimal for applications spanning digital memory, logic circuits and brain-inspired computing.
        """
        }
        ]

        candidates = ["ur.01146544531.57", "ur.011535264111.51", "ur.0767105504.29", 
                    "ur.011513332561.53", "ur.01055006635.53"]


        click.secho("Good input data, default params", fg="magenta")
        print(build_reviewers_matrix(abstracts, candidates, max_concepts=10, source="grants"))

        click.secho("Good input data, custom params max_concepts=10, source=grants", fg="magenta")
        print(build_reviewers_matrix(abstracts, candidates, max_concepts=10, source="grants"))
        # ----

        click.secho("Completed test succesfully", fg="green")


if __name__ == "__main__":
    unittest.main()
