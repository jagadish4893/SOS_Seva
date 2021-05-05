function show_modal(id)
{
    $('.tabs-container').css('opacity','0.4');
    $('#loading').show();
//    $("#passes_page").hide();
            $.ajax({
                url: '/'+window.language+ "/administration/get_pass_details/",
                data: {'emp_id':id},
                type: 'POST',
                success: function(result){
                    $('#loading').hide();
                    console.log(result);
                    $('.tabs-container').css('opacity','1');
                    //console.log(result);
                    $("#employeeName").val(result['pass_details'].name);
                    $("#uuid").val(result['pass_details'].uuid);
                    $("#status").val(result['pass_details'].status);
                    $("#reason").val(result['pass_details'].reason);
                    $("#age").val(result['pass_details'].age);
                    $("#mobile").val(result['pass_details'].mobile);
                    $("#request_pass_start").val(result['pass_details'].request_pass_start);
                    $("#request_pass_end").val(result['pass_details'].request_pass_end);
                    if (result['pass_details'].photo) {
                         $("#photo1").attr('src', '/media/' + result['pass_details'].photo);
                    }
                    if (result['pass_details'].photo) {
                         $("#idproof1").attr('src', '/media/' + result['pass_details'].idproof);
                    }
                    $("#passes_data").show();
                    $("#applicant_id").val(result['pass_details'].uuid);
                    var flag = $("[name='flag']").val()
                    if(result['pass_details'].status=='Approved'){

                          if (flag === 'Approver') {
                                 $("#preapprove_citizen").css({"display":"none"})
                                 $("#approve_citizen").css({"display":"none"})
                                 $("#reject_citizen").css({"display":"block"})
                          }
                         else {
                                 $("#approve_citizen").css({"display":"none"})
                                 $("#preapprove_citizen").css({"display":"none"})
                                 $("#reject_citizen").css({"display":"none"})
                         }

                    }
                    else if(result['pass_details'].status=='Pre Approved'){

                        if (flag === 'Approver') {
                         $("#preapprove_citizen").css({"display":"none"})
                         $("#approve_citizen").css({"display":"block"})
                         }
                        else {
                        $("#approve_citizen").css({"display":"none"})
                         $("#preapprove_citizen").css({"display":"none"})
                         }
                        $("#reject_citizen").css({"display":"block"})
                    }
                    else if(result['pass_details'].status=='Rejected'){
                        $("#approve_citizen").css('display', 'none');
                        $("#reject_citizen").css('display', 'none');
                        $("#preapprove_citizen").css({"display":"none"})

                        /*$("#reject_citizen").css({"display":"none"})
                        if (flag === 'Approver') {
                         $("#preapprove_citizen").css({"display":"none"})
                         $("#approve_citizen").css({"display":"block"})
                         }
                        else {
                        $("#approve_citizen").css({"display":"none"})
                         $("#preapprove_citizen").css({"display":"block"})
                         }*/

                    }
                    else
                    {
                        if (flag === 'Approver') {
                         $("#preapprove_citizen").css({"display":"none"})
                         $("#approve_citizen").css({"display":"block"})
                         }
                        else {
                        $("#approve_citizen").css({"display":"none"})
                         $("#preapprove_citizen").css({"display":"block"})
                         }
                        $("#reject_citizen").css({"display":"block"})
                    }
                },
                    error:function(err){
                        Alert("Error",err.statusText);

                }
        });
}