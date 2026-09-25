# Data intentionally separates documented institutional facts from party positions
# and unverified/user-supplied claims.

PCA_TIMELINE = [
    {
        "date":"19 Sep 1960",
        "title":"Indus Waters Treaty signed",
        "category":"Treaty",
        "description":"India and Pakistan signed the Indus Waters Treaty.",
        "status":"Documented"
    },
    {
        "date":"19 Aug 2016",
        "title":"Pakistan instituted arbitration",
        "category":"PCA",
        "description":"Pakistan instituted proceedings under Paragraph 2(b) of Annexure G.",
        "status":"Documented"
    },
    {
        "date":"17 Oct 2022",
        "title":"World Bank appointments",
        "category":"Neutral Expert / PCA",
        "description":"Michel Lino was appointed Neutral Expert and Sean Murphy was appointed Chairman of the Court of Arbitration.",
        "status":"Documented"
    },
    {
        "date":"15 May 2026",
        "title":"PCA maximum-pondage award",
        "category":"PCA",
        "description":"PCA issued an award concerning maximum pondage supplemental to its general-interpretation award.",
        "status":"Documented"
    },
    {
        "date":"31 Aug 2026",
        "title":"PCA status award and Ratle interim-measures order",
        "category":"PCA",
        "description":"PCA lists an award on the status of the Treaty and an order on Pakistan's interim-measures application concerning Ratle.",
        "status":"Documented"
    },
]

INDIA_RELATED_PROJECTS = [
    {"project":"Pakal Dul","capacity_mw":1000,"river_basin":"Chenab","status":"Under construction / implementation reported in 2026"},
    {"project":"Ratle","capacity_mw":850,"river_basin":"Chenab","status":"Under construction / subject to treaty dispute proceedings"},
    {"project":"Kiru","capacity_mw":624,"river_basin":"Chenab","status":"Under construction / implementation reported in 2026"},
    {"project":"Kwar","capacity_mw":540,"river_basin":"Chenab","status":"Under construction / implementation reported in 2026"},
]

DISPUTED_METRICS = [
    {"metric":"Pondage","plant":"Kishanganga","party_position":"Pakistan disputes the design and has advanced treaty-based objections; exact numerical positions should be sourced to the relevant pleadings/technical documents.","verification":"Do not treat user-supplied numerical caps as adjudicated facts."},
    {"metric":"Pondage","plant":"Ratle","party_position":"Pakistan disputes the design and has advanced treaty-based objections; exact numerical positions should be sourced to the relevant pleadings/technical documents.","verification":"Do not treat user-supplied numerical caps as adjudicated facts."},
    {"metric":"Spillways","plant":"Ratle/Kishanganga","party_position":"The proceedings address gated-spillway design under Annexure D.","verification":"Documented in PCA/Neutral Expert materials."},
    {"metric":"Power intakes","plant":"Ratle/Kishanganga","party_position":"The proceedings address intake design under Annexure D.","verification":"Documented in PCA/Neutral Expert materials."},
    {"metric":"Freeboard","plant":"Ratle","party_position":"The Neutral Expert's mandate includes the freeboard question for Ratle.","verification":"Documented in PCA materials."},
]
