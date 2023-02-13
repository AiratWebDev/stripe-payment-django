window.onload = () => {
    console.log('load_page')

    fetch('/get_key')
        .then((response) => {
                return response.json()
            }
        )
        .then((data) => {
                const stripe = Stripe(data.stripePublishableKey)
                document.getElementById("buy-button").addEventListener('click',
                    (event) => {
                        console.log('eventListener_click')
                        let quantity = document.getElementById('quantity').value
                        const pk = window.location.pathname.replace(/[^0-9]/g, '');

                        if (quantity === '0') {
                            quantity = '1'
                        }

                        fetch(`/buy/${pk}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({'quantity': quantity})
                        })
                            .then((response) => {
                                    return response.json()
                                }
                            )
                            .then((data) => {
                                    console.log(data)
                                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                                }
                            )
                            .then((result) => console.log(result))
                            .catch((error) => console.log(error))
                    }
                )
            }
        )
}
