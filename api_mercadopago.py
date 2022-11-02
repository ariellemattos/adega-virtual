import mercadopago

ACCESS_TOKEN = 'TEST-6234637222906265-110215-7178e60af20847605e8ce4eb4187c750-1230375776'

def pagamento(req, **kwargs):
    sdk = mercadopago.SDK(ACCESS_TOKEN)

    produto = kwargs['produto']
    preference = {
        "items": [
            {
                "title": produto['nomeProduto'],
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": produto['preco']
            }
        ]
    }
    
    payment_response = sdk.preference().create(preference)['response']

    return payment_response['init_point']
