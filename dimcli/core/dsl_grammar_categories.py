#!/usr/bin/python
# -*- coding: utf-8 -*-


#
# CATEGORIES_DICT is a dictionary rendering of the DSL research categories JSON
#
# last updated: 2019-09-23
#
# how to create:
#
# > search publications return category_for limit 1000
# (for each of the categories)
#
# Then remove '_stats' section, and combine them all into a py file
#
#

CATEGORIES_DICT = {
    "category_sdg": [
        {
            "count": 1348219,
            "id": "40007",
            "name": "7 Affordable and Clean Energy"
        },
        {
            "count": 1265880,
            "id": "40003",
            "name": "3 Good Health and Well Being"
        },
        {
            "count": 641929,
            "id": "40016",
            "name": "16 Peace, Justice and Strong Institutions"
        },
        {
            "count": 515160,
            "id": "40004",
            "name": "4 Quality Education"
        },
        {
            "count": 429531,
            "id": "40013",
            "name": "13 Climate Action"
        },
        {
            "count": 227782,
            "id": "40008",
            "name": "8 Decent Work and Economic Growth"
        },
        {
            "count": 195027,
            "id": "40011",
            "name": "11 Sustainable Cities and Communities"
        },
        {
            "count": 164207,
            "id": "40010",
            "name": "10 Reduced Inequalities"
        },
        {
            "count": 119014,
            "id": "40002",
            "name": "2 Zero Hunger"
        },
        {
            "count": 70387,
            "id": "40006",
            "name": "6 Clean Water and Sanitation"
        },
        {
            "count": 61860,
            "id": "40014",
            "name": "14 Life Below Water"
        },
        {
            "count": 61217,
            "id": "40015",
            "name": "15 Life on Land"
        },
        {
            "count": 57750,
            "id": "40012",
            "name": "12 Responsible Consumption and Production"
        },
        {
            "count": 43545,
            "id": "40001",
            "name": "1 No Poverty"
        },
        {
            "count": 21476,
            "id": "40005",
            "name": "5 Gender Equality"
        },
        {
            "count": 19311,
            "id": "40009",
            "name": "9 Industry, Innovation and Infrastructure"
        },
        {
            "count": 10346,
            "id": "40017",
            "name": "17 Partnerships for the Goals"
        }
    ],
    "category_uoa": [
        {
            "count": 12965896,
            "id": "30012",
            "name": "B12 Engineering"
        },
        {
            "count": 7664934,
            "id": "30001",
            "name": "A01 Clinical Medicine"
        },
        {
            "count": 5441205,
            "id": "30003",
            "name": "A03 Allied Health Professions, Dentistry, Nursing and Pharmacy"
        },
        {
            "count": 3476541,
            "id": "30011",
            "name": "B11 Computer Science and Informatics"
        },
        {
            "count": 2674165,
            "id": "30008",
            "name": "B08 Chemistry"
        },
        {
            "count": 2589803,
            "id": "30005",
            "name": "A05 Biological Sciences"
        },
        {
            "count": 2504503,
            "id": "30009",
            "name": "B09 Physics"
        },
        {
            "count": 2361360,
            "id": "30004",
            "name": "A04 Psychology, Psychiatry and Neuroscience"
        },
        {
            "count": 2348396,
            "id": "30010",
            "name": "B10 Mathematical Sciences"
        },
        {
            "count": 2260339,
            "id": "30006",
            "name": "A06 Agriculture, Veterinary and Food Science"
        },
        {
            "count": 2023701,
            "id": "30017",
            "name": "C17 Business and Management Studies"
        },
        {
            "count": 1618104,
            "id": "30007",
            "name": "B07 Earth Systems and Environmental Sciences"
        },
        {
            "count": 960452,
            "id": "30023",
            "name": "C23 Education"
        },
        {
            "count": 840151,
            "id": "30002",
            "name": "A02 Public Health, Health Services and Primary Care"
        },
        {
            "count": 662202,
            "id": "30014",
            "name": "C14 Geography and Environmental Studies"
        },
        {
            "count": 467677,
            "id": "30028",
            "name": "D28 History"
        },
        {
            "count": 447784,
            "id": "30024",
            "name": "C24 Sport and Exercise Sciences, Leisure and Tourism"
        },
        {
            "count": 398831,
            "id": "30013",
            "name": "C13 Architecture, Built Environment and Planning"
        },
        {
            "count": 389544,
            "id": "30020",
            "name": "C20 Social Work and Social Policy"
        },
        {
            "count": 380338,
            "id": "30018",
            "name": "C18 Law"
        },
        {
            "count": 355463,
            "id": "30019",
            "name": "C19 Politics and International Studies"
        },
        {
            "count": 311640,
            "id": "30026",
            "name": "D26 Modern Languages and Linguistics"
        },
        {
            "count": 275604,
            "id": "30016",
            "name": "C16 Economics and Econometrics"
        },
        {
            "count": 251384,
            "id": "30027",
            "name": "D27 English Language and Literature"
        },
        {
            "count": 200627,
            "id": "30030",
            "name": "D30 Philosophy"
        },
        {
            "count": 195652,
            "id": "30034",
            "name": "D34 Communication, Cultural and Media Studies, Library and Information Management"
        },
        {
            "count": 133441,
            "id": "30032",
            "name": "D32 Art and Design: History, Practice and Theory"
        },
        {
            "count": 130495,
            "id": "30022",
            "name": "C22 Anthropology and Development Studies"
        },
        {
            "count": 125591,
            "id": "30021",
            "name": "C21 Sociology"
        },
        {
            "count": 92204,
            "id": "30033",
            "name": "D33 Music, Drama, Dance, Performing Arts, Film and Screen Studies"
        },
        {
            "count": 87084,
            "id": "30015",
            "name": "C15 Archaeology"
        },
        {
            "count": 76316,
            "id": "30031",
            "name": "D31 Theology and Religious Studies"
        },
        {
            "count": 71109,
            "id": "30025",
            "name": "D25 Area Studies"
        },
        {
            "count": 24820,
            "id": "30029",
            "name": "D29 Classics"
        }
    ],
    "category_rcdc": [
        {
            "count": 6974252,
            "id": "507",
            "name": "Clinical Research"
        },
        {
            "count": 2977663,
            "id": "558",
            "name": "Prevention"
        },
        {
            "count": 2960147,
            "id": "387",
            "name": "Neurosciences"
        },
        {
            "count": 2879104,
            "id": "503",
            "name": "Cancer"
        },
        {
            "count": 2717263,
            "id": "526",
            "name": "Genetics"
        },
        {
            "count": 2621641,
            "id": "559",
            "name": "Rare Diseases"
        },
        {
            "count": 2253835,
            "id": "547",
            "name": "Pediatric"
        },
        {
            "count": 1984380,
            "id": "501",
            "name": "Brain Disorders"
        },
        {
            "count": 1943567,
            "id": "533",
            "name": "Infectious Diseases"
        },
        {
            "count": 1917560,
            "id": "498",
            "name": "Behavioral and Social Science"
        },
        {
            "count": 1845002,
            "id": "344",
            "name": "Digestive Diseases"
        },
        {
            "count": 1783610,
            "id": "331",
            "name": "Cardiovascular"
        },
        {
            "count": 1559869,
            "id": "337",
            "name": "Bioengineering"
        },
        {
            "count": 1494264,
            "id": "338",
            "name": "Biotechnology"
        },
        {
            "count": 1193630,
            "id": "388",
            "name": "Nutrition"
        },
        {
            "count": 1171906,
            "id": "295",
            "name": "Aging"
        },
        {
            "count": 1153989,
            "id": "380",
            "name": "Mental Health"
        },
        {
            "count": 1078591,
            "id": "445",
            "name": "Heart Disease"
        },
        {
            "count": 1009901,
            "id": "508",
            "name": "Clinical Trials and Supportive Activities"
        },
        {
            "count": 948782,
            "id": "410",
            "name": "Lung"
        },
        {
            "count": 859626,
            "id": "447",
            "name": "Hematology"
        },
        {
            "count": 854776,
            "id": "542",
            "name": "Neurodegenerative"
        },
        {
            "count": 804596,
            "id": "520",
            "name": "Emerging Infectious Diseases"
        },
        {
            "count": 783143,
            "id": "439",
            "name": "Diagnostic Radiology"
        },
        {
            "count": 753280,
            "id": "546",
            "name": "Patient Safety"
        },
        {
            "count": 746542,
            "id": "583",
            "name": "Vaccine Related"
        },
        {
            "count": 660911,
            "id": "451",
            "name": "Liver Disease"
        },
        {
            "count": 659628,
            "id": "497",
            "name": "Basic Behavioral and Social Science"
        },
        {
            "count": 567077,
            "id": "397",
            "name": "Pain Research"
        },
        {
            "count": 562711,
            "id": "443",
            "name": "Health Services"
        },
        {
            "count": 534635,
            "id": "537",
            "name": "Kidney Disease"
        },
        {
            "count": 515608,
            "id": "438",
            "name": "Diabetes"
        },
        {
            "count": 513807,
            "id": "496",
            "name": "Autoimmune Disease"
        },
        {
            "count": 509504,
            "id": "521",
            "name": "Eye Disease And Disorders Of Vision"
        },
        {
            "count": 497532,
            "id": "436",
            "name": "Dental/Oral and Craniofacial Disease"
        },
        {
            "count": 473762,
            "id": "573",
            "name": "Substance Abuse"
        },
        {
            "count": 450652,
            "id": "416",
            "name": "Contraception/Reproduction"
        },
        {
            "count": 437544,
            "id": "484",
            "name": "Stem Cell Research"
        },
        {
            "count": 422939,
            "id": "421",
            "name": "Pain Conditions - Chronic"
        },
        {
            "count": 422080,
            "id": "430",
            "name": "Complementary and Alternative Medicine"
        },
        {
            "count": 407827,
            "id": "314",
            "name": "Injury (total) Accidents/Adverse Effects"
        },
        {
            "count": 406674,
            "id": "363",
            "name": "Human Genome"
        },
        {
            "count": 404513,
            "id": "580",
            "name": "Urologic Diseases"
        },
        {
            "count": 359381,
            "id": "527",
            "name": "HIV/AIDS"
        },
        {
            "count": 356825,
            "id": "499",
            "name": "Biodefense"
        },
        {
            "count": 356172,
            "id": "444",
            "name": "Heart Disease - Coronary Heart Disease"
        },
        {
            "count": 352817,
            "id": "316",
            "name": "Breast Cancer"
        },
        {
            "count": 345878,
            "id": "469",
            "name": "Rehabilitation"
        },
        {
            "count": 344591,
            "id": "578",
            "name": "Transplantation"
        },
        {
            "count": 337166,
            "id": "389",
            "name": "Obesity"
        },
        {
            "count": 328466,
            "id": "465",
            "name": "Perinatal Period - Conditions Originating in Perinatal Period"
        },
        {
            "count": 314573,
            "id": "390",
            "name": "Nanotechnology"
        },
        {
            "count": 312027,
            "id": "308",
            "name": "Atherosclerosis"
        },
        {
            "count": 303111,
            "id": "531",
            "name": "Immunization"
        },
        {
            "count": 281733,
            "id": "437",
            "name": "Depression"
        },
        {
            "count": 279118,
            "id": "375",
            "name": "Chronic Liver Disease and Cirrhosis"
        },
        {
            "count": 266299,
            "id": "379",
            "name": "Regenerative Medicine"
        },
        {
            "count": 260234,
            "id": "543",
            "name": "Orphan Drug"
        },
        {
            "count": 243219,
            "id": "458",
            "name": "Mind and Body"
        },
        {
            "count": 224522,
            "id": "304",
            "name": "Arthritis"
        },
        {
            "count": 216988,
            "id": "487",
            "name": "Acquired Cognitive Impairment"
        },
        {
            "count": 213537,
            "id": "485",
            "name": "Stroke"
        },
        {
            "count": 210929,
            "id": "367",
            "name": "Hypertension"
        },
        {
            "count": 205852,
            "id": "517",
            "name": "Drug Abuse (NIDA Only)"
        },
        {
            "count": 203263,
            "id": "569",
            "name": "Stem Cell Research - Nonembryonic - Non-Human"
        },
        {
            "count": 201281,
            "id": "368",
            "name": "Infant Mortality/ (LBW)"
        },
        {
            "count": 197817,
            "id": "514",
            "name": "Dementia"
        },
        {
            "count": 194044,
            "id": "305",
            "name": "Assistive Technology"
        },
        {
            "count": 185634,
            "id": "427",
            "name": "Vector-Borne Diseases"
        },
        {
            "count": 185247,
            "id": "490",
            "name": "Alcoholism, Alcohol Use and Health"
        },
        {
            "count": 180810,
            "id": "414",
            "name": "Colo-Rectal Cancer"
        },
        {
            "count": 180592,
            "id": "302",
            "name": "Antimicrobial Resistance"
        },
        {
            "count": 176919,
            "id": "541",
            "name": "Networking and Information Technology R&D"
        },
        {
            "count": 175828,
            "id": "550",
            "name": "Pediatric Research Initiative"
        },
        {
            "count": 169271,
            "id": "326",
            "name": "Lung Cancer"
        },
        {
            "count": 161735,
            "id": "556",
            "name": "Pneumonia & Influenza"
        },
        {
            "count": 161079,
            "id": "448",
            "name": "Hepatitis"
        },
        {
            "count": 158223,
            "id": "493",
            "name": "Alzheimer's Disease including Alzheimer's Disease Related Dementias (AD/ADRD)"
        },
        {
            "count": 150163,
            "id": "568",
            "name": "Stem Cell Research - Nonembryonic - Human"
        },
        {
            "count": 149741,
            "id": "298",
            "name": "Alzheimer's Disease"
        },
        {
            "count": 143283,
            "id": "478",
            "name": "Sleep Research"
        },
        {
            "count": 140093,
            "id": "536",
            "name": "Intellectual and Developmental Disabilities (IDD)"
        },
        {
            "count": 139955,
            "id": "412",
            "name": "Tobacco"
        },
        {
            "count": 138102,
            "id": "480",
            "name": "Smoking and Health"
        },
        {
            "count": 132449,
            "id": "463",
            "name": "Perinatal - Birth - Preterm (LBW)"
        },
        {
            "count": 129607,
            "id": "377",
            "name": "Prostate Cancer"
        },
        {
            "count": 129360,
            "id": "353",
            "name": "Estrogen"
        },
        {
            "count": 126029,
            "id": "454",
            "name": "Lymphoma"
        },
        {
            "count": 125504,
            "id": "391",
            "name": "Organ Transplantation"
        },
        {
            "count": 120129,
            "id": "588",
            "name": "Violence Research"
        },
        {
            "count": 120119,
            "id": "522",
            "name": "Foodborne Illness"
        },
        {
            "count": 116438,
            "id": "561",
            "name": "Serious Mental Illness"
        },
        {
            "count": 113981,
            "id": "476",
            "name": "Sexually Transmitted Diseases/Herpes"
        },
        {
            "count": 107221,
            "id": "394",
            "name": "Osteoporosis"
        },
        {
            "count": 106167,
            "id": "422",
            "name": "Tuberculosis"
        },
        {
            "count": 104341,
            "id": "324",
            "name": "Injury - Trauma - (Head and Spine)"
        },
        {
            "count": 102292,
            "id": "352",
            "name": "Epilepsy"
        },
        {
            "count": 99389,
            "id": "426",
            "name": "Pneumonia"
        },
        {
            "count": 97891,
            "id": "306",
            "name": "Asthma"
        },
        {
            "count": 97449,
            "id": "313",
            "name": "Brain Cancer"
        },
        {
            "count": 95996,
            "id": "472",
            "name": "Schizophrenia"
        },
        {
            "count": 95096,
            "id": "549",
            "name": "Pediatric Cancer"
        },
        {
            "count": 91389,
            "id": "509",
            "name": "Comparative Effectiveness Research"
        },
        {
            "count": 83120,
            "id": "396",
            "name": "Ovarian Cancer"
        },
        {
            "count": 82088,
            "id": "411",
            "name": "Pancreatic Cancer"
        },
        {
            "count": 79078,
            "id": "511",
            "name": "Congenital Structural Anomalies"
        },
        {
            "count": 78257,
            "id": "553",
            "name": "Peripheral Neuropathy"
        },
        {
            "count": 73962,
            "id": "525",
            "name": "Genetic Testing"
        },
        {
            "count": 72209,
            "id": "398",
            "name": "Parkinson's Disease"
        },
        {
            "count": 71018,
            "id": "450",
            "name": "Liver Cancer"
        },
        {
            "count": 70947,
            "id": "369",
            "name": "Inflammatory Bowel Disease"
        },
        {
            "count": 68773,
            "id": "475",
            "name": "Septicemia"
        },
        {
            "count": 68644,
            "id": "317",
            "name": "Cervical Cancer"
        },
        {
            "count": 65909,
            "id": "370",
            "name": "Influenza"
        },
        {
            "count": 61919,
            "id": "429",
            "name": "Climate-Related Exposures and Conditions"
        },
        {
            "count": 60835,
            "id": "460",
            "name": "Multiple Sclerosis"
        },
        {
            "count": 60738,
            "id": "409",
            "name": "Infertility"
        },
        {
            "count": 60613,
            "id": "471",
            "name": "Rural Health"
        },
        {
            "count": 59525,
            "id": "457",
            "name": "Malaria"
        },
        {
            "count": 59016,
            "id": "482",
            "name": "Spinal Cord Injury"
        },
        {
            "count": 56647,
            "id": "452",
            "name": "Lupus"
        },
        {
            "count": 56618,
            "id": "419",
            "name": "Hepatitis - C"
        },
        {
            "count": 56124,
            "id": "361",
            "name": "Gene Therapy"
        },
        {
            "count": 52331,
            "id": "506",
            "name": "Childhood Leukemia"
        },
        {
            "count": 51837,
            "id": "554",
            "name": "Physical Rehabilitation"
        },
        {
            "count": 46273,
            "id": "418",
            "name": "Hepatitis - B"
        },
        {
            "count": 45934,
            "id": "310",
            "name": "Autism"
        },
        {
            "count": 42660,
            "id": "376",
            "name": "Chronic Obstructive Pulmonary Disease"
        },
        {
            "count": 41391,
            "id": "519",
            "name": "Emergency Care"
        },
        {
            "count": 40592,
            "id": "494",
            "name": "Anxiety Disorders"
        },
        {
            "count": 40334,
            "id": "433",
            "name": "Cost Effectiveness Research"
        },
        {
            "count": 40331,
            "id": "510",
            "name": "Conditions Affecting the Embryonic and Fetal Periods"
        },
        {
            "count": 39101,
            "id": "400",
            "name": "Suicide"
        },
        {
            "count": 38058,
            "id": "435",
            "name": "Cystic Fibrosis"
        },
        {
            "count": 36415,
            "id": "513",
            "name": "Crohn's Disease"
        },
        {
            "count": 36313,
            "id": "325",
            "name": "Injury - Traumatic brain injury"
        },
        {
            "count": 34164,
            "id": "442",
            "name": "Headaches"
        },
        {
            "count": 30626,
            "id": "557",
            "name": "Post-Traumatic Stress Disorder (PTSD)"
        },
        {
            "count": 30501,
            "id": "345",
            "name": "Digestive Diseases - (Peptic Ulcer)"
        },
        {
            "count": 29193,
            "id": "560",
            "name": "Rheumatoid Arthritis"
        },
        {
            "count": 28216,
            "id": "349",
            "name": "Eating Disorders"
        },
        {
            "count": 26993,
            "id": "589",
            "name": "Youth Violence"
        },
        {
            "count": 26749,
            "id": "309",
            "name": "Attention Deficit Disorder (ADD)"
        },
        {
            "count": 26356,
            "id": "564",
            "name": "Stem Cell Research - Embryonic - Non-Human"
        },
        {
            "count": 25721,
            "id": "575",
            "name": "Suicide Prevention"
        },
        {
            "count": 24320,
            "id": "548",
            "name": "Pediatric AIDS"
        },
        {
            "count": 24278,
            "id": "383",
            "name": "Muscular Dystrophy"
        },
        {
            "count": 24131,
            "id": "455",
            "name": "Macular Degeneration"
        },
        {
            "count": 23796,
            "id": "534",
            "name": "Injury - Childhood Injuries"
        },
        {
            "count": 23233,
            "id": "488",
            "name": "Adolescent Sexual Activity"
        },
        {
            "count": 22804,
            "id": "293",
            "name": "Acute Respiratory Distress Syndrome"
        },
        {
            "count": 22486,
            "id": "378",
            "name": "Psoriasis"
        },
        {
            "count": 22437,
            "id": "322",
            "name": "Migraines"
        },
        {
            "count": 20413,
            "id": "311",
            "name": "Cerebral Palsy"
        },
        {
            "count": 20206,
            "id": "587",
            "name": "Violence Against Women"
        },
        {
            "count": 20113,
            "id": "582",
            "name": "Uterine Cancer"
        },
        {
            "count": 20033,
            "id": "544",
            "name": "Osteoarthritis"
        },
        {
            "count": 17266,
            "id": "477",
            "name": "Sickle Cell Disease"
        },
        {
            "count": 17232,
            "id": "292",
            "name": "ALS"
        },
        {
            "count": 16739,
            "id": "332",
            "name": "Child Abuse and Neglect Research"
        },
        {
            "count": 16005,
            "id": "563",
            "name": "Stem Cell Research - Embryonic - Human"
        },
        {
            "count": 15973,
            "id": "395",
            "name": "Otitis Media"
        },
        {
            "count": 15786,
            "id": "381",
            "name": "Neuroblastoma"
        },
        {
            "count": 15727,
            "id": "359",
            "name": "Food Allergies"
        },
        {
            "count": 15649,
            "id": "403",
            "name": "Temporomandibular Muscle/Joint Disorder (TMJD)"
        },
        {
            "count": 14002,
            "id": "321",
            "name": "Methamphetamine"
        },
        {
            "count": 13842,
            "id": "424",
            "name": "Underage Drinking"
        },
        {
            "count": 13760,
            "id": "351",
            "name": "Endometriosis"
        },
        {
            "count": 13721,
            "id": "565",
            "name": "Stem Cell Research - Induced Pluripotent Stem Cell"
        },
        {
            "count": 13131,
            "id": "473",
            "name": "Scleroderma"
        },
        {
            "count": 12860,
            "id": "562",
            "name": "Sexual and Gender Minorities (SGM/LGBT*)"
        },
        {
            "count": 12655,
            "id": "300",
            "name": "Anorexia"
        },
        {
            "count": 11301,
            "id": "505",
            "name": "Cannabinoid Research"
        },
        {
            "count": 11220,
            "id": "364",
            "name": "Huntington's Disease"
        },
        {
            "count": 11112,
            "id": "577",
            "name": "Transmissible Spongiform Encephalopathy (TSE)"
        },
        {
            "count": 10894,
            "id": "566",
            "name": "Stem Cell Research - Induced Pluripotent Stem Cell - Human"
        },
        {
            "count": 10734,
            "id": "299",
            "name": "American Indians / Alaska Natives"
        },
        {
            "count": 10571,
            "id": "303",
            "name": "Aphasia"
        },
        {
            "count": 10313,
            "id": "365",
            "name": "Hydrocephalus"
        },
        {
            "count": 9713,
            "id": "441",
            "name": "HPV and/or Cervical Cancer Vaccines"
        },
        {
            "count": 9698,
            "id": "461",
            "name": "Myasthenia Gravis"
        },
        {
            "count": 9673,
            "id": "468",
            "name": "Prescription Drug Abuse"
        },
        {
            "count": 9386,
            "id": "347",
            "name": "Duchenne/ Becker Muscular Dystrophy"
        },
        {
            "count": 9362,
            "id": "532",
            "name": "Infant Mortality"
        },
        {
            "count": 9252,
            "id": "584",
            "name": "Vaccine related (AIDS)"
        },
        {
            "count": 9083,
            "id": "346",
            "name": "Down Syndrome"
        },
        {
            "count": 9050,
            "id": "570",
            "name": "Stem Cell Research - Umbilical Cord Blood/ Placenta"
        },
        {
            "count": 8908,
            "id": "453",
            "name": "Lyme Disease"
        },
        {
            "count": 8515,
            "id": "350",
            "name": "Emphysema"
        },
        {
            "count": 8472,
            "id": "539",
            "name": "Major Depressive Disorder"
        },
        {
            "count": 8328,
            "id": "500",
            "name": "Bipolar Disorder"
        },
        {
            "count": 8140,
            "id": "362",
            "name": "Homelessness"
        },
        {
            "count": 8099,
            "id": "552",
            "name": "Perinatal - Neonatal Respiratory Distress Syndrome"
        },
        {
            "count": 7921,
            "id": "535",
            "name": "Injury - Unintentional Childhood Injury"
        },
        {
            "count": 7892,
            "id": "516",
            "name": "Digestive Diseases - (Gallbladder)"
        },
        {
            "count": 7632,
            "id": "512",
            "name": "Cooley's Anemia"
        },
        {
            "count": 7234,
            "id": "467",
            "name": "Polycystic Kidney Disease"
        },
        {
            "count": 7167,
            "id": "358",
            "name": "Fibromyalgia"
        },
        {
            "count": 7081,
            "id": "491",
            "name": "Allergic Rhinitis (Hay Fever)"
        },
        {
            "count": 6849,
            "id": "348",
            "name": "Dystonia"
        },
        {
            "count": 6814,
            "id": "385",
            "name": "Neurofibromatosis"
        },
        {
            "count": 6806,
            "id": "571",
            "name": "Stem Cell Research - Umbilical Cord Blood/ Placenta - Human"
        },
        {
            "count": 6701,
            "id": "523",
            "name": "Frontotemporal Dementia (FTD)"
        },
        {
            "count": 6137,
            "id": "492",
            "name": "Alzheimer's Disease Related Dementias (ADRD)"
        },
        {
            "count": 5882,
            "id": "529",
            "name": "Health Effects of Indoor Air Pollution"
        },
        {
            "count": 5530,
            "id": "402",
            "name": "Teenage Pregnancy"
        },
        {
            "count": 5465,
            "id": "590",
            "name": "Youth Violence Prevention"
        },
        {
            "count": 5451,
            "id": "405",
            "name": "West Nile Virus"
        },
        {
            "count": 4903,
            "id": "489",
            "name": "Agent Orange & Dioxin"
        },
        {
            "count": 4885,
            "id": "301",
            "name": "Anthrax"
        },
        {
            "count": 4596,
            "id": "341",
            "name": "Fragile X Syndrome"
        },
        {
            "count": 4178,
            "id": "357",
            "name": "Fibroid Tumors (Uterine)"
        },
        {
            "count": 3871,
            "id": "423",
            "name": "Tuberous Sclerosis"
        },
        {
            "count": 3825,
            "id": "374",
            "name": "Chronic Fatigue Syndrome (ME/CFS)"
        },
        {
            "count": 3803,
            "id": "328",
            "name": "Interstitial Cystitis"
        },
        {
            "count": 3750,
            "id": "318",
            "name": "Charcot-Marie-Tooth Disease"
        },
        {
            "count": 3689,
            "id": "502",
            "name": "Burden of Illness"
        },
        {
            "count": 3685,
            "id": "579",
            "name": "Tuberculosis Vaccine"
        },
        {
            "count": 3577,
            "id": "481",
            "name": "Spina Bifida"
        },
        {
            "count": 3567,
            "id": "420",
            "name": "Hodgkin's Disease"
        },
        {
            "count": 3418,
            "id": "486",
            "name": "Substance Abuse Prevention"
        },
        {
            "count": 3400,
            "id": "574",
            "name": "Sudden Infant Death Syndrome"
        },
        {
            "count": 3313,
            "id": "356",
            "name": "Fetal Alcohol Syndrome"
        },
        {
            "count": 3307,
            "id": "479",
            "name": "Small Pox"
        },
        {
            "count": 3100,
            "id": "393",
            "name": "Osteogenesis Imperfecta"
        },
        {
            "count": 3080,
            "id": "330",
            "name": "Tourette Syndrome"
        },
        {
            "count": 2891,
            "id": "540",
            "name": "Myotonic Dystrophy"
        },
        {
            "count": 2824,
            "id": "307",
            "name": "Ataxia Telangiectasia"
        },
        {
            "count": 2591,
            "id": "483",
            "name": "Spinal Muscular Atrophy"
        },
        {
            "count": 2552,
            "id": "586",
            "name": "Vascular Cognitive Impairment/Dementia"
        },
        {
            "count": 2414,
            "id": "459",
            "name": "Mucopolysaccharidoses (MPS)"
        },
        {
            "count": 2302,
            "id": "518",
            "name": "Eczema / Atopic Dermatitis"
        },
        {
            "count": 2277,
            "id": "530",
            "name": "Human Fetal Tissue"
        },
        {
            "count": 2230,
            "id": "470",
            "name": "Rett Syndrome"
        },
        {
            "count": 2098,
            "id": "474",
            "name": "Screening And Brief Intervention For Substance Abuse"
        },
        {
            "count": 2004,
            "id": "329",
            "name": "Topical Microbicides"
        },
        {
            "count": 1859,
            "id": "538",
            "name": "Lewy Body Dementia"
        },
        {
            "count": 1726,
            "id": "336",
            "name": "Climate Change"
        },
        {
            "count": 1633,
            "id": "449",
            "name": "Lead Poisoning"
        },
        {
            "count": 1524,
            "id": "456",
            "name": "Malaria Vaccine"
        },
        {
            "count": 1495,
            "id": "567",
            "name": "Stem Cell Research - Induced Pluripotent Stem Cell - Non-Human"
        },
        {
            "count": 1361,
            "id": "495",
            "name": "Arctic"
        },
        {
            "count": 1227,
            "id": "335",
            "name": "Batten Disease"
        },
        {
            "count": 812,
            "id": "528",
            "name": "Health Effects of Household Energy Combustion"
        },
        {
            "count": 792,
            "id": "355",
            "name": "Facioscapulohumeral Muscular Dystrophy"
        },
        {
            "count": 712,
            "id": "440",
            "name": "Global Warming Climate Change"
        },
        {
            "count": 494,
            "id": "576",
            "name": "Therapeutic Cannabinoid Research"
        },
        {
            "count": 427,
            "id": "404",
            "name": "Vulvodynia"
        },
        {
            "count": 423,
            "id": "581",
            "name": "Usher Syndrome"
        },
        {
            "count": 397,
            "id": "504",
            "name": "Cannabidiol Research"
        },
        {
            "count": 283,
            "id": "585",
            "name": "Valley Fever"
        },
        {
            "count": 215,
            "id": "555",
            "name": "Pick's Disease"
        },
        {
            "count": 208,
            "id": "551",
            "name": "Pelvic Inflammatory Disease"
        },
        {
            "count": 94,
            "id": "366",
            "name": "Hyperbaric Oxygen"
        },
        {
            "count": 82,
            "id": "515",
            "name": "Diethylstilbestrol (DES)"
        },
        {
            "count": 19,
            "id": "545",
            "name": "Paget's Disease"
        },
        {
            "count": 12,
            "id": "524",
            "name": "Gene Therapy Clinical Trials"
        },
        {
            "count": 9,
            "id": "572",
            "name": "Stem Cell Research - Umbilical Cord Blood/ Placenta - Non-Human"
        },
        {
            "count": 4,
            "id": "417",
            "name": "Hepatitis - A"
        },
        {
            "count": 2,
            "id": "319",
            "name": "Homicide and Legal Interventions"
        }
    ],
    "category_hrcs_rac": [
        {
            "count": 2396058,
            "id": "10201",
            "name": "2.1 Biological and endogenous factors"
        },
        {
            "count": 1214188,
            "id": "10101",
            "name": "1.1 Normal biological development and functioning"
        },
        {
            "count": 856699,
            "id": "10601",
            "name": "6.1 Pharmaceuticals"
        },
        {
            "count": 648809,
            "id": "10501",
            "name": "5.1 Pharmaceuticals"
        },
        {
            "count": 406362,
            "id": "10402",
            "name": "4.2 Evaluation of markers and technologies"
        },
        {
            "count": 371676,
            "id": "10202",
            "name": "2.2 Factors relating to physical environment"
        },
        {
            "count": 291583,
            "id": "10401",
            "name": "4.1 Discovery and preclinical testing of markers and technologies"
        },
        {
            "count": 249259,
            "id": "10604",
            "name": "6.4 Surgery"
        },
        {
            "count": 247021,
            "id": "10801",
            "name": "8.1 Organisation and delivery of services"
        },
        {
            "count": 246925,
            "id": "10701",
            "name": "7.1 Individual care needs"
        },
        {
            "count": 132635,
            "id": "10703",
            "name": "7.3 Management and decision making"
        },
        {
            "count": 124797,
            "id": "10203",
            "name": "2.3 Psychological, social and economic factors"
        },
        {
            "count": 118931,
            "id": "10502",
            "name": "5.2 Cellular and gene therapies"
        },
        {
            "count": 84768,
            "id": "10304",
            "name": "3.4 Vaccines"
        },
        {
            "count": 71809,
            "id": "10301",
            "name": "3.1 Primary prevention interventions to modify behaviours or promote well-being"
        },
        {
            "count": 66281,
            "id": "10204",
            "name": "2.4 Surveillance and distribution"
        },
        {
            "count": 63543,
            "id": "10303",
            "name": "3.3 Nutrition and chemoprevention"
        },
        {
            "count": 54768,
            "id": "10607",
            "name": "6.7 Physical"
        },
        {
            "count": 52397,
            "id": "10102",
            "name": "1.2 Psychological and socioeconomic processes"
        },
        {
            "count": 45279,
            "id": "10606",
            "name": "6.6 Psychological and behavioural"
        },
        {
            "count": 41337,
            "id": "10803",
            "name": "8.3 Policy, ethics and research governance"
        },
        {
            "count": 35695,
            "id": "10605",
            "name": "6.5 Radiotherapy"
        },
        {
            "count": 22275,
            "id": "10603",
            "name": "6.3 Medical devices"
        },
        {
            "count": 18798,
            "id": "10702",
            "name": "7.2 End of life care"
        },
        {
            "count": 16546,
            "id": "10804",
            "name": "8.4 Research design and methodologies"
        },
        {
            "count": 15451,
            "id": "10404",
            "name": "4.4 Population screening"
        },
        {
            "count": 13219,
            "id": "10602",
            "name": "6.2 Cellular and gene therapies"
        },
        {
            "count": 11869,
            "id": "10205",
            "name": "2.5 Research design and methodologies (aetiology)"
        },
        {
            "count": 8627,
            "id": "10802",
            "name": "8.2 Health and welfare economics"
        },
        {
            "count": 7994,
            "id": "10503",
            "name": "5.3 Medical devices"
        },
        {
            "count": 7557,
            "id": "10302",
            "name": "3.2 Interventions to alter physical and biological environmental risks"
        },
        {
            "count": 5320,
            "id": "10504",
            "name": "5.4 Surgery"
        },
        {
            "count": 4867,
            "id": "10509",
            "name": "5.9 Resources and infrastructure (development of treatments)"
        },
        {
            "count": 4492,
            "id": "10103",
            "name": "1.3 Chemical and physical sciences"
        },
        {
            "count": 4217,
            "id": "10505",
            "name": "5.5 Radiotherapy"
        },
        {
            "count": 3911,
            "id": "10206",
            "name": "2.6 Resources and infrastructure (aetiology)"
        },
        {
            "count": 3272,
            "id": "10105",
            "name": "1.5 Resources and infrastructure (underpinning)"
        },
        {
            "count": 2091,
            "id": "10104",
            "name": "1.4 Methodologies and measurements"
        },
        {
            "count": 1820,
            "id": "10305",
            "name": "3.5 Resources and infrastructure (prevention)"
        },
        {
            "count": 1150,
            "id": "10609",
            "name": "6.9 Resources and infrastructure (evaluation of treatments)"
        },
        {
            "count": 1018,
            "id": "10405",
            "name": "4.5 Resources and infrastructure (detection)"
        },
        {
            "count": 998,
            "id": "10506",
            "name": "5.6 Psychological and behavioural"
        },
        {
            "count": 983,
            "id": "10403",
            "name": "4.3 Influences and impact"
        },
        {
            "count": 448,
            "id": "10608",
            "name": "6.8 Complementary"
        },
        {
            "count": 374,
            "id": "10507",
            "name": "5.7 Physical"
        },
        {
            "count": 41,
            "id": "10805",
            "name": "8.5 Resources and infrastructure (health services)"
        },
        {
            "count": 2,
            "id": "10704",
            "name": "7.4 Resources and infrastructure (disease management)"
        }
    ],
    "category_hrcs_hc": [
        {
            "count": 1993062,
            "id": "911",
            "name": "Cancer"
        },
        {
            "count": 1631954,
            "id": "894",
            "name": "Cardiovascular"
        },
        {
            "count": 1456546,
            "id": "898",
            "name": "Infection"
        },
        {
            "count": 1073124,
            "id": "890",
            "name": "Generic Health Relevance"
        },
        {
            "count": 920146,
            "id": "897",
            "name": "Neurological"
        },
        {
            "count": 802034,
            "id": "905",
            "name": "Mental Health"
        },
        {
            "count": 610840,
            "id": "906",
            "name": "Metabolic and Endocrine"
        },
        {
            "count": 564794,
            "id": "903",
            "name": "Inflammatory and Immune System"
        },
        {
            "count": 553507,
            "id": "908",
            "name": "Reproductive Health and Childbirth"
        },
        {
            "count": 534806,
            "id": "899",
            "name": "Oral and Gastrointestinal"
        },
        {
            "count": 508497,
            "id": "900",
            "name": "Musculoskeletal"
        },
        {
            "count": 333324,
            "id": "907",
            "name": "Renal and Urogenital"
        },
        {
            "count": 329426,
            "id": "896",
            "name": "Respiratory"
        },
        {
            "count": 239268,
            "id": "909",
            "name": "Stroke"
        },
        {
            "count": 216912,
            "id": "895",
            "name": "Eye"
        },
        {
            "count": 158148,
            "id": "904",
            "name": "Injuries and Accidents"
        },
        {
            "count": 106998,
            "id": "891",
            "name": "Skin"
        },
        {
            "count": 60363,
            "id": "901",
            "name": "Congenital Disorders"
        },
        {
            "count": 56561,
            "id": "902",
            "name": "Ear"
        },
        {
            "count": 52556,
            "id": "892",
            "name": "Blood"
        },
        {
            "count": 11910,
            "id": "910",
            "name": "Other"
        }
    ],
    "category_hra": [
        {
            "count": 5839488,
            "id": "3900",
            "name": "Biomedical"
        },
        {
            "count": 4963490,
            "id": "3901",
            "name": "Clinical"
        },
        {
            "count": 1291542,
            "id": "3903",
            "name": "Population & Society"
        },
        {
            "count": 860794,
            "id": "3902",
            "name": "Health services & systems"
        }
    ],
    "category_bra": [
        {
            "count": 7217489,
            "id": "4001",
            "name": "Clinical Medicine and Science"
        },
        {
            "count": 4086209,
            "id": "4000",
            "name": "Basic Science"
        },
        {
            "count": 1165190,
            "id": "4003",
            "name": "Public Health"
        },
        {
            "count": 458177,
            "id": "4002",
            "name": "Health Services Research"
        }
    ],
    "category_for": [
        {
            "count": 25778454,
            "id": "2211",
            "name": "11 Medical and Health Sciences"
        },
        {
            "count": 10516989,
            "id": "2209",
            "name": "09 Engineering"
        },
        {
            "count": 9203750,
            "id": "3053",
            "name": "1103 Clinical Sciences"
        },
        {
            "count": 8103410,
            "id": "2206",
            "name": "06 Biological Sciences"
        },
        {
            "count": 7183561,
            "id": "2203",
            "name": "03 Chemical Sciences"
        },
        {
            "count": 5735050,
            "id": "2202",
            "name": "02 Physical Sciences"
        },
        {
            "count": 4460429,
            "id": "2201",
            "name": "01 Mathematical Sciences"
        },
        {
            "count": 4407004,
            "id": "2208",
            "name": "08 Information and Computing Sciences"
        },
        {
            "count": 4123089,
            "id": "3177",
            "name": "1117 Public Health and Health Services"
        },
        {
            "count": 3316164,
            "id": "2217",
            "name": "17 Psychology and Cognitive Sciences"
        },
        {
            "count": 3083175,
            "id": "2921",
            "name": "0912 Materials Engineering"
        },
        {
            "count": 2914925,
            "id": "2471",
            "name": "0306 Physical Chemistry (incl. Structural)"
        },
        {
            "count": 2859140,
            "id": "2581",
            "name": "0601 Biochemistry and Cell Biology"
        },
        {
            "count": 2682874,
            "id": "2216",
            "name": "16 Studies in Human Society"
        },
        {
            "count": 2457529,
            "id": "3468",
            "name": "1701 Psychology"
        },
        {
            "count": 2390866,
            "id": "3120",
            "name": "1109 Neurosciences"
        },
        {
            "count": 2313315,
            "id": "2746",
            "name": "0801 Artificial Intelligence and Image Processing"
        },
        {
            "count": 2263912,
            "id": "3048",
            "name": "1102 Cardiorespiratory Medicine and Haematology"
        },
        {
            "count": 1913932,
            "id": "2220",
            "name": "20 Language, Communication and Culture"
        },
        {
            "count": 1909259,
            "id": "3142",
            "name": "1112 Oncology and Carcinogenesis"
        },
        {
            "count": 1851145,
            "id": "2207",
            "name": "07 Agricultural and Veterinary Sciences"
        },
        {
            "count": 1810707,
            "id": "2204",
            "name": "04 Earth Sciences"
        },
        {
            "count": 1695157,
            "id": "2221",
            "name": "21 History and Archaeology"
        },
        {
            "count": 1686771,
            "id": "2620",
            "name": "0604 Genetics"
        },
        {
            "count": 1685238,
            "id": "2330",
            "name": "0101 Pure Mathematics"
        },
        {
            "count": 1610939,
            "id": "2210",
            "name": "10 Technology"
        },
        {
            "count": 1482270,
            "id": "2867",
            "name": "0906 Electrical and Electronic Engineering"
        },
        {
            "count": 1475153,
            "id": "2215",
            "name": "15 Commerce, Management, Tourism and Services"
        },
        {
            "count": 1454065,
            "id": "2421",
            "name": "0299 Other Physical Sciences"
        },
        {
            "count": 1451514,
            "id": "2213",
            "name": "13 Education"
        },
        {
            "count": 1401999,
            "id": "3675",
            "name": "2103 Historical Studies"
        },
        {
            "count": 1391768,
            "id": "3158",
            "name": "1114 Paediatrics and Reproductive Medicine"
        },
        {
            "count": 1390528,
            "id": "2214",
            "name": "14 Economics"
        },
        {
            "count": 1313414,
            "id": "2389",
            "name": "0202 Atomic, Molecular, Nuclear, Particle and Plasma Physics"
        },
        {
            "count": 1198971,
            "id": "2222",
            "name": "22 Philosophy and Religious Studies"
        },
        {
            "count": 1181174,
            "id": "2205",
            "name": "05 Environmental Sciences"
        },
        {
            "count": 1175049,
            "id": "3103",
            "name": "1107 Immunology"
        },
        {
            "count": 1089260,
            "id": "2790",
            "name": "0806 Information Systems"
        },
        {
            "count": 1050254,
            "id": "3164",
            "name": "1115 Pharmacology and Pharmaceutical Sciences"
        },
        {
            "count": 1020219,
            "id": "3292",
            "name": "1402 Applied Economics"
        },
        {
            "count": 1016796,
            "id": "2344",
            "name": "0102 Applied Mathematics"
        },
        {
            "count": 996582,
            "id": "3626",
            "name": "2005 Literary Studies"
        },
        {
            "count": 976222,
            "id": "2953",
            "name": "0915 Interdisciplinary Engineering"
        },
        {
            "count": 946002,
            "id": "2648",
            "name": "0607 Plant Biology"
        },
        {
            "count": 937408,
            "id": "3001",
            "name": "1005 Communications Technologies"
        },
        {
            "count": 906219,
            "id": "2844",
            "name": "0904 Chemical Engineering"
        },
        {
            "count": 882031,
            "id": "2377",
            "name": "0201 Astronomical and Space Sciences"
        },
        {
            "count": 880822,
            "id": "2856",
            "name": "0905 Civil Engineering"
        },
        {
            "count": 873634,
            "id": "2464",
            "name": "0305 Organic Chemistry"
        },
        {
            "count": 856978,
            "id": "2597",
            "name": "0602 Ecology"
        },
        {
            "count": 817545,
            "id": "3342",
            "name": "1503 Business and Management"
        },
        {
            "count": 809779,
            "id": "3268",
            "name": "1303 Specialist Studies In Education"
        },
        {
            "count": 788132,
            "id": "2438",
            "name": "0302 Inorganic Chemistry"
        },
        {
            "count": 777625,
            "id": "3484",
            "name": "1702 Cognitive Sciences"
        },
        {
            "count": 767507,
            "id": "3114",
            "name": "1108 Medical Microbiology"
        },
        {
            "count": 759134,
            "id": "2428",
            "name": "0301 Analytical Chemistry"
        },
        {
            "count": 752809,
            "id": "3432",
            "name": "1606 Political Science"
        },
        {
            "count": 752183,
            "id": "2509",
            "name": "0403 Geology"
        },
        {
            "count": 732917,
            "id": "2358",
            "name": "0104 Statistics"
        },
        {
            "count": 717304,
            "id": "3448",
            "name": "1608 Sociology"
        },
        {
            "count": 717147,
            "id": "3128",
            "name": "1110 Nursing"
        },
        {
            "count": 711579,
            "id": "2933",
            "name": "0913 Mechanical Engineering"
        },
        {
            "count": 680860,
            "id": "2486",
            "name": "0399 Other Chemical Sciences"
        },
        {
            "count": 651170,
            "id": "2447",
            "name": "0303 Macromolecular and Materials Chemistry"
        },
        {
            "count": 602973,
            "id": "2837",
            "name": "0903 Biomedical Engineering"
        },
        {
            "count": 587365,
            "id": "2634",
            "name": "0605 Microbiology"
        },
        {
            "count": 581263,
            "id": "2218",
            "name": "18 Law and Legal Studies"
        },
        {
            "count": 577386,
            "id": "2655",
            "name": "0608 Zoology"
        },
        {
            "count": 564949,
            "id": "3494",
            "name": "1801 Law"
        },
        {
            "count": 563884,
            "id": "3253",
            "name": "1302 Curriculum and Pedagogy"
        },
        {
            "count": 529033,
            "id": "3714",
            "name": "2203 Philosophy"
        },
        {
            "count": 495600,
            "id": "2558",
            "name": "0502 Environmental Science and Management"
        },
        {
            "count": 488081,
            "id": "3416",
            "name": "1605 Policy and Administration"
        },
        {
            "count": 483065,
            "id": "3616",
            "name": "2004 Linguistics"
        },
        {
            "count": 476079,
            "id": "2766",
            "name": "0803 Computer Software"
        },
        {
            "count": 467726,
            "id": "2456",
            "name": "0304 Medicinal and Biomolecular Chemistry"
        },
        {
            "count": 461587,
            "id": "2539",
            "name": "0406 Physical Geography and Environmental Geoscience"
        },
        {
            "count": 448145,
            "id": "2878",
            "name": "0907 Environmental Engineering"
        },
        {
            "count": 447376,
            "id": "2401",
            "name": "0204 Condensed Matter Physics"
        },
        {
            "count": 446883,
            "id": "2409",
            "name": "0205 Optical Physics"
        },
        {
            "count": 428069,
            "id": "2727",
            "name": "0707 Veterinary Sciences"
        },
        {
            "count": 427348,
            "id": "2219",
            "name": "19 Studies in Creative Arts and Writing"
        },
        {
            "count": 425377,
            "id": "2353",
            "name": "0103 Numerical and Computational Mathematics"
        },
        {
            "count": 421440,
            "id": "3153",
            "name": "1113 Ophthalmology and Optometry"
        },
        {
            "count": 418060,
            "id": "3735",
            "name": "2204 Religion and Religious Studies"
        },
        {
            "count": 415592,
            "id": "2944",
            "name": "0914 Resources Engineering and Extractive Metallurgy"
        },
        {
            "count": 412950,
            "id": "3577",
            "name": "2002 Cultural Studies"
        },
        {
            "count": 399440,
            "id": "2759",
            "name": "0802 Computation Theory and Mathematics"
        },
        {
            "count": 395771,
            "id": "3097",
            "name": "1106 Human Movement and Sports Science"
        },
        {
            "count": 383243,
            "id": "2690",
            "name": "0703 Crop and Pasture Production"
        },
        {
            "count": 381415,
            "id": "3172",
            "name": "1116 Medical Physiology"
        },
        {
            "count": 371724,
            "id": "3086",
            "name": "1105 Dentistry"
        },
        {
            "count": 366798,
            "id": "2212",
            "name": "12 Built Environment and Design"
        },
        {
            "count": 352120,
            "id": "2607",
            "name": "0603 Evolutionary Biology"
        },
        {
            "count": 346160,
            "id": "2415",
            "name": "0206 Quantum Physics"
        },
        {
            "count": 329082,
            "id": "2883",
            "name": "0908 Food Sciences"
        },
        {
            "count": 303990,
            "id": "2480",
            "name": "0307 Theoretical and Computational Chemistry"
        },
        {
            "count": 286009,
            "id": "3702",
            "name": "2202 History and Philosophy of Specific Fields"
        },
        {
            "count": 274236,
            "id": "2493",
            "name": "0401 Atmospheric Sciences"
        },
        {
            "count": 270570,
            "id": "3410",
            "name": "1604 Human Geography"
        },
        {
            "count": 253142,
            "id": "2503",
            "name": "0402 Geochemistry"
        },
        {
            "count": 252038,
            "id": "2571",
            "name": "0503 Soil Sciences"
        },
        {
            "count": 235565,
            "id": "3364",
            "name": "1505 Marketing"
        },
        {
            "count": 232293,
            "id": "2899",
            "name": "0910 Manufacturing Engineering"
        },
        {
            "count": 230077,
            "id": "3657",
            "name": "2101 Archaeology"
        },
        {
            "count": 226473,
            "id": "3389",
            "name": "1601 Anthropology"
        },
        {
            "count": 223619,
            "id": "3549",
            "name": "1904 Performing Arts and Creative Writing"
        },
        {
            "count": 222831,
            "id": "3335",
            "name": "1502 Banking, Finance and Investment"
        },
        {
            "count": 217407,
            "id": "2891",
            "name": "0909 Geomatic Engineering"
        },
        {
            "count": 209186,
            "id": "3039",
            "name": "1101 Medical Biochemistry and Metabolomics"
        },
        {
            "count": 207478,
            "id": "3313",
            "name": "1403 Econometrics"
        },
        {
            "count": 205583,
            "id": "2777",
            "name": "0804 Data Format"
        },
        {
            "count": 203662,
            "id": "2681",
            "name": "0702 Animal Production"
        },
        {
            "count": 203186,
            "id": "2525",
            "name": "0404 Geophysics"
        },
        {
            "count": 199918,
            "id": "3136",
            "name": "1111 Nutrition and Dietetics"
        },
        {
            "count": 194217,
            "id": "3460",
            "name": "1699 Other Studies In Human Society"
        },
        {
            "count": 192246,
            "id": "3021",
            "name": "1007 Nanotechnology"
        },
        {
            "count": 185508,
            "id": "2534",
            "name": "0405 Oceanography"
        },
        {
            "count": 161813,
            "id": "2395",
            "name": "0203 Classical Physics"
        },
        {
            "count": 156708,
            "id": "2642",
            "name": "0606 Physiology"
        },
        {
            "count": 155471,
            "id": "3591",
            "name": "2003 Language Studies"
        },
        {
            "count": 153128,
            "id": "2820",
            "name": "0901 Aerospace Engineering"
        },
        {
            "count": 149166,
            "id": "3443",
            "name": "1607 Social Work"
        },
        {
            "count": 148579,
            "id": "2720",
            "name": "0706 Horticultural Production"
        },
        {
            "count": 146221,
            "id": "2806",
            "name": "0807 Library and Information Studies"
        },
        {
            "count": 146018,
            "id": "2708",
            "name": "0705 Forestry Sciences"
        },
        {
            "count": 133660,
            "id": "2552",
            "name": "0501 Ecological Applications"
        },
        {
            "count": 130749,
            "id": "3230",
            "name": "1205 Urban and Regional Planning"
        },
        {
            "count": 130367,
            "id": "3197",
            "name": "1199 Other Medical and Health Sciences"
        },
        {
            "count": 127476,
            "id": "3243",
            "name": "1301 Education Systems"
        },
        {
            "count": 127292,
            "id": "2700",
            "name": "0704 Fisheries Sciences"
        },
        {
            "count": 121308,
            "id": "2366",
            "name": "0105 Mathematical Physics"
        },
        {
            "count": 116918,
            "id": "3403",
            "name": "1603 Demography"
        },
        {
            "count": 112406,
            "id": "3395",
            "name": "1602 Criminology"
        },
        {
            "count": 110597,
            "id": "3570",
            "name": "2001 Communication and Media Studies"
        },
        {
            "count": 106196,
            "id": "2913",
            "name": "0911 Maritime Engineering"
        },
        {
            "count": 100125,
            "id": "3373",
            "name": "1506 Tourism"
        },
        {
            "count": 89877,
            "id": "3326",
            "name": "1501 Accounting, Auditing and Accountability"
        },
        {
            "count": 86730,
            "id": "3286",
            "name": "1401 Economic Theory"
        },
        {
            "count": 84952,
            "id": "3209",
            "name": "1202 Building"
        },
        {
            "count": 82032,
            "id": "3079",
            "name": "1104 Complementary and Alternative Medicine"
        },
        {
            "count": 77019,
            "id": "2783",
            "name": "0805 Distributed Computing"
        },
        {
            "count": 72399,
            "id": "2995",
            "name": "1004 Medical Biotechnology"
        },
        {
            "count": 71811,
            "id": "2671",
            "name": "0701 Agriculture, Land and Farm Management"
        },
        {
            "count": 69757,
            "id": "3693",
            "name": "2201 Applied Ethics"
        },
        {
            "count": 69686,
            "id": "3200",
            "name": "1201 Architecture"
        },
        {
            "count": 69113,
            "id": "3358",
            "name": "1504 Commercial Services"
        },
        {
            "count": 68713,
            "id": "3537",
            "name": "1902 Film, Television and Digital Media"
        },
        {
            "count": 67234,
            "id": "3531",
            "name": "1901 Art Theory and Criticism"
        },
        {
            "count": 63182,
            "id": "3214",
            "name": "1203 Design Practice and Management"
        },
        {
            "count": 56894,
            "id": "2987",
            "name": "1003 Industrial Biotechnology"
        },
        {
            "count": 56543,
            "id": "3669",
            "name": "2102 Curatorial and Related Studies"
        },
        {
            "count": 54928,
            "id": "2666",
            "name": "0699 Other Biological Sciences"
        },
        {
            "count": 53602,
            "id": "3381",
            "name": "1507 Transportation and Freight Services"
        },
        {
            "count": 47276,
            "id": "3544",
            "name": "1903 Journalism and Professional Writing"
        },
        {
            "count": 44855,
            "id": "2817",
            "name": "0899 Other Information and Computing Sciences"
        },
        {
            "count": 36989,
            "id": "3013",
            "name": "1006 Computer Hardware"
        },
        {
            "count": 35739,
            "id": "3561",
            "name": "1905 Visual Arts and Crafts"
        },
        {
            "count": 34187,
            "id": "3320",
            "name": "1499 Other Economics"
        },
        {
            "count": 26503,
            "id": "2830",
            "name": "0902 Automotive Engineering"
        },
        {
            "count": 19415,
            "id": "2963",
            "name": "0999 Other Engineering"
        },
        {
            "count": 18971,
            "id": "3283",
            "name": "1399 Other Education"
        },
        {
            "count": 18317,
            "id": "2968",
            "name": "1001 Agricultural Biotechnology"
        },
        {
            "count": 16916,
            "id": "2741",
            "name": "0799 Other Agricultural and Veterinary Sciences"
        },
        {
            "count": 16750,
            "id": "3036",
            "name": "1099 Other Technology"
        },
        {
            "count": 15461,
            "id": "2979",
            "name": "1002 Environmental Biotechnology"
        },
        {
            "count": 14837,
            "id": "3690",
            "name": "2199 Other History and Archaeology"
        },
        {
            "count": 7876,
            "id": "3654",
            "name": "2099 Other Language, Communication and Culture"
        },
        {
            "count": 5693,
            "id": "2549",
            "name": "0499 Other Earth Sciences"
        },
        {
            "count": 3186,
            "id": "3491",
            "name": "1799 Other Psychology and Cognitive Sciences"
        },
        {
            "count": 2877,
            "id": "3528",
            "name": "1899 Other Law and Legal Studies"
        },
        {
            "count": 2482,
            "id": "3567",
            "name": "1999 Other Studies In Creative Arts and Writing"
        },
        {
            "count": 730,
            "id": "3744",
            "name": "2299 Other Philosophy and Religious Studies"
        },
        {
            "count": 644,
            "id": "2578",
            "name": "0599 Other Environmental Sciences"
        },
        {
            "count": 237,
            "id": "3240",
            "name": "1299 Other Built Environment and Design"
        }
    ]
}
