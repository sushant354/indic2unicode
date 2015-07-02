In India, a large number of data sources like vernacular newspapers, magazine, loksabha website use proprietory fonts for displaying content in Indian languages. The proprietory fonts overload normal unicode values with language specific characters.

While proprietory fonts enable content providers to display data in Indian languages, they make document processing like extracting entities, searching with in the document very difficult.

Unicode provides codepoints for all scripts and is accepted widely. Therefore, documents in unicode can be easily processed, indexed and searched.

indic2unicode converts data in proprietory fonts to unicode. It currently supports Aryan2, Divya and Surekh fonts for devanagari script that is used by the LokSabha website for publishing debates.