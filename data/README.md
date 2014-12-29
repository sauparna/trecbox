trec.offsets.old - byte offsets into original TREC corpus on disks 1-5
DOCNO file DOC DOCNO TEXT

trec.offsets - byte offsets into cleaner corpus
DOCNO file DOCNO TEXT

When using flatten pass it the old offsets file.

On TREC document structure
----

These three seems to be around always.
DOC, DOCNO, TEXT

A title shows up in many forms.
TTL, TITLE, HEADLINE, H3, HT

Useful text blocks.
SUMMARY

Some TEXT sections are strewn with funny comment tags and other tags
too. 'within+' denotes such a TEXT section with one or more such tags
within it.

TREC document structure table

		cd1	cd2	cd3	cd4	cd5
doe
ap		HEAD+	HEAD+	HEAD	
fr		within+	within+		within+
wsj		HL	HL
ziff		TITLE	TITLE	TITLE
			SUMMARY	SUMMARY
patents				TTL
sjm				LEADPARA
				SECTION
				HEADLINE
cr					TTL
ft					HEADLINE
fbis						H3 (within+)
						HT (within+)
la						HEADLINE
						within+

TREC topic structures
----

YEAR/TAG head num dom title desc smry narr con fac nat def
  1-100  x    x   x   x     x         x    x   x       x
101-150  x    x   x   x     x    x    x    x   x   x   x
151-200       x       x     x         x
201-250       x             x
251-300       x       x     x         x
301-350       x       x     x         x
351-400       x       x     x         x
401-450       x       x     x         x
