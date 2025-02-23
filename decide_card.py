
import random

def decide_card():
    choices = ['boltcutters.jpg', 'blowtorch.jpg', 'drill.webp']
    your_number = random.randint(0,3)
    your_choice = choices[your_number]
    return your_choice

