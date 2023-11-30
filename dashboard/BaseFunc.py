class BaseFunc:
    def __init__(self, data):
        self.data = data
        

    def create_daily_orders_df(self):
        #daily order function
        daily_orders_df = self.data.resample(rule='D', on='order_approved_at').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        })
        daily_orders_df = daily_orders_df.reset_index()
        daily_orders_df.rename(columns={
            "order_id": "order_count",
            "payment_value": "revenue"
        }, inplace=True)
        
        return daily_orders_df
    
     
    def create_sum_order_items_df(self):
        #sum order order function
        sum_order_items_df = self.data.groupby("product_category_name_english")["product_id"].count().reset_index()
        sum_order_items_df.rename(columns={
            "product_id": "product_count"
        }, inplace=True)
        sum_order_items_df = sum_order_items_df.sort_values(by='product_count', ascending=False)

        return sum_order_items_df
    
    def create_order_status(self):
        #order status
        order_status_df = self.data["order_status"].value_counts().sort_values(ascending=False)
        most_common_status = order_status_df.idxmax()

        return order_status_df, most_common_status