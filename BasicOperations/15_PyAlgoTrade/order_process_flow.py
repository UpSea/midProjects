'''
Broker.onBars(self, dateTime, bars):
    # Let the fill strategy know that new bars are being processed.
    self.__fillStrategy.onBars(self, bars)

    # This is to froze the orders that will be processed in this event, to avoid new getting orders introduced
    # and processed on this very same event.
    ordersToProcess = self.__activeOrders.values()

    for order in ordersToProcess:
        # This may trigger orders to be added/removed from __activeOrders.
        self.__onBarsImpl(order, bars)
'''
