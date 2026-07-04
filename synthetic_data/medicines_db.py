# Indian Medicines Database
# Organized by therapeutic category
# Each entry: generic_name, brands (Indian), forms, strengths, category

MEDICINES = {
    # ============================================================
    # ANALGESICS / ANTIPYRETICS
    # ============================================================
    "paracetamol": {
        "generic": "Paracetamol",
        "brands": ["Crocin", "Dolo", "Calpol", "Dolopar", "Febrex", "P-250", "Pyrigesic", "Mahadol"],
        "forms": ["Tab", "Syr", "Susp", "Drops", "Inj"],
        "strengths": ["500mg", "650mg", "1g", "125mg/5ml", "250mg/5ml", "15mg/ml"],
        "category": "analgesic_antipyretic"
    },
    "ibuprofen": {
        "generic": "Ibuprofen",
        "brands": ["Brufen", "Ibugesic", "Ibuprofen", "Brufen-400", "Endolac"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["200mg", "400mg", "600mg", "800mg", "100mg/5ml"],
        "category": "nsaid"
    },
    "diclofenac": {
        "generic": "Diclofenac",
        "brands": ["Voveran", "Volini", "Diclomol", "Diclofenac", "Dolonex"],
        "forms": ["Tab", "Inj", "Gel", "Spray"],
        "strengths": ["50mg", "100mg", "75mg/3ml", "1%"],
        "category": "nsaid"
    },
    "aceclofenac": {
        "generic": "Aceclofenac",
        "brands": ["Aceclo", "Hifenac", "Zerodol", "Aceclofenac", "Dolokind"],
        "forms": ["Tab"],
        "strengths": ["100mg", "200mg"],
        "category": "nsaid"
    },
    "naproxen": {
        "generic": "Naproxen",
        "brands": ["Naprosyn", "Naproxen", "Naxen", "Xenobid"],
        "forms": ["Tab"],
        "strengths": ["250mg", "500mg"],
        "category": "nsaid"
    },
    "mefenamic_acid": {
        "generic": "Mefenamic Acid",
        "brands": ["Meftal", "Meftal-Spas", "Mefkind", "Mefenamic Acid", "Mefthil"],
        "forms": ["Tab", "Syr"],
        "strengths": ["250mg", "500mg", "50mg/5ml"],
        "category": "nsaid"
    },
    "nimesulide": {
        "generic": "Nimesulide",
        "brands": ["Nise", "Nimica", "Nimesulide", "Nimegesic", "Niltop"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["100mg", "50mg/5ml"],
        "category": "nsaid"
    },
    "aspirin": {
        "generic": "Aspirin",
        "brands": ["Aspirin", "Ecosprin", "Disprin", "Aspilet", "Loprin"],
        "forms": ["Tab"],
        "strengths": ["75mg", "150mg", "325mg", "500mg"],
        "category": "nsaid"
    },
    "tramadol": {
        "generic": "Tramadol",
        "brands": ["Tramadol", "Domadol", "Tramazac", "Tramal", "Ultramed"],
        "forms": ["Tab", "Inj", "Cap"],
        "strengths": ["50mg", "100mg", "50mg/ml"],
        "category": "analgesic_antipyretic"
    },
    "serratiopeptidase": {
        "generic": "Serratiopeptidase",
        "brands": ["Serratiopeptidase", "Serapeptase", "Serratio", "Seridase"],
        "forms": ["Tab"],
        "strengths": ["10mg"],
        "category": "enzyme"
    },
    "ketorolac": {
        "generic": "Ketorolac",
        "brands": ["Ketorolac", "Ketlur", "Ketanov", "Toroc"],
        "forms": ["Tab", "Inj", "Eye Drops"],
        "strengths": ["10mg", "30mg/ml", "0.5%"],
        "category": "nsaid"
    },

    # ============================================================
    # ANTIBIOTICS
    # ============================================================
    "amoxicillin": {
        "generic": "Amoxicillin",
        "brands": ["Novamox", "Mox", "Moxikind", "Amoxil", "Moxylife"],
        "forms": ["Tab", "Cap", "Syr", "Susp"],
        "strengths": ["250mg", "500mg", "125mg/5ml", "250mg/5ml"],
        "category": "antibiotic"
    },
    "azithromycin": {
        "generic": "Azithromycin",
        "brands": ["Azithral", "Azee", "Zithromax", "Azax", "Zady"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["250mg", "500mg", "100mg/5ml", "200mg/5ml"],
        "category": "antibiotic"
    },
    "cefixime": {
        "generic": "Cefixime",
        "brands": ["Taxim-O", "Cefolac", "Mahacef", "Oflox", "Cefixime"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["200mg", "400mg", "50mg/5ml", "100mg/5ml"],
        "category": "antibiotic"
    },
    "ceftriaxone": {
        "generic": "Ceftriaxone",
        "brands": ["Monocef", "Ceftriaxone", "Rocephin", "Cefonext", "Keftriaxone"],
        "forms": ["Inj"],
        "strengths": ["500mg", "1g", "2g"],
        "category": "antibiotic"
    },
    "cefuroxime": {
        "generic": "Cefuroxime",
        "brands": ["Ceftum", "Cefuroxime", "Cefurox", "Starcef"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["250mg", "500mg", "125mg/5ml", "250mg/5ml"],
        "category": "antibiotic"
    },
    "ciprofloxacin": {
        "generic": "Ciprofloxacin",
        "brands": ["Ciplox", "Cifran", "Ciprobid", "Ciprofloxacin", "Ciplox-TZ"],
        "forms": ["Tab", "Syr", "Eye Drops", "Ear Drops", "Cream"],
        "strengths": ["250mg", "500mg", "750mg", "100mg/5ml", "0.3%", "1%"],
        "category": "antibiotic"
    },
    "ofloxacin": {
        "generic": "Ofloxacin",
        "brands": ["Zanocin", "Tarivid", "Oflox", "Ofloxacin", "Zoflox"],
        "forms": ["Tab", "Syr", "Eye Drops", "Ear Drops"],
        "strengths": ["200mg", "400mg", "50mg/5ml", "100mg/5ml", "0.3%"],
        "category": "antibiotic"
    },
    "levofloxacin": {
        "generic": "Levofloxacin",
        "brands": ["Levaquin", "Levoflox", "Tavanic", "Leva", "Gleva"],
        "forms": ["Tab", "Inj"],
        "strengths": ["250mg", "500mg", "750mg"],
        "category": "antibiotic"
    },
    "doxycycline": {
        "generic": "Doxycycline",
        "brands": ["Doxycycline", "Vibramycin", "Doxt", "Doxt-S", "Doxypal"],
        "forms": ["Tab", "Cap"],
        "strengths": ["100mg"],
        "category": "antibiotic"
    },
    "metronidazole": {
        "generic": "Metronidazole",
        "brands": ["Flagyl", "Metrogyl", "Metron", "Metronidazole", "Metrogyl-400"],
        "forms": ["Tab", "Syr", "Susp", "Inj"],
        "strengths": ["200mg", "400mg", "200mg/5ml", "500mg/100ml"],
        "category": "antibiotic"
    },
    "norfloxacin": {
        "generic": "Norfloxacin",
        "brands": ["Norflox", "Urolex", "Norgutin", "Norfloxacin", "Norflet"],
        "forms": ["Tab"],
        "strengths": ["400mg"],
        "category": "antibiotic"
    },
    "clindamycin": {
        "generic": "Clindamycin",
        "brands": ["Dalacin", "Clin", "Clindamycin", "Clin-3", "Clindac-A"],
        "forms": ["Cap", "Inj", "Gel", "Cream"],
        "strengths": ["150mg", "300mg", "600mg/4ml", "1%"],
        "category": "antibiotic"
    },
    "erythromycin": {
        "generic": "Erythromycin",
        "brands": ["Erythrocin", "Althrocin", "Erythromycin", "Erycin", "Althrocin-500"],
        "forms": ["Tab", "Syr", "Susp", "Cream"],
        "strengths": ["250mg", "500mg", "125mg/5ml", "250mg/5ml", "2%"],
        "category": "antibiotic"
    },
    "cephalexin": {
        "generic": "Cephalexin",
        "brands": ["Sporidex", "Cephalexin", "Keflex", "Phexin", "Cephadex"],
        "forms": ["Cap", "Tab", "Syr", "Susp"],
        "strengths": ["250mg", "500mg", "125mg/5ml", "250mg/5ml"],
        "category": "antibiotic"
    },
    "meropenem": {
        "generic": "Meropenem",
        "brands": ["Meronem", "Mero", "Meromax", "Meropenem", "Meroza"],
        "forms": ["Inj"],
        "strengths": ["500mg", "1g"],
        "category": "antibiotic"
    },
    "vancomycin": {
        "generic": "Vancomycin",
        "brands": ["Vancocin", "Vancomycin", "Vancocin-CP", "Voncon"],
        "forms": ["Inj"],
        "strengths": ["500mg", "1g"],
        "category": "antibiotic"
    },
    "moxifloxacin": {
        "generic": "Moxifloxacin",
        "brands": ["Moxifloxacin", "Vigamox", "Moxi", "Avelox", "Moxiflox"],
        "forms": ["Tab", "Eye Drops", "Inj"],
        "strengths": ["400mg", "0.5%"],
        "category": "antibiotic"
    },
    "tobramycin": {
        "generic": "Tobramycin",
        "brands": ["Tobramycin", "Tobrex", "Tobaren", "Toba"],
        "forms": ["Eye Drops", "Inj"],
        "strengths": ["0.3%", "80mg/2ml"],
        "category": "antibiotic"
    },
    "chloramphenicol": {
        "generic": "Chloramphenicol",
        "brands": ["Chloramphenicol", "Chloromycetin", "Chlormycetin"],
        "forms": ["Eye Drops", "Eye Oint", "Cap"],
        "strengths": ["0.5%", "1%", "250mg", "500mg"],
        "category": "antibiotic"
    },

    # ============================================================
    # PPI / GI
    # ============================================================
    "pantoprazole": {
        "generic": "Pantoprazole",
        "brands": ["Pan", "Pantop", "Pantocid", "Pantoprazole", "Pantodac"],
        "forms": ["Tab", "Inj"],
        "strengths": ["20mg", "40mg"],
        "category": "ppi"
    },
    "omeprazole": {
        "generic": "Omeprazole",
        "brands": ["Ocid", "Omez", "Omeprazole", "Omezol", "Omitab"],
        "forms": ["Cap"],
        "strengths": ["20mg", "40mg"],
        "category": "ppi"
    },
    "rabeprazole": {
        "generic": "Rabeprazole",
        "brands": ["Rablet", "Rabicip", "Razo", "Rabeprazole", "Rabicip-LS"],
        "forms": ["Tab"],
        "strengths": ["20mg"],
        "category": "ppi"
    },
    "esomeprazole": {
        "generic": "Esomeprazole",
        "brands": ["Nexpro", "Esomeprazole", "Raciper", "Nexium", "Esomac"],
        "forms": ["Tab", "Inj"],
        "strengths": ["20mg", "40mg"],
        "category": "ppi"
    },
    "lansoprazole": {
        "generic": "Lansoprazole",
        "brands": ["Lanzol", "Lansoprazole", "Lanzol-30", "Lan-15"],
        "forms": ["Cap"],
        "strengths": ["15mg", "30mg"],
        "category": "ppi"
    },
    "ranitidine": {
        "generic": "Ranitidine",
        "brands": ["Rantac", "Aciloc", "Zinetac", "Ranitidine", "Aciloc-150"],
        "forms": ["Tab", "Inj", "Syr"],
        "strengths": ["150mg", "300mg", "50mg/2ml", "75mg/5ml"],
        "category": "antacid"
    },
    "famotidine": {
        "generic": "Famotidine",
        "brands": ["Famotidine", "Topcid", "Famocid", "Famotin"],
        "forms": ["Tab", "Inj"],
        "strengths": ["20mg", "40mg", "20mg/2ml"],
        "category": "antacid"
    },
    "domperidone": {
        "generic": "Domperidone",
        "brands": ["Domstal", "Domperidone", "Vomistop", "Domperidone", "Dombid"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["10mg", "5mg/5ml"],
        "category": "antiemetic"
    },
    "ondansetron": {
        "generic": "Ondansetron",
        "brands": ["Ondem", "Vomikind", "Emset", "Ondansetron", "Zofran"],
        "forms": ["Tab", "Inj", "Syr", "Susp"],
        "strengths": ["4mg", "8mg", "2mg/ml", "4mg/ml", "2mg/5ml"],
        "category": "antiemetic"
    },
    "metoclopramide": {
        "generic": "Metoclopramide",
        "brands": ["Perinorm", "Reglan", "Metoclopramide", "Perinorm-10"],
        "forms": ["Tab", "Inj", "Syr"],
        "strengths": ["5mg", "10mg", "5mg/ml", "10mg/ml", "5mg/5ml"],
        "category": "antiemetic"
    },
    "loperamide": {
        "generic": "Loperamide",
        "brands": ["Loperamide", "Eldoper", "Imodium", "Lopamide"],
        "forms": ["Cap", "Tab"],
        "strengths": ["2mg"],
        "category": "antidiarrheal"
    },
    "lactulose": {
        "generic": "Lactulose",
        "brands": ["Lactulose", "Duphalac", "Looz", "Livoset", "Duphalac"],
        "forms": ["Syr"],
        "strengths": ["10g/15ml", "3.35g/5ml"],
        "category": "laxative"
    },
    "bisacodyl": {
        "generic": "Bisacodyl",
        "brands": ["Bisacodyl", "Dulcolax", "Bisadyl", "Picolax"],
        "forms": ["Tab", "Supp"],
        "strengths": ["5mg", "10mg"],
        "category": "laxative"
    },
    "pancreatin": {
        "generic": "Pancreatin",
        "brands": ["Creon", "Pancreatin", "Pancreoflat", "Pankreom"],
        "forms": ["Cap"],
        "strengths": ["150mg", "10000IU", "25000IU", "40000IU"],
        "category": "enzyme"
    },
    "oral_rehydration_salts": {
        "generic": "Oral Rehydration Salts",
        "brands": ["ORS", "Electral", "ORS-200", "Walyte-ORS", "ORS-L"],
        "forms": ["Sachet", "Syr", "Susp"],
        "strengths": ["21.8g", "4.2g", "200ml"],
        "category": "supplement"
    },

    # ============================================================
    # ANTIHISTAMINES / COLD
    # ============================================================
    "cetirizine": {
        "generic": "Cetirizine",
        "brands": ["Cetzine", "Zirtzy", "Alerid", "Cetirizine", "Cetzine-10"],
        "forms": ["Tab", "Syr", "Susp", "Drops"],
        "strengths": ["5mg", "10mg", "5mg/5ml", "2.5mg/5ml"],
        "category": "antihistamine"
    },
    "levocetirizine": {
        "generic": "Levocetirizine",
        "brands": ["Xyzal", "Levocet", "Alerid-D", "Levocetirizine", "Lezyncet"],
        "forms": ["Tab", "Syr", "Susp", "Drops"],
        "strengths": ["5mg", "2.5mg/5ml", "1.25mg/5ml"],
        "category": "antihistamine"
    },
    "fexofenadine": {
        "generic": "Fexofenadine",
        "brands": ["Allegra", "Fexidine", "Fexofen", "Fexofenadine", "Alaspan"],
        "forms": ["Tab", "Susp"],
        "strengths": ["120mg", "180mg", "30mg/5ml"],
        "category": "antihistamine"
    },
    "chlorpheniramine": {
        "generic": "Chlorpheniramine",
        "brands": ["Piriton", "Cadistin", "Chlorpheniramine", "Cadistin-4"],
        "forms": ["Tab", "Syr", "Inj"],
        "strengths": ["4mg", "2mg/5ml", "10mg/ml"],
        "category": "antihistamine"
    },
    "pheniramine": {
        "generic": "Pheniramine",
        "brands": ["Avil", "Pheniramine", "Avil-25"],
        "forms": ["Tab", "Inj"],
        "strengths": ["25mg", "50mg", "22.75mg/ml"],
        "category": "antihistamine"
    },
    "promethazine": {
        "generic": "Promethazine",
        "brands": ["Phenergan", "Promethazine", "Phenergan-10", "Avomine"],
        "forms": ["Tab", "Syr", "Inj"],
        "strengths": ["10mg", "25mg", "5mg/5ml", "25mg/ml"],
        "category": "antihistamine"
    },
    "hydroxyzine": {
        "generic": "Hydroxyzine",
        "brands": ["Atarax", "Hydroxyzine", "Atarax-10", "Hyzine"],
        "forms": ["Tab", "Syr"],
        "strengths": ["10mg", "25mg", "2mg/5ml"],
        "category": "antihistamine"
    },
    "montelukast": {
        "generic": "Montelukast",
        "brands": ["Montek", "Montair", "Singulair", "Montelukast", "Montair-LC"],
        "forms": ["Tab", "Susp", "Chewable Tab"],
        "strengths": ["4mg", "5mg", "10mg"],
        "category": "antihistamine"
    },
    "loratadine": {
        "generic": "Loratadine",
        "brands": ["Loratadine", "Lomide", "Loridin", "Claritin"],
        "forms": ["Tab", "Syr"],
        "strengths": ["10mg", "5mg/5ml"],
        "category": "antihistamine"
    },
    "pseudoephedrine": {
        "generic": "Pseudoephedrine",
        "brands": ["Sudafed", "Pseudoephedrine", "Pseudocod", "Sudafed-12"],
        "forms": ["Tab", "Syr"],
        "strengths": ["30mg", "60mg", "120mg", "30mg/5ml"],
        "category": "antihistamine"
    },

    # ============================================================
    # ANTITUSSIVE / EXPECTORANT / COUGH
    # ============================================================
    "dextromethorphan": {
        "generic": "Dextromethorphan",
        "brands": ["Dex", "Benadryl", "Alex", "Dextromethorphan", "Dexorange"],
        "forms": ["Syr", "Susp"],
        "strengths": ["10mg/5ml", "15mg/5ml"],
        "category": "antitussive"
    },
    "guaifenesin": {
        "generic": "Guaifenesin",
        "brands": ["Guaifenesin", "Ascoril", "Guaifenesin", "Mucinex"],
        "forms": ["Syr", "Tab"],
        "strengths": ["100mg/5ml", "200mg", "100mg"],
        "category": "expectorant"
    },
    "ambroxol": {
        "generic": "Ambroxol",
        "brands": ["Ambroxol", "Mucolite", "Ambrolite", "Ambrodil"],
        "forms": ["Syr", "Tab", "Susp"],
        "strengths": ["30mg/5ml", "30mg", "15mg/5ml"],
        "category": "expectorant"
    },
    "bromhexine": {
        "generic": "Bromhexine",
        "brands": ["Bromhexine", "Bisolvon", "Bromhexine", "Mucobrom"],
        "forms": ["Syr", "Tab"],
        "strengths": ["4mg/5ml", "8mg/5ml", "8mg"],
        "category": "expectorant"
    },
    "terbutaline": {
        "generic": "Terbutaline",
        "brands": ["Terbutaline", "Bricanyl", "Terbutaline", "Bricarex"],
        "forms": ["Tab", "Syr", "Inj"],
        "strengths": ["2.5mg", "5mg", "1.5mg/5ml", "0.5mg/ml"],
        "category": "bronchodilator"
    },
    "salbutamol": {
        "generic": "Salbutamol",
        "brands": ["Asthalin", "Ventorlin", "Salbutamol", "Salbair", "Asthalin"],
        "forms": ["Tab", "Syr", "Inhaler", "Respule"],
        "strengths": ["2mg", "4mg", "2mg/5ml", "100mcg", "2.5mg/2.5ml", "5mg/ml"],
        "category": "bronchodilator"
    },
    "levosalbutamol": {
        "generic": "Levosalbutamol",
        "brands": ["Levolin", "Duolin", "Levosalbutamol", "Levair", "Levolin"],
        "forms": ["Inhaler", "Syr", "Respule"],
        "strengths": ["50mcg", "1.25mg/0.5ml", "1mg/5ml"],
        "category": "bronchodilator"
    },
    "ipratropium": {
        "generic": "Ipratropium",
        "brands": ["Ipratropium", "Duolin", "Ipravent", "Duonase"],
        "forms": ["Inhaler", "Respule"],
        "strengths": ["20mcg", "500mcg/2ml"],
        "category": "bronchodilator"
    },
    "budesonide": {
        "generic": "Budesonide",
        "brands": ["Budecort", "Foracort", "Entocort", "Budecort", "Budamate"],
        "forms": ["Inhaler", "Cap", "Respule"],
        "strengths": ["200mcg", "400mcg", "3mg", "0.5mg/2ml", "1mg/2ml"],
        "category": "steroid"
    },
    "tiotropium": {
        "generic": "Tiotropium",
        "brands": ["Tiotropium", "Tiova", "Tiotropium", "Spiriva"],
        "forms": ["Inhaler", "Cap"],
        "strengths": ["18mcg", "9mcg"],
        "category": "bronchodilator"
    },
    "codeine": {
        "generic": "Codeine",
        "brands": ["Codeine", "Corex", "Phensedyl", "Codeine", "Benadryl-Codeine"],
        "forms": ["Syr", "Tab"],
        "strengths": ["10mg/5ml", "15mg", "30mg"],
        "category": "antitussive"
    },
    "herbal_cough_syrups": {
        "generic": "Herbal Cough Syrups",
        "brands": ["Honitus", "Koflet", "Septilin", "Cofsils", "Strepsils", "TusQ"],
        "forms": ["Syr", "Lozenge", "Tab"],
        "strengths": ["5ml", "10ml", "2.5mg", "5mg"],
        "category": "antitussive"
    },

    # ============================================================
    # ANTIDIABETIC
    # ============================================================
    "metformin": {
        "generic": "Metformin",
        "brands": ["Glycomet", "Obimet", "Glucophage", "Metformin", "Glyciphage"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["500mg", "850mg", "1000mg", "500mg/5ml"],
        "category": "antidiabetic"
    },
    "glimepiride": {
        "generic": "Glimepiride",
        "brands": ["Amaryl", "Glimepiride", "Glimy", "Glimy-M", "Glimisave"],
        "forms": ["Tab"],
        "strengths": ["1mg", "2mg", "3mg", "4mg"],
        "category": "antidiabetic"
    },
    "gliclazide": {
        "generic": "Gliclazide",
        "brands": ["Diamicron", "Gliclazide", "Glyzid", "Reclide"],
        "forms": ["Tab"],
        "strengths": ["30mg", "60mg", "80mg"],
        "category": "antidiabetic"
    },
    "glibenclamide": {
        "generic": "Glibenclamide",
        "brands": ["Daonil", "Glibenclamide", "Glyburide", "Daonil-5"],
        "forms": ["Tab"],
        "strengths": ["5mg"],
        "category": "antidiabetic"
    },
    "pioglitazone": {
        "generic": "Pioglitazone",
        "brands": ["Piozone", "Pioglitazone", "Piozone", "P-Glar", "Piolin"],
        "forms": ["Tab"],
        "strengths": ["15mg", "30mg", "45mg"],
        "category": "antidiabetic"
    },
    "sitagliptin": {
        "generic": "Sitagliptin",
        "brands": ["Januvia", "Sitagliptin", "Istamet", "Januvia", "Sitagliptin"],
        "forms": ["Tab"],
        "strengths": ["50mg", "100mg"],
        "category": "antidiabetic"
    },
    "vildagliptin": {
        "generic": "Vildagliptin",
        "brands": ["Galvus", "Vildagliptin", "Galvus", "Vildaprex", "Vilda"],
        "forms": ["Tab"],
        "strengths": ["50mg"],
        "category": "antidiabetic"
    },
    "empagliflozin": {
        "generic": "Empagliflozin",
        "brands": ["Jardiance", "Empagliflozin", "Jardiance", "Empa", "Glyxambi"],
        "forms": ["Tab"],
        "strengths": ["10mg", "25mg"],
        "category": "antidiabetic"
    },
    "dapagliflozin": {
        "generic": "Dapagliflozin",
        "brands": ["Forxiga", "Dapagliflozin", "Forxiga", "Dapa", "Dapagard"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg"],
        "category": "antidiabetic"
    },
    "linagliptin": {
        "generic": "Linagliptin",
        "brands": ["Trajenta", "Linagliptin", "Trajenta", "Linagliptin", "Jentadueto"],
        "forms": ["Tab"],
        "strengths": ["5mg"],
        "category": "antidiabetic"
    },
    "acarbose": {
        "generic": "Acarbose",
        "brands": ["Glucobay", "Acarbose", "Glucobay", "Acarbo", "Rebose"],
        "forms": ["Tab"],
        "strengths": ["25mg", "50mg", "100mg"],
        "category": "antidiabetic"
    },
    "voglibose": {
        "generic": "Voglibose",
        "brands": ["Voglibose", "Volix", "Voglibose", "Vobose", "Volix"],
        "forms": ["Tab"],
        "strengths": ["0.2mg", "0.3mg"],
        "category": "antidiabetic"
    },
    "insulin_aspart": {
        "generic": "Insulin Aspart",
        "brands": ["NovoRapid", "NovoMix", "NovoRapid", "NovoMix-30", "Aspart"],
        "forms": ["Inj", "Cartridge", "Pen"],
        "strengths": ["100IU/ml", "40IU/ml"],
        "category": "antidiabetic"
    },
    "insulin_glargine": {
        "generic": "Insulin Glargine",
        "brands": ["Lantus", "Basalog", "Lantus", "Basalog", "Glaritus"],
        "forms": ["Inj", "Cartridge", "Pen"],
        "strengths": ["100IU/ml"],
        "category": "antidiabetic"
    },
    "insulin_regular": {
        "generic": "Insulin Regular",
        "brands": ["Actrapid", "Insugen", "Actrapid", "Insugen", "Wosulin"],
        "forms": ["Inj", "Vial", "Cartridge"],
        "strengths": ["40IU/ml", "100IU/ml"],
        "category": "antidiabetic"
    },
    "insulin_nph": {
        "generic": "Insulin NPH",
        "brands": ["Insulatard", "Insulin NPH", "Insulatard", "Huminsulin-N", "Insugen-N"],
        "forms": ["Inj", "Cartridge", "Pen"],
        "strengths": ["100IU/ml", "40IU/ml"],
        "category": "antidiabetic"
    },

    # ============================================================
    # ANTIHYPERTENSIVE / CARDIAC
    # ============================================================
    "amlodipine": {
        "generic": "Amlodipine",
        "brands": ["Amlodac", "Amlopress", "Amlip", "Amlodipine", "Amlong"],
        "forms": ["Tab"],
        "strengths": ["2.5mg", "5mg", "10mg"],
        "category": "antihypertensive"
    },
    "telmisartan": {
        "generic": "Telmisartan",
        "brands": ["Telma", "Tazloc", "Telmikaa", "Telmisartan", "Telma-AM"],
        "forms": ["Tab"],
        "strengths": ["20mg", "40mg", "80mg"],
        "category": "antihypertensive"
    },
    "losartan": {
        "generic": "Losartan",
        "brands": ["Losar", "Losartan", "Tozaar", "Losartan", "LTK"],
        "forms": ["Tab"],
        "strengths": ["25mg", "50mg", "100mg"],
        "category": "antihypertensive"
    },
    "olmesartan": {
        "generic": "Olmesartan",
        "brands": ["Olmez", "Olmesar", "Olmesartan", "Olmez", "Olsertain"],
        "forms": ["Tab"],
        "strengths": ["10mg", "20mg", "40mg"],
        "category": "antihypertensive"
    },
    "ramipril": {
        "generic": "Ramipril",
        "brands": ["Ramistar", "Cardace", "Ramipril", "Cardace", "Ramiril"],
        "forms": ["Tab", "Cap"],
        "strengths": ["2.5mg", "5mg", "10mg"],
        "category": "antihypertensive"
    },
    "enalapril": {
        "generic": "Enalapril",
        "brands": ["Envas", "Enalapril", "Envas", "Enam", "Enapril"],
        "forms": ["Tab"],
        "strengths": ["2.5mg", "5mg", "10mg"],
        "category": "antihypertensive"
    },
    "lisinopril": {
        "generic": "Lisinopril",
        "brands": ["Listril", "Lisinopril", "Listril", "Lipril", "Lisinopril"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg", "20mg"],
        "category": "antihypertensive"
    },
    "metoprolol": {
        "generic": "Metoprolol",
        "brands": ["Metolar", "Seloken", "Betaloc", "Metoprolol", "Metolar-XL"],
        "forms": ["Tab"],
        "strengths": ["25mg", "50mg", "100mg"],
        "category": "antihypertensive"
    },
    "atenolol": {
        "generic": "Atenolol",
        "brands": ["Aten", "Atenolol", "Tenormin", "Atenolol", "Aten-50"],
        "forms": ["Tab"],
        "strengths": ["25mg", "50mg", "100mg"],
        "category": "antihypertensive"
    },
    "bisoprolol": {
        "generic": "Bisoprolol",
        "brands": ["Bisoprolol", "Concor", "Bisoprolol", "Concor", "Bisocar"],
        "forms": ["Tab"],
        "strengths": ["2.5mg", "5mg", "10mg"],
        "category": "antihypertensive"
    },
    "carvedilol": {
        "generic": "Carvedilol",
        "brands": ["Carca", "Carvedilol", "Carca", "Carvil", "Cardace"],
        "forms": ["Tab"],
        "strengths": ["3.125mg", "6.25mg", "12.5mg", "25mg"],
        "category": "cardiac"
    },
    "s_amlodipine": {
        "generic": "S-Amlodipine",
        "brands": ["S-amlodipine", "Asomex", "S-amlodipine", "Asomex", "S-Amlodac"],
        "forms": ["Tab"],
        "strengths": ["2.5mg", "5mg"],
        "category": "antihypertensive"
    },
    "hydrochlorothiazide": {
        "generic": "Hydrochlorothiazide",
        "brands": ["Hydrochlorothiazide", "Aquazide", "Hydrochlorothiazide", "Aquazide", "Hydrazide"],
        "forms": ["Tab"],
        "strengths": ["12.5mg", "25mg", "50mg"],
        "category": "diuretic"
    },
    "furosemide": {
        "generic": "Furosemide",
        "brands": ["Lasix", "Fruselac", "Furosemide", "Lasix", "Frusemide"],
        "forms": ["Tab", "Inj"],
        "strengths": ["20mg", "40mg", "80mg", "20mg/2ml"],
        "category": "diuretic"
    },
    "spironolactone": {
        "generic": "Spironolactone",
        "brands": ["Aldactone", "Spironolactone", "Aldactone", "Spironolactone", "Spironolactone"],
        "forms": ["Tab"],
        "strengths": ["25mg", "50mg", "100mg"],
        "category": "diuretic"
    },
    "torsemide": {
        "generic": "Torsemide",
        "brands": ["Dytor", "Torsemide", "Dytor", "Torsemide", "Tide"],
        "forms": ["Tab", "Inj"],
        "strengths": ["5mg", "10mg", "20mg", "10mg/ml"],
        "category": "diuretic"
    },
    "digoxin": {
        "generic": "Digoxin",
        "brands": ["Lanoxin", "Digoxin", "Lanoxin", "Digoxin", "Lanoxin-Ped"],
        "forms": ["Tab", "Inj"],
        "strengths": ["0.25mg", "0.5mg/2ml", "0.05mg/ml"],
        "category": "cardiac"
    },
    "nitroglycerin": {
        "generic": "Nitroglycerin",
        "brands": ["Nitrocontin", "Sorbitrate", "Nitrocontin", "Sorbitrate", "Angised"],
        "forms": ["Tab", "Spray", "Patch"],
        "strengths": ["2.6mg", "6.4mg", "0.4mg", "0.5mg"],
        "category": "cardiac"
    },
    "isosorbide_mononitrate": {
        "generic": "Isosorbide Mononitrate",
        "brands": ["Monotrate", "Ismo", "Monotrate", "Ismo", "Isomonit"],
        "forms": ["Tab"],
        "strengths": ["10mg", "20mg", "40mg", "60mg"],
        "category": "cardiac"
    },
    "clopidogrel": {
        "generic": "Clopidogrel",
        "brands": ["Clopitab", "Plavix", "Deplatt", "Clopidogrel", "Clopitab"],
        "forms": ["Tab"],
        "strengths": ["75mg", "150mg", "300mg"],
        "category": "anticoagulant"
    },
    "atorvastatin": {
        "generic": "Atorvastatin",
        "brands": ["Atorva", "Lipicure", "Atorvastatin", "Atorva", "Lipikind"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg", "20mg", "40mg", "80mg"],
        "category": "lipid_lowering"
    },
    "rosuvastatin": {
        "generic": "Rosuvastatin",
        "brands": ["Rosuvas", "Roseday", "Crestor", "Rosuvastatin", "Rosavel"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg", "20mg", "40mg"],
        "category": "lipid_lowering"
    },
    "fenofibrate": {
        "generic": "Fenofibrate",
        "brands": ["Fenolip", "Lipicard", "Fenofibrate", "Fenolip", "Fibator"],
        "forms": ["Tab", "Cap"],
        "strengths": ["145mg", "160mg", "200mg"],
        "category": "lipid_lowering"
    },
    "simvastatin": {
        "generic": "Simvastatin",
        "brands": ["Simvotin", "Simvastatin", "Simvotin", "Simvastatin", "Simlup"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg", "20mg", "40mg"],
        "category": "lipid_lowering"
    },
    "ezetimibe": {
        "generic": "Ezetimibe",
        "brands": ["Ezetimibe", "Ezetrol", "Ezetimibe", "Ezetrol", "Ezimibe"],
        "forms": ["Tab"],
        "strengths": ["10mg"],
        "category": "lipid_lowering"
    },

    # ============================================================
    # ANTICOAGULANT
    # ============================================================
    "warfarin": {
        "generic": "Warfarin",
        "brands": ["Warf", "Acitrom", "Warfarin", "Warf", "Uniwarfin"],
        "forms": ["Tab"],
        "strengths": ["1mg", "2mg", "3mg", "5mg"],
        "category": "anticoagulant"
    },
    "acenocoumarol": {
        "generic": "Acenocoumarol",
        "brands": ["Acitrom", "Acenocoumarol", "Acitrom", "Acenocoumarol", "Acitrom"],
        "forms": ["Tab"],
        "strengths": ["1mg", "2mg", "4mg"],
        "category": "anticoagulant"
    },
    "heparin": {
        "generic": "Heparin",
        "brands": ["Heparin", "Clexane", "Heparin", "Clexane", "Heparin"],
        "forms": ["Inj"],
        "strengths": ["5000IU/ml", "25000IU/5ml"],
        "category": "anticoagulant"
    },
    "enoxaparin": {
        "generic": "Enoxaparin",
        "brands": ["Clexane", "Lovenox", "Enoxaparin", "Clexane", "Lmwh"],
        "forms": ["Inj"],
        "strengths": ["20mg", "40mg", "60mg", "80mg"],
        "category": "anticoagulant"
    },

    # ============================================================
    # ANXIOLYTIC / SEDATIVE / ANTICONVULSANT
    # ============================================================
    "alprazolam": {
        "generic": "Alprazolam",
        "brands": ["Alprax", "Alzolam", "Restyl", "Alprazolam", "Trika"],
        "forms": ["Tab"],
        "strengths": ["0.25mg", "0.5mg", "1mg", "2mg"],
        "category": "anxiolytic"
    },
    "diazepam": {
        "generic": "Diazepam",
        "brands": ["Valium", "Calmpose", "Diazepam", "Valium", "Placidyl"],
        "forms": ["Tab", "Inj"],
        "strengths": ["2mg", "5mg", "10mg", "10mg/2ml"],
        "category": "anxiolytic"
    },
    "lorazepam": {
        "generic": "Lorazepam",
        "brands": ["Larpose", "Ativan", "Lorazepam", "Larpose", "Ativan"],
        "forms": ["Tab", "Inj"],
        "strengths": ["1mg", "2mg", "4mg/ml"],
        "category": "anxiolytic"
    },
    "clonazepam": {
        "generic": "Clonazepam",
        "brands": ["Rivotril", "Clonazepam", "Lonazep", "Rivotril", "Clonazepam"],
        "forms": ["Tab", "Susp", "Inj"],
        "strengths": ["0.25mg", "0.5mg", "1mg", "2mg", "1mg/ml"],
        "category": "anticonvulsant"
    },
    "zolpidem": {
        "generic": "Zolpidem",
        "brands": ["Zolfresh", "Zolpidem", "Ambien", "Zolfresh", "Zolpidem"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg"],
        "category": "anxiolytic"
    },
    "zopiclone": {
        "generic": "Zopiclone",
        "brands": ["Zopiclone", "Zunesta", "Zopiclone", "Zunesta", "Zopicon"],
        "forms": ["Tab"],
        "strengths": ["7.5mg", "3.75mg"],
        "category": "anxiolytic"
    },
    "gabapentin": {
        "generic": "Gabapentin",
        "brands": ["Gabantin", "Neurontin", "Gabapentin", "Gabantin", "Gabapin"],
        "forms": ["Cap", "Tab", "Syr"],
        "strengths": ["100mg", "300mg", "400mg", "600mg", "800mg", "250mg/5ml"],
        "category": "anticonvulsant"
    },
    "pregabalin": {
        "generic": "Pregabalin",
        "brands": ["Pregabalin", "Lyrica", "Pregalin", "Pregabalin", "Gabantin-Plus"],
        "forms": ["Cap", "Tab"],
        "strengths": ["75mg", "150mg", "300mg"],
        "category": "anticonvulsant"
    },
    "phenytoin": {
        "generic": "Phenytoin",
        "brands": ["Eptoin", "Phenytoin", "Eptoin", "Phenytoin", "Dilantin"],
        "forms": ["Tab", "Cap", "Inj", "Susp"],
        "strengths": ["100mg", "50mg", "50mg/ml", "30mg/5ml"],
        "category": "anticonvulsant"
    },
    "carbamazepine": {
        "generic": "Carbamazepine",
        "brands": ["Tegrital", "Mazetol", "Carbamazepine", "Tegrital", "Carbamazepine"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["100mg", "200mg", "400mg", "100mg/5ml"],
        "category": "anticonvulsant"
    },
    "valproate": {
        "generic": "Valproate",
        "brands": ["Valparin", "Encorate", "Valproate", "Valparin", "Encorate"],
        "forms": ["Tab", "Syr", "Susp", "Inj"],
        "strengths": ["200mg", "300mg", "500mg", "200mg/5ml", "100mg/ml"],
        "category": "anticonvulsant"
    },
    "levetiracetam": {
        "generic": "Levetiracetam",
        "brands": ["Levipil", "Keppra", "Levetiracetam", "Levipil", "Levetiracetam"],
        "forms": ["Tab", "Syr", "Inj"],
        "strengths": ["250mg", "500mg", "750mg", "1000mg", "100mg/ml"],
        "category": "anticonvulsant"
    },
    "lamotrigine": {
        "generic": "Lamotrigine",
        "brands": ["Lametec", "Lamictal", "Lamotrigine", "Lametec", "Lamictal"],
        "forms": ["Tab"],
        "strengths": ["25mg", "50mg", "100mg", "200mg"],
        "category": "anticonvulsant"
    },

    # ============================================================
    # THYROID
    # ============================================================
    "levothyroxine": {
        "generic": "Levothyroxine",
        "brands": ["Eltroxin", "Thyronorm", "Thyrox", "Levothyroxine", "Eltroxin"],
        "forms": ["Tab"],
        "strengths": ["25mcg", "50mcg", "75mcg", "88mcg", "100mcg", "125mcg", "150mcg", "200mcg"],
        "category": "thyroid"
    },
    "carbimazole": {
        "generic": "Carbimazole",
        "brands": ["Carbimazole", "Neo-Mercazole", "Carbimazole", "Neo-Mercazole", "Carbimazole"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg"],
        "category": "thyroid"
    },
    "methimazole": {
        "generic": "Methimazole",
        "brands": ["Methimazole", "Methimazole", "Thyrocab", "Methimazole", "Methimazole"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg"],
        "category": "thyroid"
    },
    "propylthiouracil": {
        "generic": "Propylthiouracil",
        "brands": ["Propylthiouracil", "PTU", "Propylthiouracil", "PTU", "Propylthiouracil"],
        "forms": ["Tab"],
        "strengths": ["50mg"],
        "category": "thyroid"
    },

    # ============================================================
    # VITAMINS / MINERALS / SUPPLEMENTS
    # ============================================================
    "cholecalciferol": {
        "generic": "Cholecalciferol",
        "brands": ["Calcimax", "D-Rise", "Calcirol", "Cholecalciferol", "Cipcal"],
        "forms": ["Cap", "Sachet", "Tab", "Susp", "Granules"],
        "strengths": ["60000IU", "1000IU", "600IU", "1000IU/ml"],
        "category": "vitamin"
    },
    "methylcobalamin": {
        "generic": "Methylcobalamin",
        "brands": ["Mecobal", "Neurobion", "Methycobal", "Methylcobalamin", "Nurokind"],
        "forms": ["Tab", "Inj", "Cap"],
        "strengths": ["500mcg", "1500mcg", "500mcg/ml", "1000mcg/ml"],
        "category": "vitamin"
    },
    "vitamin_c": {
        "generic": "Vitamin C",
        "brands": ["Celin", "Limcee", "Vitamin C", "Celin", "Chewcee"],
        "forms": ["Tab", "Chewable Tab"],
        "strengths": ["250mg", "500mg", "1000mg"],
        "category": "vitamin"
    },
    "folic_acid": {
        "generic": "Folic Acid",
        "brands": ["Folvite", "Folic Acid", "Folvite", "Folic Acid", "Fol5"],
        "forms": ["Tab"],
        "strengths": ["1mg", "5mg"],
        "category": "vitamin"
    },
    "zinc": {
        "generic": "Zinc",
        "brands": ["Zincovit", "Z&D", "C-Zine", "Zinc", "Zincovit"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["20mg", "50mg", "20mg/5ml", "10mg/5ml"],
        "category": "mineral"
    },
    "biotin": {
        "generic": "Biotin",
        "brands": ["Biotin", "Hairbless", "Biotin", "Hairbless", "Biotin-Plus"],
        "forms": ["Tab", "Cap"],
        "strengths": ["5mg", "10mg"],
        "category": "vitamin"
    },
    "glucosamine": {
        "generic": "Glucosamine",
        "brands": ["Glucosamine", "Jointace", "Glucosamine", "Jointace", "Cartigen"],
        "forms": ["Tab", "Cap"],
        "strengths": ["500mg", "750mg"],
        "category": "supplement"
    },
    "l_arginine": {
        "generic": "L-Arginine",
        "brands": ["Argipreg", "L-Arginine", "Argipreg", "L-Arginine", "Arginine"],
        "forms": ["Sachet", "Tab", "Syr"],
        "strengths": ["5g", "100mg", "100mg/ml"],
        "category": "supplement"
    },

    # ============================================================
    # STEROIDS / IMMUNOSUPPRESSANTS
    # ============================================================
    "prednisolone": {
        "generic": "Prednisolone",
        "brands": ["Wysolone", "Prednisolone", "Omnacortil", "Wysolone", "Omnacortil"],
        "forms": ["Tab", "Syr", "Susp", "Inj"],
        "strengths": ["5mg", "10mg", "20mg", "5mg/5ml", "20mg/ml"],
        "category": "steroid"
    },
    "dexamethasone": {
        "generic": "Dexamethasone",
        "brands": ["Dexamethasone", "Decadron", "Wymesone", "Dexamethasone", "Decadron"],
        "forms": ["Tab", "Inj", "Eye Drops", "Ear Drops"],
        "strengths": ["0.5mg", "4mg", "4mg/ml", "0.1%"],
        "category": "steroid"
    },
    "methylprednisolone": {
        "generic": "Methylprednisolone",
        "brands": ["Solu-Medrol", "Depo-Medrol", "Methylprednisolone", "Solu-Medrol", "Depo-Medrol"],
        "forms": ["Inj", "Tab"],
        "strengths": ["40mg", "125mg", "500mg", "1g", "4mg", "16mg"],
        "category": "steroid"
    },
    "hydrocortisone": {
        "generic": "Hydrocortisone",
        "brands": ["Hydrocortisone", "Wycort", "Hydrocortisone", "Wycort", "Locoid"],
        "forms": ["Tab", "Inj", "Cream", "Lotion"],
        "strengths": ["10mg", "20mg", "100mg", "1%"],
        "category": "steroid"
    },
    "betamethasone": {
        "generic": "Betamethasone",
        "brands": ["Betnesol", "Betnelan", "Betamethasone", "Betnesol", "Betnelan"],
        "forms": ["Tab", "Inj", "Cream", "Drops"],
        "strengths": ["0.5mg", "1mg", "4mg/ml", "0.1%"],
        "category": "steroid"
    },
    "deflazacort": {
        "generic": "Deflazacort",
        "brands": ["Defcort", "Deflazacort", "Defcort", "Deflazacort", "Defza"],
        "forms": ["Tab", "Syr"],
        "strengths": ["6mg", "30mg", "6mg/5ml"],
        "category": "steroid"
    },
    "triamcinolone": {
        "generic": "Triamcinolone",
        "brands": ["Tricort", "Kenacort", "Triamcinolone", "Tricort", "Kenacort"],
        "forms": ["Inj", "Cream", "Dental Paste"],
        "strengths": ["40mg/ml", "0.1%"],
        "category": "steroid"
    },

    # ============================================================
    # ANTIFUNGAL
    # ============================================================
    "fluconazole": {
        "generic": "Fluconazole",
        "brands": ["Fluka", "Zocon", "Fluconazole", "Fluka", "Zocon"],
        "forms": ["Tab", "Syr", "Susp", "Inj"],
        "strengths": ["50mg", "100mg", "150mg", "200mg", "50mg/5ml", "200mg/100ml"],
        "category": "antifungal"
    },
    "itraconazole": {
        "generic": "Itraconazole",
        "brands": ["Sporanox", "Itaspor", "Canditral", "Itraconazole", "Sporanox"],
        "forms": ["Cap", "Syr", "Susp"],
        "strengths": ["100mg", "200mg", "10mg/ml"],
        "category": "antifungal"
    },
    "ketoconazole": {
        "generic": "Ketoconazole",
        "brands": ["Ketoconazole", "Nizoral", "Ketoconazole", "Nizoral", "Scalpe"],
        "forms": ["Tab", "Cream", "Shampoo", "Susp"],
        "strengths": ["200mg", "2%", "1%"],
        "category": "antifungal"
    },
    "clotrimazole": {
        "generic": "Clotrimazole",
        "brands": ["Clotrimazole", "Candid", "Clotrimazole", "Candid", "Candid-V"],
        "forms": ["Cream", "Powder", "Mouth Paint", "Vaginal Tab", "Drops"],
        "strengths": ["1%", "2%", "100mg", "500mg", "1%"],
        "category": "antifungal"
    },
    "terbinafine": {
        "generic": "Terbinafine",
        "brands": ["Terbinafine", "Lamisil", "Sebifin", "Terbinafine", "Lamisil"],
        "forms": ["Tab", "Cream", "Spray", "Powder"],
        "strengths": ["250mg", "1%"],
        "category": "antifungal"
    },
    "griseofulvin": {
        "generic": "Griseofulvin",
        "brands": ["Griseofulvin", "Grisovin", "Griseofulvin", "Grisovin", "Grifulvin"],
        "forms": ["Tab", "Susp"],
        "strengths": ["125mg", "250mg", "500mg", "125mg/5ml"],
        "category": "antifungal"
    },
    "nystatin": {
        "generic": "Nystatin",
        "brands": ["Nystatin", "Candid-M", "Nystatin", "Candid-M", "Nystatin"],
        "forms": ["Mouth Paint", "Tab", "Susp", "Cream"],
        "strengths": ["100000IU", "500000IU", "100000IU/ml", "1%"],
        "category": "antifungal"
    },

    # ============================================================
    # ANTIVIRAL
    # ============================================================
    "acyclovir": {
        "generic": "Acyclovir",
        "brands": ["Acyclovir", "Zovirax", "Acivir", "Acyclovir", "Zovirax"],
        "forms": ["Tab", "Cream", "Inj", "Eye Oint", "Susp"],
        "strengths": ["200mg", "400mg", "800mg", "5%", "250mg", "200mg/5ml"],
        "category": "antiviral"
    },
    "oseltamivir": {
        "generic": "Oseltamivir",
        "brands": ["Tamiflu", "Antiflu", "Fluvir", "Tamiflu", "Antiflu"],
        "forms": ["Cap", "Syr", "Susp"],
        "strengths": ["30mg", "45mg", "75mg", "12mg/ml"],
        "category": "antiviral"
    },
    "tenofovir": {
        "generic": "Tenofovir",
        "brands": ["Tenofovir", "Tenvir", "Tenofovir", "Tenvir", "Tenvir-EM"],
        "forms": ["Tab"],
        "strengths": ["300mg"],
        "category": "antiviral"
    },
    "entecavir": {
        "generic": "Entecavir",
        "brands": ["Entavir", "Entecavir", "Entavir", "Entecavir", "Entehep"],
        "forms": ["Tab", "Syr"],
        "strengths": ["0.5mg", "1mg", "0.05mg/ml"],
        "category": "antiviral"
    },

    # ============================================================
    # ANTHELMINTIC
    # ============================================================
    "albendazole": {
        "generic": "Albendazole",
        "brands": ["Albendazole", "Zentel", "Wormin", "Albendazole", "Zentel"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["400mg", "200mg/5ml", "400mg/10ml"],
        "category": "anthelmintic"
    },
    "mebendazole": {
        "generic": "Mebendazole",
        "brands": ["Mebendazole", "Wormin", "Mebex", "Mebendazole", "Mebex"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["100mg", "500mg", "100mg/5ml"],
        "category": "anthelmintic"
    },
    "ivermectin": {
        "generic": "Ivermectin",
        "brands": ["Ivermectin", "Ivermectol", "Scabover", "Ivermectin", "Ivermectol"],
        "forms": ["Tab", "Cream", "Lotion"],
        "strengths": ["3mg", "6mg", "12mg", "1%"],
        "category": "anthelmintic"
    },
    "praziquantel": {
        "generic": "Praziquantel",
        "brands": ["Praziquantel", "Distocide", "Praziquantel", "Distocide", "Praziquantel"],
        "forms": ["Tab"],
        "strengths": ["600mg"],
        "category": "anthelmintic"
    },
    "diethylcarbamazine": {
        "generic": "Diethylcarbamazine",
        "brands": ["Hetrazan", "Banocide", "Diethylcarbamazine", "Hetrazan", "Banocide"],
        "forms": ["Tab", "Syr"],
        "strengths": ["50mg", "100mg", "50mg/5ml"],
        "category": "anthelmintic"
    },

    # ============================================================
    # TOPICAL / OPHTHALMIC / OTIC
    # ============================================================
    "timolol": {
        "generic": "Timolol",
        "brands": ["Timolol", "Glucomol", "Timolol", "Glucomol", "Iotim"],
        "forms": ["Eye Drops"],
        "strengths": ["0.25%", "0.5%"],
        "category": "ophthalmic"
    },
    "brimonidine": {
        "generic": "Brimonidine",
        "brands": ["Brimonidine", "Alphagan", "Brimonidine", "Alphagan", "Brimodin"],
        "forms": ["Eye Drops"],
        "strengths": ["0.15%", "0.2%", "0.1%"],
        "category": "ophthalmic"
    },
    "latanoprost": {
        "generic": "Latanoprost",
        "brands": ["Latanoprost", "Xalatan", "Latanoprost", "Xalatan", "Latanoprost"],
        "forms": ["Eye Drops"],
        "strengths": ["0.005%"],
        "category": "ophthalmic"
    },
    "pilocarpine": {
        "generic": "Pilocarpine",
        "brands": ["Pilocar", "Pilocarpine", "Pilocar", "Pilocarpine", "Pilocar"],
        "forms": ["Eye Drops"],
        "strengths": ["1%", "2%", "4%"],
        "category": "ophthalmic"
    },
    "atropine": {
        "generic": "Atropine",
        "brands": ["Atropine", "Atrosulph", "Atropine", "Atrosulph", "Atropine"],
        "forms": ["Eye Drops", "Inj", "Tab"],
        "strengths": ["1%", "0.6mg/ml", "0.6mg"],
        "category": "ophthalmic"
    },
    "mupirocin": {
        "generic": "Mupirocin",
        "brands": ["Mupirocin", "T-Bact", "Mupirocin", "T-Bact", "Bactroban"],
        "forms": ["Oint", "Cream"],
        "strengths": ["2%"],
        "category": "topical"
    },
    "silver_sulfadiazine": {
        "generic": "Silver Sulfadiazine",
        "brands": ["Silvadene", "Silverex", "Silver Sulfadiazine", "Silvadene", "Silverex"],
        "forms": ["Cream"],
        "strengths": ["1%"],
        "category": "topical"
    },
    "calamine": {
        "generic": "Calamine",
        "brands": ["Calamine", "Lacto Calamine", "Calamine", "Lacto Calamine", "Calamine"],
        "forms": ["Lotion", "Cream"],
        "strengths": ["8%", "15%"],
        "category": "topical"
    },
    "benzoyl_peroxide": {
        "generic": "Benzoyl Peroxide",
        "brands": ["Benzac", "Perobar", "Benzoyl Peroxide", "Benzac", "Perobar"],
        "forms": ["Cream", "Gel", "Wash"],
        "strengths": ["2.5%", "5%", "10%"],
        "category": "topical"
    },
    "isotretinoin": {
        "generic": "Isotretinoin",
        "brands": ["Isotroin", "Sotret", "Accutane", "Isotroin", "Sotret"],
        "forms": ["Cap", "Tab"],
        "strengths": ["10mg", "20mg", "40mg"],
        "category": "topical"
    },
    "mometasone": {
        "generic": "Mometasone",
        "brands": ["Mometasone", "Elocon", "Momate", "Mometasone", "Elocon"],
        "forms": ["Cream", "Ointment", "Lotion", "Nasal Spray"],
        "strengths": ["0.1%"],
        "category": "topical"
    },
    "clobetasol": {
        "generic": "Clobetasol",
        "brands": ["Clobetasol", "Tenovate", "Lobate", "Clobetasol", "Tenovate"],
        "forms": ["Cream", "Ointment", "Lotion", "Gel"],
        "strengths": ["0.05%"],
        "category": "topical"
    },
    "fusidic_acid": {
        "generic": "Fusidic Acid",
        "brands": ["Fucidin", "Fusidic Acid", "Fucidin", "Fusidic Acid", "Fucidin"],
        "forms": ["Cream", "Ointment"],
        "strengths": ["2%"],
        "category": "topical"
    },

    # ============================================================
    # MISCELLANEOUS
    # ============================================================
    "colchicine": {
        "generic": "Colchicine",
        "brands": ["Colchicine", "Goutnil", "Colchicine", "Goutnil", "Colchicine"],
        "forms": ["Tab"],
        "strengths": ["0.5mg", "0.6mg"],
        "category": "antigout"
    },
    "allopurinol": {
        "generic": "Allopurinol",
        "brands": ["Zyloric", "Allopurinol", "Zyloric", "Allopurinol", "Zyloric"],
        "forms": ["Tab"],
        "strengths": ["100mg", "300mg"],
        "category": "antigout"
    },
    "febuxostat": {
        "generic": "Febuxostat",
        "brands": ["Feburic", "Febuxostat", "Feburic", "Febuxostat", "Feburic"],
        "forms": ["Tab"],
        "strengths": ["40mg", "80mg", "120mg"],
        "category": "antigout"
    },
    "probenecid": {
        "generic": "Probenecid",
        "brands": ["Probenecid", "Probenecid", "Probenecid", "Probenecid", "Probenecid"],
        "forms": ["Tab"],
        "strengths": ["500mg"],
        "category": "antigout"
    },
    "sildenafil": {
        "generic": "Sildenafil",
        "brands": ["Viagra", "Penegra", "Suhagra", "Sildenafil", "Manforce"],
        "forms": ["Tab"],
        "strengths": ["25mg", "50mg", "100mg"],
        "category": "urological"
    },
    "tadalafil": {
        "generic": "Tadalafil",
        "brands": ["Tadalafil", "Megalis", "Tadacip", "Tadalafil", "Megalis"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg", "20mg"],
        "category": "urological"
    },
    "modafinil": {
        "generic": "Modafinil",
        "brands": ["Modafinil", "Modalert", "Modafinil", "Modalert", "Provigil"],
        "forms": ["Tab"],
        "strengths": ["100mg", "200mg"],
        "category": "stimulant"
    },
    "oxybutynin": {
        "generic": "Oxybutynin",
        "brands": ["Oxybutynin", "Ditropan", "Oxybutynin", "Ditropan", "Oxybutynin"],
        "forms": ["Tab", "Syr"],
        "strengths": ["5mg", "1mg/ml"],
        "category": "urological"
    },
    "tamsulosin": {
        "generic": "Tamsulosin",
        "brands": ["Tamsulosin", "Urimax", "Contiflo", "Tamsulosin", "Urimax"],
        "forms": ["Cap", "Tab"],
        "strengths": ["0.4mg", "0.2mg"],
        "category": "urological"
    },
    "finasteride": {
        "generic": "Finasteride",
        "brands": ["Finasteride", "Finax", "Fincar", "Finasteride", "Finax"],
        "forms": ["Tab"],
        "strengths": ["1mg", "5mg"],
        "category": "urological"
    },
    "dutasteride": {
        "generic": "Dutasteride",
        "brands": ["Dutasteride", "Dutagen", "Dutasteride", "Dutagen", "Avodart"],
        "forms": ["Cap"],
        "strengths": ["0.5mg"],
        "category": "urological"
    },
    "pyridostigmine": {
        "generic": "Pyridostigmine",
        "brands": ["Pyridostigmine", "Distinon", "Pyridostigmine", "Distinon", "Mestinon"],
        "forms": ["Tab", "Syr"],
        "strengths": ["60mg", "12mg/ml"],
        "category": "neurological"
    },
    "baclofen": {
        "generic": "Baclofen",
        "brands": ["Baclofen", "Liofen", "Baclofen", "Liofen", "Baclof"],
        "forms": ["Tab", "Inj"],
        "strengths": ["5mg", "10mg", "25mg", "0.05mg/ml"],
        "category": "muscle_relaxant"
    },
    "thiocolchicoside": {
        "generic": "Thiocolchicoside",
        "brands": ["Thiocolchicoside", "Thiocolchicoside", "Thiocolchicoside", "Thiocolchicoside", "Thiocolchicoside"],
        "forms": ["Tab", "Inj", "Gel"],
        "strengths": ["4mg", "8mg", "4mg/ml", "0.25%"],
        "category": "muscle_relaxant"
    },
    "cyclobenzaprine": {
        "generic": "Cyclobenzaprine",
        "brands": ["Cyclobenzaprine", "Flexeril", "Cyclobenzaprine", "Flexeril", "Cyclobenzaprine"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg"],
        "category": "muscle_relaxant"
    },
    "donepezil": {
        "generic": "Donepezil",
        "brands": ["Donepezil", "Donep", "Aricept", "Donepezil", "Donep"],
        "forms": ["Tab"],
        "strengths": ["5mg", "10mg", "23mg"],
        "category": "neurological"
    },
    "rivastigmine": {
        "generic": "Rivastigmine",
        "brands": ["Rivastigmine", "Exelon", "Rivastigmine", "Exelon", "Rivamer"],
        "forms": ["Cap", "Patch", "Syr"],
        "strengths": ["1.5mg", "3mg", "4.5mg", "6mg", "2mg/ml"],
        "category": "neurological"
    },
    "memantine": {
        "generic": "Memantine",
        "brands": ["Memantine", "Admenta", "Memantine", "Admenta", "Namenda"],
        "forms": ["Tab", "Syr"],
        "strengths": ["5mg", "10mg", "2mg/ml"],
        "category": "neurological"
    },
    "misoprostol": {
        "generic": "Misoprostol",
        "brands": ["Misoprostol", "Misoclear", "Misoprostol", "Misoclear", "Cytolog"],
        "forms": ["Tab"],
        "strengths": ["200mcg"],
        "category": "gynecological"
    },
    "tranexamic_acid": {
        "generic": "Tranexamic Acid",
        "brands": ["Tranexamic Acid", "Pause", "Trenexa", "Tranexamic Acid", "Pause"],
        "forms": ["Tab", "Inj"],
        "strengths": ["500mg", "500mg/5ml", "1000mg/10ml"],
        "category": "hemostatic"
    },
    "ethamsylate": {
        "generic": "Ethamsylate",
        "brands": ["Ethamsylate", "Dicynene", "Ethamsylate", "Dicynene", "Ethamsylate"],
        "forms": ["Tab", "Inj"],
        "strengths": ["250mg", "500mg", "250mg/ml"],
        "category": "hemostatic"
    },
    "iv_fluids": {
        "generic": "IV Fluids",
        "brands": ["Dextrose", "Normal Saline", "Ringer Lactate", "Dextrose-Saline", "Dex-N"],
        "forms": ["IV", "Bottle"],
        "strengths": ["5%", "0.9%", "100ml", "500ml", "1000ml"],
        "category": "supplement"
    },
}


# Fixed Dose Combinations common in India
FDCS = {
    # ============================================================
    # ANTIBIOTIC FDCs
    # ============================================================
    "amoxicillin_clavulanate": {
        "components": ["Amoxicillin", "Clavulanic Acid"],
        "brands": ["Augmentin", "Moxclav", "Novamox-Clav", "Bactoclav", "Moxikind-CV"],
        "forms": ["Tab", "Syr", "Susp", "Inj"],
        "strengths": ["625mg", "228.5mg/5ml", "1g", "1.2g"],
        "category": "antibiotic"
    },
    "ofloxacin_ornidazole": {
        "components": ["Ofloxacin", "Ornidazole"],
        "brands": ["O2", "Zenflox-OZ", "Oflox-OZ", "Orni-O", "Oflomac-M"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["200/500mg", "50/125mg/5ml"],
        "category": "antibiotic"
    },
    "piperacillin_tazobactam": {
        "components": ["Piperacillin", "Tazobactam"],
        "brands": ["Piptaz", "Tazocin", "Piperacillin-Tazobactam", "Piptaz", "Tazocin"],
        "forms": ["Inj"],
        "strengths": ["4g/500mg", "2g/250mg"],
        "category": "antibiotic"
    },
    "cotrimoxazole": {
        "components": ["Sulfamethoxazole", "Trimethoprim"],
        "brands": ["Bactrim", "Septran", "Co-trimoxazole", "Bactrim", "Septran"],
        "forms": ["Tab", "Syr", "Susp", "Inj"],
        "strengths": ["400/80mg", "800/160mg", "200/40mg/5ml", "80/16mg/ml"],
        "category": "antibiotic"
    },
    "ivermectin_albendazole": {
        "components": ["Ivermectin", "Albendazole"],
        "brands": ["Ivermectol-ALB", "Ivermectin-Albendazole", "Albendazole-Ivermectin", "Ivermectol-ALB", "Wormin-Plus"],
        "forms": ["Tab"],
        "strengths": ["6/400mg", "12/400mg"],
        "category": "anthelmintic"
    },

    # ============================================================
    # ANALGESIC / NSAID FDCs
    # ============================================================
    "ibuprofen_paracetamol": {
        "components": ["Ibuprofen", "Paracetamol"],
        "brands": ["Combiflam", "Ibugesic-Plus", "Flexon", "Combiflam", "Ibugesic-Plus"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["400/325mg", "100/162.5mg/5ml", "325/100mg"],
        "category": "nsaid"
    },
    "diclofenac_paracetamol": {
        "components": ["Diclofenac", "Paracetamol"],
        "brands": ["Voveran-D", "Diclomol-Plus", "Signoflam", "Voveran-D", "Diclomol-Plus"],
        "forms": ["Tab", "Syr"],
        "strengths": ["50/325mg", "50/500mg"],
        "category": "nsaid"
    },
    "aceclofenac_paracetamol": {
        "components": ["Aceclofenac", "Paracetamol"],
        "brands": ["Zerodol-P", "Hifenac-P", "Ace-P", "Zerodol-P", "Hifenac-P"],
        "forms": ["Tab"],
        "strengths": ["100/325mg", "100/500mg"],
        "category": "nsaid"
    },
    "aceclofenac_paracetamol_serratiopeptidase": {
        "components": ["Aceclofenac", "Paracetamol", "Serratiopeptidase"],
        "brands": ["Zerodol-SP", "Signoflam", "Aceclo-SP", "Zerodol-SP", "Signoflam"],
        "forms": ["Tab"],
        "strengths": ["100/325/15mg", "100/500/15mg"],
        "category": "nsaid"
    },
    "tramadol_paracetamol": {
        "components": ["Tramadol", "Paracetamol"],
        "brands": ["Tramacet", "Domstal-Plus", "Tramazac-P", "Tramacet", "Domstal-Plus"],
        "forms": ["Tab", "Cap"],
        "strengths": ["37.5/325mg", "50/325mg"],
        "category": "analgesic_antipyretic"
    },
    "trypsin_chymotrypsin": {
        "components": ["Trypsin", "Chymotrypsin"],
        "brands": ["Chymoral", "Chymoral-Forte", "Chymotrypsin", "Chymoral", "Chymoral-Forte"],
        "forms": ["Tab"],
        "strengths": ["50000AU", "100000AU"],
        "category": "enzyme"
    },
    "trypsin_bromelain_rutoside": {
        "components": ["Trypsin", "Bromelain", "Rutoside"],
        "brands": ["Phlogam", "Rutoheal", "Trypsin-Bromelain-Rutoside", "Phlogam", "Rutoheal"],
        "forms": ["Tab"],
        "strengths": ["48/90/100mg"],
        "category": "enzyme"
    },
    "chlorzoxazone_ibuprofen_paracetamol": {
        "components": ["Chlorzoxazone", "Ibuprofen", "Paracetamol"],
        "brands": ["Flexon-MR", "Combiflam-MR", "Ibugesic-MR", "Flexon-MR", "Combiflam-MR"],
        "forms": ["Tab"],
        "strengths": ["250/400/325mg"],
        "category": "muscle_relaxant"
    },

    # ============================================================
    # PPI / GI FDCs
    # ============================================================
    "pantoprazole_domperidone": {
        "components": ["Pantoprazole", "Domperidone"],
        "brands": ["Pan-D", "Pantocid-DSR", "Pan-IT", "Pan-D", "Pantocid-DSR"],
        "forms": ["Cap", "Tab"],
        "strengths": ["40/30mg", "20/30mg"],
        "category": "ppi"
    },
    "rabeprazole_domperidone": {
        "components": ["Rabeprazole", "Domperidone"],
        "brands": ["Rablet-D", "Rabicip-DSR", "Razo-D", "Rablet-D", "Rabicip-DSR"],
        "forms": ["Cap", "Tab"],
        "strengths": ["20/30mg", "20/10mg"],
        "category": "ppi"
    },
    "pantoprazole_domperidone_itopride": {
        "components": ["Pantoprazole", "Domperidone", "Itopride"],
        "brands": ["PAN-IT", "Pantocid-IT", "Pantop-IT", "PAN-IT", "Pantocid-IT"],
        "forms": ["Cap", "Tab"],
        "strengths": ["40/30/50mg"],
        "category": "ppi"
    },
    "aluminum_hydroxide_magnesium_hydroxide_oxetacaine": {
        "components": ["Aluminum Hydroxide", "Magnesium Hydroxide", "Oxetacaine"],
        "brands": ["Mucaine", "Gelusil", "Mucaine", "Gelusil", "Acifix"],
        "forms": ["Syr", "Susp"],
        "strengths": ["0.291/0.98/0.2g/5ml"],
        "category": "antacid"
    },
    "aluminum_hydroxide_magnesium_hydroxide_simethicone": {
        "components": ["Aluminum Hydroxide", "Magnesium Hydroxide", "Simethicone"],
        "brands": ["Digene", "Gelusil", "Digene", "Gelusil", "Acidac"],
        "forms": ["Syr", "Tab", "Susp"],
        "strengths": ["200/200/20mg/5ml", "300/150/25mg"],
        "category": "antacid"
    },

    # ============================================================
    # ANTIHISTAMINE / COLD FDCs
    # ============================================================
    "levocetirizine_montelukast": {
        "components": ["Levocetirizine", "Montelukast"],
        "brands": ["Levomont", "Montek-LC", "Xyzal-M", "Levomont", "Montek-LC"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["5/10mg", "2.5/4mg", "2.5/5mg"],
        "category": "antihistamine"
    },
    "fexofenadine_pseudoephedrine": {
        "components": ["Fexofenadine", "Pseudoephedrine"],
        "brands": ["Allegra-D", "Fexidine-D", "Allegra-D", "Fexofen-D", "Alaspan-D"],
        "forms": ["Tab"],
        "strengths": ["120/60mg", "180/240mg"],
        "category": "antihistamine"
    },
    "pseudoephedrine_triprolidine": {
        "components": ["Pseudoephedrine", "Triprolidine"],
        "brands": ["Actifed", "Actifed-P", "Actifed", "Triprolidine-Pseudoephedrine", "Actifed"],
        "forms": ["Tab", "Syr"],
        "strengths": ["60/2.5mg", "30/1.25mg/5ml"],
        "category": "antihistamine"
    },
    "phenylephrine_chlorpheniramine_paracetamol": {
        "components": ["Phenylephrine", "Chlorpheniramine", "Paracetamol"],
        "brands": ["Cetcip-Cold", "Dolo-Cold", "Sinarest", "Cetcip-Cold", "Dolo-Cold"],
        "forms": ["Tab", "Syr", "Susp"],
        "strengths": ["5/2/500mg", "5/2/325mg"],
        "category": "antihistamine"
    },
    "caffeine_paracetamol_phenylephrine": {
        "components": ["Caffeine", "Paracetamol", "Phenylephrine"],
        "brands": ["Saridon", "Dolo-SOS", "Saridon", "Dolo-SOS", "Saridon"],
        "forms": ["Tab"],
        "strengths": ["32/250/5mg", "25/300/5mg"],
        "category": "analgesic_antipyretic"
    },

    # ============================================================
    # COUGH / COLD FDCs
    # ============================================================
    "dextromethorphan_chlorpheniramine_phenylephrine": {
        "components": ["Dextromethorphan", "Chlorpheniramine", "Phenylephrine"],
        "brands": ["Ascoril", "Alex", "Benadryl", "Ascoril", "Alex"],
        "forms": ["Syr", "Susp"],
        "strengths": ["10/2/5mg/5ml", "5/1/2.5mg/5ml"],
        "category": "antitussive"
    },
    "salbutamol_guaifenesin_bromhexine": {
        "components": ["Salbutamol", "Guaifenesin", "Bromhexine"],
        "brands": ["Ascoril", "Ambrolite", "Ascoril", "Ambrolite", "Cofdex"],
        "forms": ["Syr", "Susp"],
        "strengths": ["2/100/4mg/5ml", "1/50/2mg/5ml"],
        "category": "bronchodilator"
    },
    "formoterol_budesonide": {
        "components": ["Formoterol", "Budesonide"],
        "brands": ["Foracort", "Duolin", "Budecort", "Foracort", "Duolin"],
        "forms": ["Inhaler", "Rotacap", "Respule"],
        "strengths": ["6/200mcg", "6/400mcg", "4.5/160mcg"],
        "category": "bronchodilator"
    },

    # ============================================================
    # ANTIDIABETIC FDCs
    # ============================================================
    "glimepiride_metformin": {
        "components": ["Glimepiride", "Metformin"],
        "brands": ["Glycomet-GP", "Amaryl-M", "Glimy-M", "Glycomet-GP", "Amaryl-M"],
        "forms": ["Tab"],
        "strengths": ["1/500mg", "2/500mg", "2/1000mg", "1/1000mg"],
        "category": "antidiabetic"
    },
    "glimepiride_metformin_voglibose": {
        "components": ["Glimepiride", "Metformin", "Voglibose"],
        "brands": ["Glycomet-GP-Vog", "Glimy-MV", "Glycomet-GP-Vog", "Glimy-MV", "Glyciphage-SR"],
        "forms": ["Tab"],
        "strengths": ["2/500/0.2mg", "2/1000/0.3mg", "1/500/0.2mg"],
        "category": "antidiabetic"
    },
    "sitagliptin_metformin": {
        "components": ["Sitagliptin", "Metformin"],
        "brands": ["Janumet", "Istamet", "Janumet", "Istamet", "Sitamet"],
        "forms": ["Tab"],
        "strengths": ["50/500mg", "50/1000mg"],
        "category": "antidiabetic"
    },
    "vildagliptin_metformin": {
        "components": ["Vildagliptin", "Metformin"],
        "brands": ["Galvusmet", "Eucreas", "Galvusmet", "Eucreas", "Vildamet"],
        "forms": ["Tab"],
        "strengths": ["50/500mg", "50/1000mg", "50/850mg"],
        "category": "antidiabetic"
    },

    # ============================================================
    # ANTIHYPERTENSIVE / CARDIAC FDCs
    # ============================================================
    "amlodipine_telmisartan": {
        "components": ["Amlodipine", "Telmisartan"],
        "brands": ["Telma-AM", "Tazloc-AM", "Telmikaa-AM", "Telma-AM", "Tazloc-AM"],
        "forms": ["Tab"],
        "strengths": ["5/40mg", "5/80mg", "2.5/40mg", "10/80mg"],
        "category": "antihypertensive"
    },
    "amlodipine_lisinopril": {
        "components": ["Amlodipine", "Lisinopril"],
        "brands": ["Listril-AM", "Amlopress-L", "Listril-AM", "Amlopress-L", "Lipril-AM"],
        "forms": ["Tab"],
        "strengths": ["5/5mg", "5/10mg", "2.5/5mg"],
        "category": "antihypertensive"
    },
    "amlodipine_atorvastatin": {
        "components": ["Amlodipine", "Atorvastatin"],
        "brands": ["Amlodac-AT", "Lipicure-AS", "Amlodac-AT", "Lipicure-AS", "Atorva-AM"],
        "forms": ["Tab"],
        "strengths": ["5/10mg", "5/20mg", "10/10mg", "5/40mg"],
        "category": "antihypertensive"
    },
    "losartan_hydrochlorothiazide": {
        "components": ["Losartan", "Hydrochlorothiazide"],
        "brands": ["Losar-H", "Tozaar-H", "Losar-H", "Tozaar-H", "Losartan-H"],
        "forms": ["Tab"],
        "strengths": ["50/12.5mg", "100/12.5mg", "50/25mg"],
        "category": "antihypertensive"
    },
    "metoprolol_telmisartan": {
        "components": ["Metoprolol", "Telmisartan"],
        "brands": ["Telmikaa-AM", "Tazloc-AM", "Telmikaa-MT", "Tazloc-MT", "Metolar-T"],
        "forms": ["Tab"],
        "strengths": ["25/40mg", "50/40mg", "25/80mg"],
        "category": "antihypertensive"
    },
    "spironolactone_furosemide": {
        "components": ["Spironolactone", "Furosemide"],
        "brands": ["Aldactone-A", "Lasilactone", "Aldactone-A", "Lasilactone", "Spironolactone-Furosemide"],
        "forms": ["Tab"],
        "strengths": ["20/50mg", "50/20mg", "50/40mg"],
        "category": "diuretic"
    },
    "aspirin_clopidogrel": {
        "components": ["Aspirin", "Clopidogrel"],
        "brands": ["Clopitab-A", "Deplatt-A", "Plavix-AS", "Clopitab-A", "Deplatt-A"],
        "forms": ["Tab", "Cap"],
        "strengths": ["75/75mg", "75/150mg", "150/75mg"],
        "category": "anticoagulant"
    },
    "atorvastatin_aspirin": {
        "components": ["Atorvastatin", "Aspirin"],
        "brands": ["Atorva-ASP", "Lipicure-AS", "Ecosprin-AV", "Atorva-ASP", "Lipicure-AS"],
        "forms": ["Tab"],
        "strengths": ["10/75mg", "20/75mg", "10/150mg"],
        "category": "lipid_lowering"
    },
    "atorvastatin_fenofibrate": {
        "components": ["Atorvastatin", "Fenofibrate"],
        "brands": ["Atorva-F", "Lipicure-F", "Atorva-F", "Lipicure-F", "Fenolip-AS"],
        "forms": ["Tab"],
        "strengths": ["10/160mg", "10/145mg", "10/200mg"],
        "category": "lipid_lowering"
    },

    # ============================================================
    # NEUROLOGICAL FDCs
    # ============================================================
    "pregabalin_methylcobalamin": {
        "components": ["Pregabalin", "Methylcobalamin"],
        "brands": ["Pregalin-M", "Nervup-P", "Gabantin-Plus", "Pregalin-M", "Nervup-P"],
        "forms": ["Cap", "Tab"],
        "strengths": ["75/750mcg", "150/750mcg", "75/1500mcg"],
        "category": "anticonvulsant"
    },
    "levodopa_carbidopa": {
        "components": ["Levodopa", "Carbidopa"],
        "brands": ["Syndopa", "Tidomet", "Levodopa-Carbidopa", "Syndopa", "Tidomet"],
        "forms": ["Tab", "Cap"],
        "strengths": ["100/10mg", "250/25mg", "100/25mg"],
        "category": "neurological"
    },
    "levodopa_carbidopa_entacapone": {
        "components": ["Levodopa", "Carbidopa", "Entacapone"],
        "brands": ["Syndopa-Plus", "Stalevo", "Syndopa-Plus", "Stalevo", "Levodopa-Carbidopa-Entacapone"],
        "forms": ["Tab"],
        "strengths": ["100/25/200mg", "150/37.5/200mg", "200/50/200mg"],
        "category": "neurological"
    },

    # ============================================================
    # VITAMIN / SUPPLEMENT FDCs
    # ============================================================
    "calcium_vitamin_d3": {
        "components": ["Calcium", "Vitamin D3"],
        "brands": ["Shelcal", "Calcimax", "Calcimax-OS", "Shelcal", "Calcimax"],
        "forms": ["Tab", "Cap", "Susp"],
        "strengths": ["500/250IU", "500/500IU", "250/125IU"],
        "category": "supplement"
    },
    "b_complex": {
        "components": ["Vitamin B1", "Vitamin B2", "Vitamin B3", "Vitamin B5", "Vitamin B6", "Vitamin B12", "Folic Acid"],
        "brands": ["Becosules", "Polybion", "Cobadex", "Becelac", "Becosules"],
        "forms": ["Cap", "Tab", "Inj"],
        "strengths": ["B-Complex", "B-Complex Forte"],
        "category": "vitamin"
    },
    "b_complex_vitamin_c": {
        "components": ["Vitamin B1", "Vitamin B2", "Vitamin B3", "Vitamin B6", "Vitamin B12", "Vitamin C", "Folic Acid"],
        "brands": ["Becosules-C", "Polybion-C", "Becosules-C", "Polybion-C", "Becelac-C"],
        "forms": ["Cap", "Tab"],
        "strengths": ["B-Complex + Vitamin C"],
        "category": "vitamin"
    },
    "iron_folic_acid": {
        "components": ["Iron", "Folic Acid"],
        "brands": ["Autofer", "Fefol", "Livogen", "Autofer", "Fefol"],
        "forms": ["Tab", "Cap", "Syr"],
        "strengths": ["60/0.5mg", "100/1.5mg", "30/0.5mg"],
        "category": "supplement"
    },
    "multivitamin": {
        "components": ["Vitamin A", "Vitamin B-Complex", "Vitamin C", "Vitamin D", "Vitamin E", "Minerals"],
        "brands": ["A to Z", "Supradyn", "Revital", "Nutricharge", "A to Z"],
        "forms": ["Cap", "Tab", "Syr"],
        "strengths": ["Multivitamin", "Multivitamin + Minerals"],
        "category": "supplement"
    },
    "omega_3": {
        "components": ["Omega-3 Fatty Acids", "EPA", "DHA"],
        "brands": ["Omega-3", "Maxepa", "Omega-3", "Maxepa", "Maxepa"],
        "forms": ["Cap", "Syr"],
        "strengths": ["300mg", "500mg", "1000mg"],
        "category": "supplement"
    },
    "glucosamine_chondroitin": {
        "components": ["Glucosamine", "Chondroitin"],
        "brands": ["Jointace", "Cartigen", "Jointace", "Cartigen", "Glucosamine-Chondroitin"],
        "forms": ["Tab", "Cap"],
        "strengths": ["500/400mg", "750/600mg"],
        "category": "supplement"
    },
    "methylcobalamin_alpha_lipoic_acid_folic_acid": {
        "components": ["Methylcobalamin", "Alpha Lipoic Acid", "Folic Acid"],
        "brands": ["Nervup", "Gabantin-Plus", "Nervup", "Gabantin-Plus", "Nervijen"],
        "forms": ["Tab", "Cap"],
        "strengths": ["1500/100/1.5mg", "500/100/1.5mg"],
        "category": "vitamin"
    },
    "antioxidant": {
        "components": ["Beta-Carotene", "Vitamin C", "Vitamin E", "Selenium", "Zinc"],
        "brands": ["Antoxid", "Antioxidant", "Antoxid", "Antioxidant", "Revital-H"],
        "forms": ["Tab", "Cap"],
        "strengths": ["Antioxidant Complex"],
        "category": "supplement"
    },

    # ============================================================
    # OPHTHALMIC FDCs
    # ============================================================
    "dexamethasone_moxifloxacin": {
        "components": ["Dexamethasone", "Moxifloxacin"],
        "brands": ["Moxi-D", "Dexoren-M", "Moxi-D", "Dexoren-M", "Moxicip-D"],
        "forms": ["Eye Drops"],
        "strengths": ["0.1/0.5%", "0.1/0.5%"],
        "category": "ophthalmic"
    },
    "brimonidine_timolol": {
        "components": ["Brimonidine", "Timolol"],
        "brands": ["Brimon-T", "Combigan", "Brimon-T", "Combigan", "Brimotim"],
        "forms": ["Eye Drops"],
        "strengths": ["0.2/0.5%", "0.15/0.5%"],
        "category": "ophthalmic"
    },

    # ============================================================
    # TOPICAL FDCs
    # ============================================================
    "clindamycin_adapalene": {
        "components": ["Clindamycin", "Adapalene"],
        "brands": ["Adaclin", "Clindoxyl", "Adaclin", "Clindoxyl", "Clindac-A"],
        "forms": ["Gel", "Cream"],
        "strengths": ["1/0.1%"],
        "category": "topical"
    },
    "betamethasone_clotrimazole_gentamicin": {
        "components": ["Betamethasone", "Clotrimazole", "Gentamicin"],
        "brands": ["Candid-B", "Betnovate-GM", "Candid-B", "Betnovate-GM", "Cloben-GM"],
        "forms": ["Cream", "Ointment"],
        "strengths": ["0.05/1/0.1%"],
        "category": "topical"
    },

    # ============================================================
    # GYNECOLOGICAL FDCs
    # ============================================================
    "oral_contraceptives": {
        "components": ["Levonorgestrel", "Ethinyl Estradiol"],
        "brands": ["Mala-D", "Mala-N", "Saheli", "Mala-D", "Mala-N"],
        "forms": ["Tab"],
        "strengths": ["0.15/0.03mg", "0.075/0.03mg"],
        "category": "gynecological"
    },
    "mifepristone_misoprostol": {
        "components": ["Mifepristone", "Misoprostol"],
        "brands": ["Mifepristone+Misoprostol", "Mifty-Kit", "Clear-KIT", "Mifepristone+Misoprostol", "Mifty-Kit"],
        "forms": ["Kit", "Tab"],
        "strengths": ["200mg+200mcg", "200mg+800mcg"],
        "category": "gynecological"
    },
    "tranexamic_acid_mefenamic_acid": {
        "components": ["Tranexamic Acid", "Mefenamic Acid"],
        "brands": ["Pause-MF", "Trenexa-MF", "Pause-MF", "Trenexa-MF", "Transamine-MF"],
        "forms": ["Tab"],
        "strengths": ["500/250mg", "500/500mg"],
        "category": "hemostatic"
    },
}


# Therapeutic categories
CATEGORIES = [
    "antibiotic", "analgesic_antipyretic", "nsaid", "ppi", "antiemetic",
    "antihistamine", "antitussive", "expectorant", "bronchodilator",
    "antidiabetic", "antihypertensive", "cardiac", "lipid_lowering",
    "vitamin", "mineral", "supplement", "enzyme", "steroid",
    "antifungal", "antiviral", "anthelmintic", "laxative", "antacid",
    "muscle_relaxant", "anxiolytic", "anticonvulsant", "thyroid",
    "diuretic", "anticoagulant", "ophthalmic", "topical",
    "antigout", "urological", "neurological", "gynecological",
    "hemostatic", "stimulant", "antidiarrheal"
]