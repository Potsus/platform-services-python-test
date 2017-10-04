from handlers.rewards_handler import RewardsHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/purchase', PurchaseHandler),
    (r'/customer', CustomerHandler),
    (r'/clientele', ClienteleHandler),
]
