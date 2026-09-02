'''Repair the ToUnicode map of the fonts of a pdf that are known to carry a
broken one.

The Gazette pdfs that are set in Arial Unicode MS carry a ToUnicode map that
was built by pairing the glyphs of a run with the characters of that run one
by one. Devanagari shaping moves matra_i to the left of its cluster and the
reph to the right of its syllable, so the pairing slips exactly on the glyphs
that were moved: every consonant that occurs in a matra_i cluster is handed
the 'ि' of that cluster, matra_i is handed a consonant back, va and tha are
handed the reph of र्व and र्थ, and the reph is handed a va. A nukta pair and
a ligature lose a character in the same way.

The gazettes that are set in Nirmala UI carry a map that was built the same
way and is broken in the same way, ka and sha both being handed the 'ि' of
the cluster they were first drawn in and matra_i a consonant back.

The gazettes that are set in Mangal are broken a third way: their map hands
every glyph that the shaper made <0000> outright, so the half forms, the
conjuncts, the matra_i and the reph are not the wrong characters in the
extracted text, they are no character at all - निम्नलिखित comes out as
"न न ल खत" with a raw NUL where each missing glyph was, which is not even
well formed xml. That subset carries neither a cmap nor a post nor a GSUB,
only outlines, so nothing in it says what those glyphs are and they are
repaired from MANGAL_OUTLINES, a table keyed by what a glyph draws rather
than by its glyph id - this producer renumbers the glyphs of every subset.

The Tamil Nadu gazettes that are set in TAUElangoPanchali are broken the
first way again - the pairing slips on the vowel signs tamil draws in front
of their consonant, so கூறிற்காக comes out as கூறிற்்கநா்க - but there the
font says nothing at all: its subsets carry neither a cmap nor a post nor a
GSUB either, so every glyph of it is repaired from TAU_ELANGO_PANCHALI.

The Tamil Nadu gazettes that are set in TAU-Marutham are broken in a way of
their own, and the fault is not in the map alone: that producer re-encodes the
font. It carries one font both as Type0/Identity-H fonts with a map of their
own and as simple TrueType fonts with WinAnsiEncoding or MacRomanEncoding and
no map at all, and it gives each subset whatever latin bytes it needs, a byte
per glyph in the order that document wanted them. So the simple ones extract
as latin exactly as a legacy 8 bit font does, the identity encoded ones
extract as tamil with a stray latin letter or nothing at all wherever the font
draws a syllable as one glyph, and nothing a subset says about its own glyphs
- its cmap, the names in its post table - is about the glyphs at all. Such a
font is named in RE_ENCODED_FONTS, which is what stops the font itself being
believed over TAU_MARUTHAM; its simple embeddings are repaired by
fix_simple_font, which reads the byte -> glyph id mapping out of the subset's
cmap - the one question this producer's cmap does answer - and writes a map
keyed by the byte; and its embeddings that carry no map at all are given one
built from the table, the code of a glyph being its glyph id there.

The glyphs themselves are drawn correctly, so the text on the page is right
and only its extraction is wrong. The map is built again out of the font
itself, which says what its glyphs are three times over: the cmap of the
subset says which glyph draws which character, the subset keeps the original
uniXXXX name of the glyphs of the devanagari block, and the GSUB of the font
says which glyphs the shaper made out of which other ones, so a conjunct or a
half form is spelled out of the glyphs it was made of however it is named.
The glyphs that are left - the ones of a subset that carries neither a name
nor a cmap entry nor a rule for them - are repaired from a table.

The text that comes out of the repaired pdf is in the visual order of the
glyphs, so it still has to go through fonts/glyphs/arialuni_glyphs.py
(Arial Unicode MS), fonts/glyphs/nirmalaui_glyphs.py (Nirmala UI),
fonts/glyphs/mangal_glyphs.py (Mangal), fonts/glyphs/nudiuni_glyphs.py
(NudiUni), fonts/glyphs/tauelango_glyphs.py (TAUElangoPanchali) or
fonts/glyphs/marutham_glyphs.py (TAU-Marutham) to be put in the order that
unicode wants - see FONT_CONVERTERS below.

USAGE:
    python fix_tounicode.py input.pdf output.pdf
'''

import getopt
import hashlib
import io
import logging
import re
import sys
import unicodedata

import pymupdf
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont

from indic2unicode.langs import kannada, tamil

# the glyphs that the shaper made. They have no name of their own in the
# font, so the string of every one of them is repaired by hand. The string
# that the broken map hands such a glyph is the character it happened to be
# paired with in that document, and that differs from document to document:
# the matra_i of दि is handed a द in one gazette and the matra_i of कि a क
# in another, both by the same glyph. So a glyph is repaired to what it
# really is whatever its map says, and the comment only records the string
# that was seen first. A map that is already right says the same thing that
# the table does, so repairing it changes nothing
ARIAL_UNICODE_MS = { \
    # the half forms, which the font lays out in the order of the consonants
    # they belong to, क् at 6989 through ह् at 7022. A pdf whose map hands
    # them the halant and a zwj instead of the consonant loses the consonant
    # of every one of them, उक्त comes out as उ त and उपलब्ध as उपल् ध \
    6989: 'क्',  # seen as ‍ \
    6990: 'ख्',  # seen as ्‍ \
    6991: 'ग्',  # seen as ‍ \
    7005: 'थ्',  # seen as ्‍ \
    7007: 'ध्',  # seen as ‍ \
    7009: 'प्',  # seen as ‍ \
    7011: 'ब्',  # seen as ्‍ \
    7021: 'स्',  # seen as स्ट् \
    # the glyphs the shaper made out of a whole cluster \
    6979: 'क्ष', # seen as ि \
    6981: 'र्',  # seen as व, ा \
    7069: 'ट्र',  # seen as र \
    7081: 'ब्र',  # seen as ि \
    # the reph and the matra of the syllable it sits on, which the font
    # draws as one glyph. The GSUB of the font makes it out of matra_ii and
    # the reph, so a syllable that carries it keeps its matra: पूर्वी is
    # पूर्वी and not पूर्व \
    7278: 'ीर्', # seen as ी \
    7399: 'ष्ठ',  # seen as ि \
    # the width variants of matra_i \
    7407: 'ि',   # seen as र \
    7408: 'ि',   # seen as क, द \
    7409: 'ी',   \
    7410: 'ि',   # seen as ल, स \
    # the rest of the half forms, in the order of their consonants \
    6996: 'ज्',  \
    7004: 'त्',  \
    7008: 'न्',  # seen as a space \
    7013: 'म्',  \
    7016: 'ल्',  \
    7019: 'श्',  \
    7020: 'ष्',  \
    # the ligatures that the shaper made out of a whole cluster \
    7074: 'त्र',  # seen as ि \
    7079: 'प्र',  \
    7272: 'रू',  \
    7275: 'त्त',  \
    7286: 'ें',   \
    7289: 'ैं',   \
    7298: 'ों',  # seen as स \
    7312: 'ओं',  \
    7334: 'क्त',  # seen as ि \
    7367: 'द्व',  \
    7374: 'द्द',  \
    7378: 'द्य',  \
    7382: 'न्न',  \
    7385: 'प्त',  \
    7388: 'म्न',  \
    7397: 'ष्ट',  \
    7398: 'ष्ट्र', \
}

# THE KANNADA OF THE SAME FONT
#
# A Karnataka gazette is set in Arial Unicode MS too, and its map is broken a
# fourth way: it carries an entry for the letters of the block and for a
# handful of the forms the shaper made, and none at all for the rest. Every
# consonant that a vowel sign i or e was drawn into, every plain consonant
# that a vattu sits under, ksha and jna and the vattus of ma and ya come out
# as (cid:8243) and the like - 17,360 glyphs of the 69 page gazette this
# table was read from, one in every seven.
#
# The font lays these forms out in blocks, one glyph per consonant in the
# order of the unicode block, which is what makes them a table that can be
# written down rather than a list of a few hundred readings: the vattus run
# from 8136, the plain consonants from 8174, the dead consonants from 8206,
# the vowel sign i forms from 8243 and the vowel sign e forms from 8275. The
# blocks of the plain consonant and of the two vowel signs leave out nga,
# nya and rra, the three letters kannada writes none of these forms of, and
# the two blocks that carry a virama do not. Every anchor the document's own
# map does carry - 8136 ka, 8162 ra, 8169 sa, 8174 ka, 8206 ka, 8232 ra,
# 8243 ka, 8275 ka - falls where the blocks put it, and the glyphs of the
# blocks were read off the outlines of the subset to check it.
#
# A vattu is spelled here as the virama and its consonant, which is the
# order unicode writes a subjoined consonant in and the order the glyph
# really stands for, while a dead consonant is spelled the other way round.
# That is what keeps the two apart: the map of the pdf spells both of them
# 'ಟ್' and fonts/kannada/tunga.py has to guess between them, while this
# repair hands fonts/kannada/arialuni.py a text that says which is which.
# The virama of a dead consonant is the virama of the whole cluster, so it
# still has to move behind the vattus that follow it, which is a move of the
# order and not of the reading and is done in that converter

KANNADA_VIRAMA = kannada.KannadaUnicode().tokendict['VIRAMA']

# every kannada consonant in the order of the unicode block, ka through ha
KANNADA_CONSONANTS = [chr(code) for code in range(0x0c95, 0x0cba) \
                                if code not in (0x0ca9, 0x0cb4)]

# the same, without the three that the blocks below leave out
KANNADA_COMMON_CONSONANTS = [char for char in KANNADA_CONSONANTS \
                             if char not in ('ಙ', 'ಞ', 'ಱ')]

def kannada_block(gid, consonants, prefix = '', suffix = ''):
    '''a block of the font, one glyph per consonant in the order of the
       unicode block, drawn with the same mark before or after each of them'''
    return {gid + i: prefix + char + suffix \
            for i, char in enumerate(consonants)}

ARIAL_UNICODE_MS_KANNADA = { \
    # the arkavattu, the ra that is drawn as a mark on top of the consonant
    # that follows it and is stored behind the whole syllable it sits on.
    # It is spelled like a dead ra and the font draws the two with glyphs of
    # their own - 8135 and 8232 - so it carries the mark that says which of
    # the two it is, see langs/kannada.ARKAVATTU_MARK. Both of them stand at
    # the end of a word in the drawn order, ಅರ್ಥ as ಅಥರ್ and ಡೈರೆಕ್ಟರ್ as
    # ಡೈರೆಕ್ಟರ್, so nothing in the text around them tells them apart \
    8135: 'ರ್' + kannada.ARKAVATTU_MARK, \
}
# the vattus, ka through ha, spelled the way unicode writes them
ARIAL_UNICODE_MS_KANNADA.update(kannada_block(8136, KANNADA_CONSONANTS, \
                                              prefix = KANNADA_VIRAMA))
# the plain consonants, the form the font draws one in when a vattu or a
# vowel sign that is a glyph of its own is drawn onto it
ARIAL_UNICODE_MS_KANNADA.update(kannada_block(8174, KANNADA_COMMON_CONSONANTS))
# the dead consonants, the consonant and the virama of its cluster
ARIAL_UNICODE_MS_KANNADA.update(kannada_block(8206, KANNADA_CONSONANTS, \
                                              suffix = KANNADA_VIRAMA))
# the consonants that the vowel sign i and the vowel sign e are drawn into.
# The second half of a two part sign - ee, ii, ai, o, oo - is a glyph of its
# own and follows, so ಕೀ is the ಕಿ of this block and the length mark
ARIAL_UNICODE_MS_KANNADA.update(kannada_block(8243, KANNADA_COMMON_CONSONANTS, \
                                              suffix = 'ಿ'))
ARIAL_UNICODE_MS_KANNADA.update(kannada_block(8275, KANNADA_COMMON_CONSONANTS, \
                                              suffix = 'ೆ'))
ARIAL_UNICODE_MS_KANNADA.update({ \
    # the vowel signs u and uu where they stand on their own \
    8307: 'ು', \
    8308: 'ೂ', \
    # ma and ya end in the same stroke the vowel sign u is drawn with, so
    # the sign o of them is drawn into the letter and is one glyph \
    8309: 'ಮೊ', \
    8310: 'ಯೊ', \
    # the two clusters kannada writes as a letter of their own. Each of them
    # has a form with a headstroke, for a syllable that carries a vowel sign
    # drawn beside it, and one without \
    8319: 'ಕ್ಷ', \
    8320: 'ಕ್ಷ', \
    8322: 'ಕ್ಷಿ', \
    8323: 'ಕ್ಷೆ', \
    8324: 'ಜ್ಞ', \
    8325: 'ಜ್ಞ', \
})

# 8311 through 8318 are ligatures of a consonant and the vattu of ra that no
# page of that gazette draws, so there is nothing to read them off but the
# map that is broken - it spells 8312 'ಪ್ರ್' and 8315 'ಟ್ರ್', a virama more
# than either can stand for. They are left as the pdf has them rather than
# guessed at: a glyph left alone loses the improvement, a glyph read wrongly
# destroys the text around it

