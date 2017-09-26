import random

def generate_otp():
    r = random.randint(0,9999)
    return '{0:04d}'.format(r)