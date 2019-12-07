setInterval(function(){
    ajax_alarm_intime();
}, 5000);
$(document).ready(function () {
    ajax_alarm();
});


function ajax_alarm() {
    var url = '/alarm/';
    var result;
    $.ajax({
        url: url,
        data: {
            intime:false
        },

        success: function(return_data){
            result=return_data.result;
            var str_result = "";
            for(var i=0;i<result.length;i+=1){
                str_result = "2018年10月30日" + result[i].street_name + "的" + result[i].community_name + "从" + result[i].event_src_name + "接到"+result[i].sub_type_name+result[i].event_property_name+"，请"+result[i].dispose_unit_name+"尽快前往处理。";
                $.notify({
            	    icon: 'pe-7s-info',
            	    message: str_result
                },{
                    type: 'warning',
                    delay: 100000
                });
            }
        }
    })
};
function ajax_alarm_intime() {
    var url = '/alarm/';
    var result;
    $.ajax({
        url: url,
        data: {
            intime:true
        },

        success: function(return_data){
            result=return_data.result;
            var str_result = "";
            for(var i=0;i<result.length;i+=1){
                str_result = "2018年10月30日" + result[i].street_name + "的" + result[i].community_name + "从" + result[i].event_src_name + "接到"+result[i].sub_type_name+result[i].event_property_name+"，请"+result[i].dispose_unit_name+"尽快前往处理。";
                $.notify({
            	    icon: 'pe-7s-info',
            	    message: str_result
                },{
                    type: 'warning',
                    delay: 100000
                });
            }
        }
    })
};