ARIAL_UNICODE_MS.update(ARIAL_UNICODE_MS_KANNADA)

# The devanagari of Nirmala UI needs no glyph repaired by hand: the subsets of
# it that those gazettes carry keep the GSUB of the font, so every glyph the
# shaper made is read out of the rule that made it. The kannada of it keeps
# nothing at all, and is the whole of the table below.
#
# THE KANNADA OF NIRMALA UI
#
# A Karnataka gazette is set in Nirmala UI as well, and the subset it carries
# there keeps neither a cmap nor a post nor a GSUB - only the outlines - so
# there is nothing in the font to read a glyph back out of. Its map is short
# rather than wrong, the way the kannada map of Arial Unicode MS is: it names
# the letters of the block and stops, and every glyph the shaper made - every
# consonant a vowel sign was drawn into, every vattu, the arkavattu - has no
# entry at all and extracts as (cid:3197) and the like, 21,000 glyphs of the
# 21 page gazette this table was read from.
#
# What makes those glyphs a table that can be written down rather than a list
# of six hundred readings is that the font lays them out in blocks, in the
# order of the unicode block:
#
#   3074  the two signs, anusvara and visarga
#   3076  the vowels, a through au
#   3090  the consonants, ka through ha
#   3144  the length mark and the ai length mark
#   3161  the vattus, ka through ha
#   3197  fifteen glyphs per consonant, ka through ha: the twelve vowel signs
#         the font draws into a letter, then that letter with the anusvara,
#         with the visarga, and with its virama
#
# and none of the blocks leaves a consonant out - unlike Arial Unicode MS,
# which writes no vowel sign form of nga, nya or rra. Every anchor the
# document's own map does carry falls where the blocks put it: it names 3074
# anusvara, 3090 ka, 3092 ga, 3095 ca, 3097 ja, 3100 tta, 3102 dda, 3104 nna,
# 3105 ta, 3107 da, 3109 na, 3110 pa, 3112 ba, 3114 ma, 3116 ra, 3118 la,
# 3119 lla, 3120 va through 3124 ha and 3144 the length mark, and the rest of
# the blocks were read off the outlines of the subset.
#
# A vattu is spelled here as the virama and its consonant, which is the order
# unicode writes a subjoined consonant in, and a dead consonant the other way
# round, so the two are already different tokens by the time
# fonts/kannada/nirmalaui.py reads them - the same thing
# ARIAL_UNICODE_MS_KANNADA does, and for the same reason.
#
# The gids of this table are the gids of a font program that counts 4309
# glyphs, and Nirmala UI is carried in this corpus in four numberings - 79,
# 4309, 4923 and 5025 glyphs - so the ids of one of them mean nothing in
# another. NIRMALA_UI_GLYPH_COUNT below is what holds the table to the one it
# was read from

# the twelve vowel signs the font draws into a consonant, in the order of the
# unicode block, and then the three marks that follow them in the block of
# fifteen. Only two of the fifteen are never drawn in that gazette - the
# vowel signs ii and oo - and neither is a guess: the other thirteen are the
# block in unicode order, and ii and oo are the two gaps that order leaves
KANNADA_CONSONANT_SIGNS = [chr(code) for code in range(0x0cbe, 0x0ccd) \
                           if code not in (0x0cc4, 0x0cc5, 0x0cc9)]      \
                          + ['\u0c82', '\u0c83', KANNADA_VIRAMA]

def kannada_consonant_blocks(gid, consonants, signs):
    '''the blocks of a font that draws a glyph of its own for a consonant
       and each of the signs that can be written into it, one block of
       len(signs) glyphs per consonant in the order of the unicode block'''
    return {gid + i * len(signs) + j: char + sign \
            for i, char in enumerate(consonants) \
            for j, sign in enumerate(signs)}

NIRMALA_UI_KANNADA = { \
    # the two signs and the vowels, which the map of that gazette carries
    # only some of - it names a different handful of them in each of the four
    # ToUnicode streams it has for the one font \
    3074: '\u0c82', 3075: '\u0c83', \
}
NIRMALA_UI_KANNADA.update({3076 + i: chr(code) \
                           for i, code in enumerate( \
                               c for c in range(0x0c85, 0x0c95) \
                               if c not in (0x0c8d, 0x0c91))})
# the consonants, ka through ha, and the two length marks
NIRMALA_UI_KANNADA.update(kannada_block(3090, KANNADA_CONSONANTS))
NIRMALA_UI_KANNADA.update({3144: '\u0cd5', 3145: '\u0cd6'})
# the vattus, spelled the way unicode writes a subjoined consonant
NIRMALA_UI_KANNADA.update(kannada_block(3161, KANNADA_CONSONANTS, \
                                        prefix = KANNADA_VIRAMA))
# a glyph per consonant and sign written into it
NIRMALA_UI_KANNADA.update(kannada_consonant_blocks(3197, KANNADA_CONSONANTS, \
                                                   KANNADA_CONSONANT_SIGNS))
NIRMALA_UI_KANNADA.update({ \
    # the arkavattu, the ra that is drawn as a mark on top of the consonant
    # that follows it and is stored behind the whole syllable it sits on. It
    # is spelled like the dead ra of 3601 and the font draws the two with
    # glyphs of their own, so it carries the mark that says which of the two
    # it is, see langs/kannada.ARKAVATTU_MARK \
    4305: 'ರ್' + kannada.ARKAVATTU_MARK, \
})

# The glyphs 3125 through 3143 are the vowel signs where they stand on their
# own rather than drawn into a letter. No page of that gazette draws one, and
# the block holds three glyphs more than the block has signs - the font draws
# a second form of some of them - so which glyph is which sign is not settled
# by the order the way the blocks above are. They are left as the pdf has
# them rather than guessed at: a glyph left alone loses the improvement, a
# glyph read wrongly destroys the text around it

NIRMALA_UI = dict(NIRMALA_UI_KANNADA)

# The glyph count of the font program NIRMALA_UI_KANNADA was read from. A
# subset that keeps the glyph order of the font it was cut out of counts all
# of that font's glyphs however few it carries, so this is the whole font's
# count and every subset of that font matches it - see glyph_count. The four
# Nirmala UI in this corpus count 79, 4309, 4923 and 5025 glyphs, which is
# four different numberings of one family, and a table read off one of them
# says nothing about the others: gid 3197 is kannada kaa here and is whatever
# a 4923 glyph Nirmala UI puts there in test/test_pdfs/gazette1.pdf. Those
# other subsets draw no kannada, so nothing goes wrong today - this is what
# keeps it that way when one of them does
NIRMALA_UI_GLYPH_COUNT = 4309

# ---------------------------------------------------------------------------
# NudiUni, the unicode Nudi of the Karnataka gazette
#
# Nudi01e and the rest of that family are legacy 8 bit fonts whose text is
# the keys the typist pressed, and fonts/kannada/nudi.py decodes them. NudiUni
# is the unicode font of the same family and is a different problem: its
# glyphs really are kannada and its subsets keep a cmap and a post naming
# 148 of them, but the shaped glyphs - the form of a consonant that a vowel
# sign is written beside, the vattus, the arkavattu, the ligatures - are
# named by none of those and carry no GSUB either. Not one NudiUni subset in
# this corpus has a GSUB table, so there is no rule to read them out of and
# what a producer's ToUnicode map says about them is all there is.
#
# That map is worth nothing. Of 595 NudiUni maps read out of 400 documents,
# 443 name only the glyphs the font's own cmap already names and leave every
# shaped glyph with no entry at all, so 43% of the glyphs of such a document
# extract as nothing; 125 more hand the glyphs arbitrary greek and cyrillic;
# and the 18 that do name the shaped glyphs agree with the font's own cmap on
# a median of none of the glyphs where they can be checked, and agree with
# each other on 31 of the 100 shaped glyphs they have in common. They are a
# per document guess and not a fact about the font, so nothing here is read
# out of them.
#
# What is read here is the two blocks the font lays out regularly, each
# anchored on glyphs rendered off the subsets and read against the page:
#
#   ಕರ್ನಾಟಕ    is drawn  ಕ 85 ಾ 65 ಟ ಕ
#   ಪ್ರದತ್ತವಾ   is drawn  ಪ 128 ದ ತ 117 118 ಾ
#   ರವನ್ನು      is drawn  ರ ವ ನ ು 121
#   ಚಕ್ಕುಬಂದಿ   is drawn  ಚ ಕ ು 102 ಬ ಂ 218
#   ರಲ್ಲಿ       is drawn  ರ 235 130
#
# which puts 66 at ka and 102 at the vattu of ka and settles both blocks
# from either end. Six such anchors fall in the first block and five in the
# second, and every one of them lands where the block puts it
# ---------------------------------------------------------------------------
NUDI_UNI_KANNADA = {}
# the form of a consonant that the font draws when a vowel sign or a vattu is
# written onto it - ಭಾ is this ಭ and the sign, ಕರ್ನಾಟಕ this ನ and the sign -
# which is the plain consonant and nothing more. The 18 maps that name these
# glyphs at all spell four of them with a virama, as if the form were a dead
# consonant; it is not, and reading it that way puts a virama in the middle
# of ಕರ್ನಾಟಕ
NUDI_UNI_KANNADA.update(kannada_block(66, KANNADA_CONSONANTS))
# the vattus, ka through ha, spelled the way unicode writes a subjoined
# consonant. Glyph 101 sits between the two blocks and no page of this
# corpus draws it, so it is left as the pdf has it rather than guessed at
NUDI_UNI_KANNADA.update(kannada_block(102, KANNADA_CONSONANTS, \
                                      prefix = KANNADA_VIRAMA))

# The arkavattu is glyph 65 and is deliberately not in the table above: the
# font's own cmap names it U+0CF5, an unassigned codepoint the font uses as
# a slot of its own for it, and what the font says about a glyph wins over a
# hand table in fix_font - rightly, since the font is the better authority.
# So the repaired text spells the arkavattu U+0CF5 rather than 'ರ್' and a
# mark, and fonts/kannada/nudiuni.py reads that character as the arkavattu.
# It needs no ARKAVATTU_MARK to tell it from a dead ra, which is the one
# thing NudiUni makes easier than Arial Unicode MS: the two are already
# different characters

# The shaped glyphs above 200 are the consonants that a vowel sign is drawn
# into and the ligatures - ಕ್ಷ, ಜ್ಞ, ಷ್ಟ - and they are left alone. They do not
# fall into a block the way the two above do: ತಿ, ದಿ, ಲಿ, ಳಿ and ಸಿ were read
# off the page at glyphs 216, 218, 235, 236 and 240, and no one block start
# puts all five where they are. That is 8% of the glyphs of a NudiUni
# document still extracting as nothing, and reading them needs every glyph of
# that region rendered and identified one at a time, the way MANGAL_OUTLINES
# was built. A glyph left alone loses the improvement; a glyph read wrongly
# destroys the text around it

# The glyph count of the font program NUDI_UNI_KANNADA was read from. Every
# NudiUni subset in this corpus counts 425 - 01e, 01k, 02e and Ananth05e, in
# every weight and style - and the 145 glyphs the cmaps of 01e and Ananth05e
# both name are the same glyphs in both, so the one table serves the family.
# The guard is what drops it for a numbering that is not this one
NUDI_UNI_GLYPH_COUNT = 425

# ---------------------------------------------------------------------------
# TAU Elango Panchali, the tamil of the Tamil Nadu gazette
#
# fonts/tamil/tamelango.py decodes TAM_ELANGO_Panchali, the legacy 8 bit font
# of the same foundry, whose text is the keys the typist pressed. TAUElango-
# Panchali is the unicode font of that family and is a different problem: its
# glyphs really are tamil, and what is wrong is the map. The subsets carry
# neither a cmap nor a post nor a GSUB, only outlines - nothing in the font
# says what any of its glyphs are - and the producer's map was built by
# pairing the glyphs of a run with the characters of that run one by one, so
# it slips on exactly the glyphs tamil shaping moved: கூறிற்காக comes out as
# கூறிற்்கநா்க, the one glyph of கா being handed a '்க' and the ா a 'நா'.
#
# The slip is a different one in every document, which is why the map cannot
# be corrected out of itself: glyph 151 is the vowel sign ா, and of the maps
# read out of this corpus one calls it 'நா' and the next 'ோ'. What every one
# of them does agree on is the blocks below - the maps of two documents agree
# on ~90% of the glyphs they share, and the ~10% they differ on all sit in
# the region this table repairs.
#
# The whole font is 301 glyphs and it lays them out in blocks:
#
#   0..99      the macintosh standard glyph order, which every map in this
#              corpus gets right and which is therefore left as it is
#   100..113   the dashes, the quotes and a handful of latin extras
#   114..184   the tamil block, one glyph per assigned codepoint of it, in
#              codepoint order and skipping ௐ, which the font does not draw
#   185..207   every consonant with a pulli on it
#   208..230   every consonant with the vowel sign i written into it
#   231..253   the same with the sign ii
#   254..271   the eighteen tamil consonants with the sign u
#   272..289   the same with the sign uu
#   290..300   the ligatures - க்ஷ and ஸ்ரீ, and eight glyphs no document of
#              this corpus draws
#
# The blocks of 23 run through the eighteen tamil consonants in the order
# langs/tamil.CONSONANT_TOKENS gives and then the five grantha letters, ஶ
# first and க்ஷ not among them at all - க்ஷ carries no vowel sign in this
# corpus and is a ligature at 290 instead. The u and uu blocks are the
# eighteen tamil letters only: a grantha letter takes those two signs as
# glyphs of their own, at 154 and 155.
#
# Every reading was established by rendering the glyphs out of the embedded
# subsets of ~1,500 documents of the corpus (no one document carries them
# all) and reading them against the pages that draw them. The blocks are
# corroborated by the maps themselves: from glyph 208 on the producers' maps
# are right, and every one of their entries falls where these blocks put it.
TAMIL_UNICODE = tamil.TamilUnicode().tokendict

