import itertools
import random
import collections
import numpy as np
from enum import Enum, auto
from functools import total_ordering, cmp_to_key

class Suit(Enum):
    Diamonds = 'D'
    Hearts = 'H'
    Clubs = 'C'
    Spades = 'S'
    
@total_ordering 
class Rank(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    
'''
Return a list of all card and rank combinations, as if a standard 52 deck of cards

[(<Rank.Two: 2>, <Suit.Diamonds: 'D'>), (<Rank.Two: 2>, <Suit.Hearts: 'H'>), ... (<Rank.Ace: 14>, <Suit.Spades: 'S'>)]
'''
def getDeckOfCards():
    return list(itertools.product(Rank, Suit))


'''
Returns a tuple of a random rank and random suit

(<Rank.Six: 6>, <Suit.Clubs: 'C'>)
'''
def getRandomCard():
    return (random.choice(list(Rank)), random.choice(list(Suit)))
    

'''
Shuffles in place a list of cards (which are rank-suit pairs)
'''
def shuffleDeck(deck):
    random.shuffle(deck)
    

'''
Removes the first card from a list of cards and returns it
'''
def takeTopCard(deck):
    return deck.pop()
    

'''
Removes first numOfCards cards from the deck and returns them
'''
def getCardsFromDeck(deck, numOfCards):
    list = []
    for i in range(numOfCards):
        list.append(deck.pop())
    return list
    

'''
Gets the five cards usable by all players on the table
'''
def getCommunityCards(deck):
    return getCardsFromDeck(deck, 5)

'''
Gets the two cards given to a player at the beginning of a game
'''
def getHoleCards(deck):
    return getCardsFromDeck(deck, 2)

def orderCardsHighToLow(cards):
    cards.sort(reverse=True)

#Given a list of 5 cards, check for particular combinations
def isStraightFlush(cards):
    assert len(cards)==5
    return isStraight(cards) and isFlush(cards)

def isStraight(cards):
    assert len(cards)==5
    ranks = [rank.value for (rank, suit) in cards]
    return sorted(ranks) == list(range(min(ranks), max(ranks)+1))
    
def isFlush(cards):
    assert len(cards)==5
    return len(set([suit for (rank, suit) in cards])) == 1

def hasFullHouse(cards):
    assert len(cards)>=5
    return hasThreeOfAKind(cards) and hasPair(cards)

def hasSetOfSameRanks(cards, size):
    assert len(cards)>=size
    return size in collections.Counter([rank for (rank, suit) in cards]).values()

def hasFourOfAKind(cards):
    return hasSetOfSameRanks(cards, 4)

def hasThreeOfAKind(cards):
    return hasSetOfSameRanks(cards, 3)

def hasPair(cards):    
    return hasSetOfSameRanks(cards, 2)

def hasTwoPairs(cards):
    assert len(cards)>=4
    return list(collections.Counter([rank for (rank, suit) in cards]).values()).count(2)>=2

# Just using the Counter, assuming 5 cards
def isFullHouse(cards):
    return sorted(collections.Counter([rank for (rank, suit) in cards]).values())==[2,3]

def isFourOfAKind(cards):
    return sorted(collections.Counter([rank for (rank, suit) in cards]).values())==[1,4]

def isThreeOfAKind(cards):
    return sorted(collections.Counter([rank for (rank, suit) in cards]).values())==[1,1,3]

def isPair(cards):    
    return sorted(collections.Counter([rank for (rank, suit) in cards]).values())==[1,1,1,2]

def isTwoPairs(cards):
    return sorted(collections.Counter([rank for (rank, suit) in cards]).values())==[1,2,2]


# Poker hands

exampleStraightFlush = [
    (Rank.Jack,Suit.Clubs),
    (Rank.Ten,Suit.Clubs),
    (Rank.Nine,Suit.Clubs),
    (Rank.Eight,Suit.Clubs),
    (Rank.Seven,Suit.Clubs)
]
exampleFourOfAKind = [
    (Rank.Five,Suit.Clubs),
    (Rank.Five,Suit.Diamonds),
    (Rank.Five,Suit.Hearts),
    (Rank.Five,Suit.Spades),
    (Rank.Two,Suit.Diamonds)
]
exampleFullHouse = [
    (Rank.Six,Suit.Spades),
    (Rank.Six,Suit.Hearts),
    (Rank.Six,Suit.Diamonds),
    (Rank.King,Suit.Clubs),
    (Rank.King,Suit.Hearts)
]
exampleFlush = [
    (Rank.Jack,Suit.Diamonds),
    (Rank.Nine,Suit.Diamonds),
    (Rank.Eight,Suit.Diamonds),
    (Rank.Four,Suit.Diamonds),
    (Rank.Three,Suit.Diamonds)
]
exampleStraight = [
    (Rank.Ten,Suit.Diamonds),
    (Rank.Nine,Suit.Spades),
    (Rank.Eight,Suit.Hearts),
    (Rank.Seven,Suit.Diamonds),
    (Rank.Six,Suit.Clubs)
]
exampleThreeOfAKind = [
    (Rank.Queen,Suit.Clubs),
    (Rank.Queen,Suit.Spades),
    (Rank.Queen,Suit.Hearts),
    (Rank.Nine,Suit.Hearts),
    (Rank.Two,Suit.Spades)
]
exampleTwoPair = [
    (Rank.Jack,Suit.Hearts),
    (Rank.Jack,Suit.Spades),
    (Rank.Three,Suit.Clubs),
    (Rank.Three,Suit.Spades),
    (Rank.Two,Suit.Hearts)
]
exampleOnePair = [
    (Rank.Ten,Suit.Spades),
    (Rank.Ten,Suit.Hearts),
    (Rank.Eight,Suit.Spades),
    (Rank.Seven,Suit.Hearts),
    (Rank.Four,Suit.Clubs)
]
exampleHighCard = [
    (Rank.King,Suit.Diamonds),
    (Rank.Queen,Suit.Diamonds),
    (Rank.Seven,Suit.Spades),
    (Rank.Four,Suit.Spades),
    (Rank.Three,Suit.Hearts)
]
#We can build a map of sets of 5 cards to values of the hand, using notation similar to software release major minor patch build
def determineHandRank(hand):
    if isStraightFlush(hand):
        return 8
    if isFourOfAKind(hand):
        return 7
    if isFullHouse(hand):
        return 6
    if isFlush(hand):
        return 5
    if isStraight(hand):
        return 4
    if isThreeOfAKind(hand):
        return 3
    if isTwoPairs(hand):
        return 2
    if isPair(hand):
        return 1
    return 0

# Returns an array of values where the values in the array are compared consecutively to determine the winner
def determineTieBreakers(hand):    
    cardRanksToFrequencies = sorted(collections.Counter([rank for (rank, suit) in hand]).items(), reverse=True)
    cardRanksToFrequencies.sort(key=lambda x: x[1], reverse=True)
    return [pair[0].value for pair in cardRanksToFrequencies]

def determineHandScore(hand):
    result = determineTieBreakers(hand)
    result.insert(0, determineHandRank(hand))
    # Special Cases
    if result == [0, 14, 5, 4, 3, 2]: return [4, 5, 4, 3, 2, 1]
    if result == [5, 14, 5, 4, 3, 2]: return [8, 5, 4, 3, 2, 1]
    return result

"""
Return -1 if right is greater than left, 1 if left is greater than right, 0 if equal

scoreCompare([4, 8, 7, 6, 5, 4], [6, 3, 2])
-1

scoreCompare([5, 11, 9, 8, 4, 3], [5, 11, 7, 6, 5, 2])
1
"""
def scoreCompare(left, right):
    leftScore = determineHandScore(left)
    rightScore = determineHandScore(right)
    # Note that two hands with the same hand rank would necessarily have the same number of tiebreakers
    # Therefore if the hands are not scored according to the hand rank, we know the hand rank must match and therefore
    # the arrays have the same length
    for index, score in enumerate(leftScore):
        if not rightScore[index] == score:
            return np.sign(rightScore[index] - score)
    return 0

def splitDeckIntoFives(deck):
    return [deck[i*5: (i+1)*5] for i in range(len(deck)//5)]


