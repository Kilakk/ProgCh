ERR_TIMEOUT = 5000;

class IncrResource {
	constructor(id, rate, multiplier) {
		this.id = id;
		this.rate = rate;
		this.multiplier = multiplier;
		
		this.value = 0;
		
		this.ticking = false;
		
		update_value(this);
		update_info(this);
		ticker(this);
	}
	
	add_value(number) {
		this.value += number;
		update_value(this);
	}
	
	rem_value(number) {
		if(this.has_enough(number)) {
			this.value -= number;
			update_value(this);
		}
		
		else {
			throw "Not enough " + this.id + " to purchase!";
		}
		
		return true;
	}
	
	increment() {
		this.value += 1 * this.multiplier;
	}
	
	decrement(cost = 1) {
		this.value -= 1 * cost;
	}
	
	has_enough(number) {
		if (number > this.value) {
			return false;
		}
		
		return true;
	}
}

class CostResource extends IncrResource {
	constructor(id, rate, multiplier, other, cost) {
		super(id, rate, multiplier);
		this.cost = cost;
		this.other = other;
	}
}

function ticker(resource) {
	if(resource.ticking) {
		
		if(resource.other) {
			try {
				if(resource.other.rem_value(resource.cost)) {
					resource.increment();
				}
			}
			
			catch(err) {}
		}
		
		else {
			resource.increment();
		}
		
		update_value(resource);
	}
	
	var t = setTimeout(function() { ticker(resource) }, resource.rate);
}

function purchase(resource_selling, resource_gaining, amount, cost) {
	try {
		resource_selling.rem_value(cost);
		resource_gaining.add_value(amount);
	}
	
	catch(err) {
		document.getElementById("announcements").innerHTML = err;
		var t = setTimeout(function() { clear_announcements() }, ERR_TIMEOUT);
	}
}

function get_info(resource) {
	var per_sec = (resource.multiplier/resource.rate) * (1000);
	
	if(resource.ticking) {
		return "You produce " + resource.id + " at a rate of " + resource.multiplier + " every " + resource.rate + " ms, which is " + per_sec + " " + resource.id + " per second.";
	}
	
	else {
		return "You are not producing any " + resource.id + ".";
	}
}

function update_value(resource) {
	document.getElementById(resource.id).innerHTML = (resource.value > 0 ? resource.value : "no");
	console.log(resource.id + ": updated to " + resource.value);
}

function update_info(resource) {
	document.getElementById(resource.id + "_info").innerHTML = get_info(resource);
}

function clear_announcements() {
	document.getElementById("announcements").innerHTML = "";
}

// resources
var beans = new IncrResource("beans", 500, 1);
beans.ticking = true;
update_info(beans);

document.getElementById("beans_buy").onclick = function() {
	purchase(beans, beans, 10, 0);
}

var coffee = new CostResource("coffee", 2000, 1, beans, 7);

document.getElementById("coffee_make").onclick = function() {
	purchase(beans, coffee, coffee.multiplier, coffee.cost);
}

document.getElementById("coffee_generate").onclick = function() {
	coffee.ticking = !coffee.ticking;
	if(coffee.ticking) {
		document.getElementById("coffee_generate").innerText = "Stop Making Coffee";
	}
	
	else {
		document.getElementById("coffee_generate").innerText = "Brew Coffee Automatically";
	}
	
	update_info(coffee);
}