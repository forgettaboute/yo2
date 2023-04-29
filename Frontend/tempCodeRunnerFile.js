        var cartData = response.data.carts;
        carts = [];
        console.log(cartData);

        // loops carts
        for (let i = 0; i < cartData.length; i++) {
            let total = 0;

            // calculates avg and appends to respectice cart
            for (let j = 0; j < cartData[i].products.length; j++) {
                total += cartData[i].products[j].total;
            }
            cartData[i].cartAverage = total / cartData[i].totalQuantity;
            carts.push({"id": cartData[i].id, "cartAverage": cartData[i].cartAverage});

            console.log(cartData[i].cartAverage);
        }

        console.log(carts)