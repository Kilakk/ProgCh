class IncrResource {
	constructor(id, rate, multiplier) {
		this.id = id;
		this.rate = rate;
		this.multiplier = multiplier;
		
		this.value = 0;
		
		// start counting
		increment(this);
	}
}

function increment(resource) {
	resource.value += 1 * resource.multiplier;
		
	document.getElementById(resource.id).innerHTML = resource.value;
	var t = setTimeout(function() { increment(resource) }, resource.rate);
}	

var beans = new IncrResource("beans", 1000, 1);