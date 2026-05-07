"""
Hand-crafted test queries with ground truth answers.
Used for RAGAS evaluation.
"""

# Questions about "Attention Is All You Need" paper
EVAL_QUERIES = [
    {
        "question": "What is the Transformer architecture based on?",
        "ground_truth": (
            "The Transformer is a neural network architecture based solely on "
            "attention mechanisms, dispensing with recurrence and convolutions entirely."
        ),
    },
    {
        "question": "What is multi-head attention?",
        "ground_truth": (
            "Multi-head attention runs several attention layers in parallel, "
            "allowing the model to jointly attend to information from different "
            "representation subspaces at different positions."
        ),
    },
    {
        "question": "What BLEU score did the Transformer achieve on English-to-German translation?",
        "ground_truth": (
            "The Transformer achieved 28.4 BLEU on the English-to-German translation task, "
            "establishing a new state-of-the-art."
        ),
    },
    {
        "question": "Why is self-attention preferred over recurrent layers?",
        "ground_truth": (
            "Self-attention layers are faster than recurrent layers, can be more "
            "parallelized, and have a constant number of sequential operations, "
            "making it easier to learn long-range dependencies."
        ),
    },
    {
        "question": "What is scaled dot-product attention?",
        "ground_truth": (
            "Scaled dot-product attention computes the dot products of the query with "
            "all keys, divides each by the square root of the key dimension, and applies "
            "a softmax function to obtain the weights on the values."
        ),
    },
    {
        "question": "What datasets were used for training?",
        "ground_truth": (
            "The Transformer was trained on the WMT 2014 English-German dataset and "
            "the larger WMT 2014 English-French dataset."
        ),
    },
    {
        "question": "What optimizer was used?",
        "ground_truth": (
            "The Adam optimizer was used with beta1 = 0.9, beta2 = 0.98, "
            "and epsilon = 10^-9."
        ),
    },
    {
        "question": "How many layers does the encoder and decoder have?",
        "ground_truth": (
            "Both the encoder and decoder are composed of a stack of N = 6 "
            "identical layers."
        ),
    },
    {
        "question": "What is positional encoding?",
        "ground_truth": (
            "Positional encodings are added to input embeddings to inject information "
            "about the relative or absolute position of tokens in the sequence, using "
            "sine and cosine functions of different frequencies."
        ),
    },
    {
        "question": "What regularization techniques were used?",
        "ground_truth": (
            "Three types of regularization were employed: residual dropout, "
            "label smoothing with epsilon = 0.1, and dropout applied to embeddings."
        ),
    },
]