# one glyph per assigned codepoint of the tamil block, in codepoint order,
# 0B82 through 0BFA. The ranges are written out rather than read off
# unicodedata: the whole table hangs on this list being exactly 71 long -
# 114 + 70 is 184, and 185 is where the pulli block starts - so it must not
# be able to shift under a python whose unicode data assigns a codepoint
# this block leaves out today.
#
# ௐ (0BD0) falls in the gap between 0BCD and 0BD7 and so is skipped here,
# which is the font's own doing: it draws no om sign, and that is what puts
# ௗ at 163 and the tamil digit one at 165, where the two glyphs really are
TAMIL_CODEPOINTS = [chr(code) \
                    for first, last in ((0x0b82, 0x0b83), (0x0b85, 0x0b8a), \
                                        (0x0b8e, 0x0b90), (0x0b92, 0x0b95), \
                                        (0x0b99, 0x0b9a), (0x0b9c, 0x0b9c), \
                                        (0x0b9e, 0x0b9f), (0x0ba3, 0x0ba4), \
                                        (0x0ba8, 0x0baa), (0x0bae, 0x0bb9), \
                                        (0x0bbe, 0x0bc2), (0x0bc6, 0x0bc8), \
                                        (0x0bca, 0x0bcd), (0x0bd7, 0x0bd7), \
                                        (0x0be6, 0x0bfa)) \
                    for code in range(first, last + 1)]

# the eighteen letters of tamil proper, in the order the script lists them
# and the font lays them out
TAMIL_CONSONANTS = [TAMIL_UNICODE[token] \
                    for token in tamil.CONSONANT_TOKENS[:18]]

# the five grantha letters that follow them in every block of 23. The order
# is the font's own and is neither the codepoint order (ஜ, then ஶ ஷ ஸ ஹ) nor
# the one the script lists them in (ஜ ஷ ஸ ஹ க்ஷ): ஸ் sits at 204 and ஷ் at
# 205, ஜ் at 206 and ஹ் at 207, read off the glyphs themselves. ஶ is the
# first of the five and no subset of this corpus carries a glyph for it in
# any block - nor for the plain ஶ at 147 - which is what the order and the
# block width leave for it
TAMIL_GRANTHA = [TAMIL_UNICODE[token] \
                 for token in ('SHA', 'SA', 'SSA', 'JA', 'HA')]

def tamil_block(gid, letters, sign):
    '''a block of one glyph per letter, each of them drawn with the vowel
       sign or the pulli that the block is of'''
    return {gid + i: letter + sign for i, letter in enumerate(letters)}

TAU_ELANGO_PANCHALI = {114 + i: char \
                       for i, char in enumerate(TAMIL_CODEPOINTS)}
# the pulli forms and the two vowel signs that every letter takes, the five
# grantha letters after the eighteen tamil ones
TAU_ELANGO_PANCHALI.update( \
    tamil_block(185, TAMIL_CONSONANTS + TAMIL_GRANTHA, \
                TAMIL_UNICODE['PULLI']))
TAU_ELANGO_PANCHALI.update( \
    tamil_block(208, TAMIL_CONSONANTS + TAMIL_GRANTHA, \
                TAMIL_UNICODE['MATRA_I']))
TAU_ELANGO_PANCHALI.update( \
    tamil_block(231, TAMIL_CONSONANTS + TAMIL_GRANTHA, \
                TAMIL_UNICODE['MATRA_II']))
# the signs u and uu, which only the eighteen tamil letters are drawn with
TAU_ELANGO_PANCHALI.update( \
    tamil_block(254, TAMIL_CONSONANTS, TAMIL_UNICODE['MATRA_U']))
TAU_ELANGO_PANCHALI.update( \
    tamil_block(272, TAMIL_CONSONANTS, TAMIL_UNICODE['MATRA_UU']))
TAU_ELANGO_PANCHALI.update({ \
    # the two syllables the font draws as one glyph of their own. 290 is
    # read in யார்க்ஷையர் and 294 in ஸ்ரீதர் and ஸ்ரீகுரு
    290: TAMIL_UNICODE['KSSA'], \
    294: TAMIL_UNICODE['SHRI'], \
})

# The glyphs 291 to 293 and 295 to 300 are ligatures of the same kind that no
# document of this corpus draws and that no subset of it carries, so nothing
# says what they are and they are left as the pdf has them - a glyph left
# alone loses the improvement, a glyph read wrongly destroys the text around
# it. The same holds for 100 to 113, which are latin punctuation the maps of
# this corpus already get right

# This font is deliberately absent from BROKEN_FONT_GLYPH_COUNTS below. The
# gazette carries it in eighteen different glyph counts - a full 301 glyph
# subset in most documents and truncated ones of 295, 290, 288, 285, 284,
# 282, 271, 270, 255, 93, 90, 73, 65, 63, 29, 27 and 26 glyphs in the rest -
# but that producer's subsetter only ever drops the glyphs off the end and
# never renumbers what it keeps: of 505 subsets read out of 900 documents,
# every one of the 19,336 glyphs they share with the 301 glyph subset this
# table was read off draws the identical outline, with no disagreement
# anywhere. Holding the table to 301 would therefore refuse the repair for
# the ~7% of subsets that are merely short - one of them, a 295 glyph subset,
# sets the whole body of a change of names gazette - and refuse it for
# nothing

# Uni-Ila.Sundaram, the tamil that the Tamil Nadu gazette sets a notification
# in where TAUElangoPanchali sets the body of it - 929 of the 8,248 documents
# of that corpus draw 38,175 words in it, and a good many of them draw both.
#
# Its map is broken the same way TAU Elango's is and by a producer that knew
# it: the map is built by pairing the glyphs of a cluster with the characters
# of it, and this one hands the *first* glyph of a cluster the whole cluster
# and every glyph after it the cluster's last character. So the two glyph
# cluster மா is a ம that says "மா" and a ா that says "ா" and extracts as
# மாா, and லை - drawn ை first, tamil putting that sign in front of its
# letter - is a ை that says "லை" and a ல that says "ை" and extracts as லைை.
# A glyph a document draws in more than one cluster can only be given one
# reading, so the rest come out as some other cluster's, and the producer
# papers over those with an /ActualText span (which pdfminer does not read)
# that carries the same doubling: அறிவிக்கை is spanned as அறிவிக்கைை.
#
# A single glyph cluster - a consonant with the pulli on it, or with one of
# the four vowel signs this font draws into the letter - is a cluster whose
# first glyph is its only glyph, so those entries are right, and it is those
# that corroborate the blocks below: over the 1,072 documents of the corpus
# that carry this font, the reading these blocks give is the most frequent
# one the maps themselves hold for every one of the 90 glyphs whose id falls
# in a block and that any map names at all.
#
# The subsets carry neither a cmap nor a post nor a GSUB, only outlines, so
# nothing in the font can be read back and this table is the whole of what is
# known about its glyphs. Every reading in it was rendered off the embedded
# subsets - no one document carries them all, so the glyphs were merged over
# the 1,363 subsets of the -03 face that the corpus carries - and read against
# the pages that draw them.
#
# The whole family shares one glyph order. This corpus carries the faces
# Uni-Ila.Sundaram-01, -03, -04, -07 and -03-SC700, all of them 327 glyphs,
# and -03-SC700 is not a face of its own at all: every one of the 119 glyphs
# its subsets share with the -03 ones draws the identical outline, so despite
# its name it is that font - the opposite of TAUElangoPanchali-SC700 above,
# which really is another font and whose map is sound. -01, -04 and -07 do
# draw typefaces of their own, and it is their maps that place them here:
# 50 of the 57 glyph ids -01's name carry the reading this table gives, and
# so does the one that -07's names. The seven of -01's that they do not are
# all pulli forms its maps write as the bare consonant (225 as ங rather than
# ங்) - a second bug of the same producer, which -03's own maps show too,
# 224 being க் in 536 of this corpus's maps and a bare க in 152 of them - and
# not a difference in the order. -04 names one glyph in the whole corpus, 126
# as '~', which the -03 maps also call '~' three times where 34 of them call
# it ஏ.

# the assigned codepoints of the tamil block, 0B83 through 0BCD, one glyph
# each and in codepoint order. ஶ (0BB6) is skipped, which is the font's own
# doing - it draws no ஶ anywhere, in this block or in any of the ones below,
# and that is what puts ஷ at 150 and the vowel sign ா at 153, where the two
# glyphs really are. The ranges are written out rather than read off
# unicodedata for the reason TAMIL_CODEPOINTS above is: the blocks that
# follow hang on this list being exactly 47 long, so it must not be able to
# shift under a python whose unicode data assigns a codepoint it leaves out
# today. TAU-Marutham below lays out the same 47 codepoints and skips ஶ
# where this font does, so the list and the consonants of it serve both.
#
# The block is anchored on ஃ at 118 and not on the anusvara ஂ at 117: the
# maps of this corpus name 118 ஃ and never name 117 anything but the latin
# 'u' of a document whose whole map has slipped into the latin range, and
# tamil writes no anusvara, so whether the font carries a glyph for it - and
# so whether this block starts at 117 or at 118 - is exactly what the corpus
# cannot say. Starting it at 118 leaves 117 as the pdf has it, which costs a
# character no tamil document writes
TAMIL_CODEPOINTS_NO_SHA = \
        [chr(code) \
         for first, last in ((0x0b83, 0x0b83), (0x0b85, 0x0b8a), \
                             (0x0b8e, 0x0b90), (0x0b92, 0x0b95), \
                             (0x0b99, 0x0b9a), (0x0b9c, 0x0b9c), \
                             (0x0b9e, 0x0b9f), (0x0ba3, 0x0ba4), \
                             (0x0ba8, 0x0baa), (0x0bae, 0x0bb5), \
                             (0x0bb7, 0x0bb9), (0x0bbe, 0x0bc2), \
                             (0x0bc6, 0x0bc8), (0x0bca, 0x0bcd)) \
         for code in range(first, last + 1)]

# the 22 consonants of that block, in the same codepoint order the font lays
# them out in - which is not the order tamil.CONSONANT_TOKENS lists them in
# and so not the one TAU Elango's blocks run through: ன follows ந here,
# where the script puts it last of the eighteen
TAMIL_CONSONANTS_NO_SHA = [char for char in TAMIL_CODEPOINTS_NO_SHA \
                           if 'க' <= char <= 'ஹ']

# the eighteen letters of tamil proper among them. The signs u and uu are
# drawn into the letter and the font draws them into these eighteen only, so
# the grantha letters - ஜ among them, which codepoint order puts in the
# middle of the eighteen rather than after them - fall out of those two
# blocks and out of them alone
UNI_ILA_TAMIL_CONSONANTS = [char for char in TAMIL_CONSONANTS_NO_SHA \
                            if char not in TAMIL_GRANTHA]

UNI_ILA_SUNDARAM = {118 + i: char \
                    for i, char in enumerate(TAMIL_CODEPOINTS_NO_SHA)}
# the two vowel signs that are drawn into a letter without changing which
# eighteen take them, and the pulli. Each block is 23 wide where the letters
# are 22, and what the 23rd slot of it draws is not known - no subset of the
# corpus carries a glyph at 200, 223 or 246 and no map of it names one - so
# those three are left as the pdf has them
UNI_ILA_SUNDARAM.update( \
    tamil_block(178, TAMIL_CONSONANTS_NO_SHA, TAMIL_UNICODE['MATRA_I']))
UNI_ILA_SUNDARAM.update( \
    tamil_block(201, TAMIL_CONSONANTS_NO_SHA, TAMIL_UNICODE['MATRA_II']))
UNI_ILA_SUNDARAM.update( \
    tamil_block(224, TAMIL_CONSONANTS_NO_SHA, TAMIL_UNICODE['PULLI']))
