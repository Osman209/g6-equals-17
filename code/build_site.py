#!/usr/bin/env python3
"""
build_site.py — regenerate docs/ : one landing page and one abstract page per paper,
in the same template as the author's other sites (odd-sieve-cell-system,
prime-number-studies).

COVERS the site. Each paper page carries Google Scholar citation meta tags, which is what
makes the work indexable; the body is the abstract only, with the full text in the PDF and
on GitHub. That deliberately keeps the site clear of the LaTeX-rendering problems Jekyll
would otherwise introduce.

Editing a paper does NOT change the site text: the title, subtitle and abstract below are
the site's own copy. Change them here as well after any correction to a paper.

    python3 code/build_site.py
"""
import html
import os
import shutil

REPO = "https://github.com/Osman209/g6-equals-17"
SITE = "https://osman209.github.io/g6-equals-17"
ORCID = "0009-0004-5912-999X"
DOI = "10.5281/zenodo.22883809"
DATE = "2026-10-01"

CSS = """<style>body{max-width:52rem;margin:2.5rem auto;padding:0 1.2rem;font:16px/1.6 Georgia,"DejaVu Serif",serif;color:#1a1a1a}
h1{font-size:1.6rem;line-height:1.3;margin-bottom:.2rem}h2{font-size:1.05rem;font-weight:400;color:#555;margin-top:0}
a{color:#0b4f8a}.meta{color:#555;font-size:.92rem}.abs{margin:1.4rem 0}
ul{list-style:none;padding:0}li{margin:1.15rem 0;padding-left:.9rem;border-left:3px solid #e3e3e3}
.t{font-weight:600}.s{color:#555;font-size:.95rem}.tag{font-size:.78rem;color:#777;text-transform:uppercase;letter-spacing:.05em}
code{background:#f5f5f5;padding:.1em .3em;border-radius:3px;font-size:.9em}
.res{border:1px solid #e3e3e3;border-radius:8px;padding:1rem;text-align:center;margin:1.5rem 0;background:#fafafa}
.res .eq{font-size:1.8rem;font-style:italic}.res .note{color:#555;font-size:.9rem;margin-top:.3rem}</style>"""

