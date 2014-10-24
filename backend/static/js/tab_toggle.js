//样式中英文tab切换js 
//tab样式设置
//当页面载入完成
$(function() {
    $(".tab_content").hide(); //隐藏所有表格
    $("ul.tabs li:first").addClass("active").show(); //激活第一个中文选项卡
    $(".tab_content:first").show(); //展示第一张中文表的内容

    //点击事件
    $("ul.tabs li").click(function() {

        $("ul.tabs li").removeClass("active"); //移除当前的类
        $(this).addClass("active"); //将active类加在所选的选项卡上
        $(".tab_content").hide(); //隐藏所有tab元素

        var activeTab = $(this).find("a").attr("href"); //获取对应href
        $(activeTab).fadeIn(); //淡入所选tab
        return false;
    });
});
