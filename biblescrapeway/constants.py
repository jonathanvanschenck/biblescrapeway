# All regexs will be terminated with "[A-Za-z _\.]*$" to capture the rest of the book, including any abreviations
book_regex = [
    ["^[Gg]e","Genesis", 50],
    ["^[Ee]x","Exodus", 40],
    ["^[Ll]e","Leviticus", 27],
    ["^[Nn]u","Numbers", 36],
    ["^[Dd]e","Deuteronomy", 34],
    ["^[Jj]os","Joshua", 24],
    ["^[Jj]udg","Judges", 21],
    ["^[Rr]u","Ruth", 4],
    ["^1[ _]?[Ss]","1 Samuel", 31],
    ["^2[ _]?[Ss]","2 Samuel", 24],
    ["^1[ _]?[Kk]","1 Kings", 22],
    ["^2[ _]?[Kk]","2 Kings", 25],
    ["^1[ _]?[Cc]h","1 Chronicles", 29],
    ["^2[ _]?[Cc]h","2 Chronicles", 36],
    ["^[Ee]zr","Ezra", 10],
    ["^[Nn]e","Nehemiah", 13],
    ["^[Ee]s","Esther", 10],
    ["^[Jj]ob","Job", 42],
    ["^[Pp]s","Psalm", 150],
    ["^[Pp]r","Proverbs", 31],
    ["^[Ee]c","Ecclesiastes", 12],
    ["^[Ss]o","Song of Solomon", 8],
    ["^[Ii]s","Isaiah", 66],
    ["^[Jj]e","Jeremiah", 52],
    ["^[Ll]a","Lamentations", 5],
    ["^[Ee]ze","Ezekiel", 48],
    ["^[Dd]a","Daniel", 12],
    ["^[Hh]o","Hosea", 14],
    ["^[Jj]oe","Joel", 3],
    ["^[Aa]m","Amos", 9],
    ["^[Oo]b","Obadiah", 1],
    ["^[Jj]on","Jonah", 4],
    ["^[Mm]i","Micah", 7],
    ["^[Nn]a","Nahum", 3],
    ["^[Hh]ab","Habakkuk", 3],
    ["^[Zz]ep","Zephaniah", 3],
    ["^[Hh]ag","Haggai", 2],
    ["^[Zz]ec","Zechariah", 14],
    ["^[Mm]al","Malachi", 4],
    ["^[Mm]at","Matthew", 28],
    ["^[Mm]ar","Mark", 16],
    ["^[Ll]u","Luke", 24],
    ["^[Jj]oh","John", 21],
    ["^[Aa]c","Acts", 28],
    ["^[Rr]o","Romans", 16],
    ["^1[ _]?[Cc]o","1 Corinthians", 16],
    ["^2[ _]?[Cc]o","2 Corinthians", 13],
    ["^[Gg]a","Galatians", 6],
    ["^[Ee]p","Ephesians", 6],
    ["^[Pp]hili","Philippians", 4],
    ["^[Cc]o","Colossians", 4],
    ["^1[ _]?[Tt]h","1 Thessalonians", 5],
    ["^2[ _]?[Tt]h","2 Thessalonians", 3],
    ["^1[ _]?[Tt]i","1 Timothy", 6],
    ["^2[ _]?[Tt]i","2 Timothy", 4],
    ["^[Tt]","Titus", 3],
    ["^[Pp]hile","Philemon", 1],
    ["^[Hh]e","Hebrews", 13],
    ["^[Jj]a","James", 5],
    ["^1[ _]?[Pp]","1 Peter", 5],
    ["^2[ _]?[Pp]","2 Peter", 3],
    ["^1[ _]?[Jj]","1 John", 5],
    ["^2[ _]?[Jj]","2 John", 1],
    ["^3[ _]?[Jj]","3 John", 1],
    ["^[Jj]ude","Jude", 1],
    ["^[Rr]e","Revelation", 22],
]
