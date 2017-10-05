from handlers.rewards_handler import RewardsHandler
from handlers.purchase_handler import PurchaseHandler
from handlers.customer_handler import CustomerHandler
from handlers.clientele_handler import ClienteleHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/purchase', PurchaseHandler),
    (r'/customer', CustomerHandler),
    (r'/clientele', ClienteleHandler),
]