# the signs u and uu, which only the eighteen tamil letters are drawn with
UNI_ILA_SUNDARAM.update( \
    tamil_block(247, UNI_ILA_TAMIL_CONSONANTS, TAMIL_UNICODE['MATRA_U']))
UNI_ILA_SUNDARAM.update( \
    tamil_block(265, UNI_ILA_TAMIL_CONSONANTS, TAMIL_UNICODE['MATRA_UU']))
UNI_ILA_SUNDARAM.update({ \
    # ஸ்ரீ, which the font draws as a single glyph of its own \
    284: TAMIL_UNICODE['SHRI'], \
})

# What this table leaves out is 165 to 177 and 283, 285 to 303 and 306 to
# 326. The first is the tail of the codepoint block - the om sign, the au
# length mark, the tamil digits and the numeric signs - and it cannot be read
# off the order the way the head of it can: no subset of the corpus carries a
# glyph anywhere in that range and no map of it names one, so whether the
# font draws ௐ (and so whether ௗ is 165 or 166) is exactly what is not known.
# The cost of that is ௌ, which this font draws the way it draws ொ, out of a
# ெ in front of the letter and a length mark behind it - a syllable no
# document of this corpus writes. The rest are ligatures of the kind 284 is,
# and the same holds for them: nothing says what they are, and a glyph left
# alone loses an improvement where a glyph read wrongly destroys the text
# around it.
#
# This font is deliberately absent from BROKEN_FONT_GLYPH_COUNTS below, for
# the reason TAU Elango is: the corpus carries it in 327 glyphs and in
# truncated subsets of 305, 283, 281, 280, 278, 277, 276, 275, 272 and fewer,
# and that subsetter only ever drops the glyphs off the end. Of the 1,363
# subsets of that face read out of those 1,072 documents, exactly one glyph
# disagrees with the rest about what it draws - 267, in a file that names
# itself both -03 and -01, which is the second typeface drawing its own சூ in
# the same slot

# TAU-Marutham, the third tamil of the Tamil Nadu gazette - 163 of the 8,248
# documents of that corpus draw 281,061 glyphs in it, very often beside
# TAM_ELANGO_Panchali on the same page.
#
# It is broken a way of its own, and the fault is not in the map alone: this
# producer re-encodes the font. It carries one font over and over in a single
# document - six times in test/test_pdfs/tamil-marutham.pdf, as
# Type0/Identity-H fonts with a ToUnicode map of their own and as simple
# TrueType fonts with WinAnsiEncoding or MacRomanEncoding and no ToUnicode at
# all - and it hands each subset whatever latin bytes it needs, a byte per
# glyph in the order that document happened to want them. So the cmap of a
# subset says where the producer put a glyph and not what the glyph draws,
# and the same latin letter means a different glyph in the next subset of the
# same document: 'k' is கு in one of them and கூ in the next, 'r' is ரி in
# one and ரு in the next. The simple fonts therefore extract as that latin
# (த is 't', வி is 'v'), and the identity encoded ones extract as tamil with
# holes in it, their maps naming the letters and the pulli forms and handing
# every syllable the font draws as one glyph either one of those latin
# letters or nothing at all - அச்சகத் தொழிலில் comes out as
# "அச்சகத் ெதா\x89lல்". A few of them carry no map at all and extract as
# (cid:N) throughout, which fix_font builds a whole map for.
#
# Nothing at the level of the extracted text can undo that, which is why this
# font is repaired here rather than decoded in fonts/tamil/ the way the
# legacy 8 bit TAM_ELANGO_Panchali is: a decoder reads characters, and here
# one character is two different glyphs in one document. It is also why the
# font is named in RE_ENCODED_FONTS below - what a subset of it says about
# its own glyphs, through its cmap or through the names in its post table, is
# the producer's arbitrary encoding and has to be ignored, where for every
# other font here it is the one thing that can be trusted.
#
# The whole font is 423 glyphs and it lays them out in blocks:
#
#   0..48      the macintosh standard glyph order as far as '@' and then the
#              ascii punctuation that follows the capitals, the latin
#              letters themselves being at 260 and 286
#   49..95     the tamil block, one glyph per assigned codepoint of it in
#              codepoint order and skipping ஶ, which this font draws no more
#              than Uni-Ila.Sundaram does
#   96..119    a second க at 97 and the dashes, the quotes and the ellipsis
#              from 111
#   120..141   every consonant with the vowel sign i written into it
#   142..163   the same with the sign ii
#   164..182   the sign u, over the eighteen tamil consonants and ஜ
#   183..201   the same with the sign uu
#   202..211   ligatures, of which only ஸ்ரீ at 208 is ever drawn
#   212..235   every consonant with a pulli on it
#   260..285   'A' to 'Z', and 286..311 'a' to 'z'
#
# The two blocks that are drawn into a letter run through the 22 consonants
# in codepoint order, as Uni-Ila.Sundaram's do; the pulli block runs through
# the eighteen in the order the script itself lists them, as TAU Elango's do.
# That the one font should lay its blocks out both ways is not a reading of
# the order - the maps of this corpus name 216 ட், 220 ப் and 229 ன், which
# is the script's order, and 128 நி, 129 னி and 130 பி, which is codepoint
# order - and the glyphs were rendered and read either way round to be sure
# of it.
#
# Every reading was rendered out of the embedded subsets and read against the
# pages that draw them, and the maps corroborate them: of the ~190 glyph ids
# any map of this corpus names, all but fifteen carry the reading these
# blocks give, and every one of the fifteen is the pairing slip TAU Elango's
# map has - a ெ handed the வ it was drawn in front of, a ண handed the ை.
# Repaired and put in order, six pages of test/test_pdfs/tamil-marutham.pdf
# match a tesseract -l tam ocr of the same pages on 812 of their 861 distinct
# tamil words, and not one of the 49 that differ is mis-read: they are words
# the ocr itself got wrong.

# the letters the u and uu blocks of this font are drawn over: the 22
# consonants of the codepoint block without ஷ, ஸ and ஹ, which is the
# eighteen letters of tamil proper and ஜ
MARUTHAM_U_CONSONANTS = [char for char in TAMIL_CONSONANTS_NO_SHA \
                         if char not in (TAMIL_UNICODE['SSA'],  \
                                         TAMIL_UNICODE['SA'],   \
                                         TAMIL_UNICODE['HA'])]

TAU_MARUTHAM = {49 + i: char \
                for i, char in enumerate(TAMIL_CODEPOINTS_NO_SHA)}
# the two vowel signs the font draws into a letter, over the same 22
# consonants Uni-Ila.Sundaram draws them into
TAU_MARUTHAM.update( \
    tamil_block(120, TAMIL_CONSONANTS_NO_SHA, TAMIL_UNICODE['MATRA_I']))
TAU_MARUTHAM.update( \
    tamil_block(142, TAMIL_CONSONANTS_NO_SHA, TAMIL_UNICODE['MATRA_II']))
# the signs u and uu. Unlike every other font here this one draws them into
# ஜ as well as into the eighteen letters of tamil proper, which codepoint
# order puts in the middle of those eighteen - 166 is சு and 169 டு, so the
# two glyphs between them are ஜு and ஞு. The other three grantha letters
# take the two signs as glyphs of their own, somewhere this corpus does not
# draw
TAU_MARUTHAM.update( \
    tamil_block(164, MARUTHAM_U_CONSONANTS, TAMIL_UNICODE['MATRA_U']))
TAU_MARUTHAM.update( \
    tamil_block(183, MARUTHAM_U_CONSONANTS, TAMIL_UNICODE['MATRA_UU']))
# the pulli forms, which run through the eighteen letters in the order the
# script lists them and then the grantha ones in an order of the font's own:
# ஸ் at 230, ஷ் at 232 and ஜ் at 233, read off the glyphs themselves. What
# 231 draws is not known - no subset of this corpus carries a glyph for it -
# and neither is what follows ஜ், so ஹ் and க்ஷ் are left out with it
TAU_MARUTHAM.update( \
    tamil_block(212, TAMIL_CONSONANTS + [TAMIL_UNICODE['SA']], \
                TAMIL_UNICODE['PULLI']))
# the latin and the punctuation of the font, which it lays out in the
# macintosh standard glyph order as far as '@' and then carries on with the
# ascii punctuation that follows the capitals, the letters themselves being
# at 260 and 286. Every map of this corpus that names one of these names it
# what this says, bar the two double quotes, which one producer numbers as
# the two codepoints that follow ‘ and ’ rather than as the quotes the font
# draws - the same producer that writes ஋ for எ, counting codepoints through
# the gaps the tamil block leaves.
#
# They are here because a subset that carries no map at all needs a whole
# one built for it, and a map naming only the tamil would leave its digits,
# its spaces and its punctuation extracting as the control characters of
# their glyph ids - 13 of the 14 subsets of
# tamilnadu/2023-03-28/Extraordinary_104_Part-IV_Section-1.pdf are carried
# that way. Where a subset does carry a map they change nothing
ASCII_PUNCTUATION = ' !"#$%&\'()*+,-./0123456789:;<=>?@'

TAU_MARUTHAM.update( \
    {3 + i: char for i, char in enumerate(ASCII_PUNCTUATION)})
TAU_MARUTHAM.update( \
    {36 + i: char for i, char in enumerate('[\\]^_`{|}~')})
TAU_MARUTHAM.update( \
    {260 + i: chr(ord('A') + i) for i in range(26)})
TAU_MARUTHAM.update( \
    {286 + i: chr(ord('a') + i) for i in range(26)})
TAU_MARUTHAM.update({ \
    # the dashes, the quotes and the ellipsis. 112 is drawn nowhere and
    # named by no map, so it is left out and 111 does not run into it \
    111: '–', 113: '‘', 114: '’', 115: '“', 116: '”', 117: '…', \
})
TAU_MARUTHAM.update({ \
    # a second க, and the one glyph of this font that is a composite: it is
    # the outline of 62 shifted 277 units to the right, the wide form of the
    # letter that the gazette sets after a ை. அறிவிக்கை is drawn
    # அ றி வி க் ை 97 \
    97 : TAMIL_UNICODE['KA'],  \
    # ஸ்ரீ, which the font draws as a single glyph of its own \
    208: TAMIL_UNICODE['SHRI'], \
    232: TAMIL_UNICODE['SSA'] + TAMIL_UNICODE['PULLI'], \
    233: TAMIL_UNICODE['JA']  + TAMIL_UNICODE['PULLI'], \
})

# What this table leaves out is 46..48, 96, 98..110, 112, 118, 119, 202..211,
# 231 and everything from 234 to 259: no subset of this corpus carries a
# glyph anywhere in those ranges and no map of it names one, so nothing says
# what they are. 231 is the one that is missed - the pulli block is 24 wide
# where the eighteen letters and ஸ், ஷ் and ஜ் account for 21 of it, so the
# grantha part of it runs in an order of the font's own with one slot before
# ஷ் that this corpus never draws.
#
# This font is deliberately absent from BROKEN_FONT_GLYPH_COUNTS below, for
# the reason TAU Elango is: the corpus carries it in a full 423 glyph subset
# in 284 of the 380 font instances read out of those documents and in
# truncated subsets of 295, 288, 230, 229, 225, 222, 186, 39, 29, 25 and 24
# glyphs in the rest, and that subsetter drops the glyphs off the end without
# renumbering what it keeps. The subsets are drawn at different scales, so
# they are compared by the proportions of their glyphs rather than by their
# coordinates: of the glyphs a short subset shares with a 423 glyph one,
# every one of the tamil ones has the same proportions and only a handful of
# the small punctuation marks - a comma, a period, a bracket - measure
# differently. Their maps agree too, naming the glyphs they name what this
# table does. The faces are folded together by font_lookup_key and share the
# order as well: of the glyph ids TAU-Marutham-Bold's maps name, all 11 carry
# this table's reading, and of TAU---Marutham's - a third spelling of the
# same name - 46 of 60 do, the fourteen that do not being the same pairing
# slip again.
#
# One embedding is beyond this. tamilnadu/2023-03-28/Extraordinary_104_Part-
# IV_Section-1.pdf names a font TAU-Marutham-Identity-H, which font_lookup_key
# keeps apart from the family, and carries 1,559 bytes for it that are not a
# font program at all - so nothing says the glyph ids of that embedding are
# this font's, and its 80 glyphs are left as the pdf has them.

# Mangal is repaired by what its glyphs draw and not by their glyph ids, see
# MANGAL_OUTLINES below, so it has no table of its own here. The entry is
# what puts the font on the list of the ones that are repaired at all
MANGAL = {}

