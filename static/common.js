// 모바일 장치인지 확인하기
let is_mobile = false;
if (    navigator.userAgent.match(/Android/i) || 
        navigator.userAgent.match(/webOS/i) || 
        navigator.userAgent.match(/iPhone/i) || 
        navigator.userAgent.match(/iPad/i) || 
        navigator.userAgent.match(/iPod/i) || 
        navigator.userAgent.match(/BlackBerry/i) || 
        navigator.userAgent.match(/Windows Phone/i)
    )
    is_mobile = true;
    
window.isEmpty = function (v){
    if( v == "" || v == null || v == undefined || Number.isNaN(v) || ( v != null && typeof v == "object" &&
    !Object.keys(v).length ) ) return true;
    else return false;
};
