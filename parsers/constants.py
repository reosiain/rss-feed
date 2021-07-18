import source_specific_parsers

function_router = {
    "finam01": None,
    "vedom01": None,
    "finaz01": source_specific_parsers.finaz_parser,
    "inves01": source_specific_parsers.investing_parser,
    "inves02": source_specific_parsers.investing_parser,
    "inves03": source_specific_parsers.investing_parser,
    "inves04": source_specific_parsers.investing_parser,
    "gurut01": None,
    "prime01": source_specific_parsers.prime1_parser,
    "prime02": source_specific_parsers.prime1_parser,
    "prime03": source_specific_parsers.prime1_parser,
    "prime04": source_specific_parsers.prime1_parser,
    "prime05": source_specific_parsers.prime1_parser,
    "prime06": source_specific_parsers.prime1_parser,
    "prime07": source_specific_parsers.prime1_parser,
    "fmark01": source_specific_parsers.finmarket_interfax_parser,
}
