function set_parent(cm_id) {
    let input = document.querySelector("#hidden-inp")
    let sc = document.querySelector("#scroll-target")
    input.value = cm_id
    sc.scrollIntoView({behavior: "smooth"})
}

function send_comment(blog_id) {
    let text = $("#text")
    let parent = $("#hidden-inp")
    let axil_comment_area = $("#res")
    if (parent.val()) {
        parent = parent.val()
    } else {
        parent = false
    }
    $.get("/blog/send-comment/", {
        'text': text.val(),
        'blog_id': blog_id,
        'parent': parent
    }).then(
        res => {
            axil_comment_area.html(res)
            text.val("")
        }
    )
}

function send_product_comment(product_id, slug) {
    let text = $("#text").val();
    let comment_area = $("#res");
    $.get(`/products/send-comment/${slug}/`, {
        'text': text,
        'product_id': product_id
    }).then(
        res => {
            comment_area.html(res);
            $("#text").val("");
        }
    );
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function submitCommentAndRating(product_id, slug) {
    let text = $("#text").val();
    let rate = $("#rating").val();
    let comment_area = $("#res");

    // بررسی اینکه فیلد text و rate خالی نباشند
    if (!text.trim()) {
        Swal.fire({
            position: "center",
            icon: "error",
            title: "متن کامنت نمی‌تواند خالی باشد",
            showConfirmButton: false,
            timer: 1500
        });
        return;
    }
    if (!rate) {
        Swal.fire({
            position: "center",
            icon: "error",
            title: "رتبه‌بندی نمی‌تواند خالی باشد",
            showConfirmButton: false,
            timer: 1500
        });
        return;
    }

    $.ajax({
        url: `/products/submit-comment-and-rating/${slug}/`,
        type: 'POST',
        data: {
            'text': text,
            'rate': rate,
            'product_id': product_id
        },
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function (res) {
            if (res.status === 'success') {
                comment_area.html(res.comments_html);
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: "نظر و رتبه با موفقیت ثبت شد",
                    showConfirmButton: false,
                    timer: 1500
                });
            } else if (res.status === 'error') {
                Swal.fire({
                    position: "center",
                    icon: "error",
                    title: res.message || "خطایی رخ داده است",
                    showConfirmButton: false,
                    timer: 1500
                });
            }
            $("#text").val("");
            $("#rating").val("");
        }
    });
}