# The Mangal of these gazettes is subsetted with a map that hands a glyph the
# shaper made <0000> outright - not the wrong character, no character at all -
# so 3234 glyphs of a 31 page gazette extract as a NUL that is not even well
# formed xml. The subset keeps neither a cmap nor a post nor a GSUB, only the
# outlines, so there is nothing in it to read the glyphs back out of and the
# table below is the whole of what is known about them.
#
# It is keyed by what a glyph draws and not by its glyph id, because this
# subset renumbers its glyphs: the id of a glyph here is a number the producer
# gave it and means something else in the next document, while an outline is
# the same wherever the same font is subsetted. Keying by outline is also what
# makes the table safe - a subset that draws something else is simply not
# matched, rather than being handed the characters of a glyph it does not have.
#
# The readings were established by lining the glyph stream of the pdf up
# against an ocr of the same pages, each one recorded below with the word it
# was read in.
MANGAL_OUTLINES = { \
    # the width variants of matra_i, which the font draws to the left of the \
    # consonant they belong to \
    '233a733e6b03a9a7': 'ि',                # gid 9, seen in वाहिनी \
    '745fe5bd181e6cc3': 'ि',                # gid 24, seen in निम्नलिखित \
    'e64b5d043ea51c85': 'ि',                # gid 26, seen in प्रादेशिक \
    '6a77510666defc45': 'ि',                # gid 28, seen in निम्नलिखित \
    'ff00bd70814fa8c8': 'ि',                # gid 31, seen in अधिकारियों \
    'df9cda2ad9aa1d9b': 'ि',                # gid 33, seen in अधिकारियों \
    'f4a20fa72af9f09b': 'ि',                # gid 81, seen in गोविन्दराज \
    'bb9d7ee07e3e10d0': 'ि',                # gid 95, seen in ग्रनेडियर्स \
    '8d8a9accdd8a6e7e': 'ि',                # gid 96, seen in बिहार \
    '9d67d0f6f101bab9': 'ि',                # gid 103, seen in किशोर \
    # the width variants of matra_ii \
    '18f71f0bf42961ec': 'ी',                # gid 42, seen in सोलंकी \
    'b9c2883268791fe8': 'ी',                # gid 56, seen in फरवरी \
    # the half forms, the consonant and its halant drawn as one glyph \
    '4d3220112544804c': 'म्',               # gid 15, seen in नवम्बर \
    '94fbc6be8858a3a3': 'ष्',               # gid 21, seen in राष्ट्रपति \
    '67ee8428d64f973b': 'न्',               # gid 40, seen in पदोन्नति \
    'ef848c5e1d8722b2': 'क्',               # gid 63, seen in अक्टूबर \
    '3da0a4696801a385': 'स्',               # gid 71, seen in अगस्त \
    '8b86b3a561de9f6d': 'ब्',               # gid 75, seen in डब्ल्यू \
    '8b987d39b172bb73': 'श्',               # gid 85, seen in घनश्याम \
    '261ac6a6ad743b16': 'ड्',               # gid 87, seen in वालागड्डे \
    'd79e3821cab531ef': 'त्',               # gid 91, seen in उत्तम \
    '4f76f7ab7fde5b03': 'ज्',               # gid 98, seen in ज्योति \
    'dad21a41912d1d3c': 'ण्',               # gid 100, seen in एण्ड \
    '46c3c918364e13c9': 'च्',               # gid 112, seen in पच्चापन \
    '2e7690bab3d4fb93': 'थ्',               # gid 115, seen in पृथ्वी \
    '2e5b528112122ebd': 'ग्',               # gid 119, seen in भोनडग्गे \
    'b4251e5faf4c6810': 'द्',               # gid 120, seen in द्वेदी \
    'a8905cf229fac9e9': 'ह्',               # gid 121, seen in ब्रह्म \
    'bb3012ff1fb05d86': 'ध्',               # gid 123, seen in उपाध्याय \
    '47dd06fac6a101c4': 'क्ष्',             # gid 124, seen in लक्ष्मण \
    # the glyphs the shaper made out of a whole cluster \
    '53962e9d48c1e61a': 'ट्र',              # gid 22, seen in राष्ट्रपति \
    'cda166ec7f48543e': 'प्र',              # gid 45, seen in प्रदान \
    'b62c67cd69b449d8': 'द्र',              # gid 77, seen in सुरेन्द्र \
    '929ba8f2772ebf69': 'प्प',              # gid 80, seen in कोनडाप्पा \
    '4f08418e9b5afbe2': 'श्र',              # gid 83, seen in श्रीकान्त \
    '914a0f0cb0945287': 'ग्र',              # gid 94, seen in ग्रनेडियर्स \
    'e73330abe626649e': 'त्र',              # gid 101, seen in त्रिलोचन \
    '01e9507d182e386b': 'क्र',              # gid 102, seen in चक्रधारा \
    'e1e6473771b38f04': 'द्ध',              # gid 104, seen in सिद्धू \
    'd8b5ec6855202b02': 'ट्ट',              # gid 105, seen in भट्ट \
    '0abd7f1fa796d21b': 'ब्र',              # gid 109, seen in अब्राहम \
    '2b2a2e17f2b9bfa0': 'द्द',              # gid 122, seen in योद्द \
    # the reph, which the font draws after the whole syllable it sits on \
    '231a9cfbb99c138f': 'र्',               # gid 39, seen in सहर्ष \
    # the reph and the matra of the syllable it sits on, drawn as one glyph \
    '9b014eadb17fd075': 'ीर्',              # gid 54, seen in आर्मी \
    'e3f6f3fc3233e883': 'ेर्',              # gid 110, seen in कुर्रे \
    # a matra and the anusvara of its syllable, drawn as one glyph \
    '51337a819da041b0': 'ों',               # gid 35, seen in अधिकारियों \
    '01bcb2133e589127': 'ैं',               # gid 46, seen in रैंक \
    'f7c9a3a95b373c83': 'ें',               # gid 111, seen in वेंकटेश \
    # a vowel and its anusvara, drawn as one glyph \
    'b240fc4583c5ca08': 'ईं',               # gid 90, seen in ईंगलेश्वर \
    # the ra with its matra_u, and the two letters of a name drawn as one \
    '0b52abc5e77e9e39': 'रू',               # gid 86, seen in अरूण \
    '79ff8103748e6385': 'ल्यू',             # gid 76, seen in डब्ल्यू \
}

BROKEN_FONTS = {'Arial Unicode MS'  : ARIAL_UNICODE_MS,   \
                'Nirmala UI'        : NIRMALA_UI,         \
                'Mangal'            : MANGAL,             \
                # the weights of the unicode Nudi, which a pdf names
                # apart and which share one glyph order, see
                # NUDI_UNI_GLYPH_COUNT \
                'NudiUni01e'        : NUDI_UNI_KANNADA,   \
                'NudiUni01k'        : NUDI_UNI_KANNADA,   \
                'NudiUni02e'        : NUDI_UNI_KANNADA,   \
                'NudiUniAnanth05e'  : NUDI_UNI_KANNADA,   \
                # the tamil of the Tamil Nadu gazette. Only this face of
                # the TAU Elango family carries a broken map - the text of
                # TAUElangoPanchali-SC700 and of TAUElangoValluvan extracts
                # correctly, and font_lookup_key keeps all three apart
                'TAUElangoPanchali' : TAU_ELANGO_PANCHALI, \
                # the other tamil of the same gazette. The faces of this
                # family draw typefaces of their own and share one glyph
                # order, so one table serves them all - they are named one
                # by one because font_lookup_key keeps a face number, which
                # is what keeps TAUElangoPanchali-SC700 (whose map is sound)
                # apart from TAUElangoPanchali above. Here the SC700 face
                # carries the same broken map as the rest and is repaired
                # with them \
                'Uni-Ila.Sundaram-01'      : UNI_ILA_SUNDARAM, \
                'Uni-Ila.Sundaram-03'      : UNI_ILA_SUNDARAM, \
                'Uni-Ila.Sundaram-03-SC700': UNI_ILA_SUNDARAM, \
                'Uni-Ila.Sundaram-04'      : UNI_ILA_SUNDARAM, \
                'Uni-Ila.Sundaram-07'      : UNI_ILA_SUNDARAM, \
                # the third tamil of the same gazette. The bold and the
                # third spelling of the name are folded into this key by
                # font_lookup_key; the SC700 face is a key of its own and
                # is named beside it because its map carries the same
                # breakage rather than the sound one TAUElangoPanchali-
                # SC700's does \
                'TAU-Marutham'             : TAU_MARUTHAM, \
                'TAU-Marutham-SC700'       : TAU_MARUTHAM}

# the glyphs to repair by what they draw rather than by their glyph id, for a
# font whose subsets are renumbered - see MANGAL_OUTLINES above
BROKEN_FONT_OUTLINES = {'Mangal': MANGAL_OUTLINES}

# the fonts whose subsets are re-encoded by the producer, so that nothing a
# subset of them says about its own glyphs can be believed. Every other font
# here is repaired out of the font program first and out of a hand table only
# where the font says nothing - the cmap of a subset maps a character to the
# glyph that draws it, and that is the one thing in a broken pdf that is not
# broken. This producer instead hands each subset whatever latin bytes it
# needs, a byte per glyph in the order that document wanted them, so its
# cmap maps a character to a glyph that draws something else entirely and
# would beat the table that does know: gid 164 is கு and the cmap of one
# subset of test/test_pdfs/tamil-marutham.pdf calls it 'k'. For these fonts
# the hand table is all there is - see TAU_MARUTHAM above
RE_ENCODED_FONTS = {'TAU-Marutham', 'TAU-Marutham-SC700'}

# the glyph count of the font program a hand table above was read from, for a
# font that this corpus carries in more than one numbering. A subset that
# keeps the glyph order of the font it was cut out of counts all of that
# font's glyphs, so every subset of the font the table was read from matches
# this and every subset of another numbering of the same family does not -
# see glyph_count, which uses the count for the same question about the
# glyphs one subset donates to another.
#
# A font that is not named here has no such constraint, which is not a claim
# that its ids are safe everywhere - only that this corpus has never carried
# it in a second numbering. Nirmala UI is carried in four
BROKEN_FONT_GLYPH_COUNTS = {'Nirmala UI'      : NIRMALA_UI_GLYPH_COUNT, \
                            'NudiUni01e'      : NUDI_UNI_GLYPH_COUNT,  \
                            'NudiUni01k'      : NUDI_UNI_GLYPH_COUNT,  \
                            'NudiUni02e'      : NUDI_UNI_GLYPH_COUNT,  \
                            'NudiUniAnanth05e': NUDI_UNI_GLYPH_COUNT}

# the font whose glyph ids a type3 font of a distilled gazette names its
# glyphs after, see fix_type3_fonts below
TYPE3_GLYPH_FONT = 'Arial Unicode MS'

# the encodings of a simple font that a byte can be read back through, and
# the python codec of each. A font encoded one of these ways is not addressed
# by glyph id at all - the byte in the content stream is looked up in the
# encoding and an extractor hands out the character it finds there - so a
# re-encoded one needs a map of its own, see fix_simple_font
SIMPLE_ENCODING_CODECS = {'WinAnsiEncoding'  : 'cp1252', \
                          'MacRomanEncoding' : 'mac_roman'}

def encoding_chars(codec):
    '''the character that an encoding gives each of its bytes, as a
       byte -> character dict, leaving out the bytes it defines none for'''
    chars = {}
    for byte in range(256):
        try:
            chars[byte] = bytes([byte]).decode(codec)
        except UnicodeDecodeError:
            pass
    return chars

SIMPLE_ENCODING_CHARS = {name: encoding_chars(codec) \
                         for name, codec in SIMPLE_ENCODING_CODECS.items()}
# the byte that each of those characters lives on, the way back
SIMPLE_ENCODINGS      = {name: {char: byte for byte, char in chars.items()} \
                         for name, chars in SIMPLE_ENCODING_CHARS.items()}

# the text of a repaired font carries the characters that are really there,
# but still in the order in which the glyphs are drawn, so it has to go
# through this converter of indic2unicode and not through the one that is
# named after the font, which is for the text of a pdf that was not repaired
FONT_CONVERTERS = {'Arial Unicode MS'  : 'arialuni_glyphs',   \
                   'Nirmala UI'        : 'nirmalaui_glyphs', \
                   'Mangal'            : 'mangal_glyphs',    \
                   'NudiUni01e'        : 'nudiuni_glyphs',   \
                   'NudiUni01k'        : 'nudiuni_glyphs',   \
                   'NudiUni02e'        : 'nudiuni_glyphs',   \
                   'NudiUniAnanth05e'  : 'nudiuni_glyphs',  \
                   'TAUElangoPanchali' : 'tauelango_glyphs', \
                   'Uni-Ila.Sundaram-01'      : 'ilasundaram_glyphs', \
                   'Uni-Ila.Sundaram-03'      : 'ilasundaram_glyphs', \
                   'Uni-Ila.Sundaram-03-SC700': 'ilasundaram_glyphs', \
                   'Uni-Ila.Sundaram-04'      : 'ilasundaram_glyphs', \
                   'Uni-Ila.Sundaram-07'      : 'ilasundaram_glyphs', \
                   'TAU-Marutham'             : 'marutham_glyphs',    \
                   'TAU-Marutham-SC700'       : 'marutham_glyphs'}

