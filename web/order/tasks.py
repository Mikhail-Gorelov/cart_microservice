from order.models import OrderLine, Order
from src.celery import app


@app.task(name='update_prices')
def update_prices(**kwargs):
    variant_id = kwargs.get('product_variant').get('id')
    order_line = OrderLine.objects.filter(product_variant_id=variant_id)
    users = [i[0] for i in list(Order.objects.filter(lines__in=order_line).values_list('user_id')) if i[0] is not None]
    kwargs['users'] = users
    app.send_task(name='update_prices', kwargs=kwargs, exchange='direct', routing_key='celery')
