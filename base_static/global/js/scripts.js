function my_scope() {
    const form = document.querySelector(".form-delete")

    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault()
            const confirmed = confirm("Are you sure?")
            if (confirmed) {
                form.submit()
            }
        })
    }
}

my_scope()