# the styles of a family, which a pdf carries as fonts of their own named
# "Nirmala UI,Bold" or "NirmalaUI-Bold"
STYLE_SUFFIX_RE = re.compile(r'(bold|italic|oblique|regular|light|medium'  \
                             r'|semibold|black|condensed)+$')

def font_lookup_key(fontname):
    '''one font is embedded under more than one spelling of its name, Arial
       Unicode MS is carried both as "Arial Unicode MS" and as
       "ArialUnicodeMS", so a font is looked up by a spelling of its name
       that the separators and the case do not change. The bold of a family
       is drawn with the same glyphs as its regular and carries the same
       broken map, so it is looked up as the family too, and a subset is
       looked up as the font it is a subset of'''
    fontname = re.sub(r'^[A-Z]{6}\+', '', fontname)
    key = re.sub(r'[\s\-_,]+', '', fontname.split(',')[0]).lower()
    return STYLE_SUFFIX_RE.sub('', key) or key

BROKEN_FONTS_BY_KEY    = {font_lookup_key(name): fixes \
                          for name, fixes in BROKEN_FONTS.items()}
BROKEN_OUTLINES_BY_KEY = {font_lookup_key(name): fixes \
                          for name, fixes in BROKEN_FONT_OUTLINES.items()}
BROKEN_COUNTS_BY_KEY   = {font_lookup_key(name): count \
                          for name, count in BROKEN_FONT_GLYPH_COUNTS.items()}
FONT_CONVERTERS_BY_KEY = {font_lookup_key(name): conv  \
                          for name, conv  in FONT_CONVERTERS.items()}
RE_ENCODED_BY_KEY      = {font_lookup_key(name) for name in RE_ENCODED_FONTS}

# the lookups of a GSUB that say what a glyph was made of, and the wrapper
# that a font of this size keeps them in
SINGLE_SUBST     = 1
LIGATURE_SUBST   = 4
EXTENSION_LOOKUP = 7

HALANT = '्'

# the features that make a form which is written as a halant and then its
# consonant - the below base, post base and pre base forms - and the ones
# that make a form which is written the other way round, the half forms and
# the reph
BELOW_FORM_FEATURES = frozenset(['blwf', 'pstf', 'pref'])
HALF_FORM_FEATURES  = frozenset(['half', 'rphf'])

def get_glyph_fixes(fontname):
    '''the glyphs to repair by hand for a font known to carry a broken map,
       None for every other font'''
    return BROKEN_FONTS_BY_KEY.get(font_lookup_key(fontname))

def get_outline_fixes(fontname):
    '''the glyphs to repair by their outline for a font whose subsets do not
       number their glyphs alike, an empty dict for every other font'''
    return BROKEN_OUTLINES_BY_KEY.get(font_lookup_key(fontname), {})

def get_glyph_fixes_count(fontname):
    '''the glyph count that the hand table of a font holds for, None for a
       font whose table is not held to one'''
    return BROKEN_COUNTS_BY_KEY.get(font_lookup_key(fontname))

def trusts_own_glyphs(fontname):
    '''whether what a subset of a font says about its own glyphs - its cmap,
       the names in its post table - is about the glyphs at all, or is the
       producer's own encoding of them, see RE_ENCODED_FONTS'''
    return font_lookup_key(fontname) not in RE_ENCODED_BY_KEY

def get_font_converter(fontname):
    '''the converter that puts the text of a repaired font in the order that
       unicode wants, None if there is none for it'''
    return FONT_CONVERTERS_BY_KEY.get(font_lookup_key(fontname))

