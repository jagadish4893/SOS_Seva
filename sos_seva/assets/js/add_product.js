
function saveProductDetails()
{
    var form = new FormData($("#product_form")[0]);
            //form = form+'&updateAdv='+updateAdv;
            $.ajax({
                url: save_configDetails,
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
