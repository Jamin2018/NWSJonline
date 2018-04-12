

$(function(){
    var test = window.location.pathname;
    if(test == '/'){
        $.get("/imgs-name-list/", function(res){
            if(res['err'] === 0){
                var img_list = res['img_name_list'];
                var htm = "";
                for(var i=0;i<img_list.length;i++){
                    var temp_str = "<img class='img-responsive img-thumbnail img_32' alt='Responsive image' src='/static/imgs/datas/"+img_list[i]+"'>";
                    htm += temp_str
                }
                $('#content-inner').html(htm)
            }
        });

        $('#panel-btn-3').trigger('click');
    }else{
        $('#panel-btn-3').trigger('click');
    }
});


$('#datainput').click(function () {
    $('#panel1').removeClass('color_red');
    $('#panel1').show();
    $('#panel1').empty();
    var file_csv = document.getElementById('datacsv').files[0];
    var file_xlsx = document.getElementById('dataxlsx').files[0];
    var fd = new FormData();
    fd.append('file_csv',file_csv);
    fd.append('file_xlsx',file_xlsx);
    $('#panel1').html("<i class='fa fa-spinner fa-pulse'></i> 解析中，请稍等");
    $.ajax({
        url:"/data-input/",
        type:'POST',
        data:fd,
        datatype: 'json',
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
        success:function (arg) {
            var err = arg['err'];
            if(err == 0){
                $('#panel1').text(arg['msg']);
                $('#panel1').show()
            }else if(err == -1){
                $('#panel1').text(arg['msg']);
                $('#panel1').addClass('color_red');
                $('#panel1').show()
            }
        }
    })
});


$('#datainput2').click(function () {
    $('#panel2').html("<i class='fa fa-spinner fa-pulse'></i>");
    $.get("/data-auto-draw/", function(res){
        if(res['err'] === 0){
            var img_list = res['img_name_list'];
            var htm = "";
            for(var i=0;i<img_list.length;i++){
                var temp_str = "<img class='img-responsive img-thumbnail' alt='Responsive image' src='/static/imgs/datas/"+img_list[i]+"'>";
                htm += temp_str
            }

            var test = window.location.pathname;
            if(test == '/'){
                window.location.reload();
                $('#content-inner').html(htm)
            }
            $('#panel2').hide()
        }
    })
});

$('#panel-btn-3').click(function () {
    $('#panel-btn-3').addClass('fa-spin');
    $.get("/sku-list-update/", function(res){
        console.log(res['msg']);
        if(res['err'] == 0 ){
            var sku_list = res['msg'];
            var htm = "";
            n = 0;
            for(var i=0;i<sku_list.length;i++){
                var m = parseInt(5*Math.random());
                if(n === m){
                    if(n === 4){
                        n = 0
                    }else {
                        n = m + 1
                    }
                }else {
                    n = m
                }
                if(  n === 0){
                    var temp_str = "<button type='button' class='btn btn-warning btn-xs btn-xs-mb'"+"onclick = select_sku('"+sku_list[i]+"')>"+sku_list[i]+"</button>"
                }
                else if( n === 1){
                    var temp_str = "<button type='button' class='btn btn-info btn-xs btn-xs-mb'"+"onclick = select_sku('"+sku_list[i]+"')>"+sku_list[i]+"</button>"
                }
                else if( n === 2){
                    var temp_str = "<button type='button' class='btn btn-success btn-xs btn-xs-mb'"+"onclick = select_sku('"+sku_list[i]+"')>"+sku_list[i]+"</button>"
                }
                else if( n === 3){
                    var temp_str = "<button type='button' class='btn btn-primary btn-xs btn-xs-mb'"+"onclick = select_sku('"+sku_list[i]+"')>"+sku_list[i]+"</button>"
                }
                else if( n === 4){
                    var temp_str = "<button type='button' class='btn btn-danger btn-xs btn-xs-mb'"+"onclick = select_sku('"+sku_list[i]+"')>"+sku_list[i]+"</button>"
                }

                htm += temp_str
            }
            $('#sku_list').html(htm)
        }
        else if(res['err'] == -1){
            var htm = "<span style = 'color:red' >请将数据解析后再试试刷新</sapn>";
            $('#sku_list').html(htm);
        }
        $('#panel-btn-3').removeClass('fa-spin');
    });
});

function select_sku(sku_name) {
    var sku_list = $('#sku_id').val();
    if(sku_list.length == 0){
        var new_sku_list = sku_name;
    }
    else {
        var new_sku_list = sku_list +','+sku_name;
    }
    $('#sku_id').attr('value',new_sku_list)
}


$('#sku_id_btn').click(function () {
    var v = $('#sku_id').val();
    $('#panel_span_4').html("<i class='fa fa-spinner fa-pulse'></i>")
    if(v == ''){
        $('#panel_span_4').html("<span style='color:red;'>请输入系列名</span>")
    }else {
        $.get("/choose-sku-draw/?sku_name_list="+v , function (res) {
            if(res['err'] == 0){
                if(res['err_sku_name'] == ''){
                    $('#panel_span_4').html("<a href='/sku-chart/'>构图成功</a>")
                }else if(res['sus_sku_name'] != ''){
                    $('#panel_span_4').html("<a href='/sku-chart/'>构图成功</a><br><span style='color: red'>无效系列名："+res['err_sku_name']+"</span>")
                }else {
                    $('#panel_span_4').html("<span style='color: red'>无效系列名："+res['err_sku_name']+"</span>")
                }
            }
        })
    }


});

