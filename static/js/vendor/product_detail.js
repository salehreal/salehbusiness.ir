function add_to_cart(product_id) {
    let inp = $("#in-count").val()
    $.get("/cart/add-to-cart/", {
        "product_id": product_id,
        "count": inp
    }).then(
        res => {
            if (res.status === "not_login") {
                alert("ابتدا باید وارد حساب کاربری خود شوید")
            } else if (res.status === "error") {
                alert("عملیات با خطا مواجه شد")
            } else if (res.status === "ok") {
                Swal.fire({
                    title: "Success",
                    text: "محصول با موفقیت به سبد خرید اضافه شد",
                    icon: "success"
                });
            }
        }
    )
}