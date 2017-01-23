function post_function(post_id){

    // Test post
    if (post_id == "7"){
    	var data = [{"label": "Do", "value":10},{"label": "Do not", "value":10},{"label": "Try","value":0}]
		nv.addGraph(function(){
            var chart = nv.models.pieChart().x(function(d) {return d.label }).y(function(d) {return d.value }).showLabels(false);
            var svg = d3.select("#img_canvas").append("svg")
            svg.datum(data).transition().duration(350).call(chart)
		})
	} else if (post_id == "8"){
        $.ajax({
            type : "GET",
            url : "/get_post_text",
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                var data = JSON.parse(result);
                var margin = {top: 20, right: 20, bottom: 40, left: 20},
                width = 960 - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;

                var layout = d3.layout.cloud()
                    .size([500, 500])
                    .words(data.map(function(d) {
                      return {text: d.word, size: 10 + 0.5*d.count_normalized * 90, test: "haha"};
                    }))
                    .padding(5)
                    .rotate(function() { return ~~(Math.random() * 2) * 90; })
                    .font("Impact")
                    .fontSize(function(d) { return d.size; })
                    .on("end", draw);

                layout.start();

                function draw(words) {
                  d3.select("#img_canvas").append("svg")
                      .attr("width", layout.size()[0])
                      .attr("height", layout.size()[1])
                      .style("display","block")
                      .style("margin", "auto")
                    .append("g")
                      .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
                    .selectAll("text")
                      .data(words)
                    .enter().append("text")
                      .style("font-size", function(d) { return d.size + "px"; })
                      .style("font-family", "Impact")
                      .attr("text-anchor", "middle")
                      .attr("transform", function(d) {
                        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                      })
                      .text(function(d) { return d.text; });
                }
            },
            error: function(error) {
                console.log(error);
            }
            });
	}
}