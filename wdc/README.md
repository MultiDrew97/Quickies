# Worlds Dumbest Calculator

This is based on an idea I had a few years ago and wanted to recreate it again. It's based on the basic fact that most of everything in math is just "fancy" addition. The goal is to break down all high level functions to be nothing but addition. Since the 3 basic functions of all math can be brokwn down in this way, it shouldn't be too hard

# Proof of Concept

For exmaple, you can have the below equation:

    1 + 1 = 2

Which seems simple enough, right? But then you can have the below equation:

    1 - 1 = 0
    1 + (-1) = 0

So what about multiplication and division? Lets take a look there:

    4 * 3 = 12
    4 + 4 + 4 = 12

    12 / 4 = 3
    12 - 4 - 4 - 4 = 0

There were three 4s that could be subtracted. As proven above, subtraction is addition of negative numbers, so that would transitively mean that division is also "fancy" addition of negative numbers and counting how many times it can happen before hitting 0

So if subtraction is addition with a negative number, and division and multiplication can be broken down into these components, how else can this be expanded?

Here's another case:

    2^4 = 16

We can break it down to be as below:

    [{(2 * 2) * 2} * 2] = 16

Which then further breaks down to:

    {(2 + 2) * 2} * 2
    [{(2 + 2) + (2 + 2)} * 2]
    [{(2 + 2) + (2 + 2)} + {(2 + 2) + (2 + 2)}]

So with that, I want the challenge of making the approximation with nothing but addition