PAPERS = [
    dict(
        slug="overview",
        title="The Six-Card Cover Problem: an Overview",
        sub="The case r = 6 of the Erdos-Lovasz cover number problem: the chain from fifteen "
            "cards to seventeen, and what each stage actually rests on",
        abs="One pass over the papers. The question, which is the r = 6 case of the problem "
            "Erdos and Lovasz posed in 1974, with g(3) = 6, g(4) = 9 and g(5) = 13 known exactly; "
            "the two independent routes excluding "
            "fifteen cards; the reduction, SAT and certificate layer excluding sixteen; the "
            "explicit seventeen-card witness; and, stated plainly, which parts are finite checks, "
            "which are certificates, and which remain reading obligations that no certificate can "
            "discharge. Priority is not claimed, and the lower bound has not been independently "
            "reviewed by a human.",
    ),
    dict(
        slug="paper_1_fifteen_cards_histogram_route",
        title="Paper 1. Fifteen Cards: the Histogram Route",
        sub="Degree bounds, a finite lemma on edge covers of K7, and thirteen degree histograms",
        abs="Symbol degrees are forced into {2,3,4}; an exhaustive finite lemma about edge covers "
            "of K7 supplies the two hardest degree exclusions; a weighted counting inequality cuts "
            "the possible degree histograms to thirteen; and the thirteen are eliminated by "
            "incidence arguments. Hence g(6) is at least 16. Superseded by Paper 2, and kept as an "
            "independent second argument.",
    ),
    dict(
        slug="paper_2_eleven_card_lemma",
        title="Paper 2. The Eleven-Card Lemma",
        sub="Every eleven-card family has a four-cover, and fifteen cards then take two lines",
        abs="Every pairwise intersecting 6-uniform family of eleven cards has a transversal of size "
            "at most four. The proof splits on the maximum degree: five or more closes by pairing, "
            "four by the finite K7 lemma, and three or less by an exhaustive triangle-decomposition "
            "search over 5,373 instances. The lemma also pins the maximum degree at exactly four in "
            "the sixteen-card stage. An explicit eight-card family shows the analogue fails at eight.",
    ),
    dict(
        slug="paper_3_sixteen_cards",
        title="Paper 3. Sixteen Cards",
        sub="A finite reduction to 463 canonical cores, SAT, and independently checked DRAT proofs",
        abs="A hypothetical sixteen-card counterexample is reduced to one of 463 canonical "
            "eight-card cores; for each core the completion problem is written as a CNF formula; "
            "all 463 are unsatisfiable; and each unsatisfiability carries a DRAT certificate "
            "accepted by an independent proof checker. DRAT certification removes the SAT solver "
            "from the trusted base, but the completeness of the reduction and the faithfulness of "
            "the encoding remain separate obligations, stated as open.",
    ),
    dict(
        slug="paper_4_seventeen_card_witness",
        title="Paper 4. A Seventeen-Card Witness",
        sub="Seventeen cards on 27 symbols; 136 pairs meet and none of 80,730 five-sets covers",
        abs="An explicit pairwise intersecting 6-uniform family of seventeen cards on 27 symbols "
            "with transversal number six. All 136 card pairs intersect, and exhaustive checking of "
            "all 80,730 five-symbol subsets finds no transversal. Hence g(6) is at most 17. The "
            "check needs nothing but the standard library and uses no result from the other three "
            "papers.",
    ),
    dict(
        slug="paper_5_every_r",
        title="Paper 5. Lower Bounds for g(r): 3r - 3 for Every r, and 3.1020r for Large r",
        sub="Proposed proofs that g(r) is at least 3r - 3 for every r, at least 3r - 2 from r = 16, and asymptotically at least 3.1020r",
        abs="In the framework of Sivashankar (arXiv:2606.24878), the cover number of the remainder "
            "of maximum degree three is bounded by 4 tau <= q + r + 3, answering his question "
            "whether +4 can be +3; hence g(r) >= 3r - 3 for every r, attained at r = 3 and 4. "
            "Excluding the equality case gives g(r) >= 3r - 2 for every r >= 16, with one case left "
            "open at r = 15. A quantitative "
            "form shows a gain linear in r when the remainder is large, with a closed form at every "
            "remainder size. A second saving from the deleted cards, using a bound on the last "
            "steps of the peeling, a budget for the matching numbers of the traces of the deleted cards, and a rainbow matching theorem of Correia, Pokrovskiy and "
            "Sudakov, gives liminf g(r)/r >= 3 + (65 - 36 sqrt 2)/138 = 3.1020..., above "
            "the constant 3.0534 of Sivashankar. The proofs are proposed and "
            "unreviewed; every finite step is checked exhaustively by a named script.",
    ),
]

DISCLAIMER = (
    "No priority is claimed for any result, and this is not presented as a settled answer. "
    "The lower bound is computer-assisted and has not been independently reviewed by a human "
    "or by a proof assistant. AI tools were used throughout the work and its review; "
    "every computational claim is regenerated by a script or certified by a proof file in "
    "<code>code/</code> and <code>results/</code> of the repository. "
    "Licence: CC BY 4.0 (text), MIT (code)."
)


def page(p):
    slug, title, sub = p["slug"], p["title"], p["sub"]
    e = html.escape
    doi_link = "" if DOI.endswith("RESERVED") else (
        ' &middot; <a href="https://doi.org/%s">concept DOI</a>' % DOI)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} &mdash; Mohamed Osman</title>
