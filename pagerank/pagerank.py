import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    p_d = {}
    """ If the current page doesn't link to anything choose randomly from all the pages in the corpus """
    if len(corpus[page]) == 0:
        for p in corpus:
            p_d[p] = 1/len(corpus)
        return p_d
    """ """
    for p in corpus[page]:
        p_d[p] = damping_factor/len(corpus[page]) 
    for p in corpus:
        if p not in p_d:
            p_d[p] = (1-damping_factor)/len(corpus)
        else:
            p_d[p] += (1-damping_factor)/len(corpus) 
    return p_d

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    current_page = random.choice(tuple(corpus))
    pranks = {page: 0 for page in corpus}
    for _ in range(n):
        pranks[current_page] += 1/n
        probs = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(probs.keys()), weights=list(probs.values()))[0]
    return pranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probs = {page: 1/len(corpus) for page in corpus}
    while True:
        print(probs)
        new_probs = {}
        for page in corpus:
            new_probs[page] = (1-damping_factor)/len(corpus)
            for subpage in corpus[page]:
                new_probs[page] += damping_factor*probs[subpage]/(len(corpus[subpage]) if len(corpus[subpage]) != 0 else len(corpus))
        if all([abs(probs[page]-new_probs[page])<0.001 for page in corpus]):
            return new_probs 
        probs = new_probs 

if __name__ == "__main__":
    main()
