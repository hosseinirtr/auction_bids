from auctions.models import WatchlistItem

def watchlist_items(request):
    user = request.user  
    watchlist_items = WatchlistItem.objects.filter(user=user)
    
    listing_attributes = [item.listing for item in watchlist_items]
    return {"watchlistItem": listing_attributes, 'len' : len(watchlist_items)}