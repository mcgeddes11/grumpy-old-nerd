function post_function(post_id){

    // Test post
    if (post_id == "7"){
    	var data = [{"label": "Do", "value":0.5},{"label": "Do not", "value":0.5},{"label": "Try","value":0}]
		nv.addGraph(function(){
            var chart = nv.models.pieChart().x(function(d) {return d.label }).y(function(d) {return d.value }).showLabels(false);
            var svg = d3.select("#img_canvas").append("svg")
            svg.datum(data).transition().duration(350).call(chart)
		})
	}
}