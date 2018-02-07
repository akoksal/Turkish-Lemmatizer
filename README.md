# Turkish-Lemmatizer
This is a lemmatization tool for Turkish Language. Three steps require to make this lemmatizer. Lexicons, handling inflectional suffixes which changes lemma, and checking if suffixes are valid or not.

## 1.Lexicons
The best lexicon for Turkish language is a dictionary from Turkish Language Instutition([TDK](http://www.tdk.gov.tr/index.php?option=com_gts)). However, it is not available online as a dataset so we use alternatives.

The main alternative is from [Zargan Dictionary](http://st2.zargan.com/duyuru/Zargan_Linguistic_Resources_for_Turkish.html). The author provides 1.3M word forms with stems. So, we can gather stems from this file as lexicon.

The other alternative is Wiktionary database. You can download from [this link](https://dumps.wikimedia.org/trwiktionary/20180201/). However there are words with inflectional suffixes in wiktionary so it wouldn't help us too much.

## 2.Handling Inflextional Suffixes Which Changes Lemma(Ablauts)
There are three different ablauts which change structure of lemmas. We generate new words based on these changes. These changes are creating negative verbs(not ablaut), softening of consonants, becoming close(narrow) vowel, dropping a vowel, and zero infinitive(not ablaut).

### 2.1.Creating Negative Verbs
To generate negative words, we add -ma -me suffixes to verbs
For example: gelmek -> gelmemek, gitmek -> gitmemek

### 2.2.Softening of consonants
To handle softening of consonants, I generate softened version of each word. For lemmas end with [p,ç,t,k] except verbs, the last consonant can be transformed into [b,c,d,[gğ]] based on the suffix it had. g is possible only when word ends with nk. I generate all possible transformation and I check if softening matches in checkSuffixValidation
For example: kitap -> kitab, küçük -> küçüğ(correct one), renk -> rengi

### 2.3.Becoming Close(Narrow) Vowel
To handle "becoming close(narrow) vowel", I have used explanation in TDK site.(http://www.tdk.gov.tr/index.php?option=com_content&view=article&id=194:Unlu-Daralmasi&catid=50:yazm-kurallar&Itemid=132) When verbs whose last wovel is "a" or "e" take "-yor" suffix, their last wovel transforms into "ı" or "i". Exception is for verb demek and yemek.
For example izlemek -> izli, dinlememek -> dinlemi

### 2.4.Dropping a vowel
In Turkish, when some words with two syllables take suffix starting with vowel, word's last vowel drops. List of these words are added to the code.
For example: alın -> aln, zehir -> zehri, oğul -> oğlu 

### 2.5.Zero Infinitive
In Turkish, verbs lexicon form, generally, is with to infinitive. This suffix is "-mak" or "-mek".
For example, meaning of gelmek is "to come. However, we use root form of gelmek which is gel when we use verbs with different time forms. For example, present continuous form of gelmek is geliyor(without -mek part)
Last action transforms verbs to the zero infinitive format
For example: gelmek -> gel, almak -> al

## 3. Checking Suffixes
I have used [Éva Á. Csató & David Nathan's site](http://www.dnathan.com/language/turkish/tsd/) to find all suffixes. #TO-DO# Then program checks if remaining part of the word generates valid suffixes within this list.


## References
1. Bilgin, O. (2016). Frequency Effects in the Processing of Morphologically Complex Turkish Words (Unpublished master’s thesis). Bogaziçi University, Istanbul, Turkey. Retrieved from http://st2.zargan.com/public/resources/turkish/frequency_effects_in_turkish.pdf
2. http://www.dnathan.com/language/turkish/tsd/
