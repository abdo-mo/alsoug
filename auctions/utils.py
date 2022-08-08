from auctions.models import *
# Helper Functions

def isfloat(num):
    try:
        float(num)
    except:
        return False
    return True


def validate_bid(amount, listing):
    if Bid.objects.filter(listing=listing).first():
        if amount <= listing.current_price:
            return False
        return True
    
    if amount < listing.current_price:
        return False
    return True


# Validate listing form

def validate_new_listing(title, description, image, starting_bid, catagory):
    if title != "" and description != "" and image != "":
        if starting_bid != "" and isfloat(starting_bid):
            try:
                Catagory.objects.get(name=catagory)
            except:
                return False
            return True
        return False
    return False


def validate_operation(operation):
    if operation == "add" or operation == "remove":
        return True
    return False


def validate_close(close):
    if close == "close":
        return True
    return False


def valid_comment(comment):
    if comment != "":
        return True
    return False