<meta name="citation_title" content="{e(title)}">
<meta name="citation_author" content="Osman, Mohamed A.">
<meta name="citation_author_orcid" content="{ORCID}">
<meta name="citation_publication_date" content="{DATE.replace('-', '/')}">
<meta name="citation_online_date" content="{DATE.replace('-', '/')}">
<meta name="citation_technical_report_institution" content="The Six-Card Cover Problem (independent)">
<meta name="citation_pdf_url" content="{SITE}/papers/{slug}.pdf">
<meta name="citation_abstract_html_url" content="{SITE}/papers/{slug}.html">
<meta name="citation_language" content="en">
<meta name="description" content="{e(p['abs'][:290])}">
{CSS}</head><body>
<p class="meta"><a href="../index.html">&larr; The Six-Card Cover Problem</a></p>
<h1>{e(title)}</h1><h2>{e(sub)}</h2>
<p class="meta">Mohamed A. Osman &middot; ORCID <a href="https://orcid.org/{ORCID}">{ORCID}</a> &middot; independent researcher &middot; {DATE}</p>
<p><a href="{slug}.pdf"><strong>Download the PDF</strong></a> &middot;
<a href="{REPO}/blob/main/papers/{slug}.md">source on GitHub</a> &middot;
<a href="{REPO}">repository</a>{doi_link}</p>
<div class="abs"><strong>Abstract.</strong> {e(p['abs'])}</div>
<p class="meta">{DISCLAIMER}</p>
</body></html>
"""


def index():
    e = html.escape
    doi_item = "" if DOI.endswith("RESERVED") else (
        ' <a href="https://doi.org/%s">DOI %s</a> &middot;' % (DOI, DOI))
    items = "".join(
        f'<li><span class="t"><a href="papers/{p["slug"]}.html">{e(p["title"])}</a></span><br>'
        f'<span class="s">{e(p["sub"])}</span><br>'
        f'<span class="tag">{DATE} &middot; <a href="papers/{p["slug"]}.pdf">PDF</a></span></li>'
        for p in PAPERS
    )
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Six-Card Cover Problem &mdash; Mohamed Osman</title>
<meta name="description" content="A computer-assisted determination of g(6), the smallest pairwise intersecting 6-uniform family with transversal number 6. Four papers, nineteen scripts, 463 DRAT certificates and an explicit seventeen-card witness. Not independently reviewed; no priority claimed.">
{CSS}</head><body>
<h1>The Six-Card Cover Problem</h1>
<h2>A computer-assisted determination of g(6)</h2>
<p class="meta">Mohamed A. Osman &middot; ORCID <a href="https://orcid.org/{ORCID}">{ORCID}</a> &middot; independent researcher</p>

<div class="res"><div class="eq">g(6) = 17</div>
<div class="note">lower bound computer-assisted and not yet independently reviewed; upper bound an explicit witness</div></div>

<p>Every card carries six symbols and every two cards share one. A <em>transversal</em> is a set of
symbols meeting every card, and &tau; is the smallest size of one. The six symbols of any single card
already meet every other card, so &tau; is at most 6 always, and &tau; = 6 says that no five symbols
cover everything. The question is how few cards such a family can have.</p>

<p>Families of at most fifteen cards are excluded by two independent routes. Sixteen cards are
excluded by a finite reduction to 463 canonical cores whose SAT instances are all unsatisfiable,
each with a DRAT proof accepted by an independent checker. An explicit seventeen-card family on 27
symbols gives the matching upper bound.</p>

<p><strong>The two bounds are not evidence of the same kind.</strong> The upper bound is a witness:
seventeen sets, 136 pairs, 80,730 subsets, standard library only, nothing trusted but arithmetic.
The lower bound is computer-assisted, and a checked certificate does not establish that the
reduction reaches every counterexample or that the encoding means what the mathematics means. Both
are named as open obligations in the text.
<strong>No priority is claimed, and this is not offered as a settled answer: it needs human
review.</strong></p>

<p><a href="{REPO}">Repository</a> &middot;{doi_item}
<a href="{REPO}/blob/main/AUDIT.md">Independent re-verification log</a> &middot;
<a href="https://osman209.github.io/odd-sieve-cell-system/">The Cell System (the author's other work)</a></p>

<h3>Papers</h3><ul>{items}</ul>

<h3>Checking it yourself</h3>
<p><code>python code/verify_witness_17.py</code> &mdash; the seventeen-card family<br>
<code>python code/verify_k7.py</code> &mdash; the finite lemma, all 294,239,817 cases<br>
<code>drat-trim data/cnf/core_007.cnf data/cnf/core_007.drat</code> &mdash; one certificate</p>
<p>The first two need nothing but Python's standard library.</p>

<p class="meta">{DISCLAIMER}</p>
</body></html>
"""


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    docs = os.path.join(root, "docs")
    os.makedirs(os.path.join(docs, "papers"), exist_ok=True)
    for p in PAPERS:
        src = os.path.join(docs, "papers", p["slug"] + ".pdf")
        if not os.path.exists(src):
            print("MISSING PDF, run code/build_pdfs.sh first:", src)
        with open(os.path.join(docs, "papers", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(page(p))
        print("docs/papers/" + p["slug"] + ".html")
    with open(os.path.join(docs, "index.html"), "w", encoding="utf-8") as f:
        f.write(index())
    print("docs/index.html")
