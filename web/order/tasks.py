from src.celery import app


@app.task(name='update_prices')
def update_prices():
    print('hello world!')
