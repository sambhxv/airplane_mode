frappe.ready(function () {
    frappe.web_form.set_value('flight_price', get_random_price());
});

function get_random_price(min = 2000, max = 20000) {
    if (min % 5 !== 0) min += 5 - (min % 5);
    if (max % 5 !== 0) max -= max % 5;
    const range = (max - min) / 5;
    const randomIndex = Math.floor(Math.random() * (range + 1));
    return min + randomIndex * 5;
}
