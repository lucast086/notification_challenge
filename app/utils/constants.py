#Password policy
SPECIAL_CHARS: set[str] = {
"$",
"@",
"#",
"%",
"!",
"^",
"&",
"*",
"(",
")",
"-",
"_",
"+",
"=",
"{",
"}",
"[",
"]",
}


MIN_LENGTH: int = 5
MAX_LENGTH: int = 20
INCLUDES_SPECIAL_CHARS: bool = True
INCLUDES_NUMBERS: bool = True
INCLUDES_LOWERCASE: bool = True
INCLUDES_UPPERCASE: bool = True