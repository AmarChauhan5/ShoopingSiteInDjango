$('#mobile,#laptop,#top,#bottom').owlCarousel({
    loop:true,
    margin:10,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
            nav:false,
            dots:false,
        },
        800:{
            items:3,
            nav:true,
            dots:false,
        },
        1200:{
            items:4,
            nav:true,
           
            dots:false,
        }
    }
})

$('.plus-cart').click(function(){
    var product_id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[1];
    $.ajax({
        type:'GET',
        url:'/pluscart',
        data:{
            id : product_id
        },
        success:function(data){
            console.log("ajdghjbsj")
            document.getElementById("total_amount").innerText=data.total_amount
            eml.innerText=data.quantity
            document.getElementById("plus_shipping_amount").innerText=data.plus_shipping_amount

        }
    })
})

$('.minus-cart').click(function(){
    var product_id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[1];
    $.ajax({
        type:'GET',
        url:'/minus-cart',
        data:{
            id : product_id
        },
        success:function(data){
            document.getElementById("total_amount").innerText=data.total_amount
            eml.innerText=data.quantity
            document.getElementById("plus_shipping_amount").innerText=data.plus_shipping_amount

        }
    })
})

$('.remove-cart').click(function(){
    var product_id = $(this).attr('pid').toString();
    var eml = this.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode
    $.ajax({
        type:'GET',
        url:'/remove-cart',
        data:{
            id : product_id
        },
        success:function(data){
            document.getElementById("total_amount").innerText=data.total_amount
            eml.remove()
            document.getElementById("plus_shipping_amount").innerText=data.plus_shipping_amount

        }
    })
})



var back_end_otp = ''
$('.send_otp').click(function(){
    console.log("sended")
var email = document.getElementById("email").value
// console.log(email)
$.ajax({
    type:'GET',
    url:'/send_otp',
    data:{
        'id' : email
    },
    success:function(data){
        // console.log("success")
        // console.log(data)
        back_end_otp = data.otp
        document.getElementById("email_b").value = email;
        document.getElementById("check_mail").style.display="block";
        document.getElementById("verify-div").style.display="block";


    }
})
})

$('.verify_otp').click(function(){

var otp = document.getElementById("otp-verify").value

console.log(otp)
if(otp==back_end_otp){
        document.getElementById("verify").style.display="block";
        document.getElementById("verify").innerHTML="OTP Verify Succefully";
        document.getElementById("verify").style.color="green";
        document.getElementById("submit").disabled=false
}else{
    console.log("false to match")
        document.getElementById("verify").innerHTML="Incorrect OTP";
        document.getElementById("verify").style.display="block";
        document.getElementById("verify").style.color="red";

}
})