
PYTHON=/usr/bin/env python
EXPANDER=expander.py

.PHONY : clean help all altafsir_annotated altafsir_complete hadith_complete ocred_texts test

all: altafsir_annotated altafsir_complete hadith_complete ocred_texts

altafsir_annotated:
	@echo "\n>> Creating subcorpus for altafsir annotated..."
	$(PYTHON) $(EXPANDER) --altafsir_annotated

altafsir_complete:
	@echo "\n>> Creating subcorpus for altafsir complete..."
	$(PYTHON) $(EXPANDER) --altafsir_complete

hadith_complete:
	@echo "\n>> Creating subcorpus for hadith complete..."
	$(PYTHON) $(EXPANDER) --hasith_complete

ocred_texts:
	@echo "\n>> Creating subcorpus for ocred texts..."
	$(PYTHON) $(EXPANDER) --ocred

test:
	@echo "\n>> Creating subcorpus for tests [FOR DEBUGGING]..."
	$(PYTHON) $(EXPANDER) "--test"

help:
	@echo "    all"
	@echo "        Collect all data (except tests), tokenise it, adjust offsets and add metadata"
	@echo "    altafsir_annotated"
	@echo "        Collect, tokenise, adjust offsets and add metadata to altafsir annotated"
	@echo "    altafsir_complete"
	@echo "        Collect, tokenise, adjust offsets and add metadata to altafsir complete"
	@echo "    hadith_complete"
	@echo "        Collect, tokenise, adjust offsets and add metadata to hadith complete"
	@echo "    ocred_texts"
	@echo "        Collect, tokenise, adjust offsets and add metadata to ocred texts"
	@echo "    test"
	@echo "        Collect, tokenise, adjust offsets and add metadata from tests [DEBUG]"
	@echo ""
	@echo "usage: make [help] [all] [altafsir_annotated] [altafsir_complete] [hadith_complete] [ocred] [test]"
