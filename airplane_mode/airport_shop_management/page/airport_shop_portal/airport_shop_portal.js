frappe.pages['airport-shop-portal'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});

	page.set_title("Airport Shop Portal");

	$(frappe.render_template("airport_shop_portal", {
			// DATA AS OBJECT
		})
	).appendTo(page.body);

	render_shop_cards()

	function render_shop_cards() {
		var main_data = [];
		$.ajax({
			url: `${window.location.origin}/api/resource/Shop?fields=["shop_name","shop_code","shop_image","airport","status","route"]&order_by=status%20asc&limit_page_length=none`,
			success: function (response) {
				main_data = response.data

				if (main_data) {
					$.each(main_data, function (index, item) {
						console.log(item)
						var color = "#2376d0bf"
						if (item.status == "Available For Rent") {
							color = "#2376d0bf"
						}
						if (item.status == "Unavailable") {
							color = "#0a720a9c"
						}
						if (item.status == "Closed") {
							color = "#ad1818bf"
						}
						$(".cards-container").append(`
							<div class="card 1 p-4" key=${index}>
								<div>
									<h5>
										Shop Name: ${item.shop_name}
									</h5>
									<h5>
										Shop Code: ${item.shop_code}
									</h5>
									<h5>
									Status: 
										<span style="padding: 2px 5px;border-radius: 10px;font-size: 14px;color: white;background-color:${color};">
											${item.status} 
										</span>
									</h5>
									<h5>
										Airport: ${item.airport}
									</h5>
									<a href="../${item.route}">
										<button class="btn btn-primary">
											View Shop Details
										</button>
									</a>
								</div>
								`)
					})
				}
			}
		});
	}
}
