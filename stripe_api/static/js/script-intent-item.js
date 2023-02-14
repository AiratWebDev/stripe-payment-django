window.onload = () => {
    document.getElementById('buy-button').addEventListener('click', (event) => {
        console.log('eventListener_click')

        let quantity = document.getElementById('quantity').value

        if (quantity === '0') {
            quantity = '1'
        }

        window.location = '/payment-intent?quantity=' + quantity
    })
}
