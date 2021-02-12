from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(And(AKnight,AKnave)),
    Or(AKnight, AKnave),
    Implication(And(AKnight, AKnave), AKnight),
    Implication(Not(And(AKnight, AKnave)), AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Not(And(AKnight,AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight,BKnave)),
    Or(BKnight, BKnave),
    Implication(And(BKnave, AKnave), AKnight),
    Implication(Not(And(BKnave, AKnave)), AKnave),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Not(And(AKnight,AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight,BKnave)),
    Or(BKnight, BKnave),

    Implication(Or(And(BKnave, AKnave),And(BKnight, AKnight)), AKnight),
    Implication(Not(Or(And(BKnave, AKnave),And(BKnight, AKnight),)), AKnave),

    Implication(Or(And(BKnave, AKnight),And(AKnave, BKnight)), BKnight),
    Implication(Not(Or(And(BKnave, AKnight),And(AKnave, BKnight))), BKnave),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
aClaimKnight = Symbol("A claims he's a knight")
knowledge3 = And(
    Not(And(AKnight,AKnave)),
    Or(AKnight, AKnave),
    Not(And(BKnight,BKnave)),
    Or(BKnight, BKnave),
    Not(And(CKnight,CKnave)),
    Or(CKnight, CKnave),
    Or(aClaimKnight, Not(aClaimKnight)),
    Implication(Not(aClaimKnight), Not(AKnave)),
    Biconditional(AKnight, aClaimKnight),
    Biconditional(AKnave, Not(aClaimKnight)),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(BKnave, Not(BKnight)),
    Biconditional(CKnight, Not(CKnave)),
    Biconditional(CKnave, Not(CKnight)),

    # B's claim 1
    Implication(Not(aClaimKnight), BKnight),
    Implication(aClaimKnight, BKnave),

    # B's claim 2
    Implication(CKnave, BKnight),
    Implication(Not(CKnave), BKnave),

    # C's claim 
    Implication(AKnight, CKnight),
    Implication(Not(AKnight), CKnave),
    Implication(AKnave, CKnave),

    #problem info
    Implication(And(aClaimKnight, AKnight), AKnight),
    Implication(And(aClaimKnight, AKnave), AKnave),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
