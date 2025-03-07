function change_count(detail_id, state) {
    let bas = $('#bas')
    $.get("/cart/change-count/", {
        'detail_id': detail_id,
        'state': state
    }).then(
        res => {
            if (res.status === 'error') {
                alert('تعداد محصول کافی نیست')
            } else {
                bas.html(res)
            }
        }
    )
}

function change_count2(detail_id, state) {
    let bas = $('#bas')
    $.get("/change-count/", {
        'detail_id': detail_id,
        'state': state
    }).then(
        res => {
            if (res.status === 'error') {
                alert('تعداد محصول کافی نیست')
            } else {
                bas.html(res)
            }
        }
    )
}

function delete_detail(detail_id) {
    let bas = $('#bas')
    $.get("/cart/delete-detail/", {
        'detail_id': detail_id
    }).then(
        res => {
            if (res.status === 'error') {
                alert('Error')
            } else {
                bas.html(res)
            }
        }
    )
}

function delete_cart(cart_id) {
    let bas = $('#bas')
    $.get("/cart/delete-cart/", {
        'cart_id': cart_id
    }).then(
        res => {
            if (res.status === 'error') {
                alert('Error')
            } else {
                bas.html(res)
            }
        }
    )
}

function delete_wish_detail(detail_id) {
    let bas = $('#bas')
    $.get("/wish-list/delete-wish-detail/", {
        'detail_id': detail_id
    }).then(
        res => {
            if (res.status === 'error') {
                alert('Error')
            } else {
                bas.html(res)
            }
        }
    )
}



