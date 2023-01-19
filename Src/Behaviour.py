#Library, module

# Desperate behaviour, always bids max amount with and without discounts.
# Can bid for more than the market value, but not over the maximum amount.
A = {
  "onlyBidMaxAmount": True,
  "bidMax": 0,
  "discounts": {
    "bidOnDiscounts": True,
    "onlyBidOnDiscounts": False,
    "minimumDiscount": 0.0
  },
  "bid": lambda price, marketPrice, bidMax:
         # Can't bid over budget
         False if (price > bidMax) else
         # Can bid over market value
         True if (price > marketPrice) else 
         (price < bidMax)
}

# Bids on everything, including discounts of atleast 30% discount.
# Doesn't bid for more than the market value or over the maximum amount.
B = {
  "onlyBidMaxAmount": False,
  "bidMax": 0,
  "discounts": {
    "bidOnDiscounts": True,
    "onlyBidOnDiscounts": False,
    "minimumDiscount": 0.3
  },
  "bid": lambda price, marketPrice, bidMax:
         # Can't bid over budget
         False if (price > bidMax) else 
         # Can't bid over market value
         False if (price > marketPrice) else
         (price < bidMax)
} 