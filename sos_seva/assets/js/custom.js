//import { jsPDF } from "jspdf";
function delete_object(obj_id){
    var proceed = confirm("Do you want to delete this entry?");
    if (proceed){
        alert(obj_id);
        $.ajax({
        //url: "/administration/get_business_pass_details/",
        headers: {'Authorization': 'token 3b18512fa7b39f8ce2e749eb2dc97bbf1ac70b6b'},
        url: '/productDelete/'+obj_id,
        type: 'POST',
        success: function(result){
            window.location.reload();
        }

     });
    }
    else{
        console.log("action cancelled");
    }
}

function view_object(obj_id){
    var url = '/viewProduct/'+obj_id ;
    window.open(url, '_blank');
}

function edit_object(obj_id){
    var url = '/editProduct/'+obj_id ;
    window.open(url, '_blank');
}

function saveProductDetails()
{
//    var form = new FormData($("#product_form")[0]);
    var form = $("#product_form")[0];
    console.log(form);
//    var form = $("#product_form").serialize();
//    var form = $("#product_form").serializeArray();
//    var form = $("#product_form").serializeJSON();
//    var data = getFormData(form);
    var data = new FormData(form);
    console.log(data);
//    console.log(form);
//    data['created_by'] = '1';
//    data['created_on'] = new Date().toMysqlFormat();
    var json = JSON.stringify(data);
    console.log(json)
    $.ajax({
        headers: {'Authorization': 'token 3b18512fa7b39f8ce2e749eb2dc97bbf1ac70b6b'},
        url: "/add_new_product",
        type:'POST',
        data:json,
        processData: false,
        contentType: false,
        success: function(result){
                alert(result['msg']);
        },
        error: function(error){
            alert(error['msg']);
        }
    });
}

function updateProductDetails(){
    var form = new FormData($("#product_form")[0]);
    save_configDetails = '/productUpdate/';
            //form = form+'&updateAdv='+updateAdv;
            $.ajax({
                url: save_configDetails,
                headers: {'Authorization': 'token 3b18512fa7b39f8ce2e749eb2dc97bbf1ac70b6b'},
                type:'POST',
                data:form,
                processData: false,
                contentType: false,
                success: function(result){
                        alert(result['msg']);
                },
                error: function(error){
                    alert(error['msg']);
                }
            });
}

function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}


function twoDigits(d) {
    if(0 <= d && d < 10) return "0" + d.toString();
    if(-10 < d && d < 0) return "-0" + (-1*d).toString();
    return d.toString();
}

Date.prototype.toMysqlFormat = function() {
    return this.getUTCFullYear() + "-" + twoDigits(1 + this.getUTCMonth()) + "-" + twoDigits(this.getUTCDate()) + " " + twoDigits(this.getUTCHours()) + ":" + twoDigits(this.getUTCMinutes()) + ":" + twoDigits(this.getUTCSeconds());
};

/*
function saveProductDetails()
{
    alert("here");
    var form = new FormData($("#product_form")[0]);
            //form = form+'&updateAdv='+updateAdv;
            $.ajax({
                url: '/product/add_new_product/',
                type:'POST',
                data:form,
                processData: false,
                contentType: false,
                success: function(result){
                console.log(result);
                    //if
                    //else
                },
                error: function(error){
                console.log(error);
                }
            });
}
*/