class ToUnicodeFixer:
    def __init__(self):
        self.logger = logging.getLogger('fix_tounicode')
        # the fonts of the last document that were actually repaired
        self.fixed_fonts = set()
        # the font program of a pdf font, read once per font
        self.fontcache   = {}
        # what the font program of a pdf font names its own glyphs, read
        # once per font
        self.seedcache   = {}
        # the outline of a glyph of a pdf font, read once per glyph
        self.sigcache    = {}

    def to_nfc(self, ustr):
        '''a string in the form unicode composes it in. A nukta consonant
           comes out of this as its consonant and a nukta, which is the
           canonical form of it'''
        return unicodedata.normalize('NFC', ustr)

    def base_font(self, fontname):
        # a subsetted font is named like ABCDEE+Arial Unicode MS
        if len(fontname) > 7 and fontname[6] == '+':
            fontname = fontname[7:]
        return fontname

    def get_cmap_xref(self, doc, xref):
        key, val = doc.xref_get_key(xref, 'ToUnicode')
        if key != 'xref':
            return None
        return int(val.split()[0])

    def parse_cmap(self, doc, cmapxref):
        '''the code -> string map that the pdf carries'''
        cmap = doc.xref_stream(cmapxref).decode('latin-1')

        def to_str(hexstr):
            return bytes.fromhex(hexstr).decode('utf-16-be')

        table = {}
        for match in re.finditer(r'beginbfchar(.*?)endbfchar', cmap, re.S):
            for src, dst in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', \
                                       match.group(1)):
                table[int(src, 16)] = to_str(dst)

        for match in re.finditer(r'beginbfrange(.*?)endbfrange', cmap, re.S):
            body = match.group(1)
            # <lo> <hi> [<dst> <dst> ...]
            for lo, hi, array in re.findall(\
                    r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*\[(.*?)\]', body, re.S):
                for i, dst in enumerate(re.findall(r'<([0-9a-fA-F]+)>', array)):
                    table[int(lo, 16) + i] = to_str(dst)
            # <lo> <hi> <dst>, the last code unit of dst counts up
            body = re.sub(r'<[0-9a-fA-F]+>\s*<[0-9a-fA-F]+>\s*\[.*?\]', ' ', \
                          body, flags = re.S)
            for lo, hi, dst in re.findall(\
                    r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', body):
                lo, hi = int(lo, 16), int(hi, 16)
                units  = [dst[i:i+4] for i in range(0, len(dst), 4)]
                base   = int(units[-1], 16)
                for code in range(lo, hi + 1):
                    last = '%04X' % (base + code - lo)
                    table[code] = to_str(''.join(units[:-1] + [last]))
        return table

    def build_cmap(self, table):
        lines = ['/CIDInit /ProcSet findresource begin', '12 dict begin',   \
                 'begincmap', '/CMapName /Adobe-Identity-UCS def',          \
                 '/CMapType 2 def', '1 begincodespacerange',                \
                 '<0000> <FFFF>', 'endcodespacerange']

        items = sorted(table.items())
        # a cmap may hold at most 100 entries in one bfchar section
        for i in range(0, len(items), 100):
            chunk = items[i:i+100]
            lines.append('%d beginbfchar' % len(chunk))
            for code, ustr in chunk:
                lines.append('<%04X> <%s>' % \
                             (code, ustr.encode('utf-16-be').hex().upper()))
            lines.append('endbfchar')

        lines.extend(['endcmap',                                       \
                      'CMapName currentdict /CMap defineresource pop', \
                      'end', 'end'])
        return ('\n'.join(lines) + '\n').encode('latin-1')

    def open_font(self, doc, xref):
        '''the font program that the pdf carries for a font, None if there
           is none or it cannot be read'''
        if xref in self.fontcache:
            return self.fontcache[xref]

        font = None
        try:
            name, ext, ftype, buf = doc.extract_font(xref, named = False)
        except Exception as e:
            self.logger.warning('Could not extract the font %d: %s', xref, e)
            buf = None

        if buf:
            try:
                font = TTFont(io.BytesIO(buf), fontNumber = 0, lazy = True)
            except Exception as e:
                self.logger.warning('Could not read the font %d: %s', xref, e)

        self.fontcache[xref] = font
        return font

    def glyph_names(self, doc, xref):
        '''the name that the font gives to every one of its glyphs'''
        font = self.open_font(doc, xref)
        if font == None:
            return []

        try:
            return font.getGlyphOrder()
        except Exception as e:
            self.logger.warning('Could not read the glyphs of %d: %s', xref, e)
            return []

    # ------------------------------------------------------------------
    # what the font says its own glyphs are
    #
    # The map that the pdf carries is broken, but the font program that it
    # carries with it is not, and it says what its glyphs are three times
    # over: the cmap of the subset maps a character to the glyph that draws
    # it, the subset keeps the uniXXXX name of the glyphs it did not have to
    # rename, and the GSUB of the font says which glyphs the shaper made out
    # of which other ones. The first two are read straight off, the third is
    # followed until nothing more can be spelled out: a conjunct is the
    # string of the glyphs it was made of, a half form is its consonant and
    # a halant, and a below base form is a halant and its consonant, which
    # is the order they are written in.
    # ------------------------------------------------------------------

    def glyph_seed_strings(self, doc, xref):
        '''the glyphs of a font whose character the font names outright, as
           a glyph id -> string dict'''
        if xref in self.seedcache:
            return self.seedcache[xref]

        strings = {}
        font    = self.open_font(doc, xref)
        if font == None:
            self.seedcache[xref] = strings
            return strings

        try:
            order = font.getGlyphOrder()
            cmap  = font.getBestCmap() or {}
        except Exception as e:
            self.logger.warning('Could not read the cmap of the font %d: %s', \
                                xref, e)
            self.seedcache[xref] = strings
            return strings

        gids = {gname: gid for gid, gname in enumerate(order)}

        for code, gname in cmap.items():
            gid = gids.get(gname)
            if gid != None:
                strings.setdefault(gid, self.to_nfc(chr(code)))

        for gid, gname in enumerate(order):
            ustr = self.unicode_glyph_name(gname)
            if ustr != None:
                strings.setdefault(gid, ustr)

        self.seedcache[xref] = strings
        return strings

    def gsub_lookups(self, font):
        '''the substitutions of the GSUB of a font that say what a glyph was
           made of, as (lookup type, subtable, feature tags) with the
           extension lookups unwrapped. A lookup is taken on its own and
           the context it is used in is not looked at: what is wanted here
           is only which glyph stands for which characters, and a glyph that
           one context makes out of a cluster is that cluster in every
           other context too'''
        lookups = []

        if 'GSUB' not in font:
            return lookups

        try:
            gsub = font['GSUB'].table
            if gsub == None or gsub.LookupList == None:
                return lookups

            tags = {}
            if gsub.FeatureList != None:
                for record in gsub.FeatureList.FeatureRecord:
                    for index in record.Feature.LookupListIndex:
                        tags.setdefault(index, set()).add(record.FeatureTag)

            for index, lookup in enumerate(gsub.LookupList.Lookup):
                for subtable in lookup.SubTable:
                    if lookup.LookupType == EXTENSION_LOOKUP:
                        ltype    = subtable.ExtensionLookupType
                        subtable = subtable.ExtSubTable
                    else:
                        ltype = lookup.LookupType

                    if ltype in (SINGLE_SUBST, LIGATURE_SUBST):
                        lookups.append((ltype, subtable, tags.get(index, set())))
        except Exception as e:
            self.logger.warning('Could not read the GSUB of a font: %s', e)

        return lookups

    def substituted_string(self, parts, tags):
        '''the string of the glyph that a substitution made out of the
           glyphs whose strings these are'''
        # a half form and a reph are their consonant and a halant, which is
        # how they are written; a below base, post base or pre base form is
        # a halant and its consonant, the other way round. A substitution
        # that takes the halant in as a glyph of its own already carries it,
        # one that leaves it to the context has to be given it
        if tags & BELOW_FORM_FEATURES:
            if len(parts) == 2 and parts[1] == HALANT:
                return HALANT + parts[0]
            if len(parts) == 1:
                return HALANT + parts[0]
        elif tags & HALF_FORM_FEATURES and len(parts) == 1:
            return parts[0] + HALANT

        return ''.join(parts)

    def expand_gsub(self, font, strings):
        '''spell out every glyph that the shaper made out of the glyphs it
           was made of, until no more of them can be spelled out'''
        try:
            order = font.getGlyphOrder()
        except Exception:
            return strings

        gids    = {gname: gid for gid, gname in enumerate(order)}
        lookups = self.gsub_lookups(font)
        num     = 0

        while True:
            found = 0

            for ltype, subtable, tags in lookups:
                if ltype == SINGLE_SUBST:
                    pairs = [([source], target) for source, target \
                             in getattr(subtable, 'mapping', {}).items()]
                else:
                    pairs = []
                    for first, ligatures in \
                            getattr(subtable, 'ligatures', {}).items():
                        for ligature in ligatures:
                            pairs.append(([first] + list(ligature.Component), \
                                          ligature.LigGlyph))

                for sources, target in pairs:
                    gid = gids.get(target)
                    if gid == None or gid in strings:
                        continue

                    parts = [strings.get(gids.get(source, -1)) \
                             for source in sources]
                    if None in parts:
                        continue

                    strings[gid] = self.to_nfc(\
                                       self.substituted_string(parts, tags))
                    found += 1

            num += found
            if not found:
                break

        if num:
            self.logger.debug('%d glyph(s) spelled out of the GSUB of the ' \
                              'font', num)
        return strings

    def glyph_count(self, doc, xref):
        '''how many glyphs the font program of a pdf font has.

           Two subsets of one font number their glyphs alike when both keep
           the glyph order of the font they were cut out of, and a subset
           that does keep it counts all of that font's glyphs however few it
           actually carries - the two styles of Nirmala UI in
           test/test_pdfs/gazette1.pdf both count 4923. A subset that
           renumbers what it kept counts only what it kept, so a difference
           here says the two number their glyphs differently and neither can
           be read through the other's ids: the Mangal of a 223221 gazette is
           carried both as a subset of 886 glyphs and as one of 136.

           Outlines cannot answer this. The bold of a family draws every
           glyph differently from its regular and still numbers them alike,
           so holding a donation to a matching outline would refuse exactly
           the sharing that font_lookup_key folds the styles together for'''
        font = self.open_font(doc, xref)
        if font == None:
            return None

        try:
            return font['maxp'].numGlyphs
        except Exception as e:
            self.logger.debug('Could not read the glyph count of the font ' \
                              '%d: %s', xref, e)
            return None

    def glyph_signature(self, doc, xref, gid):
        '''what the glyph of an id draws, as a signature of its outline.

           Two subsets of one font number their glyphs alike only sometimes:
           a subset that keeps the glyph ids of the font it came out of does,
           one that renumbers what it kept does not, and nothing in the pdf
           says which of the two a subset is. What a glyph draws is the same
           either way, so it is the outline and not the id that says whether
           the glyph of an id in one subset is the glyph of that id in
           another. Composites are decomposed, since their components are
           renumbered with everything else.

           None for a glyph the font does not have, the empty string for one
           it draws nothing for - a space is a space in every subset'''
        cached = self.sigcache.get((xref, gid))
        if cached != None:
            return cached

        font = self.open_font(doc, xref)
        if font == None:
            return None

        try:
            order = font.getGlyphOrder()
            if gid < 0 or gid >= len(order):
                return None

            glyphset = font.getGlyphSet()
            pen      = DecomposingRecordingPen(glyphset)
            glyphset[order[gid]].draw(pen)

            outline = [(op, tuple(tuple(round(c) for c in point)          \
                                  for point in points if point != None))  \
                       for op, points in pen.value]
            sig = hashlib.sha1(repr(outline).encode()).hexdigest()[:16]   \
                  if outline else ''
        except Exception as e:
            self.logger.debug('Could not read the outline of glyph %d of ' \
                              'the font %d: %s', gid, xref, e)
            return None

        self.sigcache[(xref, gid)] = sig
        return sig

    def glyph_strings(self, doc, xref, learnt = None, trusted = True):
        '''what every glyph of a font stands for, as a glyph id -> string
           dict, read out of the font itself and out of what the other
           subsets of the same font in this document say.

           trusted is false for a font whose subsets the producer re-encodes,
           where what the subset says about its own glyphs is where that
           producer put them rather than what they draw - see
           RE_ENCODED_FONTS. Nothing is read out of the font for those and
           the hand table is the whole of the repair'''
        font = self.open_font(doc, xref)
        if font == None:
            return {}

        strings = dict(self.glyph_seed_strings(doc, xref)) if trusted else {}

        # a subset that draws a character only inside a conjunct keeps
        # neither a cmap entry nor a name for the glyph of that character,
        # and then nothing that is made out of it can be spelled out either.
        # Another subset of the same font in the same document does name it.
        #
        # That only holds where the two subsets number their glyphs alike,
        # though - see glyph_count. A producer that renumbers a subset gives
        # the same id to another glyph entirely, and taking a string across
        # such a pair hands this font the characters of glyphs it does not
        # draw: the Mangal of a 223221 gazette is carried as a subset of 886
        # glyphs that names 339 of them and as one of 136 that names none,
        # and without this check the first hands the second its own digits
        # and punctuation, turning a whole document into rubbish
        count = self.glyph_count(doc, xref)
        for gid, (ustr, donorcount) in (learnt or {}).items():
            if count != None and count == donorcount:
                strings.setdefault(gid, ustr)

        return self.expand_gsub(font, strings) if trusted else strings

    def learn_font_gids(self, doc, fonts):
        '''what the subsets of a font that this document carries say about
           the glyphs they name, as a font key -> {glyph id: string} dict.
           A subset that names a glyph fills in the subsets that do not'''
        learnt = {}

        for xref, (fontname, encoding) in sorted(fonts.items()):
            key = font_lookup_key(self.base_font(fontname))
            if key not in BROKEN_FONTS_BY_KEY or key in RE_ENCODED_BY_KEY:
                continue

            known = learnt.setdefault(key, {})
            for gid, ustr in self.glyph_seed_strings(doc, xref).items():
                # the glyph count is carried along so that the subset this
                # is handed to can tell whether the id means the same glyph
                # there, see glyph_strings
                seen = (ustr, self.glyph_count(doc, xref))
                if known.get(gid, seen) != seen:
                    # two subsets that are named alike do not draw the same
                    # glyphs, so neither of them can be trusted for it
                    self.logger.warning('Subsets of %s disagree on glyph ' \
                                        '%d: %r and %r', fontname, gid, \
                                        known[gid], seen)
                    known[gid] = None
                else:
                    known[gid] = seen

        for key in learnt:
            learnt[key] = {gid: seen for gid, seen in learnt[key].items() \
                           if seen != None}

        return learnt

    def is_identity(self, doc, xref, encoding):
        '''the code of a glyph is its glyph id only if the font is encoded
           with identity-h and maps the cids to the glyphs one to one'''
        if encoding != 'Identity-H':
            return False

        key, val = doc.xref_get_key(xref, 'DescendantFonts')
        if key == 'array':
            match = re.search(r'(\d+) 0 R', val)
            if match:
                key, val = doc.xref_get_key(int(match.group(1)), 'CIDToGIDMap')
                if key not in ('null', 'name') or \
                   (key == 'name' and val not in ('/Identity', 'Identity')):
                    return False
        return True

    def has_map_holes(self, table):
        '''whether a ToUnicode map hands any of its glyphs no character at
           all. A map is built to say what a glyph draws, so a <0000> in it
           is not a character but the absence of an answer, and a font whose
           map is full of them extracts as raw NULs rather than as the wrong
           text'''
        return any(ustr and set(ustr) == {'\x00'} for ustr in table.values())

    def fix_font(self, doc, xref, fontname, encoding, glyphfixes, \
                 learnt = None, outlinefixes = None, fixescount = None, \
                 trusted = True):
        if encoding in SIMPLE_ENCODINGS:
            return self.fix_simple_font(doc, xref, fontname, encoding, \
                                        glyphfixes, learnt, fixescount, \
                                        trusted)

        if not self.is_identity(doc, xref, encoding):
            self.logger.info('Font %d (%s) is not identity encoded', \
                             xref, fontname)
            return 0

        if self.open_font(doc, xref) == None:
            return 0

        cmapxref = self.get_cmap_xref(doc, xref)

        glyphfixes = self.fixes_for_numbering(doc, xref, fontname, \
                                              glyphfixes, fixescount)

        strings = self.glyph_strings(doc, xref, learnt, trusted)

        # a font that carries no map at all, whose every glyph therefore
        # extracts as (cid:N). There is nothing to walk and nothing to be
        # right or wrong, so the map is built from what is known about the
        # glyphs and written to the font, the way a type3 font's is - the
        # code of a glyph is its glyph id here, identity encoding being
        # what was just checked. 13 of the 14 TAU-Marutham subsets of
        # tamilnadu/2023-03-28/Extraordinary_104_Part-IV_Section-1.pdf are
        # carried this way
        if cmapxref == None:
            fixed = dict(strings)
            self.add_missing_glyphs(doc, xref, fixed, glyphfixes)
            if not fixed:
                return 0

            self.logger.info('Font %d (%s) carries no ToUnicode map, ' \
                             'building one for %d glyph(s)', xref, fontname, \
                             len(fixed))
            self.set_tounicode(doc, xref, fixed)
            return len(fixed)

        table = self.parse_cmap(doc, cmapxref)

        # a font that is repaired from its outlines is one whose map hands a
        # glyph no character at all. That hole is the fault the outline table
        # was read for and the only one it can speak to: a subset of the same
        # font that does describe its own glyphs - a cmap, a post, a GSUB -
        # carries the other fault instead, the pairing that slips on the
        # glyphs devanagari shaping moved, and this build repairs that one
        # only in part. Repairing it in part is worse than not at all, since
        # a map that is wrong in a way that happens to read correctly is then
        # made wrong in a way that does not: the Mangal of
        # test/test_pdfs/sebicirculars4.pdf draws बोर्ड out of a map that has
        # the reph and the da the wrong way round, and repairing only the da
        # turns it into बोडड. So such a font is left exactly as it is
        if outlinefixes and not self.has_map_holes(table):
            self.logger.debug('Font %d (%s) has no hole in its map, so it ' \
                              'is not the one the outline table was read ' \
                              'for and is left as it is', xref, fontname)
            return 0

        fixed = {}
        num   = 0
        for code, ustr in table.items():
            # what the font says this glyph is, and failing that - a subset
            # that keeps neither a name nor a rule for a glyph the shaper
            # made - what it is repaired to by hand, whatever the character
            # it was paired with in this document happens to be
            correct = strings.get(code)
            if correct == None:
                correct = glyphfixes.get(code)
            if correct == None and outlinefixes:
                # a font whose subsets are renumbered, so the glyph is looked
                # up by what it draws rather than by the number it has here
                correct = outlinefixes.get( \
                              self.glyph_signature(doc, xref, code))

            if correct != None and correct != ustr:
                num += 1
                self.logger.debug('Font %d glyph %d: %r -> %r', \
                                  xref, code, ustr, correct)
            fixed[code] = correct if correct != None else ustr

        num += self.add_missing_glyphs(doc, xref, fixed, glyphfixes)

        if num:
            doc.update_stream(cmapxref, self.build_cmap(fixed), compress = True)
        return num

    def fixes_for_numbering(self, doc, xref, fontname, glyphfixes, fixescount):
        '''the hand table of a font, emptied for a subset that does not number
           its glyphs the way the table was read off.

           A table read off one numbering of a family says nothing about the
           glyphs of another, so it is dropped for such a subset rather than
           handed it the readings of glyphs it does not draw. What the font
           itself says about its own glyphs - its cmap, its names, its GSUB -
           is not a table and still stands, so such a font is repaired from
           that alone, and a re-encoded font, which has nothing else, is left
           exactly as it is'''
        if fixescount == None or not glyphfixes:
            return glyphfixes

        count = self.glyph_count(doc, xref)
        if count == fixescount:
            return glyphfixes

        self.logger.info('Font %d (%s) counts %s glyphs and the table for ' \
                         'it was read off a font of %d, so it is repaired ' \
                         'from the font alone', xref, fontname, count, \
                         fixescount)
        return {}

    # ------------------------------------------------------------------
    # the simple fonts of a re-encoded document
    #
    # A producer that re-encodes a font carries it as simple TrueType fonts
    # as well as as an identity encoded one, and gives those no ToUnicode at
    # all: the byte in the content stream is the one it happened to give the
    # glyph, and an extractor reads it back through WinAnsiEncoding or
    # MacRomanEncoding as the latin letter that lives there. So the tamil of
    # such a font extracts as "3Ý FTà YETCÕxJ" and the only thing that says
    # which glyph a byte drew is the cmap of the subset, which maps that byte
    # to a glyph id - the one question this producer's cmap does answer.
    # A map is built for the font out of the hand table and written to it.
    # ------------------------------------------------------------------

    def byte_glyphs(self, doc, xref, encoding):
        '''the glyph that every byte of a simple font draws, as a byte ->
           glyph id dict, read out of the cmap of the subset'''
        font = self.open_font(doc, xref)
        if font == None:
            return {}

        try:
            order  = font.getGlyphOrder()
            tables = font['cmap'].tables if 'cmap' in font else []
        except Exception as e:
            # a subset that keeps no cmap and no glyph names at all: nothing
            # in it says which glyph a byte of the content stream drew, and
            # a simple font is addressed by nothing else
            self.logger.info('Nothing in the font %d says which glyph its ' \
                             'bytes draw, so it is left as it is: %s', xref, e)
            return {}

        if not tables:
            self.logger.info('The font %d carries no cmap, so nothing says ' \
                             'which glyph its bytes draw', xref)
            return {}

        gids     = {gname: gid for gid, gname in enumerate(order)}
        bytes_of = SIMPLE_ENCODINGS[encoding]
        glyphs   = {}

        for table in tables:
            for code, gname in getattr(table, 'cmap', {}).items():
                gid = gids.get(gname)
                if gid == None:
                    continue
                # a (1, 0) subtable is keyed by the byte itself and a (3, 1)
                # one by the character the encoding gives that byte
                if table.platformID == 1:
                    if 0 <= code < 256:
                        glyphs.setdefault(code, gid)
                else:
                    byte = bytes_of.get(chr(code))
                    if byte != None:
                        glyphs.setdefault(byte, gid)

        return glyphs

    def fix_simple_font(self, doc, xref, fontname, encoding, glyphfixes, \
                        learnt = None, fixescount = None, trusted = True):
        '''build the map of a simple font of a re-encoded document out of the
           glyph that its cmap says each of its bytes draws. Returns the
           number of bytes the map gained.

           A font left without a hand table - one whose subset does not number
           its glyphs the way the table was read off - is left exactly as it
           is: what such a font says about its own glyphs is the producer's
           encoding of them and cannot stand in for the table'''
        glyphfixes = self.fixes_for_numbering(doc, xref, fontname, \
                                              glyphfixes, fixescount)
        if not glyphfixes:
            return 0

        strings = self.glyph_strings(doc, xref, learnt, trusted)
        glyphs  = self.byte_glyphs(doc, xref, encoding)
        if not glyphs:
            return 0

        cmapxref = self.get_cmap_xref(doc, xref)
        table    = self.parse_cmap(doc, cmapxref) if cmapxref != None else {}

        fixed = dict(table)
        num   = 0
        for byte, gid in sorted(glyphs.items()):
            correct = strings.get(gid)
            if correct == None:
                correct = glyphfixes.get(gid)
            if correct == None or correct == table.get(byte):
                continue

            self.logger.debug('Font %d byte 0x%02X (glyph %d): %r -> %r', \
                              xref, byte, gid, table.get(byte), correct)
            fixed[byte] = correct
            num += 1

        if not num:
            return 0

        # a byte the table has nothing for is still written out, with the
        # character the encoding already gives it: this map replaces the
        # encoding for an extractor that reads one, and a partial map would
        # leave such an extractor with nothing for those bytes
        chars = SIMPLE_ENCODING_CHARS[encoding]
        for byte in glyphs:
            if byte in chars:
                fixed.setdefault(byte, chars[byte])

        self.set_tounicode(doc, xref, fixed)
        return num

    def add_missing_glyphs(self, doc, xref, fixed, glyphfixes):
        '''put back the glyphs the map has no entry for at all. A map that is
           merely wrong hands every glyph the wrong character and is repaired
           by walking it, but the kannada map of Arial Unicode MS is short
           instead: it names the letters of the block and leaves out the
           forms the shaper made, so a seventh of the text of a Karnataka
           gazette extracts as (cid:8243) and the like and there is no entry
           to walk. Only a glyph the hand table has a reading for is added,
           and only one the subset really carries, so this can add nothing
           that was not read off that font'''
        count = self.glyph_count(doc, xref)
        num   = 0
        for code, correct in glyphfixes.items():
            if code in fixed or (count != None and code >= count):
                continue
            fixed[code] = correct
            num += 1
            self.logger.debug('Font %d glyph %d: no entry -> %r', \
                              xref, code, correct)
        return num

    # ------------------------------------------------------------------
    # the type3 fonts of a distilled gazette
    #
    # A gazette that was distilled rather than written out carries its
    # devanagari as type3 fonts whose glyphs are one bit images, one font
    # per handful of glyphs. There is no font program left to read the
    # names of the glyphs from, but the /Encoding /Differences of the font
    # names every code it draws, and those names are the ones the original
    # font gave its glyphs: uni0928 for a glyph of the devanagari block and
    # g7079 for one that the shaper made, the same glyph ids that
    # ARIAL_UNICODE_MS repairs by hand. So the map of such a font can be
    # built from its /Differences alone, which is what recovers the fonts
    # that carry no ToUnicode at all and whose text comes out as (cid:9).
    # ------------------------------------------------------------------

    def type3_differences(self, doc, xref):
        '''the name that the /Encoding of a type3 font gives to every code
           it draws, as a code -> glyph name dict'''
        key, val = doc.xref_get_key(xref, 'Encoding')
        if key != 'xref':
            return {}

        try:
            encoding = doc.xref_object(int(val.split()[0]), compressed = False)
        except Exception as e:
            self.logger.warning('Could not read the encoding of %d: %s', xref, e)
            return {}

        if 'Differences' not in encoding:
            return {}

        # [ 1 /uni092E /uni0902 /g7074 ... ], a number starts a new run of
        # codes and every name after it takes the next code
        body  = encoding.split('Differences', 1)[1].split(']', 1)[0]
        names = {}
        code  = None
        for token in re.findall(r'(\d+|/[^\s/\[\]<>()]+)', body):
            if token.isdigit():
                code = int(token)
            elif code != None:
                names[code] = token[1:]
                code += 1

        return names

    def glyph_id_name(self, gname):
        '''the glyph id that a name like g7079 stands for, None otherwise'''
        match = re.fullmatch(r'g(\d+)', gname or '')
        return int(match.group(1)) if match else None

    def unicode_glyph_name(self, gname):
        '''the character that a name like uni0928 stands for, None otherwise'''
        match = re.fullmatch(r'uni([0-9A-Fa-f]{4})', gname or '')
        if not match:
            return None
        return unicodedata.normalize('NFC', chr(int(match.group(1), 16)))

    def is_devanagari(self, strings):
        '''whether any of the strings is written in devanagari'''
        for ustr in strings:
            for char in ustr:
                if 'ऀ' <= char <= 'ॿ':
                    return True
        return False

    def learn_type3_gids(self, doc, xrefs):
        '''what the type3 fonts of this document that do carry a ToUnicode
           say about the glyph ids they draw, as a glyph id -> string dict.

           The fonts of one document are subsets of a single original font,
           so a glyph id that one of them maps is the same glyph in all of
           them: the fonts that carry a map are what fills in the fonts
           that carry none, without a table of the whole font being needed'''
        learnt = {}

        for xref in xrefs:
            cmapxref = self.get_cmap_xref(doc, xref)
            if cmapxref == None:
                continue

            try:
                table = self.parse_cmap(doc, cmapxref)
            except Exception as e:
                self.logger.warning('Could not read the map of %d: %s', xref, e)
                continue

            for code, gname in self.type3_differences(doc, xref).items():
                gid = self.glyph_id_name(gname)
                if gid == None or gid in learnt:
                    continue
                ustr = table.get(code)
                if ustr:
                    learnt[gid] = ustr

        return learnt

    def set_tounicode(self, doc, xref, table):
        '''write a map for a font, making one if the font carries none'''
        cmap     = self.build_cmap(table)
        cmapxref = self.get_cmap_xref(doc, xref)

        if cmapxref == None:
            cmapxref = doc.get_new_xref()
            doc.update_object(cmapxref, '<<>>')
            doc.xref_set_key(xref, 'ToUnicode', '%d 0 R' % cmapxref)

        doc.update_stream(cmapxref, cmap, compress = True)

    def name_type3_font(self, doc, xref, fontname):
        '''give a repaired type3 font the name of the font its glyphs come
           from, so that what reads the pdf next can tell which converter
           puts its text in the order unicode wants. A type3 font carries no
           basefont of its own and pdfminer calls it "unknown" without a
           font descriptor to read a name out of'''
        key, val = doc.xref_get_key(xref, 'FontDescriptor')
        if key != 'null':
            return

        key, bbox = doc.xref_get_key(xref, 'FontBBox')
        if key != 'array':
            bbox = '[ 0 0 1000 1000 ]'

        # a space is not allowed in a pdf name, #20 is how it is written
        pdfname = fontname.replace(' ', '#20')
        fdxref  = doc.get_new_xref()
        doc.update_object(fdxref, '<< /Type /FontDescriptor /FontName /%s '  \
                                  '/Flags 4 /ItalicAngle 0 /Ascent 0 '       \
                                  '/Descent 0 /MissingWidth 0 /StemV 0 '     \
                                  '/FontBBox %s >>' % (pdfname, bbox))
        doc.xref_set_key(xref, 'FontDescriptor', '%d 0 R' % fdxref)

    def fix_type3_font(self, doc, xref, glyphfixes, learnt):
        '''build the map of a type3 font from the names its encoding gives
           its glyphs. Returns the number of codes that the map gained or
           that it had wrong'''
        names = self.type3_differences(doc, xref)
        if not names:
            return 0

        cmapxref = self.get_cmap_xref(doc, xref)
        table    = self.parse_cmap(doc, cmapxref) if cmapxref != None else {}

        fixed = dict(table)
        num   = 0
        for code, gname in names.items():
            # the name of a glyph of the devanagari block says which
            # character it is, one the shaper made is repaired by hand and,
            # failing that, from what the other fonts of this document say
            correct = self.unicode_glyph_name(gname)

            if correct == None:
                gid = self.glyph_id_name(gname)
                if gid != None:
                    correct = glyphfixes.get(gid) or learnt.get(gid)

            if correct == None or correct == table.get(code):
                continue

            self.logger.debug('Type3 font %d code %d (%s): %r -> %r', \
                              xref, code, gname, table.get(code), correct)
            fixed[code] = correct
            num += 1

        if not num:
            return 0

        # a type3 font that draws no devanagari is not one of the fonts this
        # is about, whatever its glyphs are named, and is left alone: naming
        # it after a devanagari font would send its text through a converter
        # that has no business reordering it
        if not self.is_devanagari(fixed.values()):
            self.logger.info('Type3 font %d draws no devanagari, leaving it ' \
                             'alone', xref)
            return 0

        self.set_tounicode(doc, xref, fixed)

        return num

    def fix_type3_fonts(self, doc, xrefs):
        '''repair every type3 font of the document. Returns the number of
           codes repaired, and the name of the font the glyphs come from if
           any of them was'''
        glyphfixes = BROKEN_FONTS[TYPE3_GLYPH_FONT]
        learnt     = self.learn_type3_gids(doc, xrefs)
        num        = 0

        for xref in xrefs:
            numfixed = self.fix_type3_font(doc, xref, glyphfixes, learnt)
            if numfixed:
                self.name_type3_font(doc, xref, TYPE3_GLYPH_FONT)
            num += numfixed

        if num:
            self.logger.info(\
                'Repaired %d codes of the %d type3 font(s), %d glyph id(s) ' \
                'read out of the fonts of the document itself', num,         \
                len(xrefs), len(learnt))
            self.fixed_fonts.add(TYPE3_GLYPH_FONT)

        return num

    def fix_document(self, doc):
        '''repair every font of the document that is known to carry a broken
           map. Returns the number of glyphs that were repaired, and leaves
           the names of the fonts they belong to in self.fixed_fonts'''
        fonts  = {}
        type3s = []
        for pagenum in range(doc.page_count):
            for font in doc[pagenum].get_fonts(full = True):
                xref, ext, ftype, fontname, refname, encoding = font[:6]
                fonts[xref] = (fontname, encoding)
                if ftype == 'Type3' and xref not in type3s:
                    type3s.append(xref)

        num = 0
        self.fixed_fonts = set()
        self.fontcache   = {}
        self.seedcache   = {}
        self.sigcache    = {}
        learnt = self.learn_font_gids(doc, fonts)

        for xref in sorted(fonts):
            fontname, encoding = fonts[xref]
            basefont   = self.base_font(fontname)
            glyphfixes = get_glyph_fixes(basefont)
            if glyphfixes == None:
                continue

            numfixed = self.fix_font(doc, xref, fontname, encoding, glyphfixes,
                                     learnt.get(font_lookup_key(basefont)),
                                     get_outline_fixes(basefont),
                                     get_glyph_fixes_count(basefont),
                                     trusts_own_glyphs(basefont))
            if numfixed:
                self.fixed_fonts.add(basefont)
            num += numfixed

        if type3s:
            num += self.fix_type3_fonts(doc, sorted(type3s))

        # the font programs of a document are of no use once it is repaired
        self.fontcache = {}
        self.seedcache = {}
        self.sigcache  = {}

        self.logger.info('Repaired %d glyphs in the fonts: %s', num, \
                         ', '.join(sorted(self.fixed_fonts)))
        return num

def print_usage(progname):
    print('Usage: %s input.pdf output.pdf' % progname)

if __name__ == '__main__':
    optlist = getopt.getopt(sys.argv[1:], 'h')

    for o, v in optlist[0]:
        if o == '-h':
            print_usage(sys.argv[0])
            sys.exit(0)

    if len(optlist[1]) != 2:
        print_usage(sys.argv[0])
        sys.exit(0)

    logging.basicConfig(\
        level   = logging.INFO, \
        format  = '%(asctime)s: %(name)s: %(levelname)s %(message)s', \
        datefmt = '%Y-%m-%d %H:%M:%S', \
    )

    infile, outfile = optlist[1]

    doc = pymupdf.open(infile)
    num = ToUnicodeFixer().fix_document(doc)
    doc.save(outfile)
    print('Repaired %d glyphs. Wrote %s' % (num, outfile))
