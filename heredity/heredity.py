import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def num_genes_of_person(person, one_gene, two_genes):
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0

def prob_inherit_gene(num_genes_parent, inherited):
    if num_genes_parent == 0:
        return PROBS["mutation"] if inherited else 1-PROBS["mutation"]
    elif num_genes_parent == 1:
        return 0.5
    elif num_genes_parent == 2:
        return 1-PROBS["mutation"] if inherited else PROBS["mutation"]
    else:
        raise Exception("Invalid input")

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set `have_trait` does not have the trait.
    """
    prob = 1.0
    p_trait = sum([PROBS["gene"][i]*PROBS["trait"][i][True] for i in range(3)])
    for person in people:
        num_genes = num_genes_of_person(person, one_gene, two_genes)
        shows_trait = person in have_trait 
        if people[person]["mother"] is None:
            p_a = PROBS["gene"][num_genes]
            p_b_given_a = PROBS["trait"][num_genes][shows_trait]
            prob *= p_b_given_a*p_a
        else:
            num_genes_mother = num_genes_of_person(people[person]["mother"], one_gene, two_genes)
            num_genes_father = num_genes_of_person(people[person]["father"], one_gene, two_genes)
            p_no_mutation = 1 - PROBS["mutation"]
            if num_genes == 0:
                p_a = prob_inherit_gene(num_genes_mother, False) * prob_inherit_gene(num_genes_father, False)
            elif num_genes == 1:
                p_a = prob_inherit_gene(num_genes_mother, False) * prob_inherit_gene(num_genes_father, True) + prob_inherit_gene(num_genes_mother, True) * prob_inherit_gene(num_genes_father, False)
            else:
                p_a = prob_inherit_gene(num_genes_mother, True) * prob_inherit_gene(num_genes_father, True)
            p_b_given_a = PROBS["trait"][num_genes][shows_trait]
            prob *= p_b_given_a*p_a
    return prob 


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        num_genes = num_genes_of_person(person, one_gene, two_genes)
        shows_trait = person in have_trait
        probabilities[person]["gene"][num_genes] += p
        probabilities[person]["trait"][shows_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        sum_p_gene = sum(probabilities[person]["gene"].values())
        sum_p_trait = sum(probabilities[person]["trait"].values())
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= sum_p_gene
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= sum_p_trait




if __name__ == "__main__":